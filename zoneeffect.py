import pygame
from typing import Tuple
from math import pi,atan2,cos,sin
from stats import Statistics
from buff import Buff

CATEGORIE_ZONE_EFFECT = ["NEXT_TO_LAUNCHER", "ON_CIBLE"]


class ZoneEffect(pygame.sprite.Sprite):

    def __init__(self, x_launcher:float, y_launcher:float, x_cible:float, y_cible:float, size:Tuple[int,int], display:pygame.Surface,\
                 degats_infliges:float, cooldown:int, categorie:str, sound_on_fire:pygame.mixer.Sound):
        """
        x_laucher,y_launcher: extrémité de l'émetteur de l'effet en direction de la cible.
        x_cible, y_cible: emplacement que doit viser la zoneeffect en supposant que le display
        de base est vers la droite.
        display: affichage de la zone effect.
        degats_infliges: dégats infligés à toutes les unités dans la zoneeffect.
        cooldown: temps restant avant que la zoneeffect ne prenne effet.
        categorie: type de zone effect, possibilités : "NEXT_TO_LAUNCHER", "ON_CIBLE"
        sound_on_fire: son émis par la zone effect au moment où il s'active.
        """
        super().__init__()
        assert categorie in CATEGORIE_ZONE_EFFECT, f"la categorie {categorie} de zone effect doit être dans la liste : {CATEGORIE_ZONE_EFFECT}"
        
        a = -get_angle(x_launcher,y_launcher,x_cible,y_cible)
        if categorie == "NEXT_TO_LAUNCHER":
            l,_ = size
            x=x_launcher+l/2*cos(a)
            y=y_launcher-l/2*sin(a)
        else:
            x=x_cible
            y=y_cible
        self.__image = pygame.transform.scale(display, size)
        self.__image = pygame.transform.rotate(self.__image, a/pi*180)
        self.__image.set_alpha(120)
        self.__x, self.__y = x, y
        self.__rect = self.__image.get_rect()
        self.__rect.center = (int(self.__x), int(self.__y))
        self.__mask = pygame.mask.from_surface(self.__image)
        self.__categorie = categorie
        self.__sound = sound_on_fire
        self.__statistics = Statistics(degat = degats_infliges, cooldown = cooldown)

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @property
    def rect(self) -> pygame.rect.Rect:
        return self.__rect

    @property
    def mask(self) -> pygame.mask.Mask:
        return self.__mask

    @property
    def sound(self) -> pygame.mixer.Sound:
        return self.__sound

    def add_buff(self, buff:Buff):
        """
        Rajoute un buff à self. La catégorie doit apparteneir à "cooldown", "degats_infliges".
        """
        self.__statistics.add_buff(buff)

    def change_position(self, delta_x:float, delta_y:float):
        """
        Modifier la position de la zone effect de delta_x et delta_y, ne le fait que si self appartient
        à une certaine catégorie.
        """
        if self.__categorie == "NEXT_TO_LAUNCHER":
            self.__x += delta_x
            self.__y += delta_y
            self.__rect.center = int(self.__x),int(self.__y)

    def take_effect(self) -> bool:
        """
        Si la zone effect prend effet, renvoie True.
        """
        return self.__statistics.get_value("cooldown") <= 0

    def apply_effect(self, unit):
        """
        Applique l'effet de la zone effect à unit si dans la zone effect.
        """
        if pygame.sprite.collide_mask(unit, self):
            unit.subir_degat(self.__statistics.get_value("degat"))

    def update(self):
        """
        Met à jour la zone effect.
        """
        self.__statistics.add_buff(Buff("cooldown", "ADD", -1, 0))

def get_angle(x1,y1,x2,y2):
    return atan2(y2-y1, x2-x1)