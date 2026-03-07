import pygame

#Fonction qui gere les animations du sprite

def player_animation(map):
    if map.d_save == 1:
        side = "player_right"
    else:
        side = "player_left"

    if map.en_contact:
        if map.direction == 0:
            frame = 1
        else:
            frame = int(map.anim_index)%4 + 1

    else:
        frame = 0

    x, y = map.joueur.x, map.joueur.y
    map.screen.blit(map.player_image[side][frame], (x, y))




