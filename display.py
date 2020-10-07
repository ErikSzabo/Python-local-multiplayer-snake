import pygame
from images import Image

class Display:
    """
    Tárol minden szügséges adatot a kijelzőről.
    Osztály változók:
        window: pygame display
        real_width: valódi szélessége az ablaknak
        real_height: valódi magassága az ablaknak
        width: a pálya szélessége (négyzetrácsozástól függ)
        height: a pálya magassága (négyzetrácsozástól függ)
    """

    grid_size = None
    window = None
    real_width = None
    real_height = None
    width = None
    height = None

    @staticmethod
    def init(grid_size=30, width=800, height=600, full_screen=False):
        """
        Inicializálja a kijelzőt, ha nincs megadott paraméter, akkor az alapértelmezett értékeket használja.
        Paraméterek:
            grid_size: négyzetrácsozás mérete
            width: ablak szélessége
            height: ablak magassága
            full_screen: teljes képernyős vagy nem
        """

        if grid_size >= 30 and width >= 800 and height >= 600:
            Display.grid_size = grid_size
            Display.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((width, height))
            Display.real_width = Display.window.get_width()
            Display.real_height = Display.window.get_height()
            Display.width = Display.real_width // grid_size * grid_size
            Display.height = Display.real_height // grid_size * grid_size
            Image.scale_game_images(grid_size)
        else:
            raise ValueError("Grid min. 20px\nSzélesség min. 800px\nMagasság min. 600px")
