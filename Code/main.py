from Utils.map import*
from Menu.menu import*
import pygame

# structure pygame
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
#screen = pygame.display.set_mode((1400, 800))
#screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
police = "Arial"
click = False
continue_click = False
old_w = 1280
old_h = 720

# premier initialisation
niveau = -2
if niveau > 0:
    if niveau == 1:
        element_lvl = element_lvl_1()
    elif niveau == 2:
        element_lvl = {}
    elif niveau == 3:
        element_lvl = element_lvl_3()
    else:
        element_lvl = element_lvl_1()

    element = element_map_general() | element_lvl
    map = init_map(niveau, screen)
else:
    element = init_menu(niveau, police)
#resize(element, screen.get_width(), screen.get_height(), 1280, 720)

# Boucle principale de Pygame
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            new_width = event.w
            new_height = event.h
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            resize(element, screen.get_width(), screen.get_height(), old_w, old_h)
            old_w = new_width
            old_h = new_height



        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        else:
            click = False


    # run menu ou niveau
    if niveau > 0 :
        map.click = click
        run_map(map)
        new_niveau = map.niveau
    else:
        new_niveau = run_menu(screen, element, niveau, click, continue_click)

    # initialisation de la map ou niveau lors d'un changement
    if niveau != new_niveau:
        niveau = new_niveau
        if niveau > 0:
            map = init_map(niveau, screen)
            map.screen = screen
            map_resize(map, screen.get_width(), screen.get_height(), 1280, 720)
        elif niveau == 0:
            run = False
        else:
            element = init_menu(niveau, police)
            resize(element, screen.get_width(), screen.get_height(), 1280, 720)
    continue_click = click
    pygame.display.flip()
    clock.tick(60)

pygame.quit()