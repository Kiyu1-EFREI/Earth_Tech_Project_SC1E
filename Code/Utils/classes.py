# Class pour stocker toute les varible pour le fonctionement de la map
class MapClass:
    def __init__(self, friction, vitesse_max, gravite, acceleration, screen, joueur):
        self.keys = []
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
        self.flammes = []
        self.fumee = []
        self.temps_restant = []
        self.score_max = 0
        self.max_flammes = 0

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