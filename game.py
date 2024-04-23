
from random import randint, random, choices
from math import sqrt
import pygame
import os
import sys
from button import Button
from shop import Shop
from camera import CameraGroup
from player import Player
from background import Background
from hud import HUD
from sound import *
from pickup import PickUp
from ennemy import Ennemy
from button import Button
from validation import Validation
from pop_up import Pop_Up
import extractioninfo
from weapon import Weapon
from buff import Buff
from level_select import level_select
import insertinfo
from settings import Settings


class Game():
    """
    Class game
    L'objet principal du jeu
    """
    def __init__(self,save_file:str) :
        """
        Notre jeu a besoin de variable globale facilement accessible
        Certains valeurs sont extraits ou enregistrés dans save_file
        """
        pygame.init()        
        #save_file_extraction
        self.save_file = save_file
        self.default_display, self.volume_bgm, self.volume_se, self.gemmes, self.maps_debloquees = extractioninfo.extraction_save(self.save_file)

        # Display
        pygame.display.set_caption("BAC Survivors")
        self.display = pygame.display.list_modes()[self.default_display] if self.default_display != -1 else pygame.display.list_modes()[0] # [(1920,1080),(1680,1020),(720,540)... ] 
        self.w,self.h = self.display
        self.max_w,self.max_h = 2 * self.w, 2 * self.h
        self.screen = pygame.display.set_mode((self.w, self.h)) 
        
        # text caracteristics
        pygame.font.init()
        self.font = pygame.font.SysFont('arialblack',40)

        # Time Dynamics
        self.clock = pygame.time.Clock()
        self.time = 0 #variable
        self.time_interface = 12
        self.time_playing = 60
        #Variables 
        #commands 
        self.cursor_x = 0
        self.cursor_y = 0
        self.keys = []
        self.mouses = []

        # Game loop variables
        self.running = True
        self.playing = True
        self.pausing = True
        self.gameovering = True
    
    #Game loop methods
    def stop_running(self):
        self.running = False
    def stop_playing(self):
        self.playing = False
    def stop_pausing(self):
        self.pausing = False
    def stop_gameovering(self):
        self.gameovering = False

    #Game refresh methods
    def refresh(self):
        self.cursor_x,self.cursor_y = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        self.mouses = pygame.mouse.get_pressed()
        
    #Les loops principaux -------------------------------------------------------------------

    def main(self):
        """
        Le boucle principal du jeu.
        C'est l'interface du menu principal de jeu.
        Il doit toujours être connectable
        """
        #init
        self.running = True
        #background
        path = "sprite/menu"
        backgrounds = [pygame.transform.scale(pygame.image.load(path+ "/" + background),(self.w,self.h)) for background in os.listdir(path)]
        self.ibg = 0
        self.tbg = len(backgrounds)
        self.screen.fill('black')
        #music
        sound_background('sound/main.mp3',self.volume_bgm)
        # text
        text_menu = self.font.render("BAC SURVIVORS", True, (182, 143, 64))
        text_play = self.font.render("utilisez la souris pour naviguer", True,(182, 143, 64))
        
        #Shop
        environnements_items = extractioninfo.extraction_data_item_shop_environnements("environnements_shops.json")
        environnements_items = [ei for ei in environnements_items if not ei[1] in self.maps_debloquees]
        def buy_environnement(item):
            self.gemmes -= item.prix
            self.maps_debloquees.append(item.nom)
            insertinfo.update(self.save_file,gemmes=self.gemmes,items_achetes = self.maps_debloquees)
        s = Shop(environnements_items, buy_environnement, lambda i:None, lambda i:None)

        while self.running:
            self.clock.tick(self.time_interface)
            self.refresh()
            s.update_gold(self.gemmes)
            #button
            button_sprites = pygame.sprite.Group()
            w_center = self.w//2
            play = Button( w_center, self.h//5, text_input="PLAY")
            settings = Button( w_center, self.h//2, text_input="SETTINGS")
            quit = Button( w_center, 4*self.h//5, text_input="QUIT")
            shop = Button( self.w//8 , self.h//16, text_input='SHOP')
            profile = Button( 7*self.w//8 , self.h//16, text_input='PROFILE')
            button_sprites.add(play)
            button_sprites.add(settings)
            button_sprites.add(quit)
            button_sprites.add(shop)
            button_sprites.add(profile)

            #Commands
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (self.keys[pygame.K_LALT] and self.keys[pygame.K_F4]) :
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYUP and self.keys[pygame.K_ESCAPE]) or quit.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                    def menu_quit(): self.stop_running();pygame.quit();sys.exit()
                    Validation(self.screen, 'Voulez-vous quitter le jeu?',oui_fct= menu_quit)
                if shop.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                    s.create_shop(self.screen)
                if play.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                    level = level_select(self.screen, extractioninfo.extraction_data_choix_levels(self.maps_debloquees))
                    self.play(level) if level != '' else None
                if  profile.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                    Pop_Up(self.screen,'VOTRE PROFILE',f"\nVous avez {self.gemmes} gemmes.\nVous avez débloqué {len(self.maps_debloquees)} / 6 maps")
                if settings.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                    Settings(self.screen,self.default_display,self.volume_bgm,self.volume_se,self.save_file)

            # Background dynamic transparency
            background = backgrounds[self.ibg]
            coef = -1 if self.time > 255 else 1
            background.set_alpha((coef * self.time)%255)
            text_play.set_alpha((coef * self.time)%255)
            self.time += self.time_interface
            if self.time >255*2:
                self.time = 0
                self.ibg = (self.ibg+1) % self.tbg

            # affichage
            self.screen.blit(background, (0, 0))
            self.screen.blit(text_menu, text_menu.get_rect(center=(self.w//2, text_menu.get_height()//2)))
            self.screen.blit(text_play, text_play.get_rect(center=(self.w//2, self.h - text_play.get_height()//2)))
            for button in button_sprites.sprites():
                button.update(self.cursor_x,self.cursor_y)
                button.draw(self.screen)
            pygame.display.update()
        pygame.quit()
        sys.exit()
    #-------------------------------------------------------------------------------------------------------------------------
    def pause(self,shop_play:Shop):
        """
        Interface de pause, pausing loop
        shop_play:magasin pour acheter des objets dans le jeu.
        """
        #init
        self.screen.fill('black')
        bg = pygame.transform.scale(pygame.image.load("sprite/pause.png"),(self.w,self.h))
        self.pausing = True

        #Button
        button_sprites = pygame.sprite.Group()
        resume = Button( self.w//2, self.h//5, text_input="RESUME")
        shop = Button( self.w//2, self.h//2, text_input="SHOP")
        menu = Button( self.w//2, 4*self.h//5, text_input="MAIN MENU")
        button_sprites.add(resume)
        button_sprites.add(shop)
        button_sprites.add(menu)
        
        # text
        text_pause = self.font.render("PAUSE", True, (182, 143, 64))
        text_resume = self.font.render("appuyez sur échap pour résumer", True,(182, 143, 64))
        
        while self.pausing:
            self.clock.tick(self.time_interface)
            self.refresh()
            
            #Commands
            for event in pygame.event.get():
                # La raison de ce loop c'est parce qu'on veut que les inputs soient délayés
                # car pygame.key.getpressed() est très rapide.
                # Appuyez sur échap ne serait quelque secondes peut
                # nous fait ouvrir et fermer self.pause() plusieurs fois à la suite.
                if event.type == pygame.QUIT or (self.keys[pygame.K_LALT] and self.keys[pygame.K_F4]):
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYUP and  (event.key == pygame.K_ESCAPE)) or (resume.collide(self.cursor_x,self.cursor_y) and self.mouses[0]):
                    self.stop_pausing()
                    
            if (menu.collide(self.cursor_x,self.cursor_y) and self.mouses[0]):
                def back_to_menu(): self.stop_pausing();self.stop_playing();sound_background('sound/main.mp3',self.volume_bgm)
                Validation(self.screen, 'Voulez-vous retourner au menu ?\nToute progression sera perdu',oui_fct = back_to_menu, font = pygame.font.SysFont('Arialblack',25))
            if shop.collide(self.cursor_x,self.cursor_y) and self.mouses[0]:
                shop_play.create_shop(self.screen)
            
            # text_resume dynamic transparency
            if self.time <= 255 :
                text_resume.set_alpha(self.time%255)
            elif self.time <= 255*2 :
                text_resume.set_alpha(-self.time%255)
            self.time += self.time_interface
            if self.time >255*2:
                self.time = 0

            # affichage
            self.screen.blit(bg, (0, 0))
            self.screen.blit(text_pause, text_pause.get_rect(center=(self.w//2, text_pause.get_height())))
            self.screen.blit(text_resume, text_resume.get_rect(center=(self.w//2, self.h - text_resume.get_height()//2)))
            for button in button_sprites.sprites():
                button.update(self.cursor_x,self.cursor_y)
                button.draw(self.screen)
            pygame.display.update()
    #-------------------------------------------------------------------------------------------------------------------------
    def gameover(self,player_level:int):
        """
        loop gameover
        enregistre les ggemmes obtenu durant play dans self.save_file
        """
        # init
        self.stop_playing()
        self.gameovering = True
        self.gemmes += player_level
        sound_background("sound/gameover.mp3",self.volume_bgm) #C'est fait exprès que la musique continue lorsqu'on revient dans main loop
        bg = pygame.transform.scale(pygame.image.load("sprite/gameover.png"),(self.w,self.h))
        self.screen.blit(bg,(0,0))
        text_gameover = self.font.render("GAME OVER", True, (182, 143, 64))
        self.screen.blit(text_gameover, text_gameover.get_rect(center=(self.w//2, text_gameover.get_height())))
        pygame.display.update()

        insertinfo.update(self.save_file,gemmes = self.gemmes)
        Pop_Up(self.screen,"GAME OVER",f"C'est ainsi que s'achève l'histoire de notre héro.\nCela dit, vous êtes récompensés par\n {player_level} gemmes.") 
                
        while self.gameovering:
            self.clock.tick(self.time_interface)
            self.refresh()
            #Commands
            for event in pygame.event.get():
                # La raison de ce loop c'est parce qu'on veut que les inputs soient délayés
                # car pygame.key.getpressed() est très rapide.
                # Appuyez sur échap ne serait quelque secondes peut
                # nous fait ouvrir et fermer self.pause() plusieurs fois à la suite.
                if event.type == pygame.QUIT or (self.keys[pygame.K_LALT] and self.keys[pygame.K_F4]):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP or True in self.mouses:
                    self.stop_gameovering()

            # text
            text_resume = self.font.render("appuyez sur n'importe quel touche pour revenir au menu", True,(182, 143, 64))
            
            # text_resume dynamic transparency
            if self.time <= 255 :
                text_resume.set_alpha(self.time%255)
            elif self.time <= 255*2 :
                text_resume.set_alpha(-self.time%255)
            self.time += self.time_interface
            if self.time >255*2:
                self.time = 0

            # affichage
            self.screen.blit(bg, (0, 0))
            self.screen.blit(text_gameover, text_gameover.get_rect(center=(self.w//2, text_gameover.get_height())))
            self.screen.blit(text_resume, text_resume.get_rect(center=(self.w//2, self.h - text_resume.get_height()//2)))
            pygame.display.update()

    #-------------------------------------------------------------------------------------------------------------------------
    def play(self,path_environnement):
        """
        path_environnement: chemin menant aux données pour le jeu.
        loop play
        """
        #init
        self.playing = True
        self.gold = 0
        #Extract
        player_display, weapons_info, background_display, ennemies_data, vagues_data,display_choix,bgm = extractioninfo.extraction_data_level(path_environnement)
        #bgm
        sound_background(bgm,self.volume_bgm)
        #HUD
        hud = HUD(self.w)

        # SpriteGroups
        camera_sprites = CameraGroup() # groupe contenant tous les sprites mouvantes
        ennemies_sprites = pygame.sprite.Group() # groupe pour les ennemies
        units_sprites = pygame.sprite.Group() # groupe pour les ennemies et player.
        bullets_player_sprites = pygame.sprite.Group()
        bullets_ennemy_sprites = pygame.sprite.Group()
        effects_ennemy_sprites = pygame.sprite.Group()
        effects_player_sprites = pygame.sprite.Group()
        pickup_sprites = pygame.sprite.Group()

        # Background
        background = Background((self.max_w,self.max_h),background_display)
        camera_sprites.add(background)
        camera_sprites.change_layer(background,-1)

        # Player
        player = Player(600, self.h - 10, player_display, max_health = 100, speed = 5, guerison = 0.02, cooldown_dash = 120, duree_dash = 8, power_dash = 5)
        camera_sprites.add(player)
        units_sprites.add(player)
        
       

        # Timer
        # Ennemies
        ENNEMIES = extractioninfo.extraction_ennemy(ennemies_data)
        # Levels
        LEVELS = extractioninfo.extraction_waves(vagues_data)
        numero_vague = 0

        #PICKS_UP
        PiCKUP_DROP_CHANCE = 0.13
        PICKS_UP,POIDS = extractioninfo.extraction_pickup("pick_up.json")

        #BUFFS_LEVEL_UP
        ITEMS,STATS_BUFFS = extractioninfo.extraction_items("items.json")
        WEAPONS,WEAPONS_ITEMS,weapons_unlocked = extractioninfo.extraction_weapon(weapons_info)
        
        def buy_weapon(item):
            """
            Achat d'un  weapon
            """
            if item.nom in player.nom_armes:
                player.level_up_weapon(item.nom)
            else:
                player.add_weapon(item.nom,Weapon(*WEAPONS[item.nom]))
            self.gold -= item.prix
        def buy_environment(item):
            """
            Achat d'un environnement
            """
            self.maps_debloquees.append(item.nom)
            self.gold -= item.prix
        def buy_buff(item):
            """
            Achat d'un  buff
            """
            player.add_buff(Buff(*STATS_BUFFS[item.nom]))
            self.gold -= item.prix
        ITEMS += WEAPONS_ITEMS
        shop = Shop(ITEMS, buy_environment,\
                           buy_buff,\
                           buy_weapon)
        for weapon_unlocked in weapons_unlocked:
            weapon = Weapon(*WEAPONS[weapon_unlocked])
            player.add_weapon(weapon_unlocked,weapon)

        def kill(ennemy:Ennemy):
            """
            Tue un ennemy et enclenche tous les events qui vont avec.
            """
            self.gold += ennemy.xp
            buff = Buff("xp", "ADD", -ennemy.xp, 0)
            player.add_buff(buff)
            x,y = ennemy.rect.center
            ennemy.kill()
            if random() < PiCKUP_DROP_CHANCE:  
                duree, vals_buff, display = choices(PICKS_UP, POIDS, k=1)[0]
                pickup = PickUp(x, y, duree, vals_buff, display)
                pickup_sprites.add(pickup)
                camera_sprites.add(pickup)

        #Game_loop
        while self.playing:
            #Gameover 
            if player.stats.get_value("health") <= 0 or len(LEVELS) <= numero_vague :
                self.gameover(player.level)
                continue

            #Refresh
            self.clock.tick(self.time_playing)
            self.refresh()
            shop.update_gold(self.gold)

            #System
            if self.keys[pygame.K_LALT]:
                pygame.event.set_grab(False)

            elif not self.keys[pygame.K_LALT]:
                pygame.event.set_grab(True) 

            # Player
            direction = pygame.math.Vector2()
            if self.keys[pygame.K_UP] or self.keys[pygame.K_z]:
                direction.y = -1
            elif self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
                direction.y = 1
            else:
                direction.y = 0

            if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
                direction.x = 1
            elif self.keys[pygame.K_LEFT] or self.keys[pygame.K_q]:
                direction.x = -1
            else:
                direction.x = 0
            
            """ WORK IN PROGRESS
            if self.keys[pygame.K_SPACE]:
                if player.can_activate_dash():
                    player.activate_dash()
            """

            if direction.x != 0 and direction.y != 0:
                direction *= sqrt(2)/2

            player.move(direction, units_sprites)

            # Special handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (self.keys[pygame.K_LALT] and self.keys[pygame.K_F4]):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.pause(shop)
            # player fire
            x,y = pygame.mouse.get_pos()
            x += camera_sprites.offset.x
            y += camera_sprites.offset.y
            bs = player.fire(int(x), int(y))
            for b in bs:
                bullets_player_sprites.add(b)
                camera_sprites.add(b)
            if len(bs) > 0:
                sound_effect("levels/starcraft-terran/sound/gun_shoot.mp3",self.volume_se)
            for b in bullets_player_sprites:
                if b.is_dead(0,0,self.max_w,self.max_h):
                    b.kill()

            # player effects
            zs = player.effects(int(x), int(y))
            for z in zs:
                camera_sprites.add(z)
                effects_player_sprites.add(z)

            for effect in effects_player_sprites:
                if effect.take_effect():
                    for ennemy in ennemies_sprites:
                        effect.apply_effect(ennemy)
                        if ennemy.is_dead():
                            kill(ennemy)
                    sound_effect_without_file(effect.sound,self.volume_se)     
                    effect.kill()  

            #ennemy fire
            x,y = player.coors
            for ennemy in ennemies_sprites:
                bullets,sounds = ennemy.fire(x, y)
                for sound in sounds:
                    sound_effect_without_file(sound,self.volume_se)
                for i,bullet in enumerate(bullets):
                    bullets_ennemy_sprites.add(bullet)
                    camera_sprites.add(bullet)

            for b in bullets_ennemy_sprites:
                if b.is_dead(0,0,self.max_w,self.max_h):
                    b.kill()

            #ennemy effects
            for ennemy in ennemies_sprites:
                for effect in ennemy.get_effects(x,y):
                    effects_ennemy_sprites.add(effect)
                    camera_sprites.add(effect)
            
            for effect in effects_ennemy_sprites:
                if effect.take_effect():
                    effect.apply_effect(player)
                    sound_effect_without_file(effect.sound,self.volume_se)     
                    effect.kill()       

            # units spawned by ennemies
            for ennemy in ennemies_sprites:
                x,y = ennemy.rect.center
                for name_ennemy in ennemy.get_name_ennemies_spwaned():
                    e = Ennemy(x,y,*ENNEMIES[name_ennemy])
                    e.set_xp(0)
                    ennemies_sprites.add(e)
                    camera_sprites.add(e)
                    health_bar = e.health_bar
                    camera_sprites.add(health_bar)

            for pickup in pickup_sprites:
                if pickup.is_over():
                    pickup.kill()

            pickups_collided = pygame.sprite.spritecollide(player, pickup_sprites, False, pygame.sprite.collide_mask)
            for pickup in pickups_collided:
                buff = Buff(*pickup.vals_buffs)
                player.add_buff(buff)
                pickup.kill()

            #Ennemies 
            #Spawn
            if len(ennemies_sprites) == 0:
                px,py = player.rect.center
                for ennemy in LEVELS[numero_vague]:
                    x = randint(0, self.max_w)
                    y = randint(0, self.max_h)
                    while px-self.w/2 <= x <= px+self.w and py-self.h/2 <= y <= py+self.h:
                        x = randint(0, self.max_w)
                        y = randint(0, self.max_h)
                    ennemy = Ennemy(x,y,*ENNEMIES[ennemy])
                    ennemies_sprites.add(ennemy)
                    camera_sprites.add(ennemy)
                    units_sprites.add(ennemy)
                    health_bar = ennemy.health_bar
                    camera_sprites.add(health_bar)
                numero_vague += 1

            #collide with bullet et move
            for ennemy in ennemies_sprites:
                ennemy.move(*player.coors, units_sprites)
                hits = pygame.sprite.spritecollide(ennemy, bullets_player_sprites, False, pygame.sprite.collide_mask)
                if len(hits) > 0:
                    bullet = hits[0]
                    health = ennemy.health
                    bullet.inflige_degat(ennemy)
                    bullet.kill()
                    if ennemy.is_dead():
                        kill(ennemy)

            #collide with player
            bullets_collided = pygame.sprite.spritecollide(player, bullets_ennemy_sprites, False, pygame.sprite.collide_mask)
            if len(bullets_collided) > 0:
                bullet = bullets_collided[0]
                bullet.inflige_degat(player)
                bullet.kill()

            # background with player
            if not background.rect.contains(player.rect):
                player.rect.clamp_ip(background.rect)

            # Gameplay Affichage
            self.screen.fill('black')
            camera_sprites.update()
            camera_sprites.camera_draw(player,self.screen)
            
            # HUD Affichage
            #hud.rectangle_arme(self.screen) Work in progress
            stats = player.stats
            health, health_max, xp = stats.get_values("health", "max_health", "xp")
            xp_max = player.xp_needed_between_levels
            hud.actualisation_des_barres(health, health_max, xp_max-xp, xp_max, player.level)
            hud.draw(self.screen)

            pygame.display.update() #Mise à jour de l'affichage

if '__main__' == __name__: 
    g = Game('save.json')
    g.main()
    pygame.quit()
    sys.exit()