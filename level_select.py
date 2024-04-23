from button_image import Button_Image
import pygame
import sys 


def level_select(screen,level_path_list)->str:
    """
    level_path_list: liste de dictionnaires {"background": display de l'environnement pour le choix,
                                             "path": chemin aux données de jeu.}
    Crée une boucle infinie
    Affiche une interface affichant des images de levels
    Clicker sur une des images renvoie le chemin vers le fichier contenant le level.
    Renvoie '' si on ne choisit pas de level
    """
    # Default
    pygame.font.init()
    font = pygame.font.SysFont('arialblack',40)
    w,h = screen.get_size()
    w_ecart,h_ecart = w//4,h//3 
    w_level,h_level = 4*w_ecart//5,3*h_ecart//4
    
    outline_b = pygame.transform.scale(pygame.image.load("sprite/outline_b.png"),(w_level,h_level))
    outline_h = pygame.transform.scale(pygame.image.load("sprite/outline_h.png"),(w_level,h_level))
    
    
    while True:

        #button
        level_sprites = pygame.sprite.Group()
        for i,level_path in enumerate(level_path_list):
            image_b = pygame.transform.scale(pygame.image.load(level_path + "display_choix.png"),(w_level,h_level) )
            image_h = image_b.copy()
            image_b.blit(outline_b,(0,0))
            image_h.blit(outline_h,(0,0)) 
            level = Button_Image((i%3+1)*w_ecart, h_ecart if i<3 else 2*h_ecart,w_level,h_level,image_b,image_h )
            level_sprites.add(level)
        
        quit = Button_Image(15*w//16,h//8,h//10,h//10,pygame.image.load("sprite/quit_b.png"),pygame.image.load("sprite/quit_h.png"))

        # commandes utilisateurs
        x,y = pygame.mouse.get_pos()
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
            if (event.type == pygame.KEYUP and  keys[pygame.K_ESCAPE]) or (quit.collide(x,y) and mouses[0]):
                return ''

        # text
        text_level = font.render('LEVELS', True, (214,186,115))

        # affichage
        screen.fill((153,76,0))
        level_sprites.update(x,y)
        level_sprites.draw(screen)
        quit.update(x,y)
        quit.draw(screen)
        screen.blit(text_level, text_level.get_rect(center=(w//2, text_level.get_height())))
        for i,level in enumerate(level_sprites.sprites()):
            if level.collide(x,y) and mouses[0]:
                 return level_path_list[i]

        pygame.display.update()