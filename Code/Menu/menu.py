from .niveau_menu import init_lvl_menu
from .earth_of_the_forest_menu import init_EOTF_menu
from .main_menu import init_main_menu
from Code.Utils.Utils import draw_botton

# fonction qui permet de faire tourner les menu
def run_menu(screen, element, niveau, click, continue_click, EOTF_list):
    if niveau != -3:
        niveau = draw_botton(screen, element, click, niveau, continue_click)
        return niveau
    else:
        niveau = -3
        update_upgrade(element[2:], EOTF_list)

        niveau = draw_botton(screen, element, click, niveau, continue_click)
        if niveau >= 0:
            EOTF_list[niveau] = False if EOTF_list[niveau] else True
            niveau = -3
        return niveau




# fonction qui permet d'initialiser les menu
def init_menu(menu, police, EOTF_list):
    element = []
    if menu == -2:
        element = init_main_menu(police)
    elif menu == -1:
        element = init_lvl_menu(police)
    elif menu == -3:
        element = init_EOTF_menu(police)
        update_upgrade(element[2:], EOTF_list)

    return element

def update_upgrade(element, EOTF_list):
    for i in range(len(EOTF_list)):
        img = element[i].text[:-5]
        if EOTF_list[i]:
            img += "T.png"
        else:
            img += "F.png"
        element[i].text = img