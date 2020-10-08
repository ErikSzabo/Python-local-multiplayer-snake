import pygame
from images import Image
from game.constants import Color
from utils import text_printer, input_box

class Surface:
    def __init__(self, size, parent = None):
        self.surface = pygame.Surface(size) if size != (0, 0) else pygame.Surface((0, 0), pygame.FULLSCREEN)
        self.parent: Surface = parent

    def blit(self, x, y):
        if(self.__has_parent()):
            self.parent.surface.blit(self.surface, (x, y))

    def scaled_blit_to_parent(self):
        if(self.__has_parent()):
            pygame.transform.scale(self.surface, (self.parent.width, self.parent.height), self.parent.surface)

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    def __has_parent(self):
        return self.parent is not None


class MenuSurface(Surface):
    def __init__(self, parent):
        super().__init__((1280, 720), parent)

    def redraw(self, menu):
        self.parent.surface.fill(Color.BACKGROUND)
        self.surface.fill(Color.BACKGROUND)
        colors = [Color.TEXT] * 5
        for i in range(len(colors)):
            if i == menu.current_position:
                if menu.player_num == 2:
                    colors[i] = Color.ORANGE
                else:
                    colors[i] = Color.ORANGE

        text_printer(self.surface, "Python Snake", 60, Color.GREEN, (self.width / 2, 85))
        text_printer(self.surface, "Játék", 40, colors[0], (self.width / 2, 175))
        center_rect = Image.menu_left_arrow.get_rect(center=(self.width / 2 - 150, 270))
        self.surface.blit(Image.menu_left_arrow, center_rect)
        text_printer(self.surface, "{}".format(menu.player_num), 40, colors[1], (self.width / 2, 270))
        center_rect = Image.menu_right_arrow.get_rect(center=(self.width / 2 + 150, 270))
        self.surface.blit(Image.menu_right_arrow, center_rect)
        text_printer(self.surface, "Játékos nevek...", 15, Color.TEXT, (self.width / 2, 330))

        centery = 380
        for i in range(menu.player_num):
            input_box(self.surface, 300, 60, centery, colors[i + 2])
            text_printer(self.surface, menu.player_names[i], 20, (0, 0, 0), (self.width / 2, centery))
            center_rect = Image.menu_control[i].get_rect(center=(self.width / 2 - 110, centery))
            self.surface.blit(Image.menu_control[i], center_rect)
            centery += 80

        text_printer(self.surface, "Kilépés", 40, colors[-1], (self.width / 2, 540))


class Window(Surface):
    def __init__(self):
        super().__init__((0, 0))
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class GameSurface(Surface):
    def __init__(self, parent):
        super().__init__((1280, 720), parent)

    def redraw(self, players, highscore):
        self.surface.fill(Color.BACKGROUND)

        x = [self.width/4 * 3, self.width/4]
        for i in range(len(players)):
            text_printer(self.surface, "{}: {}".format(players[i].name, players[i].score), 30, players[i].color, (x[i], 65))
            
        text_printer(self.surface, "HIGHSCORE", 30, Color.WHITE, (self.width / 2, 50))
        text_printer(self.surface, str(highscore), 30, Color.WHITE, (self.width / 2, 80))

        

class GameFieldSurface(Surface):
    def __init__(self, parent, squares):
        super().__init__((squares[0] * self.__grid_size(parent, squares, 100), squares[1] * self.__grid_size(parent, squares, 100)), parent)
        self.grid_size = self.__grid_size(parent, squares, 100)
        self.distance_from_top = 100
        Image.scale_game_images(self.grid_size)
    
    def redraw(self):
        self.surface.fill((20,20,20))

        for x in range(0, self.width + 1, self.grid_size):
            pygame.draw.line(self.surface, Color.LINE, (x, 0), (x, self.width))
        pygame.draw.line(self.surface, Color.LINE, (x-1, 0), (x-1, self.width))
        for j in range(0, self.height + 1, self.grid_size):
            pygame.draw.line(self.surface, Color.LINE, (0, j), (self.width, j))
        pygame.draw.line(self.surface, Color.LINE, (0, j-1), (self.width, j-1))
        
    def blit(self):
        game_y = self.parent.height - self.height
        game_y = max(self.distance_from_top, game_y // 2)
        super().blit(self.parent.width / 2 - self.width / 2, game_y)

    def __grid_size(self, parent, squares, distance_from_top):
        return (min(parent.width, parent.height - distance_from_top)) // max(squares)
