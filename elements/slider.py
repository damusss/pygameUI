import pygame
from .. import constants, global_input
from ..core.element import UIElement
from ..elements.button import UIButton

class UISlider(UIElement):
    def __init__(self,relative_rect,ui_manager,min_value,max_value,current_value,direction="horizontal",container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],inner_ids={
        "handle":constants.DEFAULT_SETTINGS["default_element_id"]
    }):
        super().__init__(relative_rect,ui_manager,container,visible,id)
        
        self._magic_number = self._settings["magic_numbers"]["slider"]
        self._shape_renderer.bg_color = self._shape_renderer.oc
        self._min = min_value
        self._max = max_value
        self._value = current_value
        self._direction = direction
        self._clamp_value()
        
        self._handle_button = UIButton(pygame.Rect(0,0,self._settings["magic_numbers"]["handle"],self._settings["magic_numbers"]["handle"]),self.ui_manager,container,"",id=inner_ids["handle"],_name="sliderhandle")
        
        if direction == "horizontal":
            self.change_dimensions(self.relative_rect.w,self._magic_number)
        else:
            self.change_dimensions(self._magic_number,self.relative_rect.h)
            
    def destroy(self) -> None:
        self._handle_button.destroy()
        super().destroy()
            
    def get_range(self):
        return (self._min,self._max)
    
    def set_range(self,min,max):
        self._min = min
        self._max = max
        self._clamp_value()
        self.rebuild()
            
    def set_value(self,value):
        old = self._value
        self._value = value
        self._clamp_value()
        self.rebuild()
        pygame.event.post(pygame.event.Event(constants.SLIDER_MOVED,{
            "old_value":old,
            "value":self._value,
            "rel":self._value-old,
            "percentage":self.get_percentage(),
            "manual":True,
            "slider_direction":self._direction,
            "element_ID":self._ID,
            "element_object":self
        }))
        
    def get_value(self):
        return self._value
    
    def get_percentage(self):
        return ((self._value-self._min)/(self._max-self._min))*100
    
    def set_percentage(self,percentage):
        v = (percentage*(self._max-self._min))/100
        self.set_value(v+self._min)
        
    def move_value(self,amount):
        self.set_value(self._value+amount)
        
    def move_percentage(self,amount):
        self.set_percentage(self.get_percentage()+amount)
        
    def rebuild(self):
        if self._direction == "horizontal":
            self.change_dimensions(self.relative_rect.w,self._magic_number,False)
            self._handle_button.relative_rect.center = (self.relative_rect.x+(((self._value-self._min)*self.relative_rect.w)/(self._max-self._min)),self.relative_rect.centery)
            self._handle_button.refresh_position()
        else:
            self.change_dimensions(self._magic_number,self.relative_rect.h,False)
            self._handle_button.relative_rect.center = (self.relative_rect.centerx,self.relative_rect.y+(((self._value-self._min)*self.relative_rect.h)/(self._max-self._min)))
            self._handle_button.refresh_position()
            
    def _calculate_value(self):
        if self._direction == "horizontal":
            self._value = (((self._handle_button.relative_rect.centerx-self.relative_rect.x)*(self._max-self._min))/self.relative_rect.w)+self._min
        else:
            self._value = (((self._handle_button.relative_rect.centery-self.relative_rect.y)*(self._max-self._min))/self.relative_rect.h)+self._min
    
    def update(self, dt,arg=None):
        if self._handle_button._is_clicking:
            rel = global_input.GlobalInput.mouse_rel
            if self._direction == "horizontal":
                relplusx = self._handle_button.relative_rect.centerx + rel[0]
                if rel[0] != 0 and relplusx >= self.relative_rect.left and relplusx <= self.relative_rect.right:
                    old = self._value
                    self._handle_button.update_position(rel[0],0)
                    self._calculate_value()
                    p = self._value * (1/100)
                    if self._max-p < self._value < self._max:
                        self.set_value(self._max)
                    elif self._min < self._value < self._min+p:
                        self.set_value(self._min)
                    pygame.event.post(pygame.event.Event(constants.SLIDER_MOVED,{
                        "old_value":old,
                        "value":self._value,
                        "rel":self._value-old,
                        "percentage":self.get_percentage(),
                        "slider_direction":self._direction,
                        "manual":False,
                        "element_ID":self._ID,
                        "element_object":self
                    }))
            else:
                relplusy = self._handle_button.relative_rect.centery + rel[1]
                if rel[1] != 0 and relplusy >= self.relative_rect.top and relplusy <= self.relative_rect.bottom:
                    old = self._value
                    self._handle_button.update_position(0,rel[1])
                    self._calculate_value()
                    p = self._value * (1/100)
                    if self._max-p < self._value < self._max:
                        self.set_value(self._max)
                    elif self._min < self._value < self._min+p:
                        self.set_value(self._min)
                    pygame.event.post(pygame.event.Event(constants.SLIDER_MOVED,{
                        "old_value":old,
                        "value":self._value,
                        "rel":self._value-old,
                        "percentage":self.get_percentage(),
                        "slider_direction":self._direction,
                        "manual":False,
                        "element_ID":self._ID,
                        "element_object":self
                    }))
        if self._direction == "horizontal":            
            if self._handle_button.relative_rect.centery != self.relative_rect.centery:
                self._handle_button.relative_rect.centery = self.relative_rect.centery
                self._handle_button.refresh_position()
            if self._handle_button.relative_rect.centerx < self.relative_rect.left:
                self._handle_button.relative_rect.centerx = self.relative_rect.left
                self._handle_button.refresh_position()
                self._calculate_value()
            if self._handle_button.relative_rect.centerx > self.relative_rect.right:
                self._handle_button.relative_rect.centerx = self.relative_rect.right
                self._handle_button.refresh_position()
                self._calculate_value()
        else:
            if self._handle_button.relative_rect.centerx != self.relative_rect.centerx:
                self._handle_button.relative_rect.centerx = self.relative_rect.centerx
                self._handle_button.refresh_position()
            if self._handle_button.relative_rect.centery < self.relative_rect.top:
                self._handle_button.relative_rect.centery = self.relative_rect.top
                self._handle_button.refresh_position()
                self._calculate_value()
            if self._handle_button.relative_rect.centery > self.relative_rect.bottom:
                self._handle_button.relative_rect.centery = self.relative_rect.bottom
                self._handle_button.refresh_position()
                self._calculate_value()
        
    def _clamp_value(self):
        if self._value < self._min:
            self._value = self._min
        elif self._value > self._max:
            self._value = self._max