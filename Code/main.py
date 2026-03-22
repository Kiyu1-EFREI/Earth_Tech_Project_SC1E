from Utils.map import*
import pygame

# structure pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

niveau = 1
if niveau == 1:
    element_lvl = element_lvl_1()
elif niveau == 2:
    element_lvl = {}
elif niveau == 3:
    element_lvl = element_lvl_1()
else:
    element_lvl = element_lvl_1()

element = element_map_general() | element_lvl
map = init_map(niveau,screen)



# Boucle principale de Pygame
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    run_map(map)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()