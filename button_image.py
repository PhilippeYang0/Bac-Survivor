import pygame 

# default
class Button_Image(pygame.sprite.Sprite):
    """
    Button interactive
    """
    def __init__(self,x0:int , y0:int,width:int,height:int, image,hover_image=None):
            super().__init__()

            self.x0 = x0
            self.y0 = y0
            self.base_image = pygame.transform.scale(image,(width,height))
            self.hover_image = self.base_image if hover_image == None else pygame.transform.scale(hover_image,(width,height))
            self.image = self.base_image
            self.rect = self.image.get_rect(center=(self.x0, self.y0))
    
    def collide(self,x:int,y:int) -> bool:
         """
         Renvoie True si les positions x,y sont inclus dans self.rect
         """
         col = self.rect.collidepoint((x,y))
         return col
    
    def update(self, x:int,y:int) -> None:
        """
        Change la couleur de self.text lorsque x,y sont inclus dans self.rect
        """
        self.image = self.hover_image if (self.collide(x,y) and not (self.hover_image == None)) else self.base_image

    def draw(self, screen) -> None:
        """
        Dessine self sur screen
        """
        screen.blit(self.image, self.rect)
        