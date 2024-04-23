import pygame
from button_image import Button_Image
from pop_up import Pop_Up
from validation import Validation

# text caracteristics
pygame.font.init()

class Shop_Item(Button_Image):
        
        def __init__(self, type:str, nom:str, availability:int,prix:int,image:pygame.surface.Surface):
            """
            type :  'weapon', 'buff', 'environment'
            nom : nom de l'item 
            availability : nombre de fois achetable.
            prix : prix de l'item
            image : image de l'item
            """
            assert type in ['weapon', 'buff', 'environment'], f"type devrait appartenir à 'weapon', 'buff', 'environment', ici est {type}"
            self.type = type
            self.nom = nom
            self.availability = availability
            self.prix = prix
            self.item_image = image
            self.bordure_str = "sprite/shop_item.png"
            super().__init__(0,0,0,0,pygame.image.load(self.bordure_str),pygame.image.load(self.bordure_str))

        def adjust(self,x:int,y:int,width:int,height:int):
            """
            Ajuste la taille et la disposition de self.
            """
            #text
            font = pygame.font.SysFont('arialblack',40)
            self.prix_text = font.render(str(self.prix),True,(255,255,0))
            self.h_prix_text = font.render(str(self.prix),True,(102,102,0))
            #Surfaces
            self.image = pygame.transform.scale(self.item_image,(3*width//5,3*height//5)).convert_alpha()
            self.bordure = pygame.transform.scale(pygame.image.load(self.bordure_str),(width,height)).convert_alpha()
            #Button_Image
            self.item = self.bordure
            self.item.blit(self.image,(width//2-self.image.get_width()//2,self.image.get_height()//4))
            self.h_item = self.item.copy()
            self.item.blit(self.prix_text,(width//2-self.prix_text.get_width()//2,height-self.prix_text.get_height()))
            self.h_item.blit(self.h_prix_text,(width//2-self.h_prix_text.get_width()//2,height-self.h_prix_text.get_height()))
            super().__init__(x,y,width,height,self.item,self.h_item)

        def info(self,screen):
            Pop_Up(screen,self.nom,"Work in progress")

        def buy(self,screen,oui=lambda i: None,non=lambda i:None):
            def f_oui():
                self.availability -= 1
                oui(self)
            f_non = lambda : non(self)
            Validation(screen,"Voulez-vous vraiment acheter?",oui_fct = f_oui ,non_fct = f_non)


