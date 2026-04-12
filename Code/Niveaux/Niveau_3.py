import pygame
from random import choice
from Code.Utils.Utils import aleatoire
from Code.Utils.classes import ObjetClass


def element_lvl_3():
    # Définit le lieu de spawn des poubelles
    return {
        "poubelle_plastique": [[40, 60, 10, 12]],
        "poubelle_verre": [[60, 60, 10, 12]],
        "poubelle_reste": [[80, 60, 10, 12]]
    }

def init_lvl_3(map):
    map.water = 0
    map.score = 0
    map.pollution = 0
    map.temps_restant = 60 * 60
    map.dechets = []
    map.types_dechets = ["plastique", "verre", "reste"]
    map.level3_finished = False

    map.joueur.inventory = {"plastique": 0, "verre": 0, "reste": 0}

    map.couleurs_dechets = {
        "plastique": (255, 255, 0),
        "verre": (0, 255, 0),
        "reste": (255, 0, 0)
    }

    map.poubelles = []
    map.aleatoire.nb_s, map.aleatoire.min, map.aleatoire.max = 2, 2, 4
    map.pollution_bare = ObjetClass(pygame.Rect(10, 40, 200, 25), "pollution_bare")
    map.pollution_bare.color = (255, 0, 0)

    types_poubelles_attendus = ["poubelle_plastique", "poubelle_verre", "poubelle_reste"]

    for poubelle in map.element:
        if poubelle.type in types_poubelles_attendus:
            map.poubelles.append(poubelle)
            # Assignation de la logique de tri
            if poubelle.type == "poubelle_plastique":
                poubelle.type_dechet = "plastique"
            elif poubelle.type == "poubelle_verre":
                poubelle.type_dechet = "verre"
            elif poubelle.type == "poubelle_reste":
                poubelle.type_dechet = "reste"

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
        if sum(map.joueur.inventory.values()) == 0:
            map.joueur.inventory = {"plastique": 0, "verre": 0, "reste": 0}
            map.joueur.inventory[e.type_dechet] = 1
            e.visible = False
            if e in map.dechets: map.dechets.remove(e)
            map.interaction = True


def generer_dechet(map):
    # Verification que la plateforme est libre
    if not hasattr(map, 'types_dechets') or not map.types_dechets or len(map.dechets) >= 10:
        return
    type_dechet = choice(map.types_dechets)
    plateformes = [p for p in map.element if p.type == "platform"]
    # On ne garde que les plateformes sans déchet déjà présent
    libres = [p for p in plateformes if
              not any(abs(d.rect.x - (p.rect.x + (p.rect.width - 50) // 2)) < 10 for d in map.dechets)]

    if libres:
        p = choice(libres)
        x = p.rect.x + (p.rect.width - 50) // 2
        y = p.rect.y - 50
        dechet = ObjetClass(pygame.Rect(x, y, 50, 50), "dechet")
        dechet.type_dechet = type_dechet

        # On s'assure que le nom du fichier image est correct
        img_name = f"dechet_{type_dechet}.png"
        dechet.frame = [
            pygame.transform.scale(pygame.image.load(f"./Asset/maps/{img_name}").convert_alpha(), (50, 50))]
        dechet.visible = True
        map.dechets.append(dechet)


def update_lvl_3(map):
    if not hasattr(map, 'types_dechets'):
        return

    if map.score >= 20:
        if not map.popup_active and not getattr(map, 'level3_finished', False):
            map.popup_active = True
            map.popup_timer = 1000
            map.level3_finished = True
        return

    if hasattr(map, 'pollution') and map.pollution >= 150:
        map.niveau = 0
        return

    if aleatoire(map.aleatoire):
        generer_dechet(map)

    if hasattr(map, 'pollution'):
        map.pollution = min(150, map.pollution + 0.1)