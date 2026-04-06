import pygame
import random
from random import choice, randint
from Code.Utils.Utils import *
from Code.Utils.classes import ObjetClass

def element_lvl_3():
    element = {
        "poubelle_plastique": [
            [80, 65, 4, 5]
        ],
        "poubelle_verre": [
            [100, 65, 4, 5]
        ],
        "poubelle_reste": [
            [120, 65, 4, 5]
        ]
    }
    return element

def init_lvl_3(map):
    map.water = 0
    map.score = 0
    map.pollution = 0
    map.temps_restant = 60 * 60
    map.dechets = []
    map.dechet_transporte = None
    map.timer_apparition = 0
    map.intervalle_apparition = 120
    map.types_dechets = ["plastique", "verre", "alimentaire"]
    map.couleurs_dechets = {
        "plastique": (255,255,0),
        "verre": (0,255,0),
        "alimentaire": (255,0,0)
    }
    map.poubelles = []
    map.joueur.inventory = {"plastique": 0, "verre": 0, "alimentaire": 0}
    map.aleatoire.nb_s = 2
    map.aleatoire.min = 2
    map.aleatoire.max = 4
    map.pollution_bare = ObjetClass(pygame.Rect(10, 40, 200, 25), "pollution_bare")
    map.pollution_bare.color = (255, 0, 0)
    for e in map.element:
        if e.type in ["poubelle_plastique", "poubelle_verre", "poubelle_reste"]:
            map.poubelles.append(e)
            if e.type == "poubelle_plastique":
                e.type_dechet = "plastique"
                e.color = (255,255,0)
            elif e.type == "poubelle_verre":
                e.type_dechet = "verre"
                e.color = (0, 255, 0)
            elif e.type == "poubelle_reste":
                e.type_dechet = "alimentaire"
                e.color = (255, 0, 0)

def utilisation_lvl_3(map, e):
    if e.type in ["poubelle_plastique", "poubelle_verre", "poubelle_reste"]:
        if map.joueur.inventory.get(e.type_dechet, 0) > 0:
            map.joueur.inventory[e.type_dechet] -= 1
            map.score += 1
            map.pollution = max(0, map.pollution - 5)
            map.interaction = True
        else:
            map.interaction = False

    elif e.type == "dechet":
        map.joueur.inventory[e.type_dechet] = map.joueur.inventory.get(e.type_dechet, 0) + 1
        e.visible = False
        if e in map.dechets:
            map.dechets.remove(e)
        map.interaction = True

def generer_dechet(map):
    if len(map.dechets) < 10:
        type_dechet = choice(map.types_dechets)
        couleur = map.couleurs_dechets[type_dechet]

        plateformes = [p for p in map.element if p.type == "platform"]
        if plateformes :
            p = choice(plateformes)
            x = p.rect.x + randint(10, p.rect.width - 30)
            y = p.rect.y - 20
            dechet = ObjetClass(pygame.Rect(x, y, 50, 50), "dechet")
            dechet.type_dechet = type_dechet
            dechet.color = couleur
            img_name = f"dechet_{type_dechet}.png"
            dechet.frame = [pygame.transform.scale(pygame.image.load(f"./Asset/maps/{img_name}").convert_alpha(), (50, 50))]
            dechet.visible = True
            map.dechets.append(dechet)


def update_lvl_3(map):
    if aleatoire(map.aleatoire):
        generer_dechet(map)
    gestion_pollution(map)
    if map.score >= 20:
        map.niveau = 0  # Win, return to menu

def gestion_pollution(map):
    map.pollution = min(100, map.pollution + 0.1)