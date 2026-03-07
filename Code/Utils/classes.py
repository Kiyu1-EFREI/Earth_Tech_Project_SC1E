# Création d'une classe pour contenir toutes les variables qui sont ultilisés par le moteur physique du jeu

class MapClass:
    def __init__(self, friction, vitesse_max, gravite, acceleration, element, screen, joueur):
        self.keys = []
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.direction = 0
        self.d_save = 1
        self.anim_index = 0.0
        self.friction = friction
        self.vitesse_max = vitesse_max
        self.gravite = gravite
        self.acceleration = acceleration
        self.element = element
        self.hitbox = []
        self.joueur = joueur
        self.en_contact = False
        self.niveau = 0
        self.platform_img = ''
        self.bg_img = ''
        self.player_image = {"player_right" : [], "player_left" : []}
