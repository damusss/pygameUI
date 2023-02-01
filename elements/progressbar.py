import pygame, math
from .. import constants
from ..core.element import UIElement

class UIProgressBar(UIElement):
    def __init__(self,relative_rect,ui_manager,min_value=0,max_value=1,current_value=0.5,direction="left-right",container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,visible,id,False,"progressbar")
        
        if direction not in ["left-right","right-left","top-bottom","bottom-top"]:
            raise Exception("Supported directions for 'UIProgressBar' are 'left-right', 'right-left', 'top-bottom', 'bottom-top'")
        self._min = min_value
        self._max = max_value
        self._value = current_value
        self._direction = direction
        self._draw_callback = self.on_draw
        self._bar_rect = pygame.Rect(0,0,1,1)
        self._r = self._bar_rect.copy()
        self._move_callback = self._on_move
        self._col = self._settings["fg_color"]
        self._br = self._settings["border_radius"]
        self._clamp_value()
        self.rebuild()
        
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
        pygame.event.post(pygame.event.Event(constants.PROGRESSBAR_MOVED,{
            "old_value":old,
            "value":self._value,
            "rel":self._value-old,
            "percentage":self.get_percentage(),
            "element_ID":self._ID,
            "element_object":self
        }))
        
    def get_percentage(self):
        return ((self._value-self._min)/(self._max-self._min))*100
    
    def set_percentage(self,percentage):
        v = (percentage*(self._max-self._min))/100
        self.set_value(v+self._min)
        
    def move_value(self,amount):
        self.set_value(self._value+amount)
        
    def move_percentage(self,amount):
        self.set_percentage(self.get_percentage()+amount)
        
    def get_value(self):
        return self._value
        
    def rebuild(self):
        if self._direction == "left-right" or self._direction == "right-left":
            w = ((self._value-self._min)*self.relative_rect.w)/(self._max-self._min)
            self._bar_rect.w = w
            self._bar_rect.h = self.relative_rect.h
        else:
            h = ((self._value-self._min)*self.relative_rect.h)/(self._max-self._min)
            self._bar_rect.h = h
            self._bar_rect.w = self.relative_rect.w
        self._on_move()
            
    def _on_move(self):
        if self._direction == "left-right":
            self._bar_rect.topleft = self.relative_rect.topleft
        elif self._direction == "right-left":
            self._bar_rect.topright = self.relative_rect.topright
        elif self._direction == "top-bottom":
            self._bar_rect.topleft = self.relative_rect.topleft
        else:
            self._bar_rect.bottomleft = self.relative_rect.bottomleft
        self._r = self._bar_rect.inflate(-4,-4)
        
    def _clamp_value(self):
        if self._value < self._min:
            self._value = self._min
        elif self._value > self._max:
            self._value = self._max
            
    def on_draw(self,surface,offset):
        self._r.topleft = (self._bar_rect.left+offset[0]+2,self._bar_rect.top+offset[1]+2)
        pygame.draw.rect(surface,self._col,self._r,0,self._br)