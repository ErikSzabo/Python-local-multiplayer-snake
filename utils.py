import pygame


class Stat:
    """
    Toplista elemeit lehet vele létrehozni.
    Attribútumok:
        name: játékos neve
        score: játékos pontszáma
    """

    def __init__(self, name, score):
        self.name = name
        self.score = score


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

        if grid_size >= 20 and width >= 800 and height >= 600:
            Display.grid_size = grid_size
            Display.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((width, height))
            Display.real_width = Display.window.get_width()
            Display.real_height = Display.window.get_height()
            Display.width = Display.real_width // grid_size * grid_size
            Display.height = Display.real_height // grid_size * grid_size
            Image.scale_game_images(grid_size)
        else:
            raise ValueError("Grid min. 20px\nSzélesség min. 800px\nMagasság min. 600px")


class Utils:

    @staticmethod
    def text_printer(surface, text, font_size, color, center_coords):
        """
        Kirajzol adott szöveget, adott mérettel, adott középponti koordinátákra, adott színnel.
        Paraméterek:
            surface: pygame surface amire rajzolni kell
            text: kiiratandó szöveg
            font_size: szöveg mérete
            color: szöveg színe
            center_coords: szöveg középponti koordinátája
        """
        font = pygame.font.Font("retro.ttf", font_size)
        text = font.render(text, 1, color)
        center_rect = text.get_rect(center=center_coords)
        surface.blit(text, center_rect)

    @staticmethod
    def input_box(surface, width, height, centery, color):
        """
        Létrehoz egy dobozt/téglalapot amit az adott surface-hez képest vízszintesen középre igazít.
        Paraméterek:
            surface: pygame surface amire rajzolni kell
            width: kívánt szélesség
            height: kívánt magasság
            centery: középponti y koordináta
            color: szín
        """
        input_box = pygame.Rect(0, 0, width, height)
        input_box.centerx = surface.get_width() / 2
        input_box.centery = centery
        pygame.draw.rect(surface, color, input_box)

    @staticmethod
    def load_highscores():
        """Visszatér a highscores.txt fájlból betöltött toplistával."""

        highscores = []
        try:
            with open("highscores.txt") as f:
                for i, line in enumerate(f):
                    if i == 10:
                        break
                    line_parts = line.split(" ")
                    stat = Stat(line_parts[0], int(line_parts[1].strip()))
                    highscores.append(stat)
        except FileNotFoundError:
            return []
        return highscores

    @staticmethod
    def save_highscores(highscores):
        """
        Kapott listát a highscores.txt fájlba menti.
        Paraméterek:
            highscores: Stat objektumokból álló lista
        """
        with open("highscores.txt", 'w') as f:
            i = 0
            while i < 10 and i < len(highscores):
                f.write("{} {}\n".format(highscores[i].name, highscores[i].score))
                i += 1


class Image:
    """Játékban használt képek statikus tárolója."""

    snake_heads = [
        [
            pygame.image.load("game/images/head1_left.png"),
            pygame.image.load("game/images/head1_right.png"),
            pygame.image.load("game/images/head1_down.png"),
            pygame.image.load("game/images/head1_up.png")
        ],
        [
            pygame.image.load("game/images/head2_left.png"),
            pygame.image.load("game/images/head2_right.png"),
            pygame.image.load("game/images/head2_down.png"),
            pygame.image.load("game/images/head2_up.png")
        ]
    ]

    food_image = pygame.image.load("game/images/apple.png")
    super_food_image = pygame.image.load("game/images/super_apple.png")
    menu_left_arrow = pygame.image.load("menu/images/left_arrow.png")
    menu_right_arrow = pygame.image.load("menu/images/right_arrow.png")
    menu_control = [pygame.image.load("menu/images/arrow_control.png"),
                    pygame.image.load("menu/images/wasd_control.png")]

    @staticmethod
    def scale_game_images(grid_size):
        """
        Átméretezi a játékban használt képeket a négyzetrács méretének megfelelően.
        Paraméterek:
            grid_size: négyzetrács mérete
        """
        for heads in Image.snake_heads:
            for i in range(len(heads)):
                heads[i] = pygame.transform.scale(heads[i], (grid_size, grid_size))

        Image.food_image = pygame.transform.scale(Image.food_image, (grid_size, grid_size))
        Image.super_food_image = pygame.transform.scale(Image.super_food_image, (grid_size, grid_size))
