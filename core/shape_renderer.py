import pygame
from ..import constants

class ShapeRenderer(object):
    """Internal class used to draw background and outline of elements."""
    def __init__(self,element,isFG):
        self.element = element
        self.bg_color = self.element._settings["bg_color"] if not isFG else self.element._settings["fg_color"]
        self.enable_hover_effect = False
        self.enable_click_effect = False
        self.fghc = self.element._settings["fg_hovered_color"]
        self.fgpc = self.element._settings["fg_pressed_color"]
        self.br = self.element._settings["border_radius"]
        self.oc = self.element._settings["outline_color"]
        self.oe = self.element._settings["outline_enabled"]
        self.os = self.element._settings["outline_size"]
        self.only_outline = False
        
    def render(self,surface,offset=(0,0)):
        if not self.only_outline:
            col = self.bg_color
            if self.enable_hover_effect and self.element._is_hovering:
                col = self.fghc
            if self.enable_click_effect and self.element._is_clicking:
                col = self.fgpc
            before = self.element.relative_rect.topright
            self.element.relative_rect.topright = (before[0]+offset[0],before[1]+offset[1])
            pygame.draw.rect(surface,col,self.element.relative_rect,0,self.br)
            """
            if self.oe:
                pygame.draw.rect(surface,self.oc,self.element.relative_rect,self.os,self.br)
            """
            self.element.relative_rect.topright = before
        
    def render_outline(self,surface,offset):
        before = self.element.relative_rect.topright
        self.element.relative_rect.topright = (before[0]+offset[0],before[1]+offset[1])
        if self.oe:
            pygame.draw.rect(surface,self.oc,self.element.relative_rect,self.os,self.br)
        self.element.relative_rect.topright = before