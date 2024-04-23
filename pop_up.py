import pygame
import sys
from blit_text import blit_text

# Default
pygame.font.init()
base_font = pygame.font.SysFont('arialblack',40)
b_bordure = pygame.image.load("sprite/pop_up.png")

def Pop_Up(screen,titre_input:str,text_input:str,bordure = b_bordure,font=base_font):
    """
    Crée une boucle infinie
    Affiche une interface avec une bordure au centre de l'écran actuelle affichant un texte.
    Cliquer n'importe où permet de quitter la boucle.

    screen : le display sur lequel affiché l'interaface de validation
    titre_input : le titre du message
    text_input : le message
    bordure : bordure de l'interface
    font : font du text
    """
    w,h = screen.get_size()
    image = pygame.transform.scale(bordure,(3*w//4,h//2))
    pause = True
    while pause:
        # commandes utilisateurs
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (keys[pygame.K_LALT] and keys[pygame.K_F4]):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                    pause = False

        # text
        titre = font.render(titre_input, True, (215, 252, 212))

        # affichage
        image.blit(titre, ((image.get_width()-titre.get_width())//2,image.get_height()//6))
        blit_text(image,text_input,(0,image.get_height()//3))
        screen.blit(image, image.get_rect(center = (w//2,h//2)))

        pygame.display.update()



    

