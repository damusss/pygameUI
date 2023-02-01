import pygame
from .. import constants

class TextRenderer:
    """Internal class to render text inside elements."""
    def __init__(self,element,is_entryline=False):
        self.element = element
        self.fs = self.element._settings["font_size"]
        self.font = pygame.font.SysFont(self.element._settings["font_name"],self.fs)
        self.tc = self.element._settings["text_color"]
        self.isentryline = is_entryline
        sample = self.font.render("m",True,"white")
        self.char_width = sample.get_width()
        self.rebuild()
        
    def rebuild(self):
        if self.isentryline and self.element._showchar != "raw":
            self.text_surface = self.font.render(self.element._showchar[0]*len(str(self.element._text)),True,self.tc)
        else:
            self.text_surface = self.font.render(str(self.element._text),True,self.tc)
        self.text_rect = self.text_surface.get_rect(topleft=(0,0))
        if not self.isentryline:
            match self.element._settings["text_alignment"]:
                
                case "center":  
                    self.text_rect.center = (self.element.relative_rect.w/2,self.element.relative_rect.h/2)
                case "topright":
                    self.text_rect.topright = (self.element.relative_rect.w-3,0)
                case "bottomleft":
                    self.text_rect.bottomleft = (0,self.element.relative_rect.h-3)
                case "bottomright":
                    self.text_rect.bottomright = (self.element.relative_rect.w-3,self.element.relative_rect.h-3)
                case "left":
                    self.text_rect.midleft = (0+3,self.element.relative_rect.h/2)
                case "right":
                    self.text_rect.midright = (self.element.relative_rect.w-3,self.element.relative_rect.h/2)
                case "top":
                    self.text_rect.midtop = (self.element.relative_rect.w/2,0+3)
                case "bottom":
                    self.text_rect.midbottom = (self.element.relative_rect.w/2,self.element.relative_rect.h-3)
        else:
            self.text_rect.centery = self.element.relative_rect.h/2
            self.text_rect.x = -self.char_width*self.element._char_offset + 5
        
    def render(self,surface,offset):
        #final = (self.text_rect.x+offset[0],self.text_rect.y+offset[1])
        surface.blit(self.text_surface,self.text_rect)
        
class TextBoxTextRenderer:
    def __init__(self,textbox):
        self.textbox = textbox
        self.fs = self.textbox._settings["font_size"]
        self.font = pygame.font.SysFont(self.textbox._settings["font_name"],self.fs)
        self.tc = self.textbox._settings["text_color"]
        sample = self.font.render("A",True,"white")
        self.char_width = sample.get_width()
        self.char_height = sample.get_height()
        self.line_height = self.char_height +5
        
        self.text_surfaces = list()
        
    def complete_rebuild(self):
        for surf in self.text_surfaces:
            del surf
        self.text_surfaces.clear()
        split = self.textbox._raw_text.split("\n")
        for s in split:
            self.text_surfaces.append(self.font.render(s,True,self.tc))
        
    def rebuild_index(self,line_index,text):
        surf = self.font.render(str(text),True,self.tc)
        self.text_surfaces[line_index] = surf
    
    def rebuild_add(self,line_index,text):
        self.text_surfaces.insert(line_index,self.font.render(str(text),True,self.tc))
    
    def rebuild_remove(self,line_index):
        self.text_surfaces.pop(line_index)
        
    def render(self,surface,offset):
        i = 0
        for surf in self.text_surfaces:
            surface.blit(surf,(5+offset[0]+self.textbox._surface_offset.x,5+self.line_height*i+offset[1]+self.textbox._surface_offset.y))
            i += 1