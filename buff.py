from typing import Union
import pygame

class Buff:
    def __init__(self, category:str, modifier_category:str, value:float, duree):
        """
        category: type de la valeur influencée par le buff.
        modifier_category: facon dont va être modifié la valeur liée au buff.
            Si "ADD": ajoute directement.
            Si "ADD_PER: fait la somme de tous les ADD_PER. Ajoute 1 et multiplie la valeur finale
            par le résultat.
        value: indique en quelle quantité, ou pourcentage, etc... va être modifiée
        la valeur liée au buff.
        duree: temps restant où le buff est actif. Diminue de un à chaque update.
        Si duree=0, prend effet constamment.
        """
        assert modifier_category in ("ADD","ADD_PER"), f"Le type de modifieur \
                                                         {modifier_category} n'est pas valide."
        self.__duree = duree
        self.__is_infini = duree == 0
        self.__modifier_category = modifier_category
        self.__category = category
        self.__value = value

    @property
    def duree(self) -> int:
        """
        durée restante avant la fin du buff.
        Diminue de un à chaque frame, donc d'unité 1 frame.
        """
        return int(self.__duree)

    @property
    def category(self) -> str:
        """
        category: type de la valeur influencée par le buff: par ex "speed", "degat".
        """
        return self.__category

    @property
    def modifier_category(self) -> str:
        """
        facon dont va être modifié la valeur liée au buff.
            Si "ADD": ajoute directement.
            Si "ADD_PER: fait la somme de tous les ADD_PER. Ajoute 1 et multiplie la valeur finale
            par le résultat.
        """
        return self.__modifier_category

    def is_infini(self) -> bool:
        """
        booléen indiquant si le buff a une durée limité ou non.
        """
        return self.__is_infini

    @property
    def value(self) -> Union[int, float]:
        """
        en quelle quantité, ou pourcentage, etc... va être modifiée la valeur
        liée au buff.
        """
        return self.__value

    def is_over(self) -> bool:
        """
        Renvoie True si le buff est arrivé au bout de sa durée.
        """
        return self.__duree<=0

    def update(self):
        """
        Met à jour la durée du buff.
        """
        self.__duree -= 1
    
    def copy(self) -> "Buff":
        """
        Renvoie une copie de self.
        """
        return Buff(self.__category, self.__modifier_category, self.__value, self.__duree if self.__duree != float("inf") else 0)