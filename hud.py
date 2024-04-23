# Créé par sofiane.aliane, le 20/04/2023 en Python 3.7

import pygame
from statbar import StatBar

pygame.font.init()

class HUD:
    couleur_xp = (0,0,255)
    couleur_vie = (255, 0, 0)
    HAUTEUR = 10
    font = pygame.font.SysFont('calibri', 18)

    def __init__(self,  largeur):
        """
        Contient des barres de HP et exp à hauteur prédeterminé
        Se consacre à l'affichage des valeurs à des positions fixes du screen
        """
        super().__init__()
        self.barre_xp = StatBar(0, 0, largeur,color = self.couleur_xp)
        self.barre_vie = StatBar (0, 20, largeur,color = self.couleur_vie)

        #Rectangle
        self.rect_x = 0
        self.rect_y = 25
        self.rect_width = 150
        self.longueur_rectangle = 50 # 150 de base
        self.taille_carre = self.rect_width // 3
    
    def mettre_a_jour(self, vitesse, degats, defense, player_position,camera_position,screen):
        texte = f"Vitesse = {vitesse:.2f} | Dégats = {degats:.2f} | Défense = {defense:.2f} | Position = {player_position[0]:.2f}, {player_position[1]:.2f}"

        #Création du texte
        self.surface.fill((255, 255, 255)) # remplissage de couleur blanche
        rendu_texte = self.font.render(texte, True, (0, 0, 0)) # noeud de texte en noir
        rect_texte = rendu_texte.get_rect(center=self.surface.get_rect().center) # mise en place du texte au centre du rectangle

        #Affichage du texte
        self.surface.blit(rendu_texte, rect_texte) # affichage du texte
        screen.blit(self.surface,camera_position) # affichage dans le jeu

    def rectangle_arme(self,screen):
        #Work in Progress
        for i in range(2):
            pygame.draw.rect(screen, (0,0,0), [self.rect_x + i * self.taille_carre, self.rect_y, self.taille_carre, self.longueur_rectangle], 2)
            pygame.draw.rect(screen, (255,255,255), [self.rect_x + i * self.taille_carre + 1, self.rect_y + 1, self.taille_carre - 2, self.longueur_rectangle - 2])

    def actualisation_des_barres(self, vie_actuelle, vie_max, xp_actuelle, xp_max,level):
        text = self.font.render("level" + str(level), True, (255,255,255))
        self.barre_xp.set_stat(xp_actuelle, xp_max,text)
        self.barre_vie.set_stat(vie_actuelle, vie_max)

    def draw(self, screen):
        screen.blit(self.barre_vie.image, (self.barre_vie.rect))
        screen.blit(self.barre_xp.image, (self.barre_xp.rect))
