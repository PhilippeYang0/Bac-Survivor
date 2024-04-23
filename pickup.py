import pygame

class PickUp(pygame.sprite.Sprite):
    SIZE=25

    def __init__(self, x0:int, y0:int, duree:int, vals_buff:list, display:pygame.Surface):
        """
        x0,y0: position absolue du pickup.
        duree: durée restante avant que le pickup ne disparraise.
        vals_buff: valeurs liées au buff, pour plus de détail, voir la définition de Buff.
        display: affichage du pickup.
        """
        super().__init__()
        self.__image = pygame.transform.scale(display,(self.SIZE,self.SIZE))
        self.__rect = self.__image.get_rect(center = (x0,y0))
        self.__mask = pygame.mask.from_surface(self.image)

        self.__duree = duree
        self.__vals_buffs = vals_buff

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
    def vals_buffs(self) -> list:
        """
        Valeurs du buff lié à pickup.
        """
        return self.__vals_buffs

    def is_over(self) -> bool:
        """
        Renvoie True si le pickup a fini d'exister.
        """
        return self.__duree <= 0
    
    def update(self):
        """
        Met à jour le pickup.
        """
        self.__duree -= 1