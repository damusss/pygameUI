import pygame
from ..core.element import UIElement
from .. import constants

class UIContainer(UIElement):
    """
    Holds, update and draws elements.
    
    Parameters: all UIElement common parameters plus:
    
    :param colored (bool): if True, the container will have outline and background, otherwise transparent
    """
    def __init__(self,relative_rect:pygame.Rect,ui_manager,container=None,colored=False,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],_is_window_container=False,_name="container"):
        if not _is_window_container:
            super().__init__(relative_rect,ui_manager,container,visible,id,element_name=_name)
        else:
            super().__init__(relative_rect,ui_manager,"ISWINDOWCONTAINERDONOTINIT",id="root_container",element_name="window_container")
        self._surface = pygame.Surface((relative_rect.w,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        #self._scrollable_surface = pygame.Surface((relative_rect.w,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        
        self._elements_right:list[UIElement] = list()
        self._elements:list[UIElement] = list()
        
        self._colored = colored
        self._surface_offset = pygame.Vector2()
    
    def _send_container_refresh(self):
        pass
        
    def _update_max_elements_sizes(self):
        pass
        
    def get_elements(self):
        return self._elements_right
        
    def on_update(self,dt):
        pass
        
    def rebuild(self):
        self._surface = pygame.Surface((self.relative_rect.w,self.relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self.on_rebuild()
        
    def on_rebuild(self):
        pass
        
    def _register_element(self,element:UIElement):
        self._elements_right.append(element)
        self._elements = list(reversed(self._elements_right))
        self._update_max_elements_sizes()
        
    def _on_element_destroy(self,element:UIElement):
        if element in self._elements_right:
            self._elements_right.remove(element)
        self._elements = list(reversed(self._elements_right))
        self._update_max_elements_sizes()
        
    def update_position(self, amountx, amounty):
        super().update_position(amountx, amounty)
        for el in self._elements:
            el.update_position(0,0)
            
    def update(self, dt,found_hovering=False):
        found_hovering = found_hovering
        for element in self._elements:
            if element.enabled and self.enabled:
                element.update(dt,found_hovering)
                if element.visible and not found_hovering:
                    found_hovering = element._update_hovering_status(False)
                else:
                    element._update_hovering_status(True)
            else:
                element._update_hovering_status(True)
        self.on_update(dt)
            
    def draw(self, surface:pygame.Surface,offset=(0,0)):
        if self._colored and self.visible:
            self._surface.fill(0)
            self._shape_renderer.render(surface,offset)
        else:
            if self.visible:
                self._surface.fill(0)
        if self.visible:
            for element in self._elements_right:
                if element.visible:
                    element.draw(self._surface)
        final = (self.relative_rect.x+offset[0],self.relative_rect.y+offset[1])
        surface.blit(self._surface,final)
        if self._colored and self.visible:
            self._shape_renderer.render_outline(surface,offset)
        
                    
    def event(self, event):
        if self.enabled:
            for element in self._elements:
                if element.enabled:
                    element.event(event)
                else:
                    if element._is_clicking:
                        element._is_clicking = False
                        pygame.event.post(pygame.event.Event(constants.ELEMENT_RELEASED,{
                                "element_ID":element._ID,
                                "element_object":element
                            }))
                        element.on_release()
        self.on_event(event)
        
    def destroy(self):
        if not self._is_window_container:
            els = self._elements_right.copy()
            for e in els:
                e.destroy()
            if self._container != None:
                self._container._on_element_destroy(self)
            del self
            
class UIWindowContainer(UIContainer):
    """[internal] Container used by the UIManager"""
    def __init__(self, relative_rect: pygame.Rect, ui_manager,colored=False):
        super().__init__(relative_rect,ui_manager,None,colored,True,"window_container",True,"window_container")
        
    def draw(self, surface: pygame.Surface):
        if self._colored and self.visible:
            surface.fill(0)
            self._shape_renderer.render(surface)
        if self.visible:
            for element in self._elements_right:
                if element.visible:
                    element.draw(surface)
            if self._colored:
                self._shape_renderer.render_outline(surface)

class UIScrollableContainer(UIContainer):
    """
    A container that you can bind scrollbars to. If elements exceeds the container size, a scrollbar will be able to offset them.
    
    Parameters: all UIContainer parameters.
    """
    def __init__(self,relative_rect:pygame.Rect,ui_manager,container=None,colored=False,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],_is_window_container=False,_name="container"):
        super().__init__(relative_rect,ui_manager,container,colored,visible,id,_is_window_container,_name)
        
        #self._scrollable_surface = pygame.Surface((relative_rect.w,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._vertical_scrollbar = None
        self._horizontal_scrollbar = None
        self._max_elements_height = self.relative_rect.h
        self._max_elements_width = self.relative_rect.w
        self._scrollbar_unit_vertical = 1
        self._scrollbar_unit_horizontal = 1
        self._surface_offset = pygame.Vector2()
        
    def _on_vertical_scrollbar_move(self,units):
        if self._vertical_scrollbar != None:
            self._scrollbar_unit_vertical = (self.relative_rect.h/(self._vertical_scrollbar._real_handle_height))
            self._surface_offset.y = -self._scrollbar_unit_vertical*units
            self._on_scrollbars_move()
        else:
            self._surface_offset.y = 0
        for el in self._elements_right:
            el._update_absolute_rect()
        
    def _on_horizontal_scrollbar_move(self,units):
        if self._horizontal_scrollbar != None:
            self._scrollbar_unit_horizontal = (self.relative_rect.h/(self._horizontal_scrollbar._real_handle_width))
            self._surface_offset.x = -self._scrollbar_unit_horizontal*units
            self._on_scrollbars_move()
        else:
            self._surface_offset.x = 0
        for el in self._elements_right:
            el._update_absolute_rect()
            
    def _on_scrollbars_move(self):
        pass
            
    def _propagate_refresh(self):
        for el in self._elements_right:
            el._update_absolute_rect()
            
    def _update_max_elements_sizes(self):
        v = 0
        h = 0
        for el in self._elements:
            if el.relative_rect.bottom > v:
                v = el.relative_rect.bottom
            if el.relative_rect.right > h:
                h = el.relative_rect.right
        if v < self.relative_rect.h:
            v = self.relative_rect.h
        if h < self.relative_rect.w:
            h = self.relative_rect.w
        self._max_elements_height = v
        self._max_elements_width = h
        if self._vertical_scrollbar != None:
            self._vertical_scrollbar._update_handle_height()
        if self._horizontal_scrollbar != None:
            self._horizontal_scrollbar._update_handle_width()
        #self.rebuild()
        
    def rebuild(self):
        self._surface = pygame.Surface((self.relative_rect.w,self.relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        #self._scrollable_surface = pygame.Surface((self._max_elements_width,self._max_elements_height),pygame.SRCALPHA,32).convert_alpha()
        self.on_rebuild()
        
    def _send_container_refresh(self):
        self._update_max_elements_sizes()
        if self._container:
            self._container._update_max_elements_sizes()
            
    def set_vertical_scrollbar(self,scrollbar)->None:
        """Adds a vertical scrollbar. :param scrollbar (UIVerticalScrollbar): the scrollbar to add."""
        self._vertical_scrollbar = scrollbar
        self._vertical_scrollbar._controlling_container = self
        return self
        
    def set_horizontal_scrollbar(self,scrollbar)->None:
        """Adds a horizontal scrollbar. :param scrollbar (UIHorizontalScrollbar): the scrollbar to add."""
        self._horizontal_scrollbar = scrollbar
        self._horizontal_scrollbar._controlling_container = self
        return self
        
    def draw(self, surface:pygame.Surface,offset=(0,0)):
        if self._colored and self.visible:
            self._surface.fill(0)
            self._shape_renderer.render(surface,offset)
        else:
            if self.visible:
                self._surface.fill(0)
        if self.visible:
            for element in self._elements_right:
                if element.visible:
                    if not element._is_scrollbar:
                        element.draw(self._surface,self._surface_offset)
                    else:
                        element.draw(self._surface)
        self.on_draw(self._surface)
        final = (self.relative_rect.x+offset[0],self.relative_rect.y+offset[1])
        surface.blit(self._surface,final)
        if self._colored and self.visible:
            self._shape_renderer.render_outline(surface,offset)
            
    def on_draw(self,surface):
        pass
        
        