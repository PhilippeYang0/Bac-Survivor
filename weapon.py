from typing import List
from stats import Statistics

class Weapon:

    def __init__(self, category:str, levels:List[dict]):
        """
        category: categorie de weapon. Peut prendre les valeurs "bullet" ou "effect".
        levels: statistiques de l'arme à chacun de ses niveaux. Les stats sont de la forme de dictionnaire.
        Le dictionnaire doit avoir pour clé si
            category == "bullet":
                "cooldown": durée entre chaque tir de la bullet.
                "amount_fired": nombre de balles tirées à chaque émission.
                "sound": son émis par la balle quand elle est tirée.
                "stats": statistiques de la bullet, sous forme de liste dans le même ordre que les arguments de bullet.
            category == "effect":
                "cooldown": durée entre chaque mise en place de l'effet.
                "stats": statistiques de l'effet, sous forme de liste dans le même ordre que les arguments de zoneeffect.
        """
        assert category in ["bullet", "effect"], f"category doit être 'bullet' ou 'effect', {category} n'est pas valide"
        self.__category = category
        self.__levels = levels
        self.__level = 0
        for level in levels:
            if category == "bullet":
                assert set(level.keys()) == set(["cooldown", "amount_fired", "sound", "stats"]), f"le dictionnaire doit avoir pour clé\
                                                                                'cooldown', 'sound', 'amount_fired' et 'bullets_stats',\
                                                                                ici, a {list(level.keys())}"
            else:
                assert set(level.keys()) == set(["cooldown", "stats"]), f"le dictionnaire doit avoir pour clé\
                                                                                 'cooldown', 'effects_stats',\
                                                                                 ici, a {list(level.keys())}"
        if category == "bullet":
            self.__statistiques = Statistics(cooldown = self.__levels[self.__level]["cooldown"],\
                                             amount_fired = self.__levels[self.__level]["amount_fired"])
        else:
            self.__statistiques = Statistics(cooldown = self.__levels[self.__level]["cooldown"])

        self.__cooldown = int(self.__statistiques.get_value("cooldown"))

    @property
    def category(self) -> str:
        return self.__category
    
    @property
    def level(self) -> int:
        """
        Niveau actuel de l'arme, commence à partir de 0.
        """
        return self.__level

    @property
    def cooldown(self) -> int:
        return self.__cooldown
    
    @property
    def amount_fired(self) -> int:
        """
        Renvoie une erreur si self n'est pas de category bullet.
        """
        assert self.category == "bullet", f"self n'est pas de category bullet, il devrait l'être. Il est {self.category}"
        return int(self.__statistiques.get_value("amount_fired"))

    @property
    def stats(self) -> list:
        return self.__levels[self.__level]["stats"]

    def add_buff(self, buff):
        """
        Ajoute un buff de classe Buff à self. Buff doit appartenir à "cooldown", "amount_fired".
        """
        self.__statistiques.add_buff(buff)

    def reset_cooldown(self):
        """
        Remet le cooldown de self à son état initial.
        """
        self.__cooldown = int(self.__statistiques.get_value("cooldown"))

    def level_up(self):
        """
        Fait monter l'arme de niveau. Si à atteint son niveau maximal, ne fait rien.
        """
        if self.__level < len(self.__levels) - 1:
            self.__level += 1
        self.__statistiques.adjust_value("cooldown", self.__levels[self.__level]["cooldown"])
        if self.__category == "bullet":
            self.__statistiques.adjust_value("amount_fired", self.__levels[self.__level]["amount_fired"])

    def update(self):
        """
        Met à jour self.
        """
        self.__cooldown = max(self.__cooldown-1, 0)