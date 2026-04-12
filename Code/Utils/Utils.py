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
                if el.type not in ["platform", "wall", "water_tank", "pollution_bare","water"]:
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
                                  pygame.transform.scale(pygame.image.load("./Asset/maps/tas_terre_plant.png").convert_alpha(),(30, 30))]

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
            # Surface avec alpha
            width = botton.rect.width
            height = botton.rect.height

            if is_hover and type(botton.hover) == str:
                if ".png" in botton.hover:
                    img = pygame.image.load(botton.hover).convert_alpha()
                else:
                    width += 20
                    height += 20
                    botton.rect.x -= 10
                    botton.rect.y -= 10
                    img = pygame.image.load(botton.text).convert_alpha()
            else:
                img = pygame.image.load(botton.text).convert_alpha()
            img = pygame.transform.smoothscale(img, (width, height))

            rounded = pygame.Surface((width, height), pygame.SRCALPHA)
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
            if is_hover and type(botton.hover) == str and not(".png" in botton.hover):
                botton.rect.x += 10
                botton.rect.y += 10
        else:
            if col != None and type(col) == tuple:
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
        elif map.niveau == 3:
            message = ("1- La règle des 3R\n"
                       "C’est le code secret de l'écologie :\n\n"
                       "Réduire : Est-ce que j'ai vraiment besoin de ce nouveau jouet en plastique ?\n\n"
                       "Réutiliser : Un bocal en verre peut devenir un pot à crayons stylé.\n\n"
                       "Recycler : Donne une seconde vie à tes déchets en les mettant dans la bonne poubelle.\n\n"
                       "2- Deviens un \"Chasseur de Fantômes\" Énergétiques\n"
                       "Même éteints, les appareils branchés (comme une console ou un chargeur) consomment un tout petit peu d'électricité. C'est ce qu'on appelle la consommation veille.\n"
                       "3- Manger local : Choisir une pomme de ton pays plutôt qu'une mangue venue par avion réduit énormément la pollution.")
            next_level_text = "Passage au niveau 4 dans {seconds_left}s"
            next_level = 4
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
def draw_victory(screen, map):
    if not getattr(map, 'victory', False):
        return

    # Créer un overlay sombre semi-transparent
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Afficher "Victoire !" en gros au milieu
    font = pygame.font.Font(None, 150)
    text = font.render("Victoire !", True, (0, 255, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(text, rect)

    # Message de victoire
    victory_message = ("Félicitations, Héros de la Terre !\n"
                       "Grâce à ton courage et à tes actions, le Monstre de Pollution a disparu.\n"
                       "Regarde : les fleurs repoussent, l'air devient pur et les animaux reviennent\n"
                       "habiter dans une forêt protégée. Tu as prouvé que même de petits gestes\n"
                       "peuvent sauver tout un monde. N'oublie jamais qu'en prenant soin de la\n"
                       "nature dans la vraie vie, tu as le pouvoir de transformer la planète pour de bon.\n"
                       "La nature a repris ses droits grâce à TOI !")

    # Diviser le texte en plusieurs lignes pour l'afficher
    font_small = pygame.font.Font(None, 20)
    lines = victory_message.split('\n')
    y_offset = screen.get_height() // 2 + 50

    for line in lines:
        if line.strip():
            text_surface = font_small.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 30
        else:
            y_offset += 15

    # Petit texte d'instruction
    font_click = pygame.font.Font(None, 40)
    click_text = font_click.render("Cliquez pour revenir au menu", True, (255, 255, 0))
    click_rect = click_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
    screen.blit(click_text, click_rect)

    # Si on clique n'importe où, on retourne au menu (niveau 0)
    if map.click:
        map.niveau = -2
        map.victory = False

def draw_level_intro(screen, map):
    if not map.level_intro_active:
        return

    # Créer un overlay sombre semi-transparent
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    # Dimensions de la fenêtre popup
    popup_width = 1000
    popup_height = 500
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2

    # Créer une surface avec transparence pour le popup
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)

    # Dessiner un rectangle arrondi semi-transparent
    pygame.draw.rect(popup_surface, (50, 50, 50, 240), popup_surface.get_rect(), border_radius=20)
    pygame.draw.rect(popup_surface, (100, 200, 100, 255), popup_surface.get_rect(), width=3, border_radius=20)

    # Afficher la popup sur l'écran
    screen.blit(popup_surface, (popup_x, popup_y))

    # Messages d'introduction selon le niveau
    if map.niveau == 1:
        title = "🎮 Niveau 1 : Le Réveil de la Forêt"
        objective = "Objectif : Apprendre les bases et planter la vie."
        story = (
            "Bienvenue, jeune gardien de la nature ! Ici, pas de danger : prends le temps de découvrir tes pouvoirs.\n"
            "Attrape les graines transportées par les oiseaux, plante-les et utilise l'eau de l'étang\n"
            "pour les aider à grandir. La forêt compte sur toi pour s'épanouir !")
        action = "Action : Appuie sur \"E\" pour intercepter les graines, planter et remplir ton réservoir."

    elif map.niveau == 2:
        title = "🔥 Niveau 2 : Alerte Incendie"
        objective = "Objectif : Protéger la forêt des flammes."
        story = ("Vite ! Des mégots de cigarettes et la chaleur ont déclenché un incendie.\n"
                 "Si le feu se propage trop, la forêt disparaîtra ! Remplis vite ton réservoir à l'étang\n"
                 "et fonce éteindre les flammes avant qu'il ne soit trop tard. Sois rapide, chaque seconde compte !")
        action = "Action : Récupère l'eau et appuie sur \"E\" face aux flammes pour les éteindre."

    elif map.niveau == 3:
        title = "♻️ Niveau 3 : Le Défi du Tri"
        objective = "Objectif : Nettoyer la nature et trier les déchets."
        story = ("Oh non ! Des déchets polluent notre belle forêt. Ramasse le plastique, le verre et le papier,\n"
                 "puis dépose-les dans le bac de la bonne couleur. Fais preuve de précision et de rapidité :\n"
                 "si tu te trompes, un conseil t'aidera à devenir un pro du recyclage !")
        action = "Action : Utilise la touche \"E\" pour ramasser et trier les déchets."

    elif map.niveau == 4:
        title = "👾 Niveau Final : Le Grand Combat"
        objective = "Objectif : Vaincre le Monstre de Pollution."
        story = ("Le Monstre de Pollution menace la Terre ! Évite ses nuages polluants et récupère les graines\n"
                 "qu'il projette. Utilise la puissance des graines pour le rendre vulnérable et le vaincre\n"
                 "pour de bon. Libère la nature et montre que nos actions peuvent tout changer !")
        action = "Action : Évite les trajectoires du boss et attaque-le avec les graines récupérées."

    else:
        title = "Niveau"
        objective = ""
        story = ""
        action = ""

    # Afficher le titre
    font_title = pygame.font.Font(None, 48)
    title_text = font_title.render(title, True, (100, 255, 100))
    screen.blit(title_text, (popup_x + 30, popup_y + 30))

    # Afficher l'objectif
    font_objective = pygame.font.Font(None, 32)
    objective_text = font_objective.render(objective, True, (255, 200, 100))
    screen.blit(objective_text, (popup_x + 30, popup_y + 90))

    # Afficher l'histoire
    font_story = pygame.font.Font(None, 24)
    y_offset = popup_y + 140
    for line in story.split('\n'):
        story_surface = font_story.render(line, True, (255, 255, 255))
        screen.blit(story_surface, (popup_x + 30, y_offset))
        y_offset += 35

    # Afficher l'action
    font_action = pygame.font.Font(None, 22)
    action_text = font_action.render(action, True, (200, 255, 200))
    screen.blit(action_text, (popup_x + 30, y_offset + 20))

    # Afficher "Clique pour commencer"
    font_click = pygame.font.Font(None, 28)
    click_text = font_click.render("Clique pour commencer", True, (255, 255, 0))
    screen.blit(click_text, (popup_x + popup_width // 2 - click_text.get_width() // 2, popup_y + popup_height - 50))

    # Si on clique, commencer le niveau
    if map.click:
        map.level_intro_active = False
        map.level_started = True

def gestion_timer(map, max_time): #max_time en seconde
    time = map.time/60
    timer_value = max_time - time
    if timer_value <= 0:
        timer_value = 0
    minutes = round(timer_value // 60)
    seconds = int(timer_value % 60)
    if seconds < 10:
        seconds = '0' + str(seconds)

    font = pygame.font.Font(None, 36)
    timer_text = f"{minutes}:{seconds}"
    text = font.render(timer_text, True, (255, 255, 255))
    map.screen.blit(text, (10, 70))

    if timer_value <= 0:
        return False
    else:
        return True
