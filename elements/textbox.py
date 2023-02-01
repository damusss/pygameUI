import pygame
from .. import constants
from ..elements.container import UIScrollableContainer
from ..core.text_renderer import TextBoxTextRenderer
from ..global_input import GlobalInput
from ..elements.scrollbar import UIVerticalScrollbar,UIHorizontalScrollbar

class UITextBox(UIScrollableContainer):
    def __init__(self,relative_rect,ui_manager,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,True,visible,id,False,"textbox")
        
        self._is_focused = False
        self._raw_text = "aaa\naaa"
        self._text_split = []
        self._refresh_text_list()
        self._text_renderer = TextBoxTextRenderer(self)
        
        self._cursor_index = pygame.math.Vector2(3,1)
        self._cursor_rect = pygame.Rect(0,0,2,self._text_renderer.char_height)
        self.set_vertical_scrollbar(UIVerticalScrollbar(pygame.Rect(0,0,10,self.relative_rect.h),self.ui_manager,self))
        self.set_horizontal_scrollbar(UIHorizontalScrollbar(pygame.Rect(0,0,self.relative_rect.w-self._vertical_scrollbar._magic_number,10),self.ui_manager,self))
        self.on_rebuild()
        self._on_horizontal_scrollbar_move(0)
        self._on_vertical_scrollbar_move(0)
        
        self._cursor_on = False
        self._blink_time = 500
        self._last_blink = GlobalInput.ticks
        
        self._text_renderer.complete_rebuild()
        self._find_cursor_position()
        
    def on_rebuild(self):
        self._vertical_scrollbar.relative_rect.topright = (self.relative_rect.w,0)
        self._vertical_scrollbar.refresh_position()
        self._vertical_scrollbar.change_dimensions(10,self.relative_rect.h)
        self._horizontal_scrollbar.relative_rect.bottomleft = (0,self.relative_rect.h)
        self._horizontal_scrollbar.refresh_position()
        self._horizontal_scrollbar.change_dimensions(self.relative_rect.w-self._vertical_scrollbar._magic_number,10)
        
    def _refresh_text_list(self):
        self._text_split = self._raw_text.split("\n")
        
    def _from_text_list(self):
        self._raw_text = "\n".join(self._text_split)
        
    def on_update(self, dt):
        if GlobalInput.ticks - self._last_blink > self._blink_time:
            self._cursor_on = not self._cursor_on
            self._last_blink = GlobalInput.ticks
            
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self._is_hovering:
                self.unfocus()
            else:
                self.focus()
        elif event.type == pygame.KEYDOWN:
            if self._is_focused:
                if event.key == pygame.K_BACKSPACE:
                    self._on_backspace()
                elif event.key == pygame.K_DELETE:
                    self._on_delete()
                elif event.key == pygame.K_RETURN:
                    self._on_return()
                elif event.key == pygame.K_LEFT:
                    self._on_left()
                elif event.key == pygame.K_RIGHT:
                    self._on_right()
                elif event.key == pygame.K_UP:
                    self._on_top()
                elif event.key == pygame.K_DOWN:
                    self._on_bottom()
                elif event.unicode != "":
                    self._on_unicode(event.unicode)
            
    def _on_delete(self):
        if self._cursor_index.x < len(self._text_split[int(self._cursor_index.y)]):
            row = self._text_split[int(self._cursor_index.y)]
            left = row[:int(self._cursor_index.x)]
            right = row[int(self._cursor_index.x):]
            right = right[1:]
            self._text_split[int(self._cursor_index.y)] = left+right
            self._from_text_list()
            self._text_renderer.rebuild_index(int(self._cursor_index.y),left+right)
            self._find_cursor_position()
        else:
            if self._cursor_index.y < len(self._text_split)-1:
                thattext = self._text_split[int(self._cursor_index.y)+1]
                self._text_split[int(self._cursor_index.y)] += thattext
                self._text_renderer.rebuild_index(int(self._cursor_index.y),self._text_split[int(self._cursor_index.y)])
                self._text_split.pop(int(self._cursor_index.y)+1)
                self._text_renderer.rebuild_remove(int(self._cursor_index.y)+1)
                self._from_text_list()
                self._find_cursor_position()
    
    def _on_backspace(self):
        if self._cursor_index.x > 0:
            row = self._text_split[int(self._cursor_index.y)]
            left = row[:int(self._cursor_index.x)]
            right = row[int(self._cursor_index.x):]
            left = left[:-1]
            self._text_split[int(self._cursor_index.y)] = left+right
            self._from_text_list()
            self._cursor_index.x -= 1
            self._text_renderer.rebuild_index(int(self._cursor_index.y),left+right)
            self._find_cursor_position()
        else:
            if self._cursor_index.y > 0:
                line = self._text_split[int(self._cursor_index.y)]
                self._text_split.pop(int(self._cursor_index.y))
                self._text_renderer.rebuild_remove(int(self._cursor_index.y))
                self._cursor_index.y -= 1
                row = self._text_split[int(self._cursor_index.y)]
                self._text_split[int(self._cursor_index.y)] += line
                self._text_renderer.rebuild_index(int(self._cursor_index.y),self._text_split[int(self._cursor_index.y)])
                self._cursor_index.x = len(row)
                self._from_text_list()
                self._find_cursor_position()
                
    def _on_return(self):
        current = self._text_split[int(self._cursor_index.y)]
        left = current[:int(self._cursor_index.x)]
        right = current[int(self._cursor_index.x):]
        self._text_split[int(self._cursor_index.y)] = left
        self._text_renderer.rebuild_index(int(self._cursor_index.y),left)
        self._cursor_index.y += 1
        self._text_split.insert(int(self._cursor_index.y),right)
        self._text_renderer.rebuild_add(int(self._cursor_index.y),right)
        self._cursor_index.x = 0
        self._from_text_list()
        self._find_cursor_position()
    
    def _on_left(self):
        if self._cursor_index.x > 0:
            self._cursor_index.x -= 1
            self._find_cursor_position()
        else:
            if self._cursor_index.y > 0:
                self._cursor_index.y -= 1
                self._cursor_index.x = len(self._text_split[int(self._cursor_index.y)])
                self._find_cursor_position()
    
    def _on_right(self):
        if self._cursor_index.x < len(self._text_split[int(self._cursor_index.y)]):
            self._cursor_index.x += 1
            self._find_cursor_position()
        else:
            if self._cursor_index.y < len(self._text_split)-1:
                self._cursor_index.y += 1
                self._cursor_index.x = 0
                self._find_cursor_position()
                
    def _on_top(self):
        if self._cursor_index.y > 0:
            self._cursor_index.y -= 1
            if self._cursor_index.x > len(self._text_split[int(self._cursor_index.y)]):
                self._cursor_index.x = len(self._text_split[int(self._cursor_index.y)])
            self._find_cursor_position()
    
    def _on_bottom(self):
        if self._cursor_index.y < len(self._text_split)-1:
            self._cursor_index.y += 1
            if self._cursor_index.x > len(self._text_split[int(self._cursor_index.y)]):
                self._cursor_index.x = len(self._text_split[int(self._cursor_index.y)])
            self._find_cursor_position()
    
    def _on_unicode(self,unicode):
        current = self._text_split[int(self._cursor_index.y)]
        left = current[:int(self._cursor_index.x)]
        right = current[int(self._cursor_index.x):]
        left += unicode
        self._text_split[int(self._cursor_index.y)] = left+right
        self._text_renderer.rebuild_index(int(self._cursor_index.y),left+right)
        self._cursor_index.x += 1
        self._from_text_list()
        self._find_cursor_position()
        
    def _find_cursor_position(self):
        row = self._text_split[int(self._cursor_index.y)]
        string = row[:int(self._cursor_index.x)]
        sample = self._text_renderer.font.render(string,True,"white")
        width = sample.get_width()
        self._cursor_rect.bottom = self._text_renderer.line_height * (self._cursor_index.y+1)+5+self._surface_offset.y
        self._cursor_rect.centerx = width+5+self._surface_offset.x
        self._max_elements_height = max(((len(self._text_split)+1)*self._text_renderer.line_height),self.relative_rect.h)
        m = 0
        for s in self._text_renderer.text_surfaces:
            if s.get_width() > m:
                m = s.get_width()
        self._max_elements_width = max(m,self.relative_rect.w)
        self._vertical_scrollbar._update_handle_height()
        self._horizontal_scrollbar._update_handle_width()
        if self._cursor_rect.x < 0+4:
            self._surface_offset.x += self._text_renderer.char_width
            self._horizontal_scrollbar._from_container(self._scrollbar_unit_horizontal)
            self._find_cursor_position()
        if self._cursor_rect.x > self.relative_rect.w-4-self._vertical_scrollbar._magic_number:
            self._surface_offset.x -= self._text_renderer.char_width
            self._horizontal_scrollbar._from_container(self._scrollbar_unit_horizontal)
            self._find_cursor_position()
        if self._cursor_rect.y < 0+4:
            self._surface_offset.y += self._text_renderer.line_height
            self._vertical_scrollbar._from_container(self._scrollbar_unit_vertical)
            self._find_cursor_position()
        if self._cursor_rect.y > self.relative_rect.h-4-self._horizontal_scrollbar._magic_number:
            self._surface_offset.y -= self._text_renderer.line_height
            self._vertical_scrollbar._from_container(self._scrollbar_unit_vertical)
            self._find_cursor_position()
            
    def _on_scrollbars_move(self):
        row = self._text_split[int(self._cursor_index.y)]
        string = row[:int(self._cursor_index.x)]
        sample = self._text_renderer.font.render(string,True,"white")
        width = sample.get_width()
        self._cursor_rect.bottom = self._text_renderer.line_height * (self._cursor_index.y+1)+5+self._surface_offset.y
        self._cursor_rect.centerx = width+5+self._surface_offset.x
    
    def on_draw(self, surface: pygame.Surface, offset=(0,0)):
        self._text_renderer.render(surface,offset)
        if self._cursor_on and self._is_focused:
            #copy = self._cursor_rect.copy()
            #copy.top += offset[1]+self._surface_offset.y
            #copy.bottom += offset[0]+self._surface_offset.x
            pygame.draw.rect(surface,"white",self._cursor_rect)
        
    def focus(self)->None:
        """Manually focuses the entry line."""
        if not self._is_focused:
            self._is_focused = True
            self._cursor_on = True
            self._last_blink = GlobalInput.ticks
            """
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_FOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))
            """
        
    def unfocus(self)->None:
        """Manually unfocuses the entry line"""
        if self._is_focused:
            self._is_focused = False
            """
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_UNFOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))
            """
    
    def on_press(self):
        if not self._is_focused:
            self._is_focused = True
            self._cursor_on = True
            self._last_blink = GlobalInput.ticks
            """
            pygame.event.post(pygame.event.Event(constants.ENTRYLINE_FOCUSED,{
                    "current_text":self._text,
                    "element_ID":self._ID,
                    "element_object":self
                }))
            """