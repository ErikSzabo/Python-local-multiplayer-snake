import pygame
from images import Image
from display import window
from utils import text_printer, input_box
from game.constants import Color
from surfaces import MenuSurface


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
        self.surface: MenuSurface = MenuSurface(window)
        self.full_exit = False
        self.current_position = 0  # legfelső elem
        self.max_position = 4  # legalsó elem
        self.player_number_pos = 1
        self.player_num = 2
        self.player_names = ["", ""]

    def redraw(self):
        """Újra rajzolja menüt."""

        self.surface.redraw(self)
        # self.surface.blit(window.width / 2 - self.surface.width / 2, window.height / 2 - self.surface.height / 2)
        self.surface.scaled_blit_to_parent()
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
