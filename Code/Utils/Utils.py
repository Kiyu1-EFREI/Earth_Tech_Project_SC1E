from .animation import *
import pygame

def create_elements(el):
    rect = []
    for i in el["wall"]:
        rect.append({"rect": pygame.Rect(i[0], i[1], i[2], i[3]), "type": "wall"})

    for i in el["platform"]:
        rect.append({"rect": pygame.Rect(i[0], i[1], 200, 20), "type": "platform"})

    return rect

def draw_element(screen, element, joueur, en_contact, direction, d_save, anim_index):
    pygame.draw.rect(screen, (0, 255, 100), joueur)
    player_animation(screen, en_contact, d_save, joueur, direction, anim_index)
    for p in element:
        #if p["type"] == "platform":
            pygame.draw.rect(screen, (200, 200, 200), p["rect"]) # Plateformes


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
        vy = -16

    return vx, vy, en_contact, direction

