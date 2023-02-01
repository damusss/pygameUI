import pygame
from .. import constants,global_input
from ..elements.container import UIScrollableContainer, UIContainer
from ..elements.button import UIButton

class UIWindow(UIContainer):
    def __init__(self,relative_rect,ui_manager,title="Window Title",kill_on_close=True,can_drag=True,scrollable=False,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],inner_ids={
        "titlebar":constants.DEFAULT_SETTINGS["default_element_id"],
        "closebutton":constants.DEFAULT_SETTINGS["default_element_id"],
        "container":constants.DEFAULT_SETTINGS["default_element_id"],
    }):
        super().__init__(relative_rect,ui_manager,container,True,visible,id,False,"window")
        
        self._magic_number = self._settings["magic_numbers"]["window"]
        self._kill_on_close = kill_on_close
        closebtnrect = pygame.Rect(self.relative_rect.w-self._magic_number,0,self._magic_number,self._magic_number)
        self.close_button = UIButton(closebtnrect,self.ui_manager,self,"X",id=inner_ids["closebutton"],_name="windowclosebutton")
        self.close_button._settings["text_alignment"] = "center"
        self.close_button._text_renderer.rebuild()
        topbarrect = pygame.Rect(0,0,self.relative_rect.w-self._magic_number,self._magic_number)
        self._title_bar = UIButton(topbarrect,self.ui_manager,self,title,id=inner_ids["titlebar"],_name="windowtitlebar")
        self._title_bar._settings["text_alignment"] = "left"
        self._title_bar._text_renderer.rebuild()
        innercontrect = pygame.Rect(0,self._magic_number,self.relative_rect.w,self.relative_rect.h-self._magic_number)
        if not scrollable:
            self._elements_containter = UIContainer(innercontrect,self.ui_manager,self,True,id=inner_ids["container"],_name="windowcontainer")
        else:
            self._elements_containter = UIScrollableContainer(innercontrect,self.ui_manager,self,True,id=inner_ids["container"],_name="windowcontainer")
        self._is_focused = False
        self._can_drag = can_drag
        
    def on_update(self, dt):
        if self.close_button.check_pressed():
            pygame.event.post(pygame.event.Event(constants.WINDOW_CLOSED,{
                "element_ID":self._ID,
                "element_object":self
            }))
            if self._kill_on_close:
                self.destroy()
        if self._title_bar._is_clicking and self._can_drag:
            rel = global_input.GlobalInput.mouse_rel
            self.update_position(rel[0],rel[1])
            pygame.event.post(pygame.event.Event(constants.WINDOW_MOVED,{
                "element_ID":self._ID,
                "element_object":self,
                "relative_position":self.relative_rect.topleft,
                "absolute_position":self.absolute_rect.topleft
            }))
                
    def focus(self):
        if not self._is_focused:
            self._is_focused = True
            pygame.event.post(pygame.event.Event(constants.WINDOW_FOCUSED,{
                "element_ID":self._ID,
                "element_object":self
            }))
            self._container._on_element_destroy(self)
            for el in self._container._elements:
                if hasattr(el,"_is_focused"):
                    el.unfocus()
            self._container._register_element(self)
    
    def unfocus(self):
        if self._is_focused:
            self._is_focused = False
            pygame.event.post(pygame.event.Event(constants.WINDOW_UNFOCUSED,{
                "element_ID":self._ID,
                "element_object":self
            }))
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovering:
                self.focus()
        
    def get_container(self):
        return self._elements_containter
    
    def get_title(self):
        return self._title_bar._text
    
    def set_title(self,title):
        self._title_bar.set_text(title)