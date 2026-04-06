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



# Fonction pour obtenir les éléments du niveau 4
def element_lvl_4():
    element = {
        "boss": [[1050, 150, 140, 140]]
    }
    return element

# Fonction pour initialiser le niveau 4
def init_lvl_4(map):
    # Créer le boss avec son image
    map.boss = ObjetClass(pygame.Rect(1050, 150, 140, 140), "boss")

    # Charger l'image du boss
    try:
        boss_img = pygame.image.load("./Asset/maps/boss.png").convert_alpha()
        boss_img = pygame.transform.scale(boss_img, (140, 140))
        map.boss.frame = [boss_img]
    except:
        # Si l'image n'existe pas, afficher un carré gris en attente
        map.boss.color = (60, 60, 60)

    map.boss.hp = 5
    map.boss.max_hp = 5

# Fonction pour gérer les interactions du niveau 4
def utilisation_lvl_4(map, e):
    if e.type == "boss" and map.water > 0:
        gestion_eau(map, -1)
        map.boss.hp -= 1
        if map.boss.hp <= 0:
            map.score += 1
            e.visible = False
