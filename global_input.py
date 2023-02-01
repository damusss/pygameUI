import pygame

class GlobalInput:
    mouse_pos = (0,0)
    keys_pressed = []
    mouse_pressed = []
    mouse_rel = (0,0)
    ticks = 0
    
    @classmethod
    def update(cls):
        cls.mouse_pos = pygame.mouse.get_pos()
        cls.keys_pressed = pygame.key.get_pressed()
        cls.mouse_pressed = pygame.mouse.get_pressed()
        cls.mouse_rel = pygame.mouse.get_rel()
        cls.ticks = pygame.time.get_ticks()