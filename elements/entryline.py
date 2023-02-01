import pygame
from .. import constants
from ..core.text_renderer import TextRenderer
from ..core.element import UIElement
from ..global_input import GlobalInput

class UIEntryLine(UIElement):
    """
    Single line input entry line.
    
    Parameters: all UIElement common parameters plus:
    
    :param characters_limit (int): The text lenght cannot exceed this.
    :param show (str): If different from 'raw', the text will be the original but displayed as the selected character (example: password security) 
    """
    def __init__(self,relative_rect,ui_manager,container=None,characters_limit=-1,show="raw",visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,visible,id,True,"entryline")
        
        self._surface = pygame.Surface((relative_rect.w-6,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._showchar = show
        self._text = "A"
        self._char_offset = 0
        self._text_renderer = TextRenderer(self,True)
        self._is_focused = False
        self._limit = characters_limit
        h = self._text_renderer.text_surface.get_height()
        self._text = ""
        self._cursor_rect = pygame.Rect(0,0,2,h)
        self._cursor_index = 0
        self._last_key_pressed = None
        self._t = 0
        self._tim = 500
        self._tim2 = 60
        self._ct = self._tim
        self._cursor_on = False
        self._last_cursor_update = 0
        self._cursor_blink_time = 500
        self._time_since_last = 0
        self._time_gap = 500
        self._shape_renderer.enable_hover_effect = True
        self._shape_renderer.enable_click_effect = True
        self._text_renderer.rebuild()
        self._find_cursor_position()
        
    def _find_cursor_position(self):
        string = self._text[:self._cursor_index]
        if self._showchar != "raw":
            string = self._showchar[0]*len(string)
        sample = self._text_renderer.font.render(string,True,"white")
        width = sample.get_width()
        self._cursor_rect.centery = self.relative_rect.h/2
        self._cursor_rect.x = -self._text_renderer.char_width*self._char_offset+5+width
        if self._cursor_rect.x >= self.relative_rect.w-5:
            self._char_offset += 1
            self._text_renderer.rebuild()
            self._find_cursor_position()
        elif self._cursor_rect.x <= 3:
            self._char_offset -= 1
            self._text_renderer.rebuild()
            self._find_cursor_position()
        
    def draw(self, surface,offset=(0,0)):
        if self.absolute_rect.colliderect(self._container.absolute_rect):
            self._surface.fill(0)
            #self._surface.set_colorkey("black")
            self._shape_renderer.render(surface,offset)
            self._text_renderer.render(self._surface,offset)
            if self._is_focused and (self._cursor_on or GlobalInput.ticks-self._time_since_last <= self._time_gap):
                f = (self._cursor_rect.x+offset[0],self._cursor_rect.y+offset[1])
                r = self._cursor_rect.copy()
                r.topleft = f
                pygame.draw.rect(self._surface,"white",r)
            r = self.relative_rect.inflate(-6,0)
            final = (r.x+offset[0],r.y+offset[1])
            surface.blit(self._surface,final)
            self._shape_renderer.render_outline(surface,offset)
        
    def update(self, dt, arg=None):
        if GlobalInput.ticks - self._last_cursor_update >= self._cursor_blink_time:
            self._last_cursor_update = GlobalInput.ticks
            self._cursor_on = not self._cursor_on
        if self._last_key_pressed != None:
            if GlobalInput.keys_pressed[self._last_key_pressed]:
                if GlobalInput.ticks - self._t >= self._ct:
                    if self._ct == self._tim:
                        self._ct = self._tim2
                    self._t = GlobalInput.ticks
                    self._last_cursor_update = self._t
                    self._time_since_last = self._t
                    if self._last_key_pressed == pygame.K_BACKSPACE:
                        self._on_backspace()
                    elif self._last_key_pressed == pygame.K_DELETE:
                        self._on_delete()
                    elif self._last_key_pressed == pygame.K_LEFT:
                        self._on_direction("left")
                    elif self._last_key_pressed == pygame.K_RIGHT:
                        self._on_direction("right")
                    else:
                        self._on_unicode(pygame.key.name(self._last_key_pressed))
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self._is_hovering:
                self.unfocus()
        elif event.type == pygame.KEYDOWN:
            if self._is_focused:
                if event.key == pygame.K_BACKSPACE:
                    self._on_backspace()
                    self._last_key_pressed = pygame.K_BACKSPACE
                    self._set_timings()
                elif event.key == pygame.K_DELETE:
                    self._on_delete()
                    self._last_key_pressed = pygame.K_BACKSPACE
                    self._set_timings()
                elif event.key == pygame.K_ESCAPE:
                    self.unfocus()
                    self._last_key_pressed = None
                    self._set_timings()
                elif event.key == pygame.K_LEFT:
                    self._on_direction("left")
                    self._last_key_pressed = pygame.K_LEFT
                    self._set_timings()
                elif event.key == pygame.K_RIGHT:
                    self._on_direction("right")
                    self._last_key_pressed = pygame.K_RIGHT
                    self._set_timings()
                elif event.unicode != "":
                    self._on_unicode(event.unicode)
                    try:
                        self._last_key_pressed = pygame.key.key_code(event.unicode)
                        self._set_timings()
                    except:
                        self._last_key_pressed = None
            else:
                self._last_key_pressed = None
        elif event.type == pygame.KEYUP:
            self._last_key_pressed = None
    
    def _set_timings(self):
        self._t = GlobalInput.ticks
        self._ct = self._tim
        self._time_since_last = self._t
        self._last_cursor_update = self._t
                    
    def _on_direction(self,dir):
        if dir == "left":
            if self._cursor_index > 0:
                self._cursor_index-=1
                self._find_cursor_position()
        else:
            if self._cursor_index < len(self._text):
                self._cursor_index += 1
                self._find_cursor_position()
                        
    def _on_backspace(self):
        if len(self._text) > 0:
            left = self._text[:self._cursor_index]
            right = self._text[self._cursor_index:]
            left = left[:-1]
            self._text = left+right
            self._text_renderer.rebuild()
            self._cursor_index -= 1
            self._find_cursor_position()
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_TEXT_CHANGED,{
                "char":pygame.K_BACKSPACE,
                "deleted":True,
                "current_text":self._text,
                "manual":False,
                "element_ID":self._ID,
                "element_object":self
            }))
            
    def _on_delete(self):
        if self._cursor_index < len(self._text):
            left = self._text[:self._cursor_index]
            right = self._text[self._cursor_index:]
            right = right[1:]
            self._text = left+right
            self._text_renderer.rebuild()
            self._find_cursor_position()
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_TEXT_CHANGED,{
                "char":pygame.K_DELETE,
                "deleted":True,
                "current_text":self._text,
                "manual":False,
                "element_ID":self._ID,
                "element_object":self
            }))
    
    def _on_unicode(self, unicode):
        if len(self._text) < self._limit or self._limit == -1:
            left = self._text[:self._cursor_index]
            right = self._text[self._cursor_index:]
            left += unicode
            self._text = left+right
            self._text_renderer.rebuild()
            self._cursor_index += 1
            self._find_cursor_position()
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_TEXT_CHANGED,{
                "char":unicode,
                "deleted":False,
                "current_text":self._text,
                "manual":False,
                "element_ID":self._ID,
                "element_object":self
            }))
    
    def rebuild(self):
        self._surface = pygame.Surface((self.relative_rect.w-6,self.relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._char_offset = 0
        self._cursor_index = 0
        self._text_renderer.rebuild()
    
    def set_text(self,text):
        """Manually sets the text. :param text (str): the new text"""
        self._text = text
        if len(self._text) > self._limit and self._limit != -1:
            self._text = self._text[:self._limit]
        pygame.event.post(pygame.event.Event(constants.ENTRYLINE_TEXT_CHANGED,{
                "char":text,
                "deleted":False,
                "current_text":self._text,
                "manual":True,
                "element_ID":self._ID,
                "element_object":self
            }))
        self._cursor_index = len(self._text)
        self._find_cursor_position()
        self._text_renderer.rebuild()
        
    def add_text(self,text):
        self.set_text(self._text+text)
    
    def get_text(self)->str:
        """:return: the text stored in the input. """
        return self._text
    
    def focus(self)->None:
        """Manually focuses the entry line."""
        if not self._is_focused:
            self._is_focused = True
            self._cursor_on = True
            self._last_cursor_update = GlobalInput.ticks
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_FOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))
        
    def unfocus(self)->None:
        """Manually unfocuses the entry line"""
        if self._is_focused:
            self._is_focused = False
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_UNFOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))
    
    def on_press(self):
        if not self._is_focused:
            self._is_focused = True
            self._cursor_on = True
            self._last_cursor_update = GlobalInput.ticks
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_FOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))