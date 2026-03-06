import pygame


def grind(screen, size = 10, screen_size = (1280, 720)): # dev_tool
    for i in range(0, screen_size[0], size):
        for j in range(0, screen_size[1], size):
            if (i + j) % 20 == 0:
                color = (50, 0, 0)
            else:
                color = (0, 0, 50)
            pygame.draw.rect(screen,color, pygame.Rect(i, j, size, size))




def create_elements(el):
    rect = []
    for i in el["wall"]:
        rect.append({"rect": pygame.Rect(i[0]*10, i[1]*10, i[2]*10, i[3]*10), "type": "wall"})

    for i in el["platform"]:
        rect.append({"rect": pygame.Rect(i[0]*10, i[1]*10, 120, 20), "type": "platform"})

    return rect

def draw_element(screen, element, joueur, en_contact, direction, d_save, anim_index):
    pygame.draw.rect(screen, (0, 255, 100), joueur)
    for p in element:
        #if p["type"] == "platform":
            pygame.draw.rect(screen, (200, 200, 200), p["rect"])

def collision(joueur, plateformes, vy, vx, keys):
    en_contact = False
    for p in plateformes:
        if (joueur.colliderect(p["rect"]) and (p["type"] == "wall" or p["type"] == "platform") ) or (p["rect"].top - 1 <= joueur.bottom <= p["rect"].top + 1 and p["rect"].left <= joueur.right and joueur.left <= p["rect"].right):
            if vy > 0:
                if not(keys[pygame.K_DOWN] and p["type"] == "platform"):
                    if (joueur.bottom - vy) <= p["rect"].top:
                        joueur.bottom = p["rect"].top
                        vy = 0
                        en_contact = True
                    elif joueur.colliderect(p["rect"]):
                        if vx > 0:
                            joueur.right = p["rect"].left
                        elif vx < 0:
                            joueur.left = p["rect"].right
                        vx = 0
            elif vy < 0:
                if joueur.top >= p["rect"].bottom + vy - 1:
                    joueur.top = p["rect"].bottom
                    vy = 0
                elif joueur.colliderect(p["rect"]):
                    if vx > 0:
                        joueur.right = p["rect"].left
                    elif vx < 0:
                        joueur.left = p["rect"].right
                    vx = 0
            else:
                if vx > 0:
                    joueur.right = p["rect"].left
                elif vx < 0:
                    joueur.left = p["rect"].right
                vx = 0

    return en_contact, vy, vx

def mouvement(gravite, plateformes, friction, vitesse_max, joueur, acceleration, vx, vy):
    # Mouvement horizontal
    direction = 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        direction = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 1

    if direction != 0:
        vx += direction * acceleration
    else:
        vx *= friction

    if vx > vitesse_max:
        vx = vitesse_max
    if vx < -vitesse_max:
        vx = -vitesse_max
    if abs(vx) < 0.1:
        vx = 0

    # Physique verticale
    vy += gravite

    en_contact, vy, vx = collision(joueur, plateformes, vy, vx, keys)

    # changement de coordoné
    joueur.y += vy
    joueur.x += vx


    # Saut
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and en_contact:
        vy = -14

    return vx, vy, en_contact, direction







pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

joueur = pygame.Rect(160, 380, 50, 50)
vy = 0
vx = 0
anim_index = 0.0
gravite = 0.8
d_save = 1
acceleration = 0.8
friction = 0.7
vitesse_max = 7
delete = []

element = {
    "wall" : [
        [0, 70, 130, 3],
        [-1, 0, 1, 72],
        [128, 0, 1, 72],
        [0, 45, 30, 25]
    ],
    "platform" : [
        [89, 60], [45, 60], [67, 50], [60, 21], [107, 24], [48, 41], [25, 34], [6, 23], [33, 14], [78, 31], [96, 41]
    ]
}
hitbox = create_elements(element)
press_enter = False
press_del = False
run = True
while run:
    keys = pygame.key.get_pressed()
    screen.fill((30, 30, 30))
    grind(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # dev tool
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            case_x = x // 10  # même size que dans grind()
            case_y = y // 10
            print("Case cliquée : [", case_x, ',' , case_y,"]")
            if keys[pygame.K_c]:
                hitbox.append( {'rect': pygame.Rect(case_x*10, case_y*10, 120, 20), 'type': 'platform'} )
                element["platform"].append([case_x, case_y])

            if keys[pygame.K_a] and [case_x,case_y] in element["platform"]:
                delete.append([case_x, case_y])
                hitbox.remove({'rect': pygame.Rect(case_x*10, case_y*10, 120, 20), 'type': 'platform'})
                element["platform"].remove([case_x, case_y])


    if keys[pygame.K_RETURN] and not(press_enter):
        print(str(element["platform"])[1:-1])
        press_enter = True
    elif not(keys[pygame.K_RETURN]) and press_enter:
        press_enter = False

    if keys[pygame.K_z] and len(delete) > 0 and not(press_del):
        hitbox.append({'rect': pygame.Rect(delete[-1][0] * 10, delete[-1][1] * 10, 120, 20), 'type': 'platform'})
        element["platform"].append([delete[-1][0], delete[-1][1]])
        delete.pop(-1)
        press_del = True
    elif not(keys[pygame.K_z]) and press_del:
        press_del = False

    vx, vy, en_contact, direction = mouvement(gravite, hitbox, friction, vitesse_max, joueur, acceleration, vx, vy)
    if direction != 0:
        d_save = direction
        anim_index += 0.1
    else:
        anim_index = 0.0

    draw_element(screen, hitbox, joueur, en_contact, direction, d_save, anim_index)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print(str(element["platform"])[1:-1])