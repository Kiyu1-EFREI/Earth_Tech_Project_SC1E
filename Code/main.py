from Utils.Utils import*
import pygame

pygame.init()
MIN_W, MIN_H = 1240, 700
screen = pygame.display.set_mode((MIN_W, MIN_H), pygame.RESIZABLE)
clock = pygame.time.Clock()

joueur = pygame.Rect(100, 100, 40, 40)
vy = 0
vx = 0
anim_index = 0.0
gravite = 0.8
d_save = 1
acceleration = 0.8
friction = 0.7
vitesse_max = 7

element = {
    "wall" : [
        [0, 600, 1300, 30],
        [0, 450, 300, 30]

    ],
    "platform" : [
        [150, 350],
        [450, 250]
    ]
}
hitbox = create_elements(element)

run = True
while run:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            nouvelle_largeur = max(event.w,MIN_W)
            nouvelle_hauteur = max(event.h,MIN_H)
            screen = pygame.display.set_mode((nouvelle_largeur, nouvelle_hauteur), pygame.RESIZABLE)

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