import pygame
from .. import constants,global_input
from ..elements.button import UIButton
from ..elements.container import UIContainer

class UIDropDown(UIButton):
    """
    Contains a list of options and displays the selected one.
    
    Parameters: all UIElement common parameters plus:
    
    :param starting_options (list[str]): starting list of options.
    :param selected_option (str): the firstly selected option.
    :param direction (str): Either up or down. Determines the options menu direction.
    """
    
    def __init__(self,relative_rect,ui_manager,starting_options,selected_option,direction = "down",container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],
                 inner_ids={
                     "menucontainer":constants.DEFAULT_SETTINGS["default_element_id"],
                     "arrowbutton":constants.DEFAULT_SETTINGS["default_element_id"],
                     "optionprefix":constants.DEFAULT_SETTINGS["default_element_id"]
                 }):
        super().__init__(relative_rect,ui_manager,container,selected_option,False,visible,id,"dropdown")
        self._option_prefix = inner_ids["optionprefix"]
        self._direction = direction
        self._magic_number = self._settings["magic_numbers"]["dropdown"]
        self._options_container = UIContainer(pygame.Rect(0,self.relative_rect.h,self.relative_rect.w,self._magic_number),self.ui_manager,container,True,False,id=inner_ids["menucontainer"],_name="dropdownmenu")
        self._down_arrow = "▼"
        self._up_arrow = "▲"
        ar = self._down_arrow if self._direction == "down" else self._up_arrow
        self._arrow_button = UIButton(pygame.Rect(self.relative_rect.w,self.relative_rect.y,self._magic_number,self.relative_rect.h),self.ui_manager,container,ar,False,id=inner_ids["arrowbutton"],_name="dropdownarrow")
        self._arrow_button._press_callback = self.on_press
        self._selected_option = str(selected_option)
        self._options = starting_options
        self._move_callback = self._on_move
        self._on_move()
        self.on_rebuild()
        
    def get_selected(self)->str:
        """:return: The currently selected option"""
        return self._selected_option
    
    def set_selected(self,option:str)->None:
        """Manually changes the selection. :param option (str): the selected option."""
        old = self._selected_option
        self._selected_option = str(option)
        self.set_text(self._selected_option)
        pygame.event.post(pygame.event.Event(constants.DROPDOWN_SELECTED,{
            "old":old,
            "new":str(option),
            "manual":True,
            "element_ID":self._ID,
            "element_object":self
        }))
        
    def set_options(self,options:list[str])->None:
        """Changes the options list and rebuild. :param options (list[str]): thw new options"""
        self._options = options
        self.on_rebuild()
        
    def _on_move(self):
        if self._direction == "down":
            self._options_container.set_position(self.relative_rect.bottomleft)
        else:
            self._options_container.relative_rect.bottomleft = self.relative_rect.topleft
            self._options_container.refresh_position()
        self._arrow_button.relative_rect.topleft = self.relative_rect.topright
        self._arrow_button.refresh_position()
        
    def on_rebuild(self):
        self._options_container.change_dimensions(self.relative_rect.w,self._magic_number*len(self._options)-len(self._options)+2)
        i = 0
        els = self._options_container._elements_right.copy()
        for el in els:
            el.destroy()
        options = self._options if self._direction == "down" else list(reversed(self._options))
        for option in options:
            r = pygame.Rect(0,self._magic_number*i-i,self.relative_rect.w,self._magic_number)
            btn = UIButton(r,self.ui_manager,self._options_container,option,False,id=self._option_prefix+str(i),_name="dropdownoption")
            btn._press_callback = self._on_option_click
            btn._shape_renderer.oe = False
            i += 1
        self._arrow_button.change_dimensions(self._magic_number,self.relative_rect.height)
        self._on_move()
        
    def _on_option_click(self,btn):
        old = self._selected_option
        self.set_text(btn.get_text())
        self._options_container.hide()  
        self._selected_option = self.get_text()
        if self._direction == "down":
            self._arrow_button.set_text(self._down_arrow)
        else:
            self._arrow_button.set_text(self._up_arrow)
        pygame.event.post(pygame.event.Event(constants.DROPDOWN_SELECTED,{
            "old":str(old),
            "new":str(self._selected_option),
            "manual":False,
            "element_ID":self._ID,
            "element_object":self
        }))
    
    def on_press(self,btn=None):
        if self._options_container.visible:
            self._options_container.hide()
            if self._direction == "down":
                self._arrow_button.set_text(self._down_arrow)
            else:
                self._arrow_button.set_text(self._up_arrow)
        else:
            self._options_container.show()
            if self._direction == "down":
                self._arrow_button.set_text(self._up_arrow)
            else:
                self._arrow_button.set_text(self._down_arrow)