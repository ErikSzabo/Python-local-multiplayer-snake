from random import randint
import pygame

from utils import Display


class Food:
    """
    A játékban lévő almáért felelős osztály
    Attribútumok:
        x: x koordináta
        y: y koordináta
        size: méret (size x size négyzet)
        valid_xs: érvényes x koordináták ahol megjelenhet az alma
        valid_ys: érvényes y koordináták ahol megjelenhet az alma
    """

    def __init__(self, valid_start_y, image):
        self.x = 1
        self.y = 1
        self.image = image
        self.valid_xs = range(0, Display.width - Display.grid_size, Display.grid_size)
        self.valid_ys = range(valid_start_y, Display.height - Display.grid_size, Display.grid_size)

    def recreate(self, players, other_apple):
        """
        Új koordinátát ad az almának, ami nem ütközik se a kígyókkal se a másik almával.
        Paraméterek:
            players: játékosok listája
            other_apple: a másik alma
        """

        x = self.valid_xs[randint(0, len(self.valid_xs) - 1)]
        y = self.valid_ys[randint(0, len(self.valid_ys) - 1)]
        possible_apple_rect = pygame.Rect(x, y, Display.grid_size, Display.grid_size)
        used_rects = []

        for player in players:
            head_rect = pygame.Rect(player.x, player.y, Display.grid_size, Display.grid_size)
            used_rects.append(head_rect)
            for body_rect in player.body_rects:
                used_rects.append(body_rect)

        other_apple_rect = pygame.Rect(other_apple.x, other_apple.y, Display.grid_size, Display.grid_size)
        used_rects.append(other_apple_rect)

        good_coordinates = False
        while not good_coordinates:
            for rect in used_rects:
                if possible_apple_rect.colliderect(rect):
                    x = self.valid_xs[randint(0, len(self.valid_xs) - 1)]
                    y = self.valid_ys[randint(0, len(self.valid_ys) - 1)]
                    possible_apple_rect = pygame.Rect(x, y, Display.grid_size, Display.grid_size)
                    break
            else:
                good_coordinates = True

        self.x = x
        self.y = y

    def draw(self):
        """
        Kirajzolja az almát a képernyőre.
        Paraméterek:
            window: pygame surface amire rajzolni kell
        """

        Display.window.blit(self.image, (self.x, self.y))


class SuperFood(Food):
    """
    A játékban lévő szuper almáért felelős osztály.
    Attribútumok:
        x: x koordináta
        y: y koordináta
        size: méret (size x size négyzet)
        valid_xs: érvényes x koordináták ahol megjelenhet az alma
        valid_ys: érvényes y koordináták ahol megjelenhet az alma
        visible: látható-e
        remove_time: mennyi idő múlva tűnik el
        spawn_time: mennyi időnként jelenhet meg
        spawn_counter: megjelenítő számláló
        remove_counter: eltüntető számláló
    """

    def __init__(self, valid_start_y, image):
        super().__init__(valid_start_y, image)
        self.visible = False
        self.remove_time = 300  # 5 mp mulva már el is tunik
        self.spawn_time = 240  # Alap sebességnél 4 másodpercenként van esélye spawnolni
        self.spawn_counter = 0
        self.remove_counter = 0

    def handle_collision(self):
        """Alapértékre állítja a szuper almát."""

        self.visible = False
        self.x = 1
        self.y = 1
        self.spawn_counter = 0
        self.remove_counter = 0

    def check_for_spawn(self, players, apple):
        """
        Láthatóvá teszi a szuper almát valahol a pályán ha a spawn_counter elérte a kívánt mennyiséget és pont
        összejött a 30% esély.
        """

        if self.spawn_counter >= self.spawn_time and not self.visible:
            if randint(1, 3) == 2:
                self.recreate(players, apple)
                self.visible = True
            self.spawn_counter = 0

    def check_for_remove(self):
        """Alapértékre állítja a szuper almát, ha a számláló elérte a kívánt értéket."""

        if self.remove_counter >= self.remove_time and self.visible:
            self.visible = False
            self.x = 1
            self.y = 1
            self.remove_counter = 0
            self.spawn_counter = 0

    def update_counters(self):
        """Láthatóság alapján növeli a megjelenítő/eltüntető számlálót."""

        if self.visible:
            self.remove_counter += 1
        else:
            self.spawn_counter += 1
