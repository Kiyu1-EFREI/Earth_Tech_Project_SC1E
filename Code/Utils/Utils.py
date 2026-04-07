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
            elif el.type == "water_tube":
                fill_ratio = getattr(el, 'variable', 0) / 100
                fill_ratio = max(0, min(fill_ratio, 1))
                inner_padding = 4
                inner_width = max(0, el.rect.width - inner_padding * 2)
                inner_height = max(0, int((el.rect.height - inner_padding * 2) * fill_ratio))
                inner_x = el.rect.x + inner_padding
                inner_y = el.rect.bottom - inner_padding - inner_height
                if inner_height > 0:
                    pygame.draw.rect(screen, (50, 150, 255), (inner_x, inner_y, inner_width, inner_height),
                                     border_radius=8)
                pygame.draw.rect(screen, el.color, el.rect, border_radius=12, width=3)
                segment_height = el.rect.height / 10
                for i in range(1, 10):
                    y = int(el.rect.y + segment_height * i)
                    pygame.draw.line(screen, el.color, (el.rect.x + inner_padding, y), (el.rect.x + el.rect.width - inner_padding, y), 1)

            elif len(el.frame) == 0:
                # Rendre transparent les rectangles sans images
                if el.type not in ["platform", "wall", "water_tank", "score_bare", "pollution_bare","water"]:
                    pygame.draw.rect(screen, el.color, el.rect)
                else:
                    # Créer un rectangle semi-transparent pour les éléments de jeu
                    temp_surface = pygame.Surface(el.rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, (*el.color, 0), temp_surface.get_rect(), border_radius=5)  # Transparent
                    screen.blit(temp_surface, el.rect)
            elif len(el.frame) == 1:
                if el.type == "dirt_pile":
                    img = el.frame[0]
                    screen.blit(img, (el.rect.x, el.rect.bottom - img.get_height()))
                else:
                    screen.blit(el.frame[0], el.rect.topleft)
            else:
                img = el.frame[int(el.anim_index) % len(el.frame)]
                if el.type == "dirt_pile":
                    screen.blit(img, (el.rect.x, el.rect.bottom - img.get_height()))
                else:
                    screen.blit(img, el.rect.topleft)
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
            elif key == "boss":
                try:
                    boss_img = pygame.image.load("./Asset/maps/boss.png").convert_alpha()
                    boss_img = pygame.transform.scale(boss_img, (int(i[2] * 10), int(i[3] * 10)))
                    rect[-1].frame = [boss_img]
                except Exception:
                    rect[-1].color = (60, 60, 60)

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
        "water": [[5, 43, 17, 4]],
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
    if hasattr(map, 'water_tube'):
        map.water_tube.variable = map.water

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


# fonction qui affiche une popup avec texte arrondi
def draw_popup(screen, map):
    if map.popup_active:
        # Dimensions de la fenêtre popup
        popup_width = 800
        popup_height = 400
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = (screen.get_height() - popup_height) // 2

        # Créer une surface avec transparence pour le popup
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)

        # Dessiner un rectangle arrondi semi-transparent
        pygame.draw.rect(popup_surface, (50, 50, 50, 220), popup_surface.get_rect(), border_radius=20)
        pygame.draw.rect(popup_surface, (100, 200, 100, 255), popup_surface.get_rect(), width=3, border_radius=20)

        # Afficher la popup sur l'écran
        screen.blit(popup_surface, (popup_x, popup_y))

        # Texte du message selon le niveau
        if map.niveau == 1:
            message = ("Le plastique éternel : Saviez-vous qu'une bouteille en plastique met environ 450 ans "
                       "à se\n décomposer ? Elle ne disparaît jamais vraiment, elle se transforme en microplastiques.\n\n"
                       "L'ennemi invisible : 80% des déchets marins proviennent de la terre ferme. "
                       "Chaque geste\ne compte, même loin des côtes.\n\n"
                       "Le mégot fatal : Un seul mégot de cigarette peut polluer jusqu'à 1 000 litres d'eau.")
            next_level_text = "Passage au niveau 2 dans {seconds_left}s"
            next_level = 2
        elif map.niveau == 2:
            message = ("1- L'énergie la plus propre : C'est celle que l'on ne consomme pas. \nÉteindre les lumières inutiles "
                       "n'est pas un petit geste, c'est une nécessité systémique.\n\n"
                       "2- L'or bleu : Moins de 1% de l'eau sur Terre est douce et accessible.\n Dans ce jeu comme dans la réalité, "
                       "chaque goutte est précieuse.\n\n"
                       "3- Numérique polluant : Si Internet était un pays, il serait le 3ème plus gros consommateur \nd'électricité au monde.")
            next_level_text = "Passage au niveau 3 dans {seconds_left}s"
            next_level = 3
        else:
            message = "Message par défaut"
            next_level_text = "Passage au niveau suivant dans {seconds_left}s"
            next_level = map.niveau + 1



        # Diviser le texte en plusieurs lignes pour l'afficher
        font = pygame.font.Font(None, 25)
        lines = message.split('\n')
        y_offset = popup_y + 30

        for line in lines:
            if line.strip():
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (popup_x + 20, y_offset))
                y_offset += 30
            else:
                y_offset += 15

        # Afficher le compte à rebours
        seconds_left = max(0, (map.popup_timer // 60))
        countdown_font = pygame.font.Font(None, 24)
        countdown_text = countdown_font.render(next_level_text.format(seconds_left=seconds_left), True, (255, 200, 100))
        screen.blit(countdown_text,
                    (popup_x + popup_width // 2 - countdown_text.get_width() // 2, popup_y + popup_height - 40))

        # Décrémenter le timer
        map.popup_timer -= 1

        # Si le timer atteint 0, changer de niveau
        if map.popup_timer <= 0:
            map.popup_active = False
            map.niveau = next_level

# fonction qui affiche la défaite et renvoie au menu au clic
def draw_defeat(screen, map):
    if getattr(map, 'defeat_active', False):
        # Créer un overlay sombre semi-transparent
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Afficher "Défaite" en gros au milieu
        font = pygame.font.Font(None, 150)
        text = font.render("Défaite", True, (200, 0, 0))
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)

        # Petit texte d'instruction
        font_small = pygame.font.Font(None, 40)
        sub_text = font_small.render("Cliquez pour revenir au menu", True, (255, 255, 255))
        sub_rect = sub_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(sub_text, sub_rect)

        # Si on clique n'importe où, on retourne au menu (niveau 0)
        if map.click:
            map.niveau = -2
            map.defeat_active = False
