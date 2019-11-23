from random import randint
import pygame


class Food:
    """A játékban lévő almáért felelős osztály"""

    def __init__(self, win_width, win_height, size, valid_start_y, image):
        self.x = 1
        self.y = 1
        self.size = size
        self.image = image
        self.valid_xs = range(0, win_width - self.size, self.size)
        self.valid_ys = range(valid_start_y, win_height - self.size, self.size)

    def recreate(self, players, other_apple):
        """
        Új koordinátát ad az almának, ami nem ütközik se a kígyókkal se a másik almával
        Paraméterek:
        players: játékosok listája
        other_apple: a másik alma
        """

        x = self.valid_xs[randint(0, len(self.valid_xs) - 1)]
        y = self.valid_ys[randint(0, len(self.valid_ys) - 1)]
        possible_apple_rect = pygame.Rect(x, y, self.size, self.size)
        used_rects = []

        for player in players:
            head_rect = pygame.Rect(player.x, player.y, player.size, player.size)
            used_rects.append(head_rect)
            for body_rect in player.body_rects:
                used_rects.append(body_rect)

        other_apple_rect = pygame.Rect(other_apple.x, other_apple.y, other_apple.size, other_apple.size)
        used_rects.append(other_apple_rect)

        good_coordinates = False
        while not good_coordinates:
            for rect in used_rects:
                if possible_apple_rect.colliderect(rect):
                    x = self.valid_xs[randint(0, len(self.valid_xs) - 1)]
                    y = self.valid_ys[randint(0, len(self.valid_ys) - 1)]
                    possible_apple_rect = pygame.Rect(x, y, self.size, self.size)
                    break
            else:
                good_coordinates = True

        self.x = x
        self.y = y

    def draw(self, window):
        """
        Kirajzolja az almát a képernyőre
        Paraméterek:
        window: pygame.Surface
        """

        window.blit(self.image, (self.x, self.y))


class SuperFood(Food):
    """A játékban lévő szuper almáért felelős osztály"""

    def __init__(self, win_width, win_height, size, valid_start_y, image):
        super().__init__(win_width, win_height, size, valid_start_y, image)
        self.visible = False
        self.remove_time = 300  # 5 mp mulva már el is tunik
        self.spawn_time = 240  # Alap sebességnél 4 másodpercenként van esélye spawnolni
        self.spawn_counter = 0
        self.remove_counter = 0

    def handle_collision(self):
        """Alapértékre állítja a szuper almát"""

        self.visible = False
        self.x = 1
        self.y = 1
        self.spawn_counter = 0
        self.remove_counter = 0

    def check_for_spawn(self, players, apple):
        if self.spawn_counter >= self.spawn_time and not self.visible:
            if randint(1, 3) == 2:
                self.recreate(players, apple)
                self.visible = True
            self.spawn_counter = 0

    def check_for_remove(self):
        """Alapértékre állítja a szuper almát, ha a számláló elérte a kívánt értéket"""

        if self.remove_counter >= self.remove_time and self.visible:
            self.visible = False
            self.x = 1
            self.y = 1
            self.remove_counter = 0
            self.spawn_counter = 0

    def update_counters(self):
        """Láthatóság alapján növeli a megjelenítő/eltüntető számlálót"""

        if self.visible:
            self.remove_counter += 1
        else:
            self.spawn_counter += 1
