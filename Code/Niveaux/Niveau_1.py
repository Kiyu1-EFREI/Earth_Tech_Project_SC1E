import pygame
import math
from Code.Utils.Utils import *

# interaction specifique au niveau 1
def utilisation_lvl_1(map, e):
    if e.type == "dirt_pile":
        # permet de mettre de l'eau sur une graine
        if map.water > 0 and e.anim_index == 1 and e.variable < 100 and (not map.press_e or map.interaction):
            gestion_eau(map, -1)
            e.variable += 1
            map.interaction = True
        else:
            map.interaction = False

        # permet de mettre une graine dans un tas de terre
        if e.anim_index == 0 and map.seed:
            map.seed = False
            e.anim_index = 1
            e.rect.y -= 10
            e.rect.height += 10

        # permet de faire grandir la graine
        elif e.variable >= 100 and e.anim_index == 1 :
            e.anim_index = 2
            e.rect.y -= 10
            e.rect.height += 10
            map.score += 1

    elif e.type == "oiseau" and e.variable[4] and map.seed == False and map.press_e == False:
        map.seed = True
        e.variable[4] = False
        print("seeeeed")

# gestion des trajectoire des oiseaux
def avancer_oiseau(map, vitesse):
    for o in map.oiseau:
        o.variable[3] -= vitesse
        if o.variable[3] > 360:
            o.variable[3] -= 360
        elif o.variable[3] < -360:
            o.variable[3] += 360

        # desparition de l'oiseau
        if ( 70 < o.variable[3] < 110 or -70 > o.variable[3] > -110 ) and o.variable[4] == False and o.visible == True:
            o.visible = False

        # calcul de la trajectoire
        rad = math.radians(o.variable[3])
        o.rect.x = o.variable[0] + o.variable[2] * math.cos(rad)
        o.rect.y = o.variable[1] + o.variable[2] * math.sin(rad)

# element specifique au niveau 1
def element_lvl_1():
    element = {
        "dirt_pile" : [[115, 68, 3, 2],[72, 68, 3, 2],[38, 68, 3, 2]]
    }
    return element

# initialisation des element et parametre pour le niveau 1
def init_lvl_1(map):
    map.oiseau = [
        ObjetClass(pygame.Rect(0, 0, 40, 40), "oiseau"),
        ObjetClass(pygame.Rect(580, 90, 40, 40), "oiseau"),
        ObjetClass(pygame.Rect(1180, 110, 40, 40), "oiseau")
    ]

    for i in map.oiseau:
        i.anim_speed = 0.15
        for j in range(1,4):
            i.frame.append(pygame.transform.scale(pygame.image.load("./Asset/maps/bird_"+str(j)+".png").convert_alpha(), (40, 40)))

    map.oiseau[0].variable = [60, -10, 110, 300, True] # [centre_x, centre_y, rayon, angle, a_une_seed]
    map.oiseau[1].variable = [620, -60, 180, 60, True]
    map.oiseau[2].variable = [1150, -20, 150, 180, True]



