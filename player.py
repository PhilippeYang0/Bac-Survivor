from typing import List, Tuple
from bullet import Bullet
import pygame
from math import atan2, cos, sin
from stats import Statistics
from buff import Buff
from zoneeffect import ZoneEffect

class Player(pygame.sprite.Sprite):
    __SIZE = 50
    __BASE_COST_XP = 10
    __MUL_XP_PER_LEVEL = 1.5
    __MUL_MAX_HEALTH_PER_LEVEL = 1.1

    def __init__(self, x0:int, y0:int, display_player:pygame.Surface, **kwargs):
        """
        x0,y0: emplacements x et y absolus du player.
        display_player: image de player
        kwargs: statistiques de self: "max_health", "speed", "guerison", "dash_cooldown", "duree_dash", "power_dash"
        """
        
        super().__init__()
        self.__image = pygame.transform.scale(display_player,(self.__SIZE,self.__SIZE))
        self.__rect = self.__image.get_rect(center = (x0,y0))
        self.__mask = pygame.mask.from_surface(self.image)

        self.__bullets = pygame.sprite.Group()
        self.__effects = pygame.sprite.Group()
        self.__weapons = {}

        self.__level = 0
      
        stats_obligatoires = ["max_health", "guerison", "speed", "cooldown_dash", "duree_dash", "power_dash"]
        assert set(kwargs.keys()) == set(stats_obligatoires), f"kwargs devrait contenir {stats_obligatoires}, pas {list(kwargs.keys())}"
        health = kwargs["max_health"]
        guerison = kwargs["guerison"]
        speed = kwargs["speed"]
        cooldown_dash = kwargs["cooldown_dash"]
        duree_dash = kwargs["duree_dash"]
        power_dash = kwargs["power_dash"]

        self.__statistics = Statistics(max_health = health, health = health, guerison = guerison,\
                                       speed = speed, xp = self.__BASE_COST_XP, dash_cooldown = cooldown_dash,\
                                       duree_dash = duree_dash, power_dash = power_dash)
        self.__weapons_buffs = []
        self.__bullets_buffs = []
        self.__effects_buffs = []
        self.__delta_x = 0
        self.__delta_y = 0

        self.__dash_cooldown = 0


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
    def coors(self) -> Tuple[float, float]:
        """
        Renvoie les coordonnées absolues de self en son centre.
        """
        return self.rect.center

    @property
    def stats(self):
        """
        Les statistiques: xp, health, player etc... de self.
        """
        return self.__statistics
    
    @property
    def level(self) -> int:
        """
        Niveau actuel de self, commence à partir de 0.
        """
        return self.__level
    
    @property
    def nom_armes(self) -> List[str]:
        """
        Le nom de toutes les armes de self.
        """
        return list(self.__weapons.keys())

    @property
    def xp_needed_between_levels(self) -> float:
        """
        Niveau requis pour passer d'un niveau à un autre en commencant à 0 xp.
        """
        return self.__BASE_COST_XP*self.__MUL_XP_PER_LEVEL**self.__level

    def level_up_weapon(self, nom:str):
        """
        Fait level up l'arme nom de self.
        """
        self.__weapons[nom].level_up()

    def __level_up(self):
        """
        Fait monter de niveau self.
        """
        for w in self.__weapons.values():
            w.level_up()
        self.__level += 1
        max_health = self.__statistics.get_value("max_health")
        self.add_buff(Buff("health", "ADD",  max_health*(self.__MUL_MAX_HEALTH_PER_LEVEL-1), 0))
        self.add_buff(Buff("max_health", "ADD_PER", self.__MUL_MAX_HEALTH_PER_LEVEL, 0))
        self.add_buff(Buff("xp", "ADD", self.xp_needed_between_levels, 0))

    def add_weapon(self, nom:str, weapon):
        """
        Rajoute une arme à self qui s'appelle nom.
        """
        self.__weapons[nom] = weapon
        for buff in self.__weapons_buffs:
            weapon.add_buff(buff.copy())

    def subir_degat(self, degat:float):
        """
        Inflige dégat à self.
        """
        buff = Buff("health", "ADD", -degat, 0)
        self.add_buff(buff)

    def update(self):
        """
        Met à jour la position, la vie, les buffs du joueur.
        """
        for w in self.__weapons.values():
            w.update()
        self.__statistics.update()

        for b in self.__bullets:
            b.set_owner_pos(*self.rect.center)
        for ze in self.__effects:
            ze.change_position(self.__delta_x, self.__delta_y)

        for buff in self.__weapons_buffs + self.__bullets_buffs + self.__effects_buffs:
            buff.update()
        
        if self.__statistics.get_value("xp") <= 0:
            self.__level_up()
        
        health, max_health = self.__statistics.get_values("health", "max_health")
        if health > max_health:
            self.__statistics.add_buff(Buff("health","ADD",0,max_health-health))

        self.__dash_cooldown = max(self.__dash_cooldown-1, 0)

    def add_buff(self, buff):
        """
        Rajoute un buff à self.
        La catégorie du buff doit correspondre à une catégorie des stats de self, ou de ses weapons ou de ses bullets.
        """
        if buff.category in ("amount_fired", "cooldown"):
            self.__weapons_buffs.append(buff)
            for w in self.__weapons.values():
                w.add_buff(buff.copy())
            return
        if buff.category == "speed":
            self.__bullets_buffs.append(buff)
            self.__statistics.add_buff(buff)
        elif buff.category == "degat":
            self.__bullets_buffs.append(buff)
            self.__effects_buffs.append(buff)
        elif buff.category == "time_before_activation":
            self.__effects_buffs.append(buff)
        else:
            self.__statistics.add_buff(buff)

    def move(self, direction:pygame.math.Vector2, sprites: pygame.sprite.Group):
        """
        direction: direction dans laquelle va se déplacer self.
        sprites: tous les sprites avec qui self peut entrer en collision dont lui même.
        Déplace self.
        """
        speed = self.__statistics.get_value("speed")
        old_x,old_y = self.rect.center
        self.rect.center += direction * speed
        sprites_collided = pygame.sprite.spritecollide(self, sprites, False)
        sprites_collided = [sprite_collided for sprite_collided in sprites_collided if sprite_collided != self]
        if len(sprites_collided) > 0:
            sprites_x = list(map(lambda sprite: sprite.rect.center[0], sprites_collided))
            sprites_y = list(map(lambda sprite: sprite.rect.center[1], sprites_collided))
            global_x = sum(sprites_x)/len(sprites_x)
            global_y = sum(sprites_y)/len(sprites_y)
            x,y = self.rect.center
            angle = get_angle(global_x, global_y, x, y)
            x += cos(angle) * speed
            y += sin(angle) * speed
            self.__rect.center = int(x),int(y)
        x,y = self.rect.center
        self.__delta_x,self.__delta_y = x-old_x,y-old_y
        

    def fire(self, x_cursor:int, y_cursor:int) -> List[Bullet]:
        """
        Renvoie toutes les balles tirées par le joueur à cet instant.
        x_cursor, y_cursor: coordonnées absolues de la souris.
        """
        bullets = []
        x,y = self.rect.center
        for weapon in self.__weapons.values():

            if weapon.category != "bullet" or weapon.cooldown > 0:
                continue
            weapon.reset_cooldown()
            for _ in range(weapon.amount_fired):
                b=Bullet(x, y, x_cursor, y_cursor, *weapon.stats)
                for buff in self.__bullets_buffs:
                    b.add_buff(buff)
                bullets.append(b)
                self.__bullets.add(b)
        return bullets
    
    def effects(self, x_cursor:int, y_cursor:int) -> List[ZoneEffect]:
        """
        Renvoie tous les effets activés par self en cet instant
        x_cursor, y_cursor: coordonnées absolues de la souris.
        """
        effects = []
        x,y = self.rect.center
        for weapon in self.__weapons.values():
            if weapon.category != "effect" or weapon.cooldown > 0:
                continue
            weapon.reset_cooldown()
            a = get_angle(x,y,x_cursor,y_cursor)
            l,h = self.__image.get_size()
            x += cos(a) * l/2
            y += sin(a) * h/2
            ze = ZoneEffect(x, y, x_cursor, y_cursor, *weapon.stats)
            for buff in self.__effects_buffs:
                ze.add_buff(buff.copy())
            effects.append(ze)
            self.__effects.add(ze)
        return effects

    def kill(self):
        """
        A activer quand self doit être éliminé.
        """
        for b in self.__bullets:
            if b.must_die_with_owner():
                b.kill()
        for ze in self.__effects:
            ze.kill()
        super().kill()

    def can_activate_dash(self) -> bool:
        """
        Renvoie True si self peut activer son dash.
        """
        return self.__dash_cooldown <= 0

    def activate_dash(self):
        """
        Active le dash de self.
        """
        dash_cooldown,duree_dash,power_dash = self.__statistics.get_values("dash_cooldown", "duree_dash", "power_dash")
        self.__dash_cooldown = dash_cooldown
        self.add_buff(Buff("speed","ADD_PER",power_dash,duree_dash))

def get_angle(x1:float, y1:float, x2:float, y2:float) -> float:
    return atan2(y2-y1, x2-x1)