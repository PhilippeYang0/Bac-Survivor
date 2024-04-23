from button_image import Button_Image
from insertinfo import update
from validation import Validation
import pygame
import sys



def Settings(screen,actual_display:int,volume_bgm:float,volume_se:float,save_file:str):
    """
    Interface dans lequel on peut modifier  3 valeurs de save.json :
    actual_display, volume_bgm,volume_se
    """
    #init
    pygame.font.init()
    w,h = screen.get_size()
    font = pygame.font.SysFont('arialblack',40)
    color =  (224,224,224)
    default_display_list = pygame.display.list_modes()
    default_display_list_size = len(default_display_list)

    #Buttons
    y_ecart = h//4
    x_left = w//8
    x_right = 7*w//8

    arrow_width,arrow_height = w//8,h//8
    button_image_sprites = pygame.sprite.Group()
    prev_display = Button_Image(x_left,y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/left_b.png"),pygame.image.load("sprite/left_h.png"))
    next_display = Button_Image(x_right,y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/right_b.png"),pygame.image.load("sprite/right_h.png"))
    prev_bgm = Button_Image(x_left,2*y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/left_b.png"),pygame.image.load("sprite/left_h.png"))
    next_bgm = Button_Image(x_right,2*y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/right_b.png"),pygame.image.load("sprite/right_h.png"))
    prev_se = Button_Image(x_left,3*y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/left_b.png"),pygame.image.load("sprite/left_h.png"))
    next_se = Button_Image(x_right,3*y_ecart,arrow_width,arrow_height,pygame.image.load("sprite/right_b.png"),pygame.image.load("sprite/right_h.png"))
    
    valide = Button_Image(w//2,7*h//8,h//8,h//8,pygame.image.load("sprite/valide_b.png"),pygame.image.load("sprite/valide_h.png"))
    quit = Button_Image(15*w//16,h//8,h//10,h//10,pygame.image.load("sprite/quit_b.png"),pygame.image.load("sprite/quit_h.png"))

    button_image_sprites.add(prev_display)
    button_image_sprites.add(next_display)
    button_image_sprites.add(prev_bgm)
    button_image_sprites.add(next_bgm)
    button_image_sprites.add(prev_se)
    button_image_sprites.add(next_se)
    button_image_sprites.add(valide)
    button_image_sprites.add(quit)
    

    pause = True
    while pause:
        volume_bgm = round(volume_bgm,2)
        volume_se = round(volume_se,2)

        #text
        settings = font.render('SETTINGS',True,color)
        display = font.render(f'{default_display_list[actual_display]}',True,color)
        bgm = font.render(str(volume_bgm),True,color)
        se = font.render(str(volume_se),True,color)
        
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
            #display
            if event.type == pygame.MOUSEBUTTONUP and mouses[0]:
                if prev_display.collide(x,y)  and actual_display > 0:
                    actual_display -= 1
                if next_display.collide(x,y) and actual_display < default_display_list_size-1:
                    actual_display += 1
                #bgm On manipule des float, on dira qu'un volume de 0.05 c'est à peu près muet
                if prev_bgm.collide(x,y) and volume_bgm > 0:
                    volume_bgm -= 0.05
                if next_bgm.collide(x,y) and volume_bgm < 1:
                    volume_bgm += 0.05
                #se
                if prev_se.collide(x,y) and volume_se > 0:
                    volume_se -= 0.05
                if next_se.collide(x,y) and volume_se < 1:
                    volume_se += 0.05
                #sauvergadement des settings
                if valide.collide(x,y):
                    Validation(screen,"Voulez-vous changer les settings?\nVous devez redémarrer le jeu\npour effectuer les changements")
                    update(save_file,actual_display,volume_bgm,volume_se)
                    pause = False
        
        #Affichage
        screen.fill((128,128,128)) #Gray
        for button_image in button_image_sprites.sprites():
            button_image.update(x,y)
            button_image.draw(screen)
        screen.blit(settings, settings.get_rect(center=(w//2, settings.get_height())))
        screen.blit(display, display.get_rect(center=(w//2, y_ecart)))
        screen.blit(bgm, bgm.get_rect(center=(w//2, 2*y_ecart)))
        screen.blit(se, se.get_rect(center=(w//2, 3*y_ecart)))

        button_image_sprites.update(x,y)
        button_image_sprites.draw(screen)

        pygame.display.update()