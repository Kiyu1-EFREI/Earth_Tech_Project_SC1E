import pygame
import random
import math
from Code.Utils.Utils import *

def element_lvl_3():
    element = {
        "platform": [
            [0, 70, 130, 1],
            [20, 55, 15, 1],
            [50, 45, 15, 1],
            [80, 35, 15, 1],
            [110, 25, 15, 1],
        ],
        "wall": [
            [0, 0, 1, 72],
            [129, 0, 1, 72],
            [-1, 0, 1, 72]
        ],
        "water_source": [
            [5, 69, 5, 1],
            [120, 69, 5, 1]
        ]
    }
    return element

def init_lvl_3(map):
    map.water = 50
    map.score = 0
    map.score_max = 15
    map.max_flammes = 8
    map.temps_restant = 60 * 60
    map.fumee = []
    map.flammes = []
    
    positions_flammes = [
        (300, 500),
        (500, 400),
        (700, 300),
        (900, 200),
    ]
    
    for pos in positions_flammes:
        flamme = ObjetClass(pygame.Rect(pos[0], pos[1], 30, 40), "fire")
        flamme.variable = {
            "intensite": random.randint(30, 50),
            "flicker": 1.0,
            "anim": random.randint(0, 10),
            "age": 0
        }
        flamme.visible = True
        flamme.color = (255, 100, 0)
        map.flammes.append(flamme)


#def utilisation_lvl_3(map, e):

def animer_flamme(map, vitesse):
    for f in map.flammes:
        if f.visible and f.variable["intensite"] > 0:
            flicker = random.uniform(0.8, 1.2)
            f.variable["flicker"] = flicker
            f.variable["anim"] = (f.variable["anim"] + vitesse) % 10

def animer_fumee(map):
    for f in map.fumee[:]:
        f.variable["vie"] -= 1
        f.rect.x += f.variable["vx"]
        f.rect.y += f.variable["vy"]
        
        if f.variable["vie"] <= 0:
            map.fumee.remove(f)

def update_timer_lvl_3(map):
    map.temps_restant -= 1
    if map.temps_restant <= 0:
        map.temps_restant = 0
        return True
    return False