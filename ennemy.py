from math import cos, sin, atan2
from statbar import StatBar
from bullet import Bullet
from typing import List,Tuple,Any
from random import random
from zoneeffect import ZoneEffect

import pygame


class Ennemy(pygame.sprite.Sprite):
    __HEALTH_BAR_HEIGHT = 10
    __HEALTH_BAR_COLOR = (255,0,0)

    def __init__(self, x0:int, y0:int, max_health:float, speed:float, xp:int, size:Tuple[int,int], display:pygame.Surface,\
                 bullets_cooldowns:List[int] = [], amounts_fired:List[int] = [], bullets_sound_on_fire:List[pygame.mixer.Sound] = [], stats_bullets:List[List[Any]] = [],\
                 effects_cooldowns: List[int] = [], stats_effects: List[List[Any]] = [],\
                 ennemies_spawn_cooldowns: List[int] = [], names_ennemies: List[str] = []):
        """
        x0, y0: coordonnées initiales absolues de self.
        max_health: vie maximale de l'ennemi.
        speed: vitesse de déplacement de l'ennemi.
        size: taille de l'unité.
        display: image de l'ennemi.
        bullets_cooldowns: durées entre chaque tir de chaque type de balle.
        amounts_fired: nombre de balles tirées à chaque coup de chaque type de balle.
        bullets_sound_on_fire: sons à qu'émet une balle quand elle est tirée pour chaque type de balle.
        stats_bullets: statistiques de chaque type de balle. Chaque argument est dans le même ordre que les arguments
        de la classe Bullet.
        Les types de balles sont renseignées dans le même ordre.
        effects_cooldowns: durées entre l'activation de chaque type de zoneeffect.
        stats_effects: statistiques de chaque type d'effet. Chaque argument est dans le même ordre que les arguments
        de la classe ZoneEffect.
        Les types de ZoneEffect sont renseignés dans le même ordre.
        ennemies_spawn_cooldowns: durées entre le spaw de chaque ennemies.
        names_ennemies: nom de chaque type d'ennemy spawn par self.
        Les types d' Ennemy sont renseignés dans le même ordre.
        """
        super().__init__()
        self.__image = pygame.transform.scale(display,size)
        self.__rect = self.__image.get_rect(center = (x0,y0))
        self.__mask = pygame.mask.from_surface(self.__image)
        self.__x, self.__y = x0,y0
        self.__health = max_health
        self.__max_health = max_health
        self.__speed = speed
        self.__xp = xp
        taille_x, taille_y = size
        self.__health_bar = StatBar(self.rect.x, self.rect.y+taille_y, taille_x, self.__HEALTH_BAR_HEIGHT, self.__HEALTH_BAR_COLOR)

        self.__bullets = pygame.sprite.Group()

        self.__amounts_fired = amounts_fired
        self.__times_between_fires = bullets_cooldowns.copy()
        self.__bullets_cooldowns = [cooldown * random() for cooldown in bullets_cooldowns]
        self.__bullets_sound_on_fire = bullets_sound_on_fire.copy()
        self.__bullets_stats = stats_bullets

        self.__effects = pygame.sprite.Group()

        self.__times_between_effects = effects_cooldowns.copy()
        self.__effects_cooldowns = [cooldown * random() for cooldown in effects_cooldowns]
        self.__effects_stats = stats_effects

        self.__times_between_ennemies_spawn = ennemies_spawn_cooldowns.copy()
        self.__ennemies_spawn_cooldowns = [cooldown * random() for cooldown in ennemies_spawn_cooldowns]
        self.__names_ennemies = names_ennemies

        self.__delta_x = 0
        self.__delta_y = 0

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
    
    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @property
    def mask(self) -> pygame.Mask:
        return self.__mask

    @property
    def health(self) -> float:
        """
        La vie de self.
        """
        return self.__health

    @property
    def health_bar(self) -> StatBar:
        """
        Sprite représentant la barre de vie de self.
        """
        return self.__health_bar

    @property
    def xp(self) -> int:
        """
        Nombre d'xp que le player remporte en tuant self.
        """
        return self.__xp
    
    def set_xp(self, xp:int):
        """
        Change la valeur de l'xp donné par self.
        """
        self.__xp = xp

    def fire(self, x_player:int, y_player:int) -> Tuple[List[Bullet],List[pygame.mixer.Sound]]:
        """
        (x_player, y_player): emplacement absolu de player.
        Renvoie toutes les balles tirées par self à cet instant.
        Renvoie aussi le son émis par les balles tirées.
        """
        bullets = []
        sounds = []
        for i, cooldown in enumerate(self.__bullets_cooldowns):
            if cooldown > 0:
                continue

            sounds.append(self.__bullets_sound_on_fire[i])

            self.__bullets_cooldowns[i] = self.__times_between_fires[i]
            x,y = self.__x, self.__y
            for _ in range(self.__amounts_fired[i]):
                b = Bullet(x, y, x_player, y_player, *self.__bullets_stats[i])
                bullets.append(b)
                self.__bullets.add(b)
        return bullets,sounds

    def get_effects(self, x_player:int, y_player:int) -> List[ZoneEffect]:
        """
        (x_player, y_player): emplacement absolu de player.
        Renvoie tous les effets activés par self à cet instant.
        """
        effects = []
        for i, cooldown in enumerate(self.__effects_cooldowns):
            if cooldown > 0:
                continue

            self.__effects_cooldowns[i] = self.__times_between_effects[i]
            x,y = self.__x, self.__y
            a = get_angle(x,y,x_player,y_player)
            l,h = self.__image.get_size()
            x += cos(a) * l/2
            y += sin(a) * h/2
            ze = ZoneEffect(x, y, x_player, y_player, *self.__effects_stats[i])
            effects.append(ze)
            self.__effects.add(ze)
        return effects
        
    def get_name_ennemies_spwaned(self) -> List[str]:
        """
        Renvoie les noms de chaque type d'ennemy crées par self en cet instant.
        """
        names_ennemies = []
        for i, cooldown in enumerate(self.__ennemies_spawn_cooldowns):
            if cooldown > 0:
                continue

            self.__ennemies_spawn_cooldowns[i] = self.__times_between_ennemies_spawn[i]
            names_ennemies.append(self.__names_ennemies[i])
        return names_ennemies

    def update(self):
        """
        Met à jour la position de self.
        Méthode à lancer à chaque frame.
        """
        for i in range(len(self.__bullets_cooldowns)):
            self.__bullets_cooldowns[i] -= 1
        for i in range(len(self.__effects_cooldowns)):
            self.__effects_cooldowns[i] -= 1
        for i in range(len(self.__ennemies_spawn_cooldowns)):
            self.__ennemies_spawn_cooldowns[i] -= 1

        self.__rect.center = int(self.__x), int(self.__y)

        self.__health_bar.set_pos(self.rect.x, self.rect.y + self.rect.size[1])
        self.__health_bar.set_stat(self.__health, self.__max_health)

        for b in self.__bullets:
            b.set_owner_pos(self.__x, self.__y)

        for ze in self.__effects:
            ze.change_position(self.__delta_x,self.__delta_y)
    
    def move(self, cible_x:int, cible_y:int, sprites: pygame.sprite.Group):
        """
        cible_x, cible_y:Indique à self l'emplacement de la cible où se rendre.
        sprites: tous les sprites avec qui self peut entrer en collision dont lui même.
        Déplace self.
        """        
        x,y = self.__x, self.__y
        angle = get_angle(x,y,cible_x,cible_y)
        new_x = self.__x + cos(angle) * self.__speed
        new_y = self.__y + sin(angle) * self.__speed
        self.__rect.center = int(new_x),int(new_y)
        sprites_collided = pygame.sprite.spritecollide(self, sprites, False)
        sprites_collided = [sprite_collided for sprite_collided in sprites_collided if sprite_collided != self]
        if len(sprites_collided) > 0:
            sprites_x = list(map(lambda sprite: sprite.rect.center[0], sprites_collided))
            sprites_y = list(map(lambda sprite: sprite.rect.center[1], sprites_collided))
            global_x = sum(sprites_x)/len(sprites_x)
            global_y = sum(sprites_y)/len(sprites_y)
            angle = get_angle(global_x, global_y, self.__x, self.__y)
            new_x += cos(angle) * self.__speed
            new_y += sin(angle) * self.__speed
            self.__rect.center = int(new_x),int(new_y)
        self.__delta_x = new_x - self.__x
        self.__delta_y = new_y - self.__y
        self.__x = new_x
        self.__y = new_y

    def is_dead(self) -> bool:
        """
        Renvoie True si self est mort.
        """
        return self.__health <= 0

    def subir_degat(self, degat:int):
        """
        Inflige degat à self.
        """
        self.__health -= degat

    def kill(self):
        """
        A activer quand self doit être éliminé.
        """
        self.__health_bar.kill()
        for b in self.__bullets:
            if b.must_die_with_owner():
                b.kill()
        for ze in self.__effects:
            ze.kill()
        super().kill()

def get_angle(x1,y1,x2,y2):
    return atan2(y2-y1, x2-x1)