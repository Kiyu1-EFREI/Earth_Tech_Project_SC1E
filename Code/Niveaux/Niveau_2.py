import pygame
import math
from Code.Utils.Utils import *
from random import randint, random, uniform

# permet de cree les objet fire
def create_fire(map, x, y):
    anim_speed = uniform(0.16,0.22)
    frame = []
    for i in range(1,11):
        frame.append(pygame.transform.scale(pygame.image.load("./Asset/maps/fire_"+str(i)+".png").convert_alpha(), (40, 45)))

    fire = ObjetClass(pygame.Rect(x * 10, y * 10, 30, 35), "fire")
    fire.frame = frame
    fire.anim_speed = anim_speed
    fire.variable = 10
    map.fire.append(fire)

# interaction sppecifique au niveau 1
def utilisation_lvl_2(map, e):
    # permet d'etteindre le feu
    if e.type == "fire" and map.water >= 10 and not map.press_e:
        gestion_eau(map, -10)
        e.variable -= 10
        if e.variable <= 0:
            map.fire.remove(e)
            map.score -= 1
            map.level_2_extinguished += 1

            # Vérifier si le joueur a gagné
            if map.level_2_extinguished >= 20:
                map.popup_active = True
                map.popup_timer = 1000

# permet de gerer les feu
def generation_fire(map):
    if map.level_2_extinguished >= 20:
        return
    if len(map.fire) <= 1:
        nb_fire = 1
    elif aleatoire(map.aleatoire):
        nb_fire = 1
    else:
        nb_fire = 0

    # determination des coordonée
    if nb_fire == 1 and len(map.fire) < 15:
        placement = False
        while not placement:
            x = randint(5, 120)
            y = randint(7, 65)
            placement = True
            for e in map.element[1:] + map.fire:
                if pygame.Rect(x * 10,y * 10, 30, 35).colliderect(e.rect) or (0 < x < 40 and 33 < y < 75):
                    placement = False
        map.score += 1
        create_fire(map, x, y)
    elif len(map.fire) >= 15:
        print("Perdu")

# initialisation des element et parametre pour le niveau 2
def init_lvl_2(map):

    create_fire(map, 111, 18)
    create_fire(map, 94, 55)
    create_fire(map, 38, 10)
    map.aleatoire.s = 2
    map.aleatoire.min = 2
    map.aleatoire.max = 4
    map.score = 3
    map.level_2_extinguished = 0
