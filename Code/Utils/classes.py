# Class pour stocker toute les varible pour le fonctionement de la map
class MapClass:
    def __init__(self, friction, vitesse_max, gravite, acceleration, screen, joueur):
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

# Classe pour gerer l'aleatoire
class AleatoireClass:
    def __init__(self, s, min, max):
        self.nb_s = s
        self.min = min
        self.max = max
        self.time = 0

# Classe pour cree les button
class ButtonClass:
    def __init__(self, rect, text, police , action, hover=(100, 100, 100), border_r = 8, color=(70, 130, 180), text_color=(255, 255, 255)):
        self.rect = rect
        self.text = text
        self.frame = []
        self.police  = police
        self.color = color
        self.hover = hover
        self.text_color = text_color
        self.action = action
        self.border_r = border_r