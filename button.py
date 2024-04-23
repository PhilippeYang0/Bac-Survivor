import pygame 

# default
pygame.font.init()
base_font = pygame.font.SysFont('arialblack',40)
b_color =  (215, 252, 212)
h_color = (255,255,255)

class Button(pygame.sprite.Sprite):
    """
    Boutton interactive
    """
    def __init__(self,x0:int , y0:int, text_input:str, font=base_font, base_color=b_color, hovering_color=h_color):
            super().__init__()

            self.x0 = x0
            self.y0 = y0
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.rect = self.text.get_rect(center=(self.x0, self.y0))
    
    def collide(self,x:int,y:int) -> bool:
         """
         Renvoie True si les positions x,y sont inclus dans self.rect
         """
         col = self.rect.collidepoint((x,y))
         return col
    
    def update(self, x:int,y:int) -> None:
        """
        update la couleur de self.text lorsque x,y sont inclus dans self.rect
        """
        color = self.hovering_color if self.collide(x,y) else self.base_color
        self.text = self.font.render(self.text_input,True,color)

    def draw(self, screen) -> None:
        """
        Dessine self sur screen
        """
        screen.blit(self.text, self.rect)
        