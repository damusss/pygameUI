import pygame
from .. import constants
from ..core.element import UIElement
from ..core.image_renderer import ImageRenderer

class UIImage(UIElement):
    """
    Displays an image. The image will be resized to the relative rect size.
    
    Parameters: all UIElement common parameters plus:
    
    :param image (pygame.Surface): the first image to display.
    """
    def __init__(self,relative_rect,ui_manager,image=True,container=None,visible=True,id=constants.DEFAULT_SETTINGS["default_element_id"]):
        super().__init__(relative_rect,ui_manager,container,visible,id,element_name="image")
        
        self._image_renderer = ImageRenderer(self,image)
        
    def change_image(self,image:pygame.Surface)->None:
        """Sets a new image and resizes it if needed. :param image (pygame.Surface): the new image"""
        self._image_renderer.change_image(image)
        
    def rebuild(self):
        self._image_renderer.rebuild()
        
    def draw(self, surface,offset=(0,0)):
        if self.absolute_rect.colliderect(self._container.absolute_rect):
            self._image_renderer.render(surface,offset)