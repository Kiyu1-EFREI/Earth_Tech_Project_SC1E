from .parametre_menu import init_par_menu
from .main_menu import init_main_menu
from Code.Utils.Utils import draw_botton

# fonction qui permet de faire tourner les menu
def run_menu(screen, element, niveau, click, continue_click):
    niveau = draw_botton(screen, element, click, niveau, continue_click)
    return niveau

police = "Arial"

# fonction qui permet d'initialiser les menu
def init_menu(menu, police):
    element = []
    if menu == -2:
        element = init_main_menu(police)
    elif menu == -1:
        # IMPORTANT:
        # Replace this with the real level-menu initializer if you have one,
        # for example: init_niveau_menu(police)
        element = []
    elif menu == -3:
        element = init_par_menu(police)

    return element