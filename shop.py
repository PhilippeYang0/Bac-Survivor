from shop_item import Shop_Item
from button_image import Button_Image
from pop_up import Pop_Up
import pygame
import sys

# text caracteristics
pygame.font.init()

class Shop():
    """
    Inteface de boutique
    Les shop sera affiché avec des pages
    Chaque page peut contenir 8 items.
    Le player peut changer de pages grâce aux bouttons associés
    """
    def __init__(self,item_list,buy_environnement,buy_buff,buy_weapon):
        """
        buy_environnement: fonction à activer quand on achète un environnement.
        buy_buff: fonction à activer quand on achète un buff.
        buy_weapon: fonction à activer quand on achète une arme.
        item dans items
        item = (type,nom,prix,image)
        """
        self.item_list = pygame.sprite.Group()
        for item in item_list:
            self.item_list.add(Shop_Item(*item))
        self.max = len(item_list)//8 + ( 1 if len(item_list)%8 != 0 else 0 )
        self.gold = 0
        self.current_page = 0
        self.current_page_list = []
        self.current_sprites_group = pygame.sprite.Group()
        self.buy_environnement, self.buy_buff, self.buy_weapon = buy_environnement,buy_buff,buy_weapon

    def update_gold(self,gold) -> None :
        """
        Met à jour le gold du shop
        """
        self.gold = gold

    def next_page(self) -> None:
        """
        Augmente la page actuelle de 1
        """
        self.current_page += 1 if self.current_page < self.max-1 else 0

    def prev_page(self) -> None:
        """
        Augmente la page actuelle de 1
        """
        self.current_page -= 1 if self.current_page != 0 else 0
    
    def page_update(self) -> None:
        """
        Renvoie une liste d'items de la page actuelle
        """
        self.current_page_list = self.item_list.sprites()[self.current_page*8: self.current_page*8 + 7 if self.current_page*8 + 7 < self.max else None]
        
    def update_item_list(self):
        """
        Met à jour la liste d'items de self.
        """
        self.item_list = pygame.sprite.Group([item for item in self.item_list if item.availability > 0])

    def page_items_update(self,w,h) -> None:
        w_ecart,h_ecart = w//5,h//3 
        w_item,h_item = 4*w_ecart//5,3*h_ecart//4
        self.page_update()
        self.current_sprites_group = pygame.sprite.Group()
        for i,e in enumerate(self.current_page_list):
            e.adjust((i%4+1) * w_ecart, h_ecart if i<4 else 2*h_ecart,w_item,h_item)
            self.current_sprites_group.add(e)
    

    def create_shop(self,screen):
        """
        Crée l'interface et l'affiche
        """
        w,h = screen.get_size()
        
        font = pygame.font.SysFont('arialblack',40)
        color =  (214,186,115)
        bg = pygame.transform.scale(pygame.image.load("sprite/shop.png"),(w,h))

        #Buttons
        button_image_sprites = pygame.sprite.Group()
        prev = Button_Image(w//8,7*h//8,w//8,h//8,pygame.image.load("sprite/left_b.png"),pygame.image.load("sprite/left_h.png"))
        next = Button_Image(7*w//8,7*h//8,w//8,h//8,pygame.image.load("sprite/right_b.png"),pygame.image.load("sprite/right_h.png"))
        help = Button_Image(13*w//16,h//8,h//10,h//10,pygame.image.load("sprite/help_b.png"),pygame.image.load("sprite/help_h.png"))
        quit = Button_Image(15*w//16,h//8,h//10,h//10,pygame.image.load("sprite/quit_b.png"),pygame.image.load("sprite/quit_h.png"))

        button_image_sprites.add(prev)
        button_image_sprites.add(next)
        button_image_sprites.add(help)
        button_image_sprites.add(quit)

        self.page_items_update(w,h)
        self.refresh_item_list = False
        pause = True
        while pause:
            #refresh
            if self.refresh_item_list:
                self.refresh_item_list = False
                self.update_item_list()
                self.page_items_update(w,h)
            gold = font.render(str(self.gold),True,(255,255,0))
            titre = font.render("SHOP",True,color)
            page = font.render(f"{self.current_page + 1} / {self.max}",True,color)
            
            # affichage / commandes utilisateurs
            x,y = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            mouses = pygame.mouse.get_pressed()
                        
            #Button Interactions
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (keys[pygame.K_LALT] and keys[pygame.K_F4]):
                    pygame.quit()
                    sys.exit()
            if   keys[pygame.K_ESCAPE]or (quit.collide(x,y) and mouses[0]):
                    pause = False
            if  prev.collide(x,y) and mouses[0]:
                self.prev_page()
                self.page_items_update(w,h)
            elif  next.collide(x,y) and mouses[0]:
                self.next_page()
                self.page_items_update(w,h)   
            elif help.collide(x,y) and mouses[0]:
                Pop_Up(screen,"AIDE","click gauche pour acheter\nclick droit pour voir les détails\néchap pour quitter")

            #Affichage
            screen.fill((153,76,0))
            screen.blit(bg, (0, 0))
            for button_image in button_image_sprites.sprites():
                button_image.update(x,y)
                button_image.draw(screen)
            screen.blit(titre, titre.get_rect(center=(w//2, 3*titre.get_height()//2)))
            screen.blit(gold, titre.get_rect(center=(w//6, 3*gold.get_height()//2)))
            screen.blit(page, titre.get_rect(center=(w//2, h-3*titre.get_height()//2)))

            #Items Interaction
            self.current_sprites_group.update(x,y)
            self.current_sprites_group.draw(screen)
            for item in self.current_sprites_group.sprites():
                if item.collide(x,y):
                    if mouses[2]:
                        item.info(screen)
                    elif mouses[0] and item.prix <= self.gold:
                        def bb(item):
                            #Achat d'un buff
                            self.buy_buff(item)
                            if item.availability <= 0:
                                self.refresh_item_list = True
                            self.gold -= item.prix
                        def be(item):
                            #Achat d'un level (environnement)
                            self.buy_environnement(item)
                            if item.availability <= 0:
                                self.refresh_item_list = True
                            self.gold -= item.prix
                        def bw(item):
                            #Achat d'un weapon
                            self.buy_weapon(item)
                            if item.availability <= 0:
                                self.refresh_item_list = True
                            self.gold -= item.prix
                        if item.type == "buff":
                            item.buy(screen, bb)
                        elif item.type == "environment":
                            item.buy(screen, be)
                        else:
                            item.buy(screen, bw)

            pygame.display.update()