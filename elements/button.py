from ..core.element import UIElement
from .. import global_input, constants
from ..core.text_renderer import TextRenderer
from ..core.shape_renderer import ShapeRenderer
import pygame

class UIButton(UIElement):
    """
    Every element can throw press and release events but with this special events are sent and text/shape is drawn.
    
    Parameters: all UIElement common parameters plus:
    
    :param text (str): text to be displayed on the button.
    :param enable_long_press (bool): if True, once the button is clicked the press state is kept until a new click happens. 
    """
    def __init__(self,relative_rect,ui_manager,container=None,text="Button",enable_long_press=False,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"],_name="button"):
        super().__init__(relative_rect,ui_manager,container,visible,id,True,_name)
        self._surface = pygame.Surface((relative_rect.w,relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._text = text
        self._text_renderer = TextRenderer(self)
        self._shape_renderer.enable_hover_effect = True
        self._shape_renderer.enable_click_effect = True
        if enable_long_press:
            self._enable_long_press = True
        
    def rebuild(self):
        self._surface = pygame.Surface((self.relative_rect.w,self.relative_rect.h),pygame.SRCALPHA,32).convert_alpha()
        self._text_renderer.rebuild()
        self.on_rebuild()
        
    def on_rebuild(self):
        pass
        
    def set_text(self,text:str)->None:
        """
        Changes the displayed text.
        
        :param text (str): the new text.
        """
        self._text = text
        self._text_renderer.rebuild()
        
    def get_text(self)->str:
        """:return: the text displayed"""
        return self._text
    
    def draw(self, surface,offset=(0,0)):
        if  self.absolute_rect.colliderect(self._container.absolute_rect):
            self._surface.fill(0)
            #self._surface.set_colorkey("black")
            self._shape_renderer.render(surface,offset)
            self._text_renderer.render(self._surface,offset)
            final = (self.relative_rect.x+offset[0],self.relative_rect.y+offset[1])
            surface.blit(self._surface,final)
            self._shape_renderer.render_outline(surface,offset)
        
    def on_press(self):
        pygame.event.post(pygame.event.Event(constants.BUTTON_PRESSED,{
            "element_ID":self._ID,
            "element_object":self
        }))
        
    def on_release(self):
        pygame.event.post(pygame.event.Event(constants.BUTTON_RELEASED,{
            "element_ID":self._ID,
            "element_object":self
        }))