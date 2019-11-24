import pygame


class Stat:
    """
    Toplista elkészítéséhez használatos
    Nevet és pontszámot tárol
    """
    def __init__(self, name, score):
        self.name = name
        self.score = score


class DisplayMonitor:
    """Kijelző ablakról tartalmaz minden szükséges információt"""

    def __init__(self, grid_size):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.real_width = self.window.get_width()
        self.real_height = self.window.get_height()
        self.width = self.real_width // grid_size * grid_size
        self.height = self.real_height // grid_size * grid_size


class Utils:

    @staticmethod
    def text_printer(surface, text, font_size, color, center_coords):
        """
        Kirajzol adott szöveget adott mérettel, adott középponti koordinátákra adott színnel
        Paraméterek:
        surface: pygame.Surface
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
        Létrehoz egy dobozt/téglalapot amit az adott surface-hez képest vízszintesen középre igazít
        surface: pygame.Surface
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
        """Visszatér a fájlból betöltött toplistával"""

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
        Kapott listát fájlba menti
        Paraméterek:
        highscores: Stat objektumokból álló lista
        """
        with open("highscores.txt", 'w') as f:
            i = 0
            while i < 10 and i < len(highscores):
                f.write("{} {}\n".format(highscores[i].name, highscores[i].score))
                i += 1


class Image:
    """Játékban használt képek statikus tárolója"""

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
        Átméretezi a játékban használt képeket a négyzetrács méretének megfelelően
        Paraméterek:
        grid_size: négyzetrács mérete
        """
        for heads in Image.snake_heads:
            for i in range(len(heads)):
                heads[i] = pygame.transform.scale(heads[i], (grid_size, grid_size))

        Image.food_image = pygame.transform.scale(Image.food_image, (grid_size, grid_size))
        Image.super_food_image = pygame.transform.scale(Image.super_food_image, (grid_size, grid_size))
