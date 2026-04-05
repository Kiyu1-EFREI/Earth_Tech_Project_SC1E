from Code.Utils.classes import *
import pygame

police = "Arial"


def init_main_menu(police):
    # Use Pygame's default font instead of SysFont to avoid system font scan issues.
    # This is more reliable across machines and prevents crashes during startup.
    title_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 48)

    element = [
        ButtonClass(
            pygame.Rect(0, 0, 1280, 720),
            "Asset/menu/main_menu_background.png",
            title_font,
            None,
            (100, 100, 100),
            0
        ),
        ButtonClass(
            pygame.Rect(340, 130, 600, 120),
            "Asset/menu/main_menu_txt.png",
            title_font,
            None,
            (100, 100, 100),
            0
        ),
        ButtonClass(
            pygame.Rect(460, 360, 360, 80),
            "Jouer",
            button_font,
            -1
        ),
        ButtonClass(
            pygame.Rect(460, 470, 360, 80),
            "Quitter",
            button_font,
            0
        )
    ]
    return element