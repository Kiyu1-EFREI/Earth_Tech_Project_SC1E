from .classes import *
import pygame
from random import random

# fonction pour faire apparaitre les element de la map (platforme, fond, etc ...)
def draw_element(screen, element): # element -> list d'objet de la class ObjetClass
    screen.fill((30, 30, 30))
    for el in element:
        if el.visible:
            if el.type == "background":
                if len(el.frame) > 0:
                    screen.blit(el.frame[0], (0, 0))
            elif len(el.frame) == 0:
                pygame.draw.rect(screen, el.color, el.rect)
            elif len(el.frame) == 1:
                screen.blit(el.frame[0], el.rect.topleft)
            else:
                screen.blit(el.frame[int(el.anim_index) % len(el.frame)], el.rect.topleft)
                el.anim_index += el.anim_speed

# fonction qui cree une list d'element de la class ObjetClass et qui les renvoie dans une list
def create_element(element, niveau = 0, bg = '0'): # element = {"water" : [[160, 380, 50, 50]], "wall" : [[0, 70, 140, 3], [-1, 0, 1, 72]]}
    rect = []

    rect.append(ObjetClass('', 'background'))
    if bg != '0':
        rect[0].frame = [pygame.transform.scale(pygame.image.load("./Asset/" + bg).convert(), (1280, 720))]

    for key, val in element.items():
        for i in val:
            rect.append(ObjetClass(pygame.Rect(i[0]*10, i[1]*10, i[2]*10, i[3]*10), key))

            if key == "platform":
                if niveau == 1:
                    p_img = 'ciel_platform.png'
                else:
                    p_img = 'forest_platforme.png'
                rect[-1].frame = [pygame.transform.scale(pygame.image.load("./Asset/maps/" + p_img).convert_alpha(),(120, 35))]

            elif key == "dirt_pile":
                rect[-1].frame = [pygame.transform.scale(pygame.image.load("./Asset/maps/tas_terre.png").convert_alpha(),(30, 20)),
                                  pygame.transform.scale(pygame.image.load("./Asset/maps/tas_terre_haut.png").convert_alpha(),(30, 30)),
                                  pygame.transform.scale(pygame.image.load("./Asset/maps/tas_terre_plant.png").convert_alpha(),(30, 40))]

            elif key == "poubelle_plastique":
                rect[-1].frame = [pygame.transform.scale(pygame.image.load("./Asset/maps/poubelle_plastique.png").convert_alpha(), (100, 100))]

            elif key == "poubelle_verre":
                rect[-1].frame = [pygame.transform.scale(pygame.image.load("./Asset/maps/poubelle_verre.png").convert_alpha(), (100, 100))]

            elif key == "poubelle_reste":
                rect[-1].frame = [pygame.transform.scale(pygame.image.load("./Asset/maps/poubelle_reste.png").convert_alpha(), (100, 100))]

            elif key == "water":
                rect[-1].color = (0, 0, 255)

    return rect


def element_map_general():
    # Initialisation de la position de chaque elements de la map
    element = {
        "wall": [
            [0, 70, 140, 3],
            [-1, 0, 1, 72],
            [128, 0, 1, 72],
            [0, 45, 30, 25]
        ],
        "water": [[1, 43, 14, 4]],
        "platform": [
            [89, 60, 12, 2],
            [45, 60, 12, 2],
            [67, 50, 12, 2],
            [60, 21, 12, 2],
            [107, 24, 12, 2],
            [48, 41, 12, 2],
            [25, 34, 12, 2],
            [6, 23, 12, 2],
            [33, 14, 12, 2],
            [78, 31, 12, 2],
            [96, 41, 12, 2]
        ],
    }
    return element

# fonction gerer le niveau d'eau
def gestion_eau(map, value):
    map.water += value
    if map.water > 100:
        map.water = 100
    elif map.water < 0:
        map.water = 0
    h = 120 * (map.water / 100)
    map.water_tank.rect.height = h
    map.water_tank.rect.y = 660 - h

# fonction qui gere la taille de la barre
def gestion_score_bare(map, value): # value en %
    map.score_bare.rect.width = 200 * (value / 100)

# fonction qui gere la taille de la barre de pollution
def gestion_pollution_bare(map):
    if hasattr(map, 'pollution_bare'):
        map.pollution_bare.rect.width = 200 * (map.pollution / 100)

# fonction qui gere l'aleatoire
def aleatoire(a):
    if a.time/60 > a.max:
        a.time = 0
        return True
    elif a.time/60 > a.min and random() < (a.nb_s / 60):
        a.time = 0
        return True
    return False

# fonction qui dessine les bouttons
def draw_botton(screen, element, click, niveau, continue_click):
    mouse = pygame.mouse.get_pos()
    for botton in element:
        is_hover = botton.rect.collidepoint(mouse)
        if is_hover:
            if click and not continue_click  and botton.action != None:
                niveau = botton.action
            col = botton.hover
        else:
            col = botton.color

        if ".png" in botton.text:
            # Charger l'image
            if is_hover and type(botton.hover) == str:
                img = pygame.image.load(botton.hover).convert_alpha()
            else:
                img = pygame.image.load(botton.text).convert_alpha()
            img = pygame.transform.smoothscale(img, (botton.rect.width, botton.rect.height))

            # Surface avec alpha
            rounded = pygame.Surface((botton.rect.width, botton.rect.height), pygame.SRCALPHA)

            # Dessiner un rectangle arrondi blanc (servira de masque)
            pygame.draw.rect(
                rounded,
                (255, 255, 255),
                rounded.get_rect(),
                border_radius=botton.border_r
            )

            # Appliquer le masque : on copie l'image dans la surface arrondie
            rounded.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Afficher
            screen.blit(rounded, botton.rect)

        else:
            if col != None:
                pygame.draw.rect(screen, col, botton.rect, border_radius=botton.border_r)
            txt = botton.police.render(botton.text, True, botton.text_color)
            screen.blit(txt, txt.get_rect(center=botton.rect.center))
    return niveau


def resize(elements, new_w, new_h, old_w, old_h):
    scale_x = new_w / old_w
    scale_y = new_h / old_h
    if type(elements) != list:
        elements = [elements]
    for el in elements:
        w = el.rect.width
        h = el.rect.height

        if w == h:
            if w * scale_x < h * scale_y:
                el.rect.width *= scale_x
                el.rect.height *= scale_x
            else:
                el.rect.width *= scale_y
                el.rect.height *= scale_y
        else:
            el.rect.width *= scale_x
            el.rect.height *= scale_y
        el.rect.x *= scale_x
        el.rect.y *= scale_y

        if len(el.frame) > 0:
            for i in range(len(el.frame)):
                el.frame[i] = pygame.transform.scale(el.frame[i], (el.rect.width, el.rect.height))
