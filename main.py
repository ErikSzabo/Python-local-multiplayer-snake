import pygame
from menu.menu import Menu
from game.game import Game
from game.snake import Snake
from game.end import EndScreen
from utils import Image, Display
from game.constants import Color

pygame.init()


def player_init(menu):
    """
    Visszaadja a létrehozott játékosok listáját
    Paraméterek:
        menu: létrehozott menü
    """
    players = []
    starting_x = [Display.width - Display.grid_size * 5, Display.grid_size * 5]
    colors = [Color.GREEN, Color.ORANGE]
    control = [
        [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP],
        [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]
    ]
    for i in range(menu.player_num):
        player = Snake(menu.player_names[i], starting_x[i], Display.height / 2, Image.snake_heads[i],
                       colors[i], control[i])
        players.append(player)
    return players


def start_menu(menu):
    """
    Elindítja menüt
    Paraméterek:
        menu: létrehozott menü
    """

    menu.redraw()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            menu.name_input_handler(event.key, event.unicode)
            if menu.navigation(event.key):
                break
        if event.type == pygame.QUIT:
            menu.full_exit = True
            break


def enter_listener() :
    """Megállítja a programot egy enter billentyű leütéséig"""

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return False
        if event.type == pygame.QUIT:
            return True


def main():
    """Program főkontrollere ami elindítja a játékot"""

    # Alap inicializáció
    pygame.mouse.set_visible(False)
    Display.init(30, 990, 780)
    menu = Menu()

    while True:
        # Menü kezelő
        start_menu(menu)

        # Játék indul ha nem kilépést választottunk
        if menu.full_exit:
            break

        # Player lista elkésztése a menü adatai és a MenuData class alapértékei alapján
        players = player_init(menu)

        # Játék elindítása
        game = Game(players)
        if game.start():   # Visszatér True értékkel ha a felhasználó megnyomta az X-et
            break

        # Amint vége a játéknak az EndScreen következik
        endscreen = EndScreen(game.players)
        endscreen.draw()

        # Folyamatosan várunk az enter billenytu lenyomására majd visszatérünk a menübe
        if enter_listener():   # Visszatér True értékkel ha a felhasználó megnyomta az X-et
            break


main()
