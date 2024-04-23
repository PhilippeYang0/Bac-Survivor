from typing import List

class Statistics:
    """
    Classe permettant de gérer les statistics d'une entité avec les stats qui vont avec.
    """
    def __init__(self, **kwargs):
        """
        kwargs : statistiques accompagnées de leur nom. Ce seront les statistiques gérées par Statistics.
        """
        self.__statistiques = kwargs.copy()
        self.__buffs = []
        self.__add = {cle:0 for cle in self.__statistiques.keys()}
        self.__add_per = {cle:1 for cle in self.__statistiques.keys()}
    
    @property
    def buffs(self) -> list:
        """
        Tous les buffs de self sous forme de list.
        """
        return self.__buffs

    @property
    def categories(self) -> List[str]:
        """
        Catégories de self
        """
        return list(self.__statistiques.keys())

    def add_buff(self, buff):
        """
        Rajoute un buff à la liste de buffs de self.
        La catégorie du buff doit être une de self.
        """
        stats_category = list(self.__statistiques.keys())
        assert buff.category in stats_category, f"la catégorie de statistique {buff.category} pour un buff\
                                                    n'est pas valide. Elle doit appartenir à {stats_category}."
        if buff.is_infini():
            if buff.modifier_category == "ADD_PER":
                self.__add_per[buff.category] += buff.value
            else:
                self.__statistiques[buff.category] += buff.value
            return
        
        self.__buffs.append(buff)

    def get_vanilla_value(self, category) -> float:
        """
        category: type de valeur, appartient à l'un des types de self.
        Renvoie les valeurs sans la modification des buffs de category.
        """
        stats_category = list(self.__statistiques.keys())
        assert category in stats_category, f"la catégorie: {category} n'est pas valide. Doit appartenir à {stats_category}"
        return self.__statistiques[category]

    def get_vanilla_values(self, *categories) -> List[float]:
        """
        categories: type de valeur, appartient à l'un des types de self.
        Renvoie les valeurs sans la modification des buffs de category.
        """
        return [self.get_vanilla_value(category) for category in categories]

    def get_value(self, category:str) -> float:
        """
        categoy: type de valeur, appartient à l'un des types de self.
        Renvoie la valeur de type category.
        Modifie dans cet ordre, d'abord les ajouts de valeur fixe: +30, -20, etc...
        puis les ajouts en terme de points de pourcentage: +20%, -12%. On additionne ces valeurs,
        on a +8% et on applique à la valeur à renvoyer.
        """
        stats_category = list(self.__statistiques.keys())
        assert category in stats_category, f"la catégorie: {category} n'est pas valide. Doit appartenir à {stats_category}"
        val = self.__statistiques[category] + self.__add[category]
        percentage = self.__add_per[category]
        for buff in self.buffs:
            if buff.category == category:
                if buff.modifier_category == "ADD":
                    val+=buff.value
                else:
                    percentage+=buff.value
        return val*percentage
        

    def get_values(self, *categories) -> List[float]:
        """
        categories: types des valeur, appartiennent à l'un des types de self.
        Renvoie les valeurs de type categories.
        Modifie dans cet ordre, d'abord les ajouts de valeur fixe: +30, -20, etc...
        puis les ajouts en terme de points de pourcentage: +20%, -12%. On additionne ces valeurs,
        on a +8% et on applique à la valeur à renvoyer.
        """
        return [self.get_value(category) for category in categories]

    def adjust_value(self, category:str, value:float):
        """
        Met la valeur de category à value. Garde les buffs qu'ils soient de modifier "ADD" ou "ADD_PER".
        category doit appartenir à une des catégories de self.
        """
        stats_category = list(self.__statistiques.keys())
        assert category in stats_category, f"la catégorie: {category} n'est pas valide. Doit appartenir à {stats_category}"
        self.__statistiques[category] = value

    def update(self):
        """
        Met à jour les buffs de self.
        """
        new_buffs = []
        for b in self.buffs:
            b.update()
            if not b.is_over():
                new_buffs.append(b)
        self.__buffs = new_buffs