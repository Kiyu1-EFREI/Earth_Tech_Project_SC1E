import pygame
import random
from Code.Utils.Utils import *
from Code.Utils.classes import ObjetClass

def element_lvl_3():
    element = {
        "poubelle_plastique": [
            [10, 65, 4, 5]
        ],
        "poubelle_verre": [
            [60, 65, 4, 5]
        ],
        "poubelle_papier": [
            [110, 65, 4, 5]
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
    map.types_dechets = ["plastique", "verre", "papier"]
    map.couleurs_dechets = {
        "plastique": (255,255,0),
        "verre": (0,255,0),
        "papier": (0,0,255)
    }
    map.poubelles = []
    map.joueur.inventory = {"plastique": 0, "verre": 0, "papier": 0}
    for e in map.element:
        if e.type in ["poubelle_plastique", "poubelle_verre", "poubelle_papier"]:
            map.poubelles.append(e)
            if e.type == "poubelle_plastique":
                e.type_dechet = "plastique"
                e.color = (255,255,0)
            elif e.type == "poubelle_verre":
                e.type_dechet = "verre"
                e.color = (0, 255, 0)
            elif e.type == "poubelle_papier":
                e.type_dechet = "papier"
                e.color = (0, 0, 255)

def utilisation_lvl_3(map, e):
    if e.type in ["poubelle_plastique", "poubelle_verre", "poubelle_papier"]:
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
        type_dechet = random.choice(map.types_dechets)
        couleur = map.couleurs_dechets[type_dechet]

        plateformes = [p for p in map.element if p.type == "platform"]
        if plateformes :
            p = random.choice(plateformes)
            x = p.rect.x + random.randint(10, p.rect.width - 30)
            y = p.rect.y - 20
            dechet = ObjetClass(pygame.Rect(x, y, 20, 20), "dechet")
            dechet.type_dechet = type_dechet
            dechet.color = couleur
            dechet.visible = True
            map.dechets.append(dechet)


def update_lvl_3(map):
    if aleatoire(map.aleatoire):
        generer_dechet(map)
    gestion_pollution(map)

def gestion_pollution(map):
    # Augmente la pollution lentement au cours du temps
    map.pollution = min(100, map.pollution + 0.1)  # Augmente de 0.1 par frame, max 100
