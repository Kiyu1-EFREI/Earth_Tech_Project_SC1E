from .Utils import*

def collision(map, p):
    if (map.joueur.colliderect(p["rect"]) and (p["type"] == "wall" or p["type"] == "platform")) or (p["rect"].top - 1 <= map.joueur.bottom <= p["rect"].top + 1 and p["rect"].left <= map.joueur.right and map.joueur.left <= p["rect"].right):
        if map.vy > 0 and (map.joueur.bottom - map.vy) <= p["rect"].top:
            map.joueur.bottom = p["rect"].top
            map.vy = 0
            map.en_contact = True
        elif map.vy < 0 and map.joueur.top >= p["rect"].bottom + map.vy - 1:
            map.joueur.top = p["rect"].bottom
            map.vy = 0

        elif map.joueur.left < p["rect"].right and (abs(map.joueur.left - p["rect"].right) < 15):
            map.joueur.left = p["rect"].right
        elif map.joueur.right > p["rect"].left and (abs(map.joueur.right - p["rect"].left) < 15):
             map.joueur.right = p["rect"].left

def interaction(map):
    map.en_contact = False
    for p in map.hitbox:
        collision(map, p)

        if map.joueur.colliderect(p["rect"]) and p["type"] == "water" and map.keys[pygame.K_e]:
            print("water !")

def mouvement(map):
    # changement de coordoné
    map.joueur.y += map.vy
    map.joueur.x += map.vx

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

def run_map(map):
    map.keys = pygame.key.get_pressed()

    mouvement(map)
    interaction(map)

    if map.direction != 0:
        map.d_save = map.direction
        map.anim_index += 0.3
    else:
        map.anim_index = 0.0

    draw_element(map.screen, map.hitbox+[{"rect":map.joueur, "type":"player"}], map, map.bg_img)


def init_map(map, niveau):
    map.vx = 0
    map.vy = 0
    map.direction = 0
    map.d_save = 1
    map.hitbox = create_element(map.element)
    map.niveau = niveau

    if niveau == 1:
        p_img = 'ciel_platform.png'
        bg_img = 'ciel_background.png'
    else:
        p_img = 'forest_platform.png'
        bg_img = 'forest_background.png'
    map.platform_img = pygame.transform.scale(pygame.image.load("./Textures/maps/" + p_img).convert_alpha(), (120, 20))
    map.bg_img = pygame.transform.scale(pygame.image.load("./Textures/maps/" + bg_img).convert(), (1280, 720))


    map.player_image["player_right"] = [
        pygame.transform.scale(pygame.image.load("./Textures/player/player_right_jump.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_right_1.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_right_2.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_right_3.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_right_4.png"), (50, 50))
    ]

    map.player_image["player_left"] = [
        pygame.transform.scale(pygame.image.load("./Textures/player/player_left_jump.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_left_1.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_left_2.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_left_3.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("./Textures/player/player_left_4.png"), (50, 50))
    ]


