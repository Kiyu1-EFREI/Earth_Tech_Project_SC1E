import pygame
pygame.init()

pygame.display.set_caption("Forest Frontiers")
screen = pygame.display.set_mode((1530,795))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermer")


def collision(map, p):
    if (map.joueur.colliderect(p["rect"]) and (p["type"] == "wall" or p["type"] == "platform")) or (p["rect"].top - 1 <= map.joueur.bottom <= p["rect"].top + 1 and p["rect"].left <= map.joueur.right and map.joueur.left <= p["rect"].right):
        if map.vy > 0:
            if (map.joueur.bottom - map.vy) <= p["rect"].top:
                map.joueur.bottom = p["rect"].top
                map.vy = 0
                map.en_contact = True
            elif map.joueur.colliderect(p["rect"]):
                if map.vx > 0:
                    map.joueur.right = p["rect"].left
                elif map.vx < 0:
                    map.joueur.left = p["rect"].right
                map.vx = 0
        elif map.vy < 0:
            if map.joueur.top >= p["rect"].bottom + map.vy - 1:
                map.joueur.top = p["rect"].bottom
                map.vy = 0
            elif map.joueur.colliderect(p["rect"]):
                if map.vx > 0:
                    map.joueur.right = p["rect"].left
                elif map.vx < 0:
                    map.joueur.left = p["rect"].right
                map.vx = 0
        else:
            if map.vx > 0:
                map.joueur.right = p["rect"].left
            elif map.vx < 0:
                map.joueur.left = p["rect"].right
            map.vx = 0