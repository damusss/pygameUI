import pygame
from .. import constants, global_input
from ..elements.button import UIButton
from ..elements.container import UIContainer

class UIVerticalScrollbar(UIContainer):
    def __init__(self,relative_rect,ui_manager,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],inner_ids={
            "handle":constants.DEFAULT_SETTINGS["default_element_id"]
        },_name="scrollbar"):
        
        super().__init__(relative_rect,ui_manager,container,True,visible,id,False,_name=_name)
        self._magic_number = self._settings["magic_numbers"]["scrollbar"]
        self.change_dimensions(self._magic_number,relative_rect.h)
    
        self._controlling_container = None
        self._handle_height = self.relative_rect.h
        self._real_handle_height = self._handle_height
        self._handle_button = UIButton(pygame.Rect(0,0,self._magic_number,self._handle_height),self.ui_manager,self,"=",id=inner_ids["handle"],_name="scrollbarhandle")
        self._is_scrollbar = True
        
    def _from_container(self,unit):
        self._handle_button.relative_rect.top = -self._controlling_container._surface_offset.y*unit
        self._handle_button.refresh_position()
        
    def _update_handle_height(self):
        h = self.relative_rect.h*(1/self._controlling_container._max_elements_height)
        h*=self.relative_rect.h
        h*=self._controlling_container.relative_rect.h/self.relative_rect.h
        self._real_handle_height = h
        if h > self._magic_number:
            self._handle_height = h
        else:
            self._handle_height = self._magic_number
        if self._handle_height > self.relative_rect.h:
            self._handle_height = self.relative_rect.h
        self._handle_button.change_dimensions(self._magic_number,self._handle_height)
        
    def on_rebuild(self):
        if self.relative_rect.w != self._magic_number:
            self.change_dimensions(self._magic_number,self.relative_rect.h)
        
    def on_update(self, dt):
        if self._handle_button._is_clicking:
            rel = global_input.GlobalInput.mouse_rel
            if rel[1] != 0:
                if self._handle_button.relative_rect.y+rel[1]>=0 and self._handle_button.relative_rect.bottom+rel[1]<=self.relative_rect.h:
                    self._handle_button.update_position(0,rel[1])
                    if self._controlling_container != None and self.relative_rect.h != self._handle_button.relative_rect.h:
                        self._controlling_container._on_vertical_scrollbar_move(self._handle_button.relative_rect.top)
                        pygame.event.post(pygame.event.Event(constants.SCROLLBAR_MOVED,{
                            "scrollbar_direction":"vertical",
                            "rel":rel[1],
                            "element_ID":self._ID,
                            "element_object":self
                        }))
            
        if self._handle_button.relative_rect.x != 0:
            self._handle_button.set_position((0,self._handle_button.relative_rect.y))
        if self._handle_button.relative_rect.y < 0:
            self._handle_button.set_position((0,0))
            if self._controlling_container != None and self.relative_rect.h != self._handle_button.relative_rect.h:
                self._controlling_container._on_vertical_scrollbar_move(self._handle_button.relative_rect.top)
        if self._handle_button.relative_rect.bottom > self.relative_rect.h:
            self._handle_button.set_position((0,self.relative_rect.h-self._handle_height))
            if self._controlling_container != None and self.relative_rect.h != self._handle_button.relative_rect.h:
                self._controlling_container._on_vertical_scrollbar_move(self._handle_button.relative_rect.top)
                
class UIHorizontalScrollbar(UIContainer):
    def __init__(self,relative_rect,ui_manager,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,True,visible,id,False,"scrollbar")
        self._magic_number = self._settings["magic_numbers"]["scrollbar"]
        self.change_dimensions(relative_rect.w,self._magic_number)
        
        self._controlling_container = None
        self._handle_width = self.relative_rect.w
        self._real_handle_width = self._handle_width
        self._handle_button = UIButton(pygame.Rect(0,0,self._handle_width,self._magic_number),self.ui_manager,self,"=",_name="scrollbarhandle")
        self._is_scrollbar = True
        
    def _from_container(self,unit):
        self._handle_button.relative_rect.left = -self._controlling_container._surface_offset.x*unit
        self._handle_button.refresh_position()
        
    def on_rebuild(self):
        if self.relative_rect.h != self._magic_number:
            self.change_dimensions(self.relative_rect.w,self._magic_number)
        
    def _update_handle_width(self):
        w = self.relative_rect.w*(1/self._controlling_container._max_elements_width)
        w*=self.relative_rect.w
        w*=self._controlling_container.relative_rect.w/self.relative_rect.w
        self._real_handle_width = w
        if w > self._magic_number:
            self._handle_width = w
        else:
            self._handle_width = self._magic_number
        if self._handle_width > self.relative_rect.w:
            self._handle_width = self.relative_rect.w
        self._handle_button.change_dimensions(self._handle_width,self._magic_number)
        
    def on_update(self, dt):
        if self._handle_button._is_clicking:
            rel = global_input.GlobalInput.mouse_rel
            if rel[0] != 0:
                if self._handle_button.relative_rect.x+rel[0]>=0 and self._handle_button.relative_rect.right+rel[0]<=self.relative_rect.w:
                    self._handle_button.update_position(rel[0],0)
                    if self._controlling_container != None and self.relative_rect.w != self._handle_button.relative_rect.w:
                        self._controlling_container._on_horizontal_scrollbar_move(self._handle_button.relative_rect.left)
                        pygame.event.post(pygame.event.Event(constants.SCROLLBAR_MOVED,{
                            "scrollbar_direction":"horizontal",
                            "rel":rel[0],
                            "element_ID":self._ID,
                            "element_object":self
                        }))
            
        if self._handle_button.relative_rect.y != 0:
            self._handle_button.set_position((self._handle_button.relative_rect.x,0))
        if self._handle_button.relative_rect.x < 0:
            self._handle_button.set_position((0,0))
            if self._controlling_container != None and self.relative_rect.w != self._handle_button.relative_rect.w:
                self._controlling_container._on_horizontal_scrollbar_move(self._handle_button.relative_rect.left)
        if self._handle_button.relative_rect.right > self.relative_rect.w:
            self._handle_button.set_position((self.relative_rect.w-self._handle_width,0))
            if self._controlling_container != None and self.relative_rect.w != self._handle_button.relative_rect.w:
                self._controlling_container._on_horizontal_scrollbar_move(self._handle_button.relative_rect.left)