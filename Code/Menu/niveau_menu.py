from Code.Utils.classes import*
import pygame

def init_lvl_menu(police):
    element = [
        ButtonClass(pygame.Rect(0, 0, 1280, 720), "Asset/menu/niveau_menu_background.png", pygame.font.Font(None, 48), None, (100, 100, 100), 0),
        ButtonClass(pygame.Rect(440, 50, 400, 250), "Asset/menu/niveau_menu_txt.png", pygame.font.Font(None, 48),None, (100, 100, 100), 0),
        ButtonClass(pygame.Rect(195, 320, 200, 200), "1", pygame.font.Font(None, 200), 1),
        ButtonClass(pygame.Rect(425, 320, 200, 200), "2", pygame.font.Font(None, 200), 2),
        ButtonClass(pygame.Rect(655, 320, 200, 200), "3", pygame.font.Font(None, 200), 3),
        ButtonClass(pygame.Rect(885, 320, 200, 200), "4", pygame.font.Font(None, 200), 4),
        ButtonClass(pygame.Rect(1220, 10, 50, 50), "Asset/menu/upgrade.png", pygame.font.Font(None, 200), -3)
    ]
    return element
