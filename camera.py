import pygame

class CameraGroup(pygame.sprite.LayeredUpdates):
    """
    pygame.sprite.group
    Groupe de sprites qui se centre sur player
    """
    def __init__(self):
        super().__init__()

        # camera offset
        self.offset = pygame.math.Vector2()
        
        #zoom
        self.zoom_scale = 1
        
    def center_target(self,player,half_w,half_h):
        """
        la fenêtre d'affichage centre sur player
        """
        self.offset.x = player.rect.centerx - half_w
        self.offset.y = player.rect.centery - half_h

    def camera_draw(self,player,screen):
        """
        Fonction principale
        la fenêtre d'affichage centre sur player
        tous les autres sprites ont une positions relatifs au positions absolu du player du caméra.
        """
        w,h = screen.get_size()
        half_w = w // 2
        half_h = h // 2
        self.center_target(player,half_w,half_h)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image,offset_pos)


        #la fonction ne marche pas
        #map(lambda sprite : screen.blit(sprite.image, sprite.rect.topleft - self.offset), self.sprites())

        