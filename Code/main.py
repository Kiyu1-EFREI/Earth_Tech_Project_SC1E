from Utils.map import*
from Utils.classes import*
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
joueur = pygame.Rect(160, 380, 50, 50)

# Initialisation de la position de chaque elements qui sera affiché a l'écran

element = {

    "wall" : [
        [0, 70, 140, 3],
        [-1, 0, 1, 72],
        [128, 0, 1, 72],
        [0, 45, 30, 25]
    ],
    "water" : [[1,43,14,4]],
    "platform" : [
        [89, 60],
        [45, 60],
        [67, 50],
        [60, 21],
        [107, 24],
        [48, 41],
        [25, 34],
        [6, 23],
        [33, 14],
        [78, 31],
        [96, 41]
    ]
}

map = MapClass(0.7, 7, 0.8, 0.8, element, screen, joueur)
init_map(map, 0)

# Boucle principale de Pygame

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    run_map(map)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()