import pygame
from ..import constants
from ..core.element import UIElement
from ..core.text_renderer import TextRenderer

class UILabel(UIElement):
    """
    Displays simple text.
    
    Parameters: all UIElement common parameters plus:
    
    :param text (str): The text.
    """
    def __init__(self,relative_rect,ui_manager,text="Label",container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,visible,id,False,"label")
        
        self._surface = pygame.Surface((relative_rect.w,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._text = text
        self._text_renderer = TextRenderer(self)
        
    def rebuild(self):
        self._surface = pygame.Surface((self.relative_rect.w,self.relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._text_renderer.rebuild()
        
    def set_text(self,text:str)->None:
        """Changes the text. :param text (str): the new text"""
        self._text = text
        self._text_renderer.rebuild()
        
    def get_text(self)->str:
        """:return: the current text"""
        return self._text
    
    def draw(self, surface,offset=(0,0)):
        if self.absolute_rect.colliderect(self._container.absolute_rect):
            self._surface.fill(0)
            #self._surface.set_colorkey("black")
            #self.shape_renderer.render(surface)
            self._text_renderer.render(self._surface,offset)
            final = (self.relative_rect.x+offset[0],self.relative_rect.y+offset[1])
            surface.blit(self._surface,final)