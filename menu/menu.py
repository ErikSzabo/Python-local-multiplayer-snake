import pygame
from images import Image
from display import Display
from utils import text_printer, input_box
from game.constants import Color


class Menu:
    """
    Létrehozza a játékhoz szükséges menüt.
    Attribútumok:
        surface: pygame surface amire rajzolva lesz a menü
        full_exit: teljes kilépést választotta-e a felhasználó
        current_position: megmutatja jelenleg hol tartózkodik a felhasználó a menüben
        max_position: a menü utolsó elemének pozíciója
        player_number_pos: a mneü játékos szám kiválasztó elemének pozíciója
        player_num: jelenleg éppen hány játékosra van beállítva menü
        player_names: a játékosok nevei
    """

    def __init__(self):
        self.surface = pygame.Surface((800, 600))
        self.full_exit = False
        self.current_position = 0  # legfelső elem
        self.max_position = 4  # legalsó elem
        self.player_number_pos = 1
        self.player_num = 2
        self.player_names = ["", ""]

    def redraw(self):
        """Újra rajzolja menüt."""

        Display.window.fill(Color.BACKGROUND)
        self.surface.fill(Color.BACKGROUND)
        colors = [Color.TEXT] * 5
        for i in range(len(colors)):
            if i == self.current_position:
                if self.player_num == 2:
                    colors[i] = Color.ORANGE
                else:
                    colors[i] = Color.ORANGE

        text_printer(self.surface, "Python Snake", 80, Color.GREEN, (self.surface.get_width() / 2, 55))

        text_printer(self.surface, "Játék", 60, colors[0], (self.surface.get_width() / 2, 175))

        center_rect = Image.menu_left_arrow.get_rect(center=(self.surface.get_width() / 2 - 200, 270))
        self.surface.blit(Image.menu_left_arrow, center_rect)

        text_printer(self.surface, "{}".format(self.player_num), 60, colors[1],
                           (self.surface.get_width() / 2, 270))

        center_rect = Image.menu_right_arrow.get_rect(center=(self.surface.get_width() / 2 + 200, 270))
        self.surface.blit(Image.menu_right_arrow, center_rect)

        text_printer(self.surface, "Játékos nevek...", 20, Color.TEXT, (self.surface.get_width() / 2, 330))

        centery = 380
        for i in range(self.player_num):
            input_box(self.surface, 300, 60, centery, colors[i + 2])
            text_printer(self.surface, self.player_names[i], 20, (0, 0, 0),
                               (self.surface.get_width() / 2, centery))
            center_rect = Image.menu_control[i].get_rect(center=(self.surface.get_width() / 2 - 110, centery))
            self.surface.blit(Image.menu_control[i], center_rect)
            centery += 80

        text_printer(self.surface, "Kilépés", 60, colors[-1], (self.surface.get_width() / 2, 540))

        s_center_rect = self.surface.get_rect(center=(Display.window.get_width() / 2, Display.window.get_height() / 2))
        Display.window.blit(self.surface, s_center_rect)
        pygame.display.update()

    def navigation(self, key):
        """
        Billentyü leütés függvényében navigál a menüben.
        Paraméterek:
            key: pygame event lenyomott billentyűje
        """

        if key == pygame.K_DOWN:
            if self.current_position < self.max_position:
                if self.player_num == 1 and self.current_position == self.max_position - 2:
                    self.current_position = self.max_position
                else:
                    self.current_position += 1
                self.redraw()
        elif key == pygame.K_UP:
            if self.current_position > 0:
                if self.player_num == 1 and self.current_position == self.max_position:
                    self.current_position -= 2
                else:
                    self.current_position -= 1
                self.redraw()
        elif key == pygame.K_RIGHT:
            if self.current_position == self.player_number_pos:
                if self.player_num == 1:
                    self.player_num += 1
                    self.redraw()
        elif key == pygame.K_LEFT:
            if self.current_position == self.player_number_pos:
                if self.player_num == 2:
                    self.player_num -= 1
                    self.redraw()
        elif key == pygame.K_RETURN:
            if self.current_position == 0:
                return True
            elif self.current_position == self.max_position:
                self.full_exit = True
                return True
        return False

    def name_input_handler(self, key, key_unicode):
        """
        Ha megfelelő pozíción van a felhasználó és leüt egy billentyüt, akkor annak a billentyűnek a szöveges
        reprezentációjával bővül a megfelelő játékos név.
        Paraméterek:
            key: pygame event lenyomott billentyűje
            key_unicode: leütött karakter szöveges reprezentációja
        """

        if self.current_position == 2:
            if key == pygame.K_BACKSPACE:
                self.player_names[0] = self.player_names[0][0:len(self.player_names[0]) - 1]
            else:
                self.player_names[0] += key_unicode
            self.redraw()
        elif self.current_position == 3:
            if key == pygame.K_BACKSPACE:
                self.player_names[1] = self.player_names[1][0:len(self.player_names[1]) - 1]
            else:
                self.player_names[1] += key_unicode
            self.redraw()
