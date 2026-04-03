import pygame
import random

# Constantes de jeu
GRAVITY = 800  # Valeur de 'g' dans l'équation
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class PollutionCloud(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy0):
        super().__init__()
        # Visuel du nuage
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (100, 100, 100), (15, 15), 15)  # Gris polluant
        self.rect = self.image.get_rect(center=(x, y))

        # Variables de position précises (float) pour éviter les erreurs d'arrondi
        self.pos_x = float(x)
        self.pos_y = float(y)

        # Vecteurs de vitesse
        self.vx = vx  # Vitesse horizontale constante
        self.vy = vy0  # Vitesse verticale initiale

    def update(self, dt):
        """
        Applique l'équation de mouvement :
        v_y = v_y0 + g * t  (la vitesse change avec le temps)
        y = y0 + v_y * t    (la position change avec la vitesse)
        """
        # 1. Mise à jour de la vitesse verticale (accélération par la gravité)
        self.vy += GRAVITY * dt

        # 2. Mise à jour des positions
        self.pos_x += self.vx * dt
        self.pos_y += self.vy * dt

        # 3. Application au rect de collision
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Supprimer si le nuage sort de l'écran
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0:
            self.kill()


class PollutionMonster:
    def __init__(self):
        self.hp = 10
        self.vulnerable = False
        self.clouds = pygame.sprite.Group()
        self.rect = pygame.Rect(700, 300, 80, 150)  # Position à droite

    def launch_cloud(self):
        """
        Génère un nuage avec une trajectoire parabolique aléatoire
        allant de la droite vers la gauche.
        """
        # Point de départ (bouche du monstre)
        origin_x = self.rect.left
        origin_y = self.rect.centery

        # vx négatif car on va vers la gauche (aléatoire entre -200 et -500)
        vx = random.uniform(-500, -200)

        # vy0 négatif pour lancer vers le haut au début (impulsion initiale)
        # aléatoire entre -400 et -700
        vy0 = random.uniform(-700, -400)

        # Création du projectile
        new_cloud = PollutionCloud(origin_x, origin_y, vx, vy0)
        self.clouds.add(new_cloud)

    def _check_cloud_hits(self, player):
        """Vérifie la collision entre les nuages et le joueur."""
        hits = pygame.sprite.spritecollide(player, self.clouds, True)
        for hit in hits:
            player.lose_life()