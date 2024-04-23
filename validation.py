from button import Button
import pygame
import sys 
from blit_text import blit_text

# Default
pygame.font.init()
base_font = pygame.font.SysFont('arialblack',40)
b_color =  (255,255,255)
h_color = (115,115,115)
b_bordure = pygame.image.load("sprite/validation.png")

def Validation(screen,text_input:str,bordure = b_bordure,font=base_font, base_color=b_color, hovering_color=h_color,oui_fct= lambda : None,non_fct= lambda : None):
    """
    Crée une boucle infinie
    Affiche une interface avec une bordure au centre de l'écran actuelle affichant un texte et des bouttons:
    "texte texte texte texte texte texte texte texte "
                     oui    non

    screen : le display sur lequel affiché l'interaface de validation
    text_input : le message sur lequel on répond oui ou non
    bordure : bordure de l'interface
    font : font du text
    base_color : couleur du text
    hovering_color : couleur du text lorsque la souris est au dessus
    oui_fct : None par défaut sinon une fonction
    non_fct : None par défaut sinon une fonction
    """

    pause = True

    while pause:
        w,h = screen.get_size()
        x,y = pygame.mouse.get_pos()

        #interface 
        image = pygame.transform.scale(bordure,(3*w//4,h//2))
        rect = image.get_rect(center = (w//2,h//2))
        #button
        button_sprites = pygame.sprite.Group()
        oui = Button( w//2 - 200,  h//2 + 50 +25//2, 
                        text_input="OUI", font=font, base_color=base_color, hovering_color=hovering_color)
        non = Button( w//2 + 200 , h//2 + 50 +25//2, 
                            text_input="NON", font=font, base_color=base_color, hovering_color=hovering_color)

        button_sprites.add(oui)
        button_sprites.add(non)

        # commandes utilisateurs
        mouses = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            # La raison de ce loop c'est parce qu'on veut que les inputs soient très précis
            # mais en même temps, c'est tellement précis que appuyer sur escape pendant quelques milisecondes
            # nous fait ouvrir et fermer pause() plusieurs fois à la suite.
            # C'est pour donner un temps de pause avant de quitter pause().
            if event.type == pygame.QUIT or (keys[pygame.K_LALT] and keys[pygame.K_F4]):
                pygame.quit()
                sys.exit()
            if oui.collide(x,y) and mouses[0]:
                    pause = False
                    oui_fct() 
            if (event.type == pygame.KEYUP and  event.key == pygame.K_ESCAPE) or (non.collide(x,y) and mouses[0]):
                    pause = False
                    non_fct()

        # text

        # affichage
        blit_text(image,text_input,(0,image.get_height()//3))
        screen.blit(image, rect.topleft)
        for button in button_sprites.sprites():
             button.update(x,y)
             button.draw(screen)
        
        pygame.display.update()



    

