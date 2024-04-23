import pygame
from math import sin,cos,pi,atan2 
from random import uniform
from typing import Tuple
from stats import Statistics

BULLET_CATEGORIES = ["CIRCLE","DIRECT"]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x:float, y:float, x_cible:int, y_cible:int, velocity:int, degat:int, dispersion: float, display:pygame.Surface, size:Tuple[int,int], bullet_category:str):
        """
        x: position centrale absolue x de la bullet.
        y: position centrale absolue y de la bullet.
        x_cible: emplacement absolu x de la cible de la balle.
        y_cible: emplacement absolu y de la cible de la balle.
        velocity: vitesse de la bullet.
        à vers la droite, progresse dans le sens contraire des aiguilles d'une montre.
        dispersion: indique à quel point la balle se dirigera précisément vers la cible.
        A 0: précision absolue, à 1 plus aucune précision.
        degat: dégats infligés par la bullet au contact avec l'ennemi.
        size: taille de la bullet.
        display: affichage de la bullet.
        pierce: nombre d'ennemi que l'arme va pouvoir touché avant de se dissiper.
        bullet_category: catégorie à laquelle appartient la bullet, peut faire varier
        ses déplacements. Types possibles: "CIRCLE", "DIRECT"
        """
        assert bullet_category in BULLET_CATEGORIES, f"La catégorie {bullet_category} n'est pas une catégorie valide,\
                                                         veuillez choisir parmi {BULLET_CATEGORIES}"

        super().__init__()

        self.__angle = get_angle(x,y,x_cible,y_cible)
        self.__angle += uniform(-dispersion,dispersion)*pi

        self.__image = pygame.transform.scale(display, size)
        self.__image = pygame.transform.rotate(self.__image, -self.__angle*180/pi)
        self.__rect = self.__image.get_rect()
        self.__mask = pygame.mask.from_surface(self.__image)
        self.__x = x
        self.__y = y
        self.__size = size
        self.__category = bullet_category

        self.__statistics = Statistics(speed = velocity, degat = degat)

        self.__owner_x = 0
        self.__owner_y = 0

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
    
    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @property
    def mask(self) -> pygame.Mask:
        return self.__mask

    def add_buff(self, buff):
        """
        Ajoute un buff de classe Buff à self.
        La catégorie du buff doit être "degat", ou "speed".
        """
        self.__statistics.add_buff(buff)

    def must_die_with_owner(self) -> bool:
        """
        Si self doit mourir en même temps que celui qui l'a émis, renvoie True.
        """
        return self.__category == "CIRCLE"

    def inflige_degat(self, cible):
        """
        Inflige des dégats à cible.
        """
        cible.subir_degat(self.__statistics.get_value("degat"))

    def within_border(self, x_min:int, y_min:int, x_max:int, y_max:int) -> bool:
        """
        Renvoie True si la bullet est entre les coordonnées x_min, y_min, x_max, y_max.
        """
        x,y = self.__x, self.__y
        taille_x, taille_y = self.__size
        return x_min < x+taille_x/2 and x-taille_x/2 < x_max and\
                    y_min < y+taille_y/2 and y-taille_y/2 < y_max

    def is_dead(self, x_min:int, y_min:int, x_max:int, y_max:int) -> bool:
        """
        Renvoie True si self doit être éliminé.
        C'est le cas si il est en dehors des limites( x_min, y_min, x_max, y_max).
        """
        return not self.within_border(x_min, y_min, x_max, y_max)

    def set_owner_pos(self, owner_x, owner_y):
        """
        (owner_x, owner_y): coordonnées de l'émetteur de la bullet..
        """
        self.__owner_x,self.__owner_y = owner_x,owner_y

    def update(self):
        """
        met à jour les valeurs de self.
        """
        speed = self.__statistics.get_value("speed")
        if self.__category == "DIRECT":
            self.__x += cos(self.__angle) * speed
            self.__y += sin(self.__angle) * speed
        elif self.__category == "CIRCLE":
            self.__angle += speed/100
            self.__x = self.__owner_x+cos(self.__angle+pi/2) * speed*30
            self.__y = self.__owner_y+sin(self.__angle+pi/2) * speed*30
        
        self.rect.center = (int(self.__x), int(self.__y))

def get_angle(x1,y1,x2,y2):
    return atan2(y2-y1, x2-x1)