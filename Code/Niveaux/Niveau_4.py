import pygame
import random

from Code.Utils.Utils import create_element
from Code.Utils.classes import Player
# Constantes de jeu
GRAVITY = 800  # Valeur de 'g' dans l'équation
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_HEIGHT = 80
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

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


class MonstrePollution(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((140, 140), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (60, 60, 60), (70, 70), 70)
        self.rect = self.image.get_rect(center=(x, y))

        self.clouds = pygame.sprite.Group()

        self.max_hp = 5
        self.hp = self.max_hp
        self.vulnerable = False
        self.alive = True

        self.font = pygame.font.Font(None, 36)

        # cadence de tir
        self.fire_interval = 1.2
        self.fire_timer = 0.0

        # paramètres de tir
        self.min_flight_time = 0.8
        self.max_flight_time = 1.6

    def choose_target_point(self, player):
        """
        Choisit un point approximatif vers lequel tirer.
        On vise généralement autour du centre du joueur avec un léger décalage.
        """
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-20, 30)
        return player.rect.centerx + offset_x, player.rect.centery + offset_y

    def launch_cloud(self, origin_x=None, origin_y=None, player=None):
        """
        Génère un nuage avec une trajectoire parabolique visant approximativement le joueur.
        Le tir part du boss et suit une vitesse initiale calculée pour atteindre la cible.
        """
        if origin_x is None:
            origin_x = self.rect.left
        if origin_y is None:
            origin_y = self.rect.centery

        if player is None:
            # Tir aléatoire si aucun joueur n'est fourni
            vx = random.uniform(-500, -200)
            vy0 = random.uniform(-700, -400)
        else:
            target_x, target_y = self.choose_target_point(player)

            dx = target_x - origin_x
            dy = target_y - origin_y

            # Temps de vol choisi dans une plage raisonnable
            flight_time = random.uniform(self.min_flight_time, self.max_flight_time)

            # Calcul des vitesses initiales pour atteindre à peu près la cible
            vx = dx / flight_time
            vy0 = (dy - 0.5 * GRAVITY * (flight_time ** 2)) / flight_time

            # Petite variation pour éviter des tirs trop parfaits
            vx += random.uniform(-40, 40)
            vy0 += random.uniform(-40, 40)

        new_cloud = PollutionCloud(origin_x, origin_y, vx, vy0)
        self.clouds.add(new_cloud)

    def update(self, dt, player):
        """
        Chef d'orchestre du boss :
        - cadence de tir
        - mise à jour des nuages
        - collisions nuages / joueur
        """
        if not self.alive:
            return

        self.fire_timer += dt
        if self.fire_timer >= self.fire_interval:
            self.fire_timer = 0.0
            self.launch_cloud(player=player)

        self.clouds.update(dt)

        if player is not None:
            self._check_cloud_hits(player)

    def _check_cloud_hits(self, player):
        """
        Vérifie la collision entre les nuages et le joueur.
        Si collision, le joueur perd une vie.
        """
        hits = pygame.sprite.spritecollide(player, self.clouds, True)
        for _hit in hits:
            player.lose_life()

    def draw_hp_bar(self, surface):
        """
        Affiche la barre de vie du boss.
        """
        bar_x = 30
        bar_y = 30
        bar_w = 300
        bar_h = 25

        # Fond
        pygame.draw.rect(surface, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h))
        # Vie restante
        hp_ratio = max(self.hp, 0) / self.max_hp
        pygame.draw.rect(surface, (180, 50, 50), (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
        # Contour
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)

        text = self.font.render(f"Monstre de Pollution: {self.hp}/{self.max_hp}", True, (255, 255, 255))
        surface.blit(text, (bar_x, bar_y + 32))

    def draw(self, surface):
        """
        Affiche le boss, les nuages et la barre de vie.
        """
        if self.alive:
            surface.blit(self.image, self.rect)
        self.clouds.draw(surface)
        self.draw_hp_bar(surface)

    def become_vulnerable(self):
        """
        Le boss devient vulnérable quand une graine pousse près de lui.
        """
        if self.alive:
            self.vulnerable = True

    def take_damage(self, amount):
        """
        Le boss ne perd de la vie que s'il est vulnérable.
        """
        if not self.alive:
            return

        if self.vulnerable:
            self.hp -= amount
            self.vulnerable = False

            if self.hp <= 0:
                self.die()

    def _reset_vulnerability(self):
        """
        Le boss redevient invulnérable après avoir été touché.
        """
        self.vulnerable = False

    def die(self):
        """
        Déclenche la fin du combat :
        - vide les nuages
        - désactive le boss
        - prépare l'animation de victoire
        """
        self.alive = False
        self.clouds.empty()

class Level4:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(
            pygame.image.load("./Asset/maps/forest_background.png").convert(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.player = Player(120, GROUND_Y - 60)
        self.player.vy = 0
        self.player.on_ground = True

        self.boss = MonstrePollution(1050, 250)
        self.level_finished = False
        self.victory = False
        self.game_over = False
        self.font = pygame.font.Font(None, 72)

        self.player_speed = 300
        self.jump_speed = 430
        self.player_vy = 0.0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_over = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.boss.become_vulnerable()
                self.boss.take_damage(1)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        speed = 300
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.player.rect.x -= int(speed * dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.rect.x += int(speed * dt)
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.player.rect.y -= int(speed * dt)

        self.player.rect.x = max(0, min(SCREEN_WIDTH - self.player.rect.width, self.player.rect.x))
        self.player.rect.y = max(0, min(SCREEN_HEIGHT - self.player.rect.height, self.player.rect.y))

        self.boss.update(dt, self.player)

        if self.player.is_dead():
            self.game_over = True

        if not self.boss.alive:
            self.level_finished = True
            self.victory = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, (90, 160, 80), (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))

        self.screen.blit(self.player.image, self.player.rect)
        self.player.draw_hp(self.screen)
        self.boss.draw(self.screen)

        if self.game_over and not self.victory:
            text = self.font.render("GAME OVER", True, (255, 50, 50))
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if self.victory:
            text = self.font.render("VICTOIRE !", True, (50, 255, 50))
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))


def init_lvl_4(screen):
    return Level4(screen)


