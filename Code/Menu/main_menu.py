from Code.Utils.classes import*
import pygame

def init_main_menu(police):
    element = [
        ButtonClass(pygame.Rect(0, 0, 1280, 720), "Asset/menu/main_menu_background.png", pygame.font.SysFont(police, 48), None, (100,100,100), 0),
        ButtonClass(pygame.Rect(340, 130, 600, 120), "Asset/menu/main_menu_txt.png",pygame.font.SysFont(police, 48), None, (100, 100, 100), 0),
        ButtonClass(pygame.Rect(460, 360, 360, 80), "Jouer", pygame.font.SysFont(police, 48), -1),
        ButtonClass(pygame.Rect(460, 470, 360, 80), "Quitter", pygame.font.SysFont(police, 48), 0)
    ]
    return element
































import pygame
import sys

# ---------- Constantes ----------
WIDTH, HEIGHT = 1280, 720
FPS = 60

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
ACCENT = (70, 130, 180)

BACK_BTN_RECT = pygame.Rect(20, 20, 140, 50)

# ---------- Classe Button ----------
class Button:
    def __init__(self, rect, text, font, color=ACCENT, hover_color=LIGHT_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surf):
        mouse = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse)
        col = self.hover_color if is_hover else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, self.text_color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ---------- Fonctions utilitaires ----------
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Pygame - Sélection de niveau")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)
    return screen, clock, font, small_font

def create_menu_buttons(font):
    btn_w, btn_h = 360, 80
    gap = 30
    start_y = (HEIGHT - (2 * btn_h + gap)) // 2
    center_x = (WIDTH - btn_w) // 2

    btn_jouer = Button((center_x, start_y, btn_w, btn_h), "Jouer", font)
    print(center_x, start_y, btn_w, btn_h)
    btn_quit = Button((center_x, start_y + btn_h + gap, btn_w, btn_h), "Quitter", font)
    print(center_x, start_y + btn_h + gap, btn_w, btn_h)
    return {"jouer": btn_jouer, "quit": btn_quit}

def create_level_buttons(font):
    # Crée 4 boutons côte à côte centrés horizontalement
    btn_w, btn_h = 200, 80
    spacing = 30
    total_width = 4 * btn_w + 3 * spacing
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT // 2
    level_buttons = []
    for i in range(4):
        rect = (start_x + i * (btn_w + spacing), y - btn_h // 2, btn_w, btn_h)
        level_buttons.append(Button(rect, f"Niveau {i+1}", font))
        print(start_x + i * (btn_w + spacing), y - btn_h // 2, btn_w, btn_h)
    return level_buttons

def draw_menu(screen, font, buttons):
    screen.fill(GRAY)
    title = font.render("Mon Jeu", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//6)))
    buttons["jouer"].draw(screen)
    buttons["quit"].draw(screen)

def draw_level_selection(screen, font, small_font, level_buttons):
    screen.fill((30, 30, 50))
    title = font.render("Choisis un niveau", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//6)))
    for btn in level_buttons:
        btn.draw(screen)
    # Bouton retour
    pygame.draw.rect(screen, (120,120,120), BACK_BTN_RECT, border_radius=8)
    back_txt = small_font.render("Retour", True, WHITE)
    screen.blit(back_txt, back_txt.get_rect(center=BACK_BTN_RECT.center))

def draw_playing_placeholder(screen, font, small_font, selected_level):
    screen.fill((10, 50, 10))
    txt = font.render(f"En jeu - Niveau {selected_level}", True, WHITE)
    screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.draw.rect(screen, (120,120,120), BACK_BTN_RECT, border_radius=8)
    back_txt = small_font.render("Menu", True, WHITE)
    screen.blit(back_txt, back_txt.get_rect(center=BACK_BTN_RECT.center))

def process_events(state, buttons, level_buttons, selected_level):
    """
    Traite les événements et renvoie (nouvel_etat, running_bool, selected_level).
    États possibles: "menu", "select_level", "playing"
    """
    running = True
    new_state = state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if buttons["jouer"].is_clicked(event):
                new_state = "select_level"
            if buttons["quit"].is_clicked(event):
                running = False

        elif state == "select_level":
            # clic sur un niveau
            for idx, btn in enumerate(level_buttons):
                if btn.is_clicked(event):
                    selected_level = idx + 1
                    new_state = "playing"
                    break
            # bouton retour
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BTN_RECT.collidepoint(event.pos):
                    new_state = "menu"

        elif state == "playing":
            # bouton retour vers menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BTN_RECT.collidepoint(event.pos):
                    new_state = "menu"
                    selected_level = None

    return new_state, running, selected_level

# ---------- Point d'entrée ----------
if __name__ == "__main__":
    screen, clock, font, small_font = init_pygame()
    menu_buttons = create_menu_buttons(font)
    level_buttons = create_level_buttons(font)
    state = "menu"
    running = True
    selected_level = None

    # Boucle principale (seule partie hors fonctions)
    while running:
        state, running, selected_level = process_events(state, menu_buttons, level_buttons, selected_level)

        if state == "menu":
            draw_menu(screen, font, menu_buttons)
        elif state == "select_level":
            draw_level_selection(screen, font, small_font, level_buttons)
        elif state == "playing":
            draw_playing_placeholder(screen, font, small_font, selected_level)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()