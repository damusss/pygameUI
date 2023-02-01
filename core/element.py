import pygame
from .shape_renderer import ShapeRenderer
from .. import global_input
from .. import constants

class CoordinateLikeObject:
    """
    Empty class used for type snippets.
    
    Valid coordinate objects: Vector2, tuple[number,number], list[number,number], Iterable
    """
    pass

class UIElement(object):
    """
    Basic class used by all UI elements holding core information and methods.
    
    Common parameters:
    
    :param relative_rect (pygame.Rect): rect used for position relative to the parent container and sizes.
    :param ui_manager (UIManager): the instance of the UIManager.
    :param container (UIContainer): container this element is inside.
    :param visible (bool): whether the element starts as visible.
    :param id (str): the id for the object (and used by the settings).
    
    Reserved Parameters:
    
    :param isFG (bool): [internal] tells the shaper renderer what color to use.
    :param element_name (str): [internal] the name to use in the settings. Overridden by the other elements.
    """
    def __init__(self,relative_rect:pygame.Rect,ui_manager,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],isFG = False,element_name="element"):
        self.ui_manager = ui_manager
        self._settings = self.ui_manager._get_settings(id,element_name)
        self._container = container
        self.relative_rect:pygame.Rect = relative_rect
        self._is_window_container =False
        if self._container != None:
            
            if self._container != "ISWINDOWCONTAINERDONOTINIT":
                self.absolute_rect = pygame.Rect(self._container.absolute_rect.x+self.relative_rect.x,
                                             self._container.absolute_rect.y+self.relative_rect.y,
                                             self.relative_rect.w,
                                             self.relative_rect.h)
                self._container._register_element(self)
            else:
                self.absolute_rect = self.relative_rect.copy()
                self._container = None
                self._is_window_container = True
        else:
            self.absolute_rect = self.relative_rect.copy()
            self._container = self.ui_manager.window_container
            self._container._register_element(self)
        self.visible = visible
        self.enabled = True
        self._shape_renderer = ShapeRenderer(self,isFG)
        self._is_hovering = False
        self._ID = id
        self._is_clicking = False
        self._was_clicking = False
        self._enable_long_press = False
        self._press_callback = None
        self._release_callback = None
        self._is_scrollbar = False
        self._move_callback = None
        self._draw_callback = None
        
    def refresh_position(self)->None:
        """
        Call this if you set the position of 'relative_rect' manually to refresh things. Never change 'relative_rect' sizes manually.
        """
        self.update_position(0,0)
        
    def _send_container_refresh(self):
        """[internal]"""
        if self._container:
            self._container._update_max_elements_sizes()
        
    def show(self)->None:
        """Sets 'visible' to True"""
        self.visible = True
        
    def hide(self)->None:
        """Sets 'visible' to False"""
        if not self._is_window_container:
            self.visible = False
        
    def enable(self)->None:
        """Sets 'enabled' to True"""
        self.enabled = True
        
    def disable(self)->None:
        """Sets 'enabled' to False"""
        if not self._is_window_container:
            self.enabled = False
        
    def is_hovering(self)->bool:
        """
        Is the element being hovered? (False if somthing is covering it)
        
        :return: True or False
        """
        return self._is_hovering
    
    def is_hovering_absolute(self)->bool:
        """
        Same as 'is_hovering()' but ignores other elements covering it
        """
        return self.absolute_rect.collidepoint(global_input.GlobalInput.mouse_pos)
    
    def _update_hovering_status(self,is_false):
        """[internal]"""
        if is_false:
            if self._is_hovering:
                self.__send_unhover_event()
            self._is_hovering = False
            return self._is_hovering
        else:
            if self.absolute_rect.collidepoint(global_input.GlobalInput.mouse_pos):
                if self._is_hovering:
                    self.__send_hovering_event()
                    
                else:
                    self.__send_hover_event()
                self._is_hovering = True
                return self._is_hovering
            else:
                if self._is_hovering:
                    self.__send_unhover_event()
                self._is_hovering = False
                return self._is_hovering
    
    def __send_unhover_event(self):
        """[internal]"""
        pygame.event.post(pygame.event.Event(constants.ELEMENT_UNHOVERED, {
                "element_ID":self._ID,"element_object":self
            }))
        self.on_unhover()

    def __send_hovering_event(self):
        """[internal]"""
        pygame.event.post(pygame.event.Event(constants.ELEMENT_HOVERING, {
                        "element_ID":self._ID,"element_object":self
                    }))
        
    def __send_hover_event(self):
        """[internal]"""
        pygame.event.post(pygame.event.Event(constants.ELEMENT_HOVERED, {
                        "element_ID":self._ID,"element_object":self
                    }))
        self.on_hover()
        
    def update(self,dt:float,other_arg=None)->None:
        """[internal] Overriden by other elements"""
        pass
    
    def set_position(self,relative_topleft:CoordinateLikeObject)->None:
        """
        Changes the relative rect topleft.
        
        :param relative_topleft (CoordinateLikeObject): the new topleft.
        """
        if not self._is_window_container:
            self.relative_rect.x = relative_topleft[0]
            self.relative_rect.y = relative_topleft[1]
            self._update_absolute_rect()
            if self._move_callback:
                self._move_callback()
                
    def set_position_absolute(self,absolute_position:CoordinateLikeObject)->None:
        """
        Changes the absolute element position.
        
        :param absolute_position (CoordinateLikeObject): the new absolute position.
        """
        if self._container != None:
            self.set_position((absolute_position[0]-self._container.absolute_rect[0],absolute_position[1]-self._container.absolute_rect[1]))
        else:
            self.set_position(absolute_position)
                
    def set_center(self,relative_center:CoordinateLikeObject)->None:
        """
        Changes the relative rect center
        
        :param relative_center (CoordinateLikeObject): the new center.
        
        """
        if not self._is_window_container:
            self.relative_rect.x = relative_center[0]-self.relative_rect.w/2
            self.relative_rect.y = relative_center[1]-self.relative_rect.h/2
            self._update_absolute_rect()
                
    def _update_absolute_rect(self):
        """[internal]"""
        if self._container:
            if not self._is_scrollbar:
                self.absolute_rect = pygame.Rect(self._container.absolute_rect.x+self.relative_rect.x+self._container._surface_offset.x,
                                                self._container.absolute_rect.y+self.relative_rect.y+self._container._surface_offset.y,
                                                self.relative_rect.w,
                                                self.relative_rect.h)
            else:
                self.absolute_rect = pygame.Rect(self._container.absolute_rect.x+self.relative_rect.x,
                                                self._container.absolute_rect.y+self.relative_rect.y,
                                                self.relative_rect.w,
                                                self.relative_rect.h)
        else:
            self.absolute_rect = self.relative_rect.copy()
        self._send_container_refresh()
        self._propagate_refresh()
        
    def _propagate_refresh(self):
        pass
        
    def update_position(self,amountx:int|float,amounty:int|float)->None:
        """
        Moves the element by some amount
        
        :param amountx (int or float): the x amount
        :param amounty (int or float): the y amount
        """
        if not self._is_window_container:
            self.relative_rect.x += amountx
            self.relative_rect.y += amounty
            self._update_absolute_rect()
                
    def set_position_relative(self,relx:float,rely:float)->None:
        """
        Sets the relative rect position relative to the container. relx and rely are multiplied by the container sizes.
        'relx' = 0.5 and 'rely' = 0.5 will result in the topleft being placed in the middle of the container.
        
        :param relx (int) and rely (int): x and y relative multipliers. Range 0-1.
        """
        if self._container != None:
            x = self._container.relative_rect.w*relx
            y = self._container.relative_rect.h*rely
            self.set_position((x,y))
            
    def set_center_relative(self,relx:float,rely:float)->None:
        """
        Sets the relative rect position relative to the container. relx and rely are multiplied by the container sizes.
        'relx' = 0.5 and 'rely' = 0.5 will result in the center being placed in the middle of the container.
        
        :param relx (int) and rely (int): x and y relative multipliers. Range 0-1.
        """
        if self._container != None:
            x = self._container.relative_rect.w*relx-self.relative_rect.w/2
            y = self._container.relative_rect.h*rely-self.relative_rect.h/2
            self.set_position((x,y))
        
    def change_dimensions(self,width:int,height:int,_rebuild:bool=True)->None:
        """
        Changes the rect sizes and rebuilds the element.
        
        :param width (int) and height (int): the new width and height.
        :param _rebuild (bool): [internal] whether to rebuild the object. Should always be True.
        """
        if not self._is_window_container:
            if width > 0:
                self.relative_rect.w = width
            if height > 0:
                self.relative_rect.h = height
            self._update_absolute_rect()
            if _rebuild:
                self.rebuild()
        
    def rebuild(self):
        """[internal] Overridden by other elements."""
        pass
    
    def draw(self,surface,offset=(0,0)):
        """[internal]"""
        if self.absolute_rect.colliderect(self._container.absolute_rect):
            self._shape_renderer.render(surface,offset)
            if self._draw_callback:
                self._draw_callback(surface,offset)
            self._shape_renderer.render_outline(surface,offset)
    
    def event(self,event):
        """[internal]"""
        self._was_clicking = self._is_clicking
        if self.visible and self._container.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._is_hovering:
                    if not self._enable_long_press:
                        self._is_clicking = True
                        pygame.event.post(pygame.event.Event(constants.ELEMENT_PRESSED,{
                            "element_ID":self._ID,
                            "element_object":self
                        }))
                        self.on_press()
                        if self._press_callback:
                            self._press_callback(self)
                    else:
                        if self._is_clicking:
                            self._is_clicking = False
                            pygame.event.post(pygame.event.Event(constants.ELEMENT_RELEASED,{
                            "element_ID":self._ID,
                            "element_object":self
                            }))
                            self.on_release()
                            if self._release_callback:
                                self._release_callback(self)
                        else:
                            self._is_clicking = True
                            pygame.event.post(pygame.event.Event(constants.ELEMENT_PRESSED,{
                                "element_ID":self._ID,
                                "element_object":self
                            }))
                            self.on_press()
                            if self._press_callback:
                                self._press_callback(self)
            elif event.type == pygame.MOUSEBUTTONUP:
                if not self._enable_long_press:
                    if self._is_clicking:
                        self._is_clicking = False
                        pygame.event.post(pygame.event.Event(constants.ELEMENT_RELEASED,{
                            "element_ID":self._ID,
                            "element_object":self
                        }))
                        self.on_release()
                        if self._release_callback:
                            self._release_callback(self)
        else:
            if self._is_clicking:
                self._is_clicking = False
                pygame.event.post(pygame.event.Event(constants.ELEMENT_RELEASED,{
                        "element_ID":self._ID,
                        "element_object":self
                    }))
                self.on_release()
                if self._release_callback:
                    self._release_callback(self)
        self.on_event(event)
                
    def on_event(self,event):
        """[internal]"""
        pass
    
    def destroy(self)->None:
        """Removes the element from the container and destroys it."""
        if not self._is_window_container:
            if self._container != None:
                self._container._on_element_destroy(self)
            del self
        
    def check_pressed(self)->bool:
        """
        Check if the element is being pressed at that frame.
        
        :return: True or False
        """
        if not self.visible or not self._container.visible or not self.enabled:return False
        if self._enable_long_press:
            if self._is_clicking:return True
            return False
        return self._is_clicking and not self._was_clicking
    
    def check_released(self)->bool:
        """
        Check if the element is being released at that frame.
        
        :return: True or False
        """
        if not self.visible or not self._container.visible or not self.enabled:return False
        if self._enable_long_press:
            if self._is_clicking:return False
            return True
        return self._was_clicking and not self._is_clicking
    
    def on_press(self):
        """[internal]"""
        pass
    
    def on_release(self):
        """[internal]"""
        pass
    
    def on_hover(self):
        """[internal]"""
        pass
    
    def on_unhover(self):
        """[internal]"""
        pass