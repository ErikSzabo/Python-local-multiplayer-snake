import pygame
from random import randint
from copy import deepcopy

class Food:
    """
    A játékban lévő almáért felelős osztály
    Attribútumok:
        x: x koordináta
        y: y koordináta
        valid_xs: érvényes x koordináták ahol megjelenhet az alma
        valid_ys: érvényes y koordináták ahol megjelenhet az alma
    """

    def __init__(self, surface, image):
        self.x = -1000
        self.y = -1000
        self.image = image
        self.valid_rects = []
        for x in range(0, surface.width, surface.grid_size):
            for y in range(0, surface.height, surface.grid_size):
                self.valid_rects.append(pygame.Rect(x, y, surface.grid_size, surface.grid_size))

    def recreate(self, players, other_apple, grid_size):
        used_rects = []

        for player in players:
            head_rect = pygame.Rect(player.x, player.y, grid_size, grid_size)
            used_rects.append(head_rect)
            for body_rect in player.body_rects:
                used_rects.append(body_rect)

        other_apple_rect = pygame.Rect(other_apple.x, other_apple.y, grid_size, grid_size)
        used_rects.append(other_apple_rect)

        possible_rects = []

        for rect in self.valid_rects:
            possible_rects.append(rect)
            for used_rect in used_rects:
                if rect.colliderect(used_rect):
                    possible_rects.pop()
                    break
        
        valid_rect = possible_rects[randint(0, max(0, len(possible_rects) - 1))]

        self.x = valid_rect.x
        self.y = valid_rect.y

    def draw(self, surface):
        """Kirajzolja az almát a képernyőre."""

        surface.blit(self.image, (self.x, self.y))


class SuperFood(Food):
    """
    A játékban lévő szuper almáért felelős osztály.
    Attribútumok:
        x: x koordináta
        y: y koordináta
        valid_xs: érvényes x koordináták ahol megjelenhet az alma
        valid_ys: érvényes y koordináták ahol megjelenhet az alma
        visible: látható-e
        remove_time: mennyi idő múlva tűnik el
        spawn_time: mennyi időnként jelenhet meg
        spawn_counter: megjelenítő számláló
        remove_counter: eltüntető számláló
    """

    def __init__(self, surface, image):
        super().__init__(surface, image)
        self.visible = False
        self.remove_time = 300  # 5 mp mulva már el is tunik
        self.spawn_time = 240  # Alap sebességnél 4 másodpercenként van esélye spawnolni
        self.spawn_counter = 0
        self.remove_counter = 0

    def handle_collision(self):
        """Alapértékre állítja a szuper almát."""

        self.__reset()

    def check_for_spawn(self, players, apple, grid_size):
        """
        Láthatóvá teszi a szuper almát valahol a pályán ha a spawn_counter elérte a kívánt mennyiséget és pont
        összejött a 30% esély.
        """

        if self.spawn_counter >= self.spawn_time and not self.visible:
            if randint(1, 3) == 2:
                self.recreate(players, apple, grid_size)
                self.visible = True
            self.spawn_counter = 0

    def check_for_remove(self):
        """Alapértékre állítja a szuper almát, ha a számláló elérte a kívánt értéket."""

        if self.remove_counter >= self.remove_time and self.visible:
            self.__reset()

    def update_counters(self):
        """Láthatóság alapján növeli a megjelenítő/eltüntető számlálót."""

        if self.visible:
            self.remove_counter += 1
        else:
            self.spawn_counter += 1

    def __reset(self):
        self.x = -1000
        self.y = -1000
        self.visible = False
        self.spawn_counter = 0
        self.remove_counter = 0
