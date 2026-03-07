from .animation import *
import pygame

def draw_element(screen, element, classe, bg = '0'): # element = [{'rect': <rect(0, 700, 1300, 30)>, 'type': 'wall'}, {'rect': <rect(-10, 0, 10, 720)>, 'type': 'wall'}]
    if bg != '0':
        screen.blit(bg, (0, 0))

    else:
        screen.fill((30, 30, 30))


    for el in element:
        if el["type"] == "platform":
            screen.blit(classe.platform_img, el["rect"].topleft)
            #pygame.draw.rect(screen, (200, 200, 200), el["rect"])
        elif el["type"] == "water":
            pygame.draw.rect(screen, (0, 0, 255), el["rect"])
        elif el["type"] == "wall":
            pygame.draw.rect(screen, (100, 100, 100), el["rect"])
        elif el["type"] == "player":
            pygame.draw.rect(screen, (0, 255, 100), el["rect"])
            player_animation(classe)

def create_element(element): # element = "player" : [[160, 380, 50, 50]], "wall" : [[0, 70, 140, 3], [-1, 0, 1, 72]]
    rect = []

    for key, val in element.items():
        for i in val:
            if key != 'platform':
                rect.append({"rect": pygame.Rect(i[0]*10, i[1]*10, i[2]*10, i[3]*10), "type": key})
            else:
                rect.append({"rect": pygame.Rect(i[0]*10, i[1]*10, 120, 20), "type": "platform"})

    return rect

def interagir(events, joueur_rect, objets_interactifs):
    touche_e_pressee = False
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            touche_e_pressee = True 
            break
    if not touche_e_pressee:
        return 0
