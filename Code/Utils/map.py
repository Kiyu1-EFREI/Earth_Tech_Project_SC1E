from Code.Niveaux.Niveau_1 import*
from Code.Niveaux.Niveau_2 import*
from Code.Niveaux.Niveau_3 import*
from Code.Niveaux.Niveau_4 import*
from Code.Niveaux.Niveau_4 import init_lvl_4, SCREEN_WIDTH, SCREEN_HEIGHT
from .Utils import*
from .classes import*



# fontion pour gerer les colisions avec les objets
def collision(map, p):
    if (map.joueur.rect.colliderect(p.rect) or (p.rect.top - 1 <= map.joueur.rect.bottom <= p.rect.top + 1 and p.rect.left <= map.joueur.rect.right and map.joueur.rect.left <= p.rect.right)) and (p.type == "wall" or p.type == "platform"):
        #vertical
        if map.vy > 0 and (map.joueur.rect.bottom - map.vy) <= p.rect.top:
            map.joueur.rect.bottom = p.rect.top
            map.vy = 0
            map.en_contact = True
        elif map.vy < 0 and map.joueur.rect.top >= p.rect.bottom + map.vy - 1:
            map.joueur.rect.top = p.rect.bottom
            map.vy = 0

        # horizontal
        elif map.joueur.rect.left < p.rect.right and (abs(map.joueur.rect.left - p.rect.right) < 15):
            map.joueur.rect.left = p.rect.right
        elif map.joueur.rect.right > p.rect.left and (abs(map.joueur.rect.right - p.rect.left) < 15):
             map.joueur.rect.right = p.rect.left

# Fonction pour gérer les interaction/utilisation avec la touche E
def utilisation(map, e):
    if map.joueur.rect.colliderect(e.rect):
        if e.type == "water" and map.niveau != 3 and map.water < 100:
            gestion_eau(map, 2)
        elif e.type == "water_source" and map.niveau == 3 and map.water < 100:
            gestion_eau(map, 20)

        if map.niveau == 1:
            utilisation_lvl_1(map, e)
        elif map.niveau == 2:
            utilisation_lvl_2(map, e)
        elif map.niveau == 3:
            utilisation_lvl_3(map, e)
        elif map.niveau == 4:
            utilisation_lvl_4(map, e)

def utilisation_lvl_4(map, e):
    # Pour le niveau 4, les interactions sont gérées dans run_map
    pass


# Fonction qui rassemble la gest des colision et les interaction pour eviter des boucle similaire
def interaction(map):
    map.en_contact = False
    for e in map.element[1:] + map.oiseau + map.fire + map.dechets:
        collision(map, e)
        if map.keys[pygame.K_e]:
            utilisation(map, e)

# fonction pour gerer touts les mouvements du joueur
def mouvement(map):
    # changement de coordoné
    map.joueur.rect.y += map.vy
    map.joueur.rect.x += map.vx

    # Mouvement horizontal
    map.direction = 0

    if map.keys[pygame.K_LEFT] or map.keys[pygame.K_q]:
        map.direction = -1
    if map.keys[pygame.K_RIGHT] or map.keys[pygame.K_d]:
        map.direction += 1

    if map.direction != 0:
        map.vx += map.direction * map.acceleration
    else:
        map.vx *= map.friction

    if map.vx > map.vitesse_max:
        map.vx = map.vitesse_max
    if map.vx < -map.vitesse_max:
        map.vx = -map.vitesse_max
    if abs(map.vx) < 0.1:
        map.vx = 0

    # Physique verticale
    map.vy += map.gravite

    # Saut
    if (map.keys[pygame.K_SPACE] or map.keys[pygame.K_UP]) and map.en_contact:
        map.vy = -14

# fonction qui permet de faire tourner la map
def run_map(map):
    map.keys = pygame.key.get_pressed()
    map.aleatoire.time += map.aleatoire.speed
    map.time += 1

    # Afficher l'introduction du niveau
    draw_level_intro(map.screen, map)

    # Si l'intro est active, ne pas faire le gameplay
    if map.level_intro_active:
        return


    mouvement(map)
    interaction(map)

    if map.direction != 0:
        map.d_save = map.direction
    else:
        map.joueur.anim_index = 0.0

    map.joueur.frame = map.player_img[map.d_save][map.en_contact]
    draw_list = map.element + map.oiseau + map.fire + map.dechets + [map.water_tube, map.score_bare, map.joueur]
    if hasattr(map, 'pollution_bare'):
        draw_list.append(map.pollution_bare)
    draw_element(map.screen, draw_list)

    if (map.niveau == 1 or map.niveau == 4) and getattr(map, 'seed_box', None) is not None:
        pygame.draw.rect(map.screen, (30, 30, 30), map.seed_box)
        pygame.draw.rect(map.screen, (255, 255, 255), map.seed_box, 3, border_radius=8)
        if map.seed and map.niveau == 1:
            img_path = "./Asset/maps/graine.png"
            img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (40, 40))
            map.screen.blit(img, (map.seed_box.x + 5, map.seed_box.y + 5))
        elif map.seed and map.niveau == 4:
            img_path = "./Asset/maps/graine_magique.png"
            img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (40, 40))
            map.screen.blit(img, (map.seed_box.x + 5, map.seed_box.y + 5))

    # Afficher le popup si actif
    draw_popup(map.screen, map)
    # Afficher la défaite si active
    draw_defeat(map.screen, map)
    # Afficher la victoire si active
    draw_victory(map.screen, map)
    # Si défaite est active, arrêter le gameplay
    if getattr(map, 'defeat_active', False) or getattr(map, 'victory', False):
        return


    if map.niveau == 3:
        font = pygame.font.Font(None, 36)
        score_text = f"Déchets déposés: {map.score}"
        text = font.render(score_text, True, (255, 255, 255))
        map.screen.blit(text, (10, 70))

        x_pos = 10
        y_pos = 100
        if hasattr(map.joueur, 'inventory'):
            for type_dechet, count in map.joueur.inventory.items():
                if count > 0:
                    img_path = f"./Asset/maps/dechet_{type_dechet}.png"
                    img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (50, 50))
                    map.screen.blit(img, (x_pos, y_pos))
                    x_pos += 60

    if map.keys[pygame.K_e]:
        map.press_e = True
    else:
        map.press_e = False

    if map.niveau == 1:
        avancer_oiseau(map, 2)
    elif map.niveau == 2:
        generation_fire(map)
        gestion_score_bare(map, (map.score * 100)/15)
        map.reste_time = gestion_timer(map, map.time_start)
    elif map.niveau == 3:
        update_lvl_3(map)
        gestion_pollution_bare(map)
        gestion_score_bare(map, (map.score * 100) / 10)
    elif map.niveau == 4:
        dt = 1 / 60  # Assuming 60 FPS
        if not map.game_over and not map.victory:
            map.boss.update(dt, map.joueur)

        # Check seed pickup
        if map.press_e and not map.seed:
            seed_hits = pygame.sprite.spritecollide(map.joueur, map.boss.seeds, True)
            if seed_hits:
                map.seed = True

        # Check attack on boss
        if map.keys[pygame.K_e] and map.joueur.rect.colliderect(map.boss.rect) and map.seed:
            map.boss.become_vulnerable()
            map.boss.take_damage(1)
            map.seed = False

        # Draw boss
        map.boss.draw(map.screen)

        # Draw player HP
        font = pygame.font.Font(None, 36)
        hp_text = f"HP: {map.joueur.hp}/{map.joueur.max_hp}"
        text = font.render(hp_text, True, (255, 255, 255))
        map.screen.blit(text, (10, 10))

        # Check win condition
        if not map.boss.alive and not map.victory:
            map.victory = True

        # Check game over
        if map.joueur.hp <= 0 and not map.game_over:
            map.game_over = True
            map.defeat_active = True
        




# fonction pour initialiser la map
def init_map(niveau, screen, EOTF_list):
    if niveau == 1:
        element_lvl = element_lvl_1()
    elif niveau == 2:
        element_lvl = {}
    elif niveau == 3:
        element_lvl = element_lvl_3()
    elif niveau == 4:
        element_lvl = element_lvl_4()
    else:
        element_lvl = element_lvl_1()

    element = element_map_general() | element_lvl

    joueur = ObjetClass(pygame.Rect(160, 380, 50, 50), "player")
    map = MapClass(0.7, 7, 0.8, 0.8, screen, joueur)
    map.vx = 0
    map.vy = 0
    map.direction = 0
    map.d_save = 1
    map.niveau = niveau
    if niveau == 1:
        map.element = create_element(element, niveau, "maps/ciel_background.png")
    else:
        map.element = create_element(element, niveau, "maps/forest_background.png")

    map.joueur.anim_speed = 0.2
    map.player_img[1][True] = [
        pygame.transform.scale(pygame.image.load("./Asset/player/player_right_1.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_right_2.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_right_3.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_right_4.png").convert_alpha(), (50, 50))
    ]
    map.player_img[-1][True] = [
        pygame.transform.scale(pygame.image.load("./Asset/player/player_left_1.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_left_2.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_left_3.png").convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Asset/player/player_left_4.png").convert_alpha(), (50, 50))
    ]

    map.player_img[1][False] = [pygame.transform.scale(pygame.image.load("./Asset/player/player_right_jump.png").convert_alpha(), (50, 50))]
    map.player_img[-1][False] = [pygame.transform.scale(pygame.image.load("./Asset/player/player_left_jump.png").convert_alpha(), (50, 50))]

    map.water_tube = ObjetClass(pygame.Rect(15, 530, 65, 120), "water_tube")
    map.water_tube.color = (255, 255, 255)
    map.water_tube.variable = 0

    map.score_bare = ObjetClass(pygame.Rect(10, 10, 0, 25), "score_bare")
    map.score_bare.color = (0, 0, 0)

    if niveau == 1 or niveau == 4:
        map.seed_box = pygame.Rect(15, 660, 50, 50)
    else:
        map.seed_box = None

    if niveau == 4:
        map.water_tube.visible = False
    elif niveau == 1:
        map.score_bare.visible = False

    if niveau == 1:
        init_lvl_1(map)
    elif niveau == 2:
        init_lvl_2(map)
    elif niveau == 3:
        init_lvl_3(map)
    elif niveau == 4:
        init_lvl_4(map)
        map.background_elements = map.element

    map_upgrade_applid(map, EOTF_list)

    return map

# fonction resize map
def map_resize(map, screen_width, screen_height, old_w, old_h):
    resize(map.element[1:], screen_width, screen_height, old_w, old_h)
    resize(map.oiseau, screen_width, screen_height, old_w, old_h)
    resize(map.fire, screen_width, screen_height, old_w, old_h)
    resize(map.joueur, screen_width, screen_height, old_w, old_h)

def map_upgrade_applid(map, EOTF_list):
    if EOTF_list[0]:
        map.vitesse_max = 12
    if EOTF_list[1]:
        map.friction = 0.99
    if EOTF_list[2]:
        map.time_start *= 2