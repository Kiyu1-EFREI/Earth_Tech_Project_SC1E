from Code.Utils.classes import*
import pygame

def init_EOTF_menu(police):
    element = [
        ButtonClass(pygame.Rect(0, 0, 1280, 720), "Asset/menu/EOTF_menu_background.png", pygame.font.SysFont(police, 48), None, (100, 100, 100), 0),
        ButtonClass(pygame.Rect(440, 50, 400, 250), "Asset/menu/EOTF_menu_txt.png", pygame.font.SysFont(police, 48),None, (100, 100, 100), 0),
        ButtonClass(pygame.Rect(310, 320, 200, 200), "Asset/menu/speed_F.png", pygame.font.SysFont(police, 200), 0),
        ButtonClass(pygame.Rect(540, 320, 200, 200), "Asset/menu/icefloor_F.png", pygame.font.SysFont(police, 200), 1),
        ButtonClass(pygame.Rect(770, 320, 200, 200), "Asset/menu/time_F.png", pygame.font.SysFont(police, 200), 2),
        ButtonClass(pygame.Rect(10, 10, 50, 50), "Asset/menu/back.png", pygame.font.SysFont(police, 200), -1,"Asset/menu/back_hover.png")
    ]
    return element

