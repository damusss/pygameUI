import pygame

ELEMENT_HOVERED = pygame.event.custom_type()
ELEMENT_UNHOVERED = pygame.event.custom_type()
ELEMENT_HOVERING = pygame.event.custom_type()
ELEMENT_PRESSED = pygame.event.custom_type()
ELEMENT_RELEASED = pygame.event.custom_type()
BUTTON_PRESSED = pygame.event.custom_type()
BUTTON_RELEASED = pygame.event.custom_type()
ENTRYLINE_TEXT_CHANGED = pygame.event.custom_type()
ENTRYLINE_FOCUSED = pygame.event.custom_type()
ENTRYLINE_UNFOCUSED = pygame.event.custom_type()
WINDOW_CLOSED = pygame.event.custom_type()
WINDOW_MOVED = pygame.event.custom_type()
WINDOW_FOCUSED = pygame.event.custom_type()
WINDOW_UNFOCUSED = pygame.event.custom_type()
SCROLLBAR_MOVED = pygame.event.custom_type()
SELECTION_CHANGED = pygame.event.custom_type()
SELECTION_REMOVED = pygame.event.custom_type()
SELECTION_ADDED = pygame.event.custom_type()
CHECKBOX_SELECTED = pygame.event.custom_type()
CHECKBOX_UNSELECTED = pygame.event.custom_type()
DROPDOWN_SELECTED = pygame.event.custom_type()
PROGRESSBAR_MOVED = pygame.event.custom_type()
SLIDER_MOVED = pygame.event.custom_type()

DEFAULT_SETTINGS = {
    "bg_color":(20,20,20),
    "fg_color":(40,40,40),
    "fg_hovered_color":(50,50,50),
    "fg_pressed_color":(30,30,30),
    "outline_color":(80,80,80),
    "text_color":(220,220,220),
    "font_name":"Segoe UI",
    "font_size":18,
    "text_alignment":"center",
    "outline_enabled":True,
    "outline_size":2,
    "border_radius":0,
    "default_element_id":"unnamed_element",
    "magic_numbers":{
        "selectionlist":30,
        "window":30,
        "scrollbar":24,
        "dropdown":30,
        "slider":10,
        "handle":24
    }
}

SETTINGS = [
    
]

AVAILABLE_NAMES = [
    "element",
    "button",
    "checkbox",
    "label",
    "image",
    "dropdown",
    "dropdownarrow",
    "dropdownmenu",
    "dropdownoption",
    "container",
    "window",
    "windowtitlebar",
    "windowclosebutton",
    "windowcontainer",
    "entryline",
    "progressbar",
    "scrollbar",
    "scrollbarhandle",
    "selectionlist",
    "selectionlistbutton",
    "selectionlistscrollbar",
    "slider",
    "sliderhandle",
]

FS_INVISIBLE = 6
FS_SMALL = 12
FS_MEDIUM = 18
FS_BIG = 30
FS_GIANT = 50
FS_MONSTROUS = 100