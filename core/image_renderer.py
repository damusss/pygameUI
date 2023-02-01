import pygame
from .. import constants

class ImageRenderer:
    """Internal class used for rendering images by 'UIImage'"""
    def __init__(self,element,surface):
        self.element = element
        self.original_surface = surface
        self.surface = self.original_surface
        self.eo = self.element._settings["outline_enabled"]
        self.oc = self.element._settings["outline_color"]
        self.os = self.element._settings["outline_size"]
        self.br = self.element._settings["border_radius"]
        self.rebuild()
        
    def change_image(self,image):
        self.original_surface = image
        self.surface = self.original_surface
        self.rebuild()
        
    def rebuild(self):
        self.surface = pygame.transform.scale(self.original_surface,(self.element.relative_rect.w,self.element.relative_rect.h))
        
    def render(self,surface,offset=(0,0)):
        offsetted = (self.element.relative_rect.x+offset[0],self.element.relative_rect.y+offset[1])
        surface.blit(self.surface,offsetted)
        if self.eo:
            before = self.element.relative_rect.topright
            self.element.relative_rect.topright = (before[0]+offset[0],before[1]+offset[1])
            pygame.draw.rect(surface,self.oc,self.element.relative_rect,self.os,self.br)
            self.element.relative_rect.topright = before