import pygame
import random
from Utils.Utils import init_map, run_map
from Utils.classes import ObjetClass

class Niveau_3:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.grande_font = pygame.font.Font(None, 72)
        self.petite_font = pygame.font.Font(None, 24)

        self.elements = {
            "platform": [
                [0, 70, 130, 1],
                [20, 55, 15, 1],
                [50, 45, 15, 1],
                [80, 35, 15, 1],
                [110, 25, 15, 1],
            ],
            "wall": [
                [0, 0, 1, 72],
                [129, 0, 1, 72],
                [-1, 0, 1, 72]   
            ],
            "water": [
                [5, 69, 5, 1],
                [120, 69, 5, 1]
            ]
        }

        self.map = init_map(3, self.elements, screen)
        self.map.water = 50
        self.flammes = []
        self.temps_restant = 60