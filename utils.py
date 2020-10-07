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
    font = pygame.font.Font("assets/fonts/retro.ttf", font_size)
    text = font.render(text, 1, color)
    center_rect = text.get_rect(center=center_coords)
    surface.blit(text, center_rect)

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
