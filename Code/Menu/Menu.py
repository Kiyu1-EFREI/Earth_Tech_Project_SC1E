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
