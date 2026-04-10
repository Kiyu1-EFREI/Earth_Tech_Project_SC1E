import pygame





# Class pour stocker toute les varible pour le fonctionement de la map





class MapClass:
    def __init__(self, friction, vitesse_max, gravite, acceleration, screen, joueur):
        self.time = 0
        self.reste_time = True
        self.time_start = 0
        self.keys = []
        self.aleatoire = AleatoireClass(1, 100, 2000)
        self.click = False
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.direction = 0
        self.d_save = 1
        self.friction = friction
        self.vitesse_max = vitesse_max
        self.gravite = gravite
        self.acceleration = acceleration
        self.element = []
        self.joueur = joueur
        self.en_contact = False
        self.interaction = False
        self.niveau = 0
        self.player_img = {1: {True : [], False : []},-1:{True : [], False : []}}
        self.water = 0
        self.water_tank = ''
        self.score = 0
        self.score_bare = ''
        self.seed = False
        self.oiseau = []
        self.fire = []
        self.press_e = False
        self.dechets = []
        self.dechet_transporte = None
        self.timer_apparition = 0
        self.intervalle_apparition = 120
        self.types_dechets = []
        self.couleurs_dechets = {}
        self.popup_active = False
        self.popup_timer = 0


# Class pour cree des element, avec ou sans animation, qui vont etre ou pas, afficher a l'ecran
class ObjetClass:
    def __init__(self, rect, type):
        self.rect = rect
        self.type = type
        self.frame = []
        self.anim_index = 0.0
        self.anim_speed = 0
        self.visible = True
        self.color = (100, 100, 100)
        self.variable = 0
        if type == "player":
            self.hp = 5
            self.max_hp = 5

# Classe pour gerer l'aleatoire
class AleatoireClass:
    def __init__(self, s, min, max):
        self.speed = 1
        self.nb_s = s
        self.min = min
        self.max = max
        self.time = 0

# Classe pour cree les button
class ButtonClass:
    def __init__(self, rect, text, police , action, hover="", border_r = 8, color=(70, 130, 180), text_color=(255, 255, 255)):
        self.rect = rect
        self.text = text
        self.police  = police
        self.color = color
        self.hover = hover
        self.text_color = text_color
        self.action = action
        self.border_r = border_r


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (50, 150, 255), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x, y))

        self.max_hp = 5
        self.hp = self.max_hp

        self.font = pygame.font.Font(None, 36)

    def lose_life(self, amount=1):
        """
        Retire des points de vie au joueur.
        """
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        """
        Renvoie True si le joueur n'a plus de vie.
        """
        return self.hp <= 0

    def draw_hp(self, surface):
        """
        Affiche la barre de vie du joueur à l'écran.
        """
        bar_x = 30
        bar_y = 70
        bar_w = 250
        bar_h = 20

        # Fond de barre
        pygame.draw.rect(surface, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h))

        # Vie restante
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (50, 200, 50), (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))

        # Contour
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)

        # Texte
        text = self.font.render(f"Vie du joueur : {self.hp}/{self.max_hp}", True, (255, 255, 255))
        surface.blit(text, (bar_x, bar_y + 28))