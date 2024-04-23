import pygame
from typing import Tuple

class StatBar(pygame.sprite.Sprite):
    """
    Permet de gérer une barre représentant une statistique.
    """

    def __init__(self, x0:int, y0:int, largeur:int, hauteur:int = 20, color:Tuple[int,int,int] = (255,0,0)):
        """
        (x0, y0): coordonées actuelles de la barre de stat en haut à gauche.
        largeur: largeur de la barre de stat.
        """
        super().__init__()
        self.__largeur = largeur
        self.__hauteur = hauteur
        self.__color = color
        self.image = pygame.Surface((largeur, self.__hauteur))
        self.image.fill(self.__color)
        self.rect = self.image.get_rect(center = (x0+largeur/2,y0+self.__hauteur/2))

    def set_pos(self, x:int, y:int):
        """
        (x, y): coordonées actuelles de la barre de stat
        """
        self.rect.x, self.rect.y = x,y

    def set_stat(self, actual_stat:float, stat_max:float,text = None):
        """
        actual_stat: valeur actuelle de la statistique.
        max_stat: valeur maximale de la statistique.
        """
        assert stat_max > 0, f"La valeur maximale d'une stat devrait être supérieure à 0. stat_max = {stat_max}"
        actual_stat = min(actual_stat, stat_max)
        self.image = pygame.Surface((self.__largeur*max(actual_stat,0)/stat_max, self.__hauteur))
        self.image.fill(self.__color)
        if text != None:
            self.image.blit(text,self.rect)
    
    def update(self):
        """
        Met à jour self.
        """
        pass