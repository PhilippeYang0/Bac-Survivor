import pygame

class Background(pygame.sprite.Sprite):
    """
    Sprite Background
    Compatible avec camera.center_draw(player)
    """
    def __init__(self,size:tuple,image:pygame.Surface):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect(topleft = (0,0))
