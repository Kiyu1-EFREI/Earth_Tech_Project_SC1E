import pygame

def init_par_menu(police):
    element = [
        pygame.image.load("Asset/menu/parametre_menu_background.png").convert_alpha(),
        [pygame.transform.scale(pygame.image.load("Asset/menu/parametre_menu_txt.png").convert_alpha(), (400, 100)), (440, 150)],
    ]
    return element