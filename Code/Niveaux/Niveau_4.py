import pygame
import random
from Code.Utils.Utils import create_element, gestion_eau
from Code.Utils.classes import Player, ObjetClass
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
class MagicSeed(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy0, platforms=None):
        super().__init__()
        # Visuel de la graine
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (50, 200, 50), (10, 10), 10)  # Vert magique
        self.rect = self.image.get_rect(center=(x, y))

        # Variables de position précises (float)
        self.pos_x = float(x)
        self.pos_y = float(y)

        # Vecteurs de vitesse
        self.vx = vx
        self.vy = vy0

        self.on_ground = False
        self.platforms = platforms if platforms else []

    def check_platform_collision(self):
        """
        Vérifie la collision avec les plateformes et le sol.
        """
        # Vérifier collision avec le sol
        if self.pos_y >= GROUND_Y - self.rect.height // 2:
            return True

        # Vérifier collision avec les plateformes
        for platform in self.platforms:
            plat_rect = pygame.Rect(platform['rect'])
            if self.rect.colliderect(plat_rect) and self.vy >= 0:
                # Vérifier si la graine tombe sur la plateforme (par le haut)
                if self.pos_y + self.rect.height // 2 >= plat_rect.top and self.pos_y - self.rect.height // 2 <= plat_rect.top:
                    return True

        return False

    def update(self, dt):
        """
        Trajectoire parabolique pour la graine.
        """
        if not self.on_ground:
            self.vy += GRAVITY * dt
            self.pos_x += self.vx * dt
            self.pos_y += self.vy * dt

            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)

            if self.check_platform_collision():
                self.pos_y = GROUND_Y - self.rect.height // 2
                self.vx = 0
                self.vy = 0
                self.on_ground = True


class MonstrePollution(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms=None):
        super().__init__()
        self.image = pygame.Surface((140, 140), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (60, 60, 60), (70, 70), 70)
        self.rect = self.image.get_rect(center=(x, y))

        self.clouds = pygame.sprite.Group()
        self.seeds = pygame.sprite.Group()

        self.max_hp = 7
        self.hp = self.max_hp
        self.vulnerable = False
        self.alive = True

        self.font = pygame.font.Font(None, 36)

        # cadence de tir
        self.fire_interval = 3.0
        self.fire_timer = 0.0

        # paramètres de tir
        self.min_flight_time = 3.0
        self.max_flight_time = 5.0

        # Timer pour la graine magique (aléatoire autour de 15 secondes)
        self.seed_timer = 0.0
        self.seed_interval = random.uniform(12, 18)

        # Stocker les plateformes pour les collisions des graines
        self.platforms = platforms if platforms else []

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

    def launch_seed(self):
        """
        Lance une graine magique avec une trajectoire parabolique aléatoire sur la map.
        """
        origin_x = self.rect.centerx
        origin_y = self.rect.centery

        # Point cible aléatoire sur la map - entre les limites (respecter les murs à x = -1 et x = 128 en unités)
        # Convertir à pixels: -1 * 10 = -10 et 128 * 10 = 1280
        # Lancer la graine entre 0 et 1280 (entre les murs)
        target_x = random.randint(20, 1260)
        target_y = random.randint(100, GROUND_Y - 100)

        dx = target_x - origin_x
        dy = target_y - origin_y

        flight_time = random.uniform(1.5, 3.0)

        vx = dx / flight_time
        vy0 = (dy - 0.5 * GRAVITY * (flight_time ** 2)) / flight_time

        new_seed = MagicSeed(origin_x, origin_y, vx, vy0, platforms=self.platforms)
        self.seeds.add(new_seed)

    def update(self, dt, player):
        """
        Chef d'orchestre du boss :
        - cadence de tir
        - mise à jour des nuages
        - collisions nuages / joueur
        - timer pour la graine
        """
        if not self.alive:
            return

        self.fire_timer += dt
        if self.fire_timer >= self.fire_interval:
            self.fire_timer = 0.0
            self.launch_cloud(player=player)

        self.seed_timer += dt
        if self.seed_timer >= self.seed_interval:
            self.seed_timer = 0.0
            self.seed_interval = random.uniform(12, 18)  # Reset timer aléatoire
            self.launch_seed()

        self.clouds.update(dt)
        self.seeds.update(dt)

        if player is not None:
            self._check_cloud_hits(player)

    def _check_cloud_hits(self, player):
        """
        Vérifie la collision entre les nuages et le joueur.
        Si collision, le joueur perd une vie.
        """
        hits = pygame.sprite.spritecollide(player, self.clouds, True)
        for _hit in hits:
            player.hp -= 1

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
        self.seeds.draw(surface)
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
        - vide les nuages et graines
        - désactive le boss
        - prépare l'animation de victoire
        """
        self.alive = False
        self.clouds.empty()
        self.seeds.empty()



# Fonction pour obtenir les éléments du niveau 4
def element_lvl_4():
    element = {
        "boss": [[96, 1, 30, 25]]
    }
    return element

# Fonction pour initialiser le niveau 4
def init_lvl_4(map):
    # Créer la liste des plateformes pour les collisions des graines
    platforms = [
        {'rect': pygame.Rect(89*10, 60*10, 12*10, 2*10)},
        {'rect': pygame.Rect(45*10, 60*10, 12*10, 2*10)},
        {'rect': pygame.Rect(67*10, 50*10, 12*10, 2*10)},
        {'rect': pygame.Rect(60*10, 21*10, 12*10, 2*10)},
        {'rect': pygame.Rect(107*10, 24*10, 12*10, 2*10)},
        {'rect': pygame.Rect(48*10, 41*10, 12*10, 2*10)},
        {'rect': pygame.Rect(25*10, 34*10, 12*10, 2*10)},
        {'rect': pygame.Rect(6*10, 23*10, 12*10, 2*10)},
        {'rect': pygame.Rect(33*10, 14*10, 12*10, 2*10)},
        {'rect': pygame.Rect(78*10, 31*10, 12*10, 2*10)},
        {'rect': pygame.Rect(96*10, 41*10, 12*10, 2*10)}
    ]
    # Créer le boss avec la classe MonstrePollution
    map.boss = MonstrePollution(1050, 150, platforms=platforms)
    map.joueur.hp = 5
    map.joueur.max_hp = 5
    map.game_over = False
    map.victory = False
