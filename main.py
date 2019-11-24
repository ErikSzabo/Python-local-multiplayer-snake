import pygame
from menu.menu import Menu
from game.game import Game
from game.snake import Snake
from game.end import EndScreen
from utils import Image, DisplayMonitor
from game.constants import Color

pygame.init()


def player_init(menu, display, grid_size):
    """
    Visszaadja a létrehozott játékosok listáját
    Paraméterek:
    menu: létrehozott menü
    display: kijelzőt tároló objektum
    grid_size: négyzetrács mérete
    """
    players = []
    starting_x = [display.width - grid_size * 5, grid_size * 5]
    colors = [Color.GREEN, Color.ORANGE]
    control = [
        [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP],
        [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]
    ]
    for i in range(menu.player_num):
        player = Snake(menu.player_names[i], starting_x[i], display.height / 2, Image.snake_heads[i],
                       colors[i], grid_size, control[i])
        players.append(player)
    return players


def start_menu(menu, display):
    """
    Elindítja menüt
    Paraméterek:
    menu: létrehozott menü
    display: kijelzőt tároló objektum
    """

    menu.redraw(display.window)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            menu.name_input_handler(event.key, display.window, event.unicode)
            if menu.navigation(event.key, display.window):
                break


def enter_listener() :
    """Megállítja a programot egy enter billentyű leütéséig"""

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            break


def main():
    """Program főkontrollere ami elindítja a játékot"""

    grid_size = 30
    if grid_size != 20:
        Image.scale_game_images(grid_size)

    # Alap inicializáció
    pygame.mouse.set_visible(False)
    display = DisplayMonitor(grid_size)
    menu = Menu()

    while True:
        # Menü kezelő
        start_menu(menu, display)

        # Játék indul ha nem kilépést választottunk
        if menu.full_exit:
            break

        # Player lista elkésztése a menü adatai és a MenuData class alapértékei alapján
        players = player_init(menu, display, grid_size)

        # Játék elindítása
        game = Game(players, display, grid_size)
        game.start_game(display)

        # Amint vége a játéknak az EndScreen következik
        endscreen = EndScreen(game.players)
        endscreen.draw(display.window)

        # Folyamatosan várunk az enter billenytu lenyomására majd visszatérünk a menübe
        enter_listener()


main()
