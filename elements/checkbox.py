import pygame
from .. import constants
from ..elements.button import UIButton

class UICheckbox(UIButton):
    """
    A button that sends special events and changes the text on press.
    If you want you can change the '_on_string' and '_off_string' (str) attributes.
    
    Parameters: all UIElement common parameters
    """
    def __init__(self, relative_rect, ui_manager, container=None, visible=True, id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect, ui_manager, container, "", True, visible, id,"checkbox")
        
        self._on_string = "•"
        self._off_string = ""
        self._settings["text_alignment"] = "center"
        
        self._text_renderer.font = pygame.font.Font(None,int(self._settings["font_size"]*3))
        
    def on_press(self):
        self.set_text(self._on_string)
        pygame.event.post(pygame.event.Event(constants.CHECKBOX_SELECTED,{
            "element_ID":self._ID,
            "element_object":self
        }))
        
    def on_release(self):
        self.set_text(self._off_string)
        pygame.event.post(pygame.event.Event(constants.CHECKBOX_UNSELECTED,{
            "element_ID":self._ID,
            "element_object":self
        }))