import pygame
from . import global_input
from .core.element import UIElement
from .elements.container import UIContainer,UIWindowContainer, UIScrollableContainer
from .constants import *
from .elements.label import UILabel
from .elements.button import UIButton
from .elements.image import UIImage
from .elements.entryline import UIEntryLine
from .elements.window import UIWindow
from .elements.scrollbar import UIVerticalScrollbar,UIHorizontalScrollbar
from .elements.selectionlist import UISelectionList
from .elements.checkbox import UICheckbox
from .elements.dropdown import UIDropDown
from .elements.progressbar import UIProgressBar
from .elements.slider import UISlider
from .elements.textbox import UITextBox

class UIManager:
    def __init__(self,window_sizes:tuple[int],colored_window_container:bool=False,default_settings_override=None,settings=None):
        self.settings = list()
        if settings != None:
            self.settings = settings
        self.window_container = UIWindowContainer(pygame.Rect(0,0,window_sizes[0],window_sizes[1]),self,colored=colored_window_container)
            
        if default_settings_override != None:
            self._override_default_settings(default_settings_override)
        
    def _get_settings(self,element_id,element_name):
        settings = DEFAULT_SETTINGS.copy()
        if len(self.settings)>0:
            for s in self.settings:
                if "element_ids" in s or "element_names" in s:
                    if "element_names" in s:
                        if element_name in s["element_names"]:
                            for k in s["settings"].keys():
                                settings[k] = s["settings"][k]
                    if "element_ids" in s:
                        if element_id in s["element_ids"]:
                            for k in s["settings"].keys():
                                settings[k] = s["settings"][k]
                            break
                else:
                    raise Exception("User defined settings must define either the 'element_ids' or 'element_names' key")
        return settings
        
    def _override_default_settings(self,default_settings):
        for key in default_settings.keys():
            if key in DEFAULT_SETTINGS:
                DEFAULT_SETTINGS[key] = default_settings[key]
            else:
                raise Exception(f"Cannot modify key '{key}' in 'DEFAULT_SETTINGS' because the original does not contain it")
    
    def draw_ui(self,screen):
        self.window_container.draw(screen)
    
    def update_ui(self,delta_time):
        global_input.GlobalInput.update()
        self.window_container.update(delta_time)
    
    def handle_events(self,event):
        self.window_container.event(event)