import pygame

pygame.font.init()
b_font = pygame.font.SysFont('arialblack', 40)

def blit_text(surface, text, pos, font=b_font, color=(255, 255, 255)):
    """
    Affichage de text, qui prend en compte les sauts à la ligne.
    """
    words = [word.split('\n') for word in text.splitlines()]  
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x,y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  
                y += word_height  
            surface.blit(word_surface, (word_surface.get_rect(center = (max_width//2, y))))
            x += word_width + space
        x = pos[0] 
        y += word_height 
