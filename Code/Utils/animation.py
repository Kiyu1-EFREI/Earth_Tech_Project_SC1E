import pygame

def player_animation(screen, en_contact, d_save, joueur, direction, anim_index):
    player_right = [
        pygame.image.load("./Textures/player/player_right_1.png"),
        pygame.image.load("./Textures/player/player_right_2.png"),
        pygame.image.load("./Textures/player/player_right_3.png"),
        pygame.image.load("./Textures/player/player_right_4.png")
    ]

    player_left = [
        pygame.image.load("./Textures/player/player_left_1.png"),
        pygame.image.load("./Textures/player/player_left_2.png"),
        pygame.image.load("./Textures/player/player_left_3.png"),
        pygame.image.load("./Textures/player/player_left_4.png")
    ]

    if en_contact:
        if d_save == 1 :
            frames = player_right
        else:
            frames = player_left

        if direction == 0:
            image = frames[0]
        else:
            image = frames[int(anim_index)%4]

    else:
        if d_save == 1 :
            image = pygame.image.load("./Textures/player/player_right_jump.png")
        else:
            image = pygame.image.load("./Textures/player/player_left_jump.png")

    x, y = joueur.x, joueur.y
    player_image = pygame.transform.scale(image, (40, 40))
    player_rect = player_image.get_rect(center=(x+20, y+20))
    screen.blit(player_image, player_rect)




