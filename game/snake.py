from enum import IntEnum
import pygame
from game.constants import Direction, Color
from utils import Display


class Snake:
    """Játékosokért felelős osztály"""

    def __init__(self, name, x, y, head_images, color, control):
        self.name = name
        self.x = x
        self.y = y
        self.head_images = head_images
        self.color = color
        self.score = 0
        self.length = 3
        self.direction = Direction.DOWN
        self.velocity = 3 + round(Display.grid_size / 20)
        self.key_pressed = False
        self.is_lost = False
        self.control = control
        self.body_rects = []
        self.rotate_points = []

    def calculate_velocity(self):
        """Beállítja a helyes sebességet kigyó(játékos) számára a pontszáma alapján"""

        score_breakpoints = [100, 90, 70, 50, 30, 20, 10]
        velocities = [10, 9, 8, 7, 6, 5, 4]
        for i in range(len(velocities)):
            velocities[i] = round(velocities[i] + (Display.grid_size / 20))

        for i in range(len(score_breakpoints)):
            if self.score >= score_breakpoints[i]:
                self.velocity = velocities[i]
                break

    def detect_wall_collision(self, first_y):
        """
        Visszatér igaz/hamis értékkel attől függően, hogy a játékos falnak ütközött-e.
        Paraméterek:
            win_width: pálya szélessége
            win_height: pálya magassága
            first_y: az az y koordináta, ahol kezdődik a pálya
        """

        if self.direction == Direction.LEFT:
            return self.x < 0
        elif self.direction == Direction.RIGHT:
            return self.x + Display.grid_size > Display.width
        elif self.direction == Direction.DOWN:
            return self.y + Display.grid_size > Display.height
        elif self.direction == Direction.UP:
            return self.y < first_y

    def detect_food_collision(self, apple):
        """
        Visszatér igaz/hamis értékkel attől függően, hogy a játékos almának ütközött-e.
        Paraméterek:
            apple: alma, vagy szuper alma
        """

        head_rect = pygame.Rect(self.x, self.y, Display.grid_size, Display.grid_size)
        apple_rect = pygame.Rect(apple.x, apple.y, Display.grid_size, Display.grid_size)
        return head_rect.colliderect(apple_rect)

    def detect_self_collision(self):
        """Visszatér igaz/hamis értékkel attől függően, hogy a játékos magába ütközött-e."""

        head_rect = pygame.Rect(self.x, self.y, Display.grid_size, Display.grid_size)
        for body_rect in self.body_rects:
            if head_rect.colliderect(body_rect):
                return True
        return False

    def detect_enemy_collision(self, enemy_snake):
        """
        Visszatér igaz/hamis értékkel attől függően, hogy a játékos másik játékosba ütközött-e.
        Paraméterek:
            enemy_snake: másik játékos
        """

        enemy_head_rect = pygame.Rect(enemy_snake.x, enemy_snake.y, Display.grid_size, Display.grid_size)
        head_rect = pygame.Rect(self.x, self.y, Display.grid_size, Display.grid_size)
        if head_rect.colliderect(enemy_head_rect):
            return True
        for body_rect in enemy_snake.body_rects:
            if head_rect.colliderect(body_rect):
                return True
        return False

    def draw(self):
        """
        Kirajzolja a kígyót.
        Paraméterek:
            window: kijelző surface amit a DisplayMonitor tárol
        """

        Display.window.blit(self.head_images[self.direction], (self.x, self.y))

        for body_rect in self.body_rects:
            pygame.draw.rect(Display.window, self.color, body_rect)

    def add_rotate_point(self, rotate_point):
        """
        Hozzáad egy forgáspontot a játékos forgáspontjaihoz.
        Paraméterek:
            rotate_point: forgáspont
        """

        self.rotate_points.append(rotate_point)

    def get_reverse_direction(self):
        """Visszatér a játékos ellenkező irányával."""

        if self.direction == Direction.LEFT:
            return Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            return Direction.LEFT
        elif self.direction == Direction.DOWN:
            return Direction.UP
        elif self.direction == Direction.UP:
            return Direction.DOWN

    def controlled_move(self, event):
        """
        Elmozgatja a játékost irányítóbillentyűtől függően.
        Paraméterek:
            event: billentyű event
        """

        if event.key not in self.control or self.key_pressed:
            return

        new_direction = self.direction
        for i in range(len(self.control)):
            if event.key == self.control[i]:
                new_direction = i
                break

        if new_direction == self.direction or new_direction == self.get_reverse_direction():
            return

        if self.direction == Direction.LEFT:
            self.x -= self.x - self.x // Display.grid_size * Display.grid_size
        elif self.direction == Direction.RIGHT:
            self.x = self.x // Display.grid_size * Display.grid_size + Display.grid_size
        elif self.direction == Direction.DOWN:
            self.y = self.y // Display.grid_size * Display.grid_size + Display.grid_size
        elif self.direction == Direction.UP:
            self.y -= self.y - self.y // Display.grid_size * Display.grid_size

        rotate_point = RotatePoint(self.x, self.y, self.direction)
        self.add_rotate_point(rotate_point)

        self.direction = Direction(new_direction)
        self.move()
        self.key_pressed = True

    def move(self):
        """Mozgatja a játékost a jelenlegi irányába."""

        #####################
        ### fej mozgatása ###
        #####################
        if self.direction == Direction.LEFT:
            self.x -= self.velocity
        elif self.direction == Direction.RIGHT:
            self.x += self.velocity
        elif self.direction == Direction.DOWN:
            self.y += self.velocity
        elif self.direction == Direction.UP:
            self.y -= self.velocity

        ########################
        ### Test mozgatása ###
        ########################
        # 1. kitöröljük az előző pillanatban tárolt test építőelemeit
        self.body_rects = []
        # 2. Felvesszük utolsó forgáspontként a kígyó fejét, mivel innen indulunk visszafele a rajzolásban
        self.rotate_points.append(RotatePoint(self.x, self.y, self.direction))
        # 3. csak addig építjük tovább a testét amíg kell
        length_in_pixels = self.length * Display.grid_size

        # 4. Visszafele haladva a forgáspontok iránya mentén haladva elkezdjük felépíteni a kígyó testét téglalapokból
        i = len(self.rotate_points) - 1
        while i > 0 and length_in_pixels > 0:
            # Felvesszük a forgáspont kezdő koordinátáit és irányát
            start_x, start_y = self.rotate_points[i].x, self.rotate_points[i].y
            to_direction = self.rotate_points[i].backward_direction
            # Az előtte lévőét is
            end_x, end_y = self.rotate_points[i - 1].x, self.rotate_points[i - 1].y

            # Iránytól, és maradék hossztól függően megépítjük a téglalapokat
            if to_direction == Direction.LEFT:
                is_longer = length_in_pixels > start_x - end_x
                body_rect = pygame.Rect(end_x, end_y, start_x - end_x, Display.grid_size) if is_longer else pygame.Rect(start_x - length_in_pixels, start_y, length_in_pixels, Display.grid_size)
                length_in_pixels -= start_x - end_x
                self.body_rects.append(body_rect)
            elif to_direction == Direction.RIGHT:
                is_longer = length_in_pixels > end_x - start_x
                body_rect = pygame.Rect(start_x + Display.grid_size, start_y, end_x - start_x, Display.grid_size) if is_longer else pygame.Rect(start_x + Display.grid_size, start_y, length_in_pixels, Display.grid_size)
                length_in_pixels -= end_x - start_x
                self.body_rects.append(body_rect)
            elif to_direction == Direction.DOWN:
                is_longer = length_in_pixels > end_y - start_y
                body_rect = pygame.Rect(start_x, start_y + Display.grid_size, Display.grid_size, end_y - start_y) if is_longer else pygame.Rect(start_x, start_y + Display.grid_size, Display.grid_size, length_in_pixels)
                length_in_pixels -= end_y - start_y
                self.body_rects.append(body_rect)
            elif to_direction == Direction.UP:
                is_longer = length_in_pixels > start_y - end_y
                body_rect = pygame.Rect(end_x, end_y, Display.grid_size, start_y - end_y) if is_longer else pygame.Rect(end_x, end_y - length_in_pixels + start_y - end_y, Display.grid_size, length_in_pixels)
                length_in_pixels -= start_y - end_y
                self.body_rects.append(body_rect)
            i -= 1

        # 5. Ha még maradt testhossz, de nincs további forgáspont, mint viszonyítási alap
        if length_in_pixels > 0:
            start_x, start_y = self.rotate_points[i].x, self.rotate_points[i].y
            to_direction = self.rotate_points[i].backward_direction
            if to_direction == Direction.LEFT:
                body_rect = pygame.Rect(start_x - length_in_pixels, start_y, length_in_pixels, Display.grid_size)
            elif to_direction == Direction.RIGHT:
                body_rect = pygame.Rect(start_x + Display.grid_size, start_y, length_in_pixels, Display.grid_size)
            elif to_direction == Direction.DOWN:
                body_rect = pygame.Rect(start_x, start_y + Display.grid_size, Display.grid_size, length_in_pixels)
            elif to_direction == Direction.UP:
                body_rect = pygame.Rect(start_x, start_y - length_in_pixels, Display.grid_size, length_in_pixels)
            self.body_rects.append(body_rect)

        # 6. A továbbiakban teljesen haszontalan forgáspontoktól megszabadulunk
        self.rotate_points = self.rotate_points[i:]

        # 7. A fent hozzáadatot forgáspontot (fej) töröljük, mert később változni fog a koordinátája
        self.rotate_points.pop()


class RotatePoint:
    """Forgáspontok létrehozásáért felelős osztály"""

    def __init__(self, x, y, forward_direction):
        self.x = x
        self.y = y
        self.backward_direction = forward_direction
        self.reverse()

    def reverse(self):
        """Ellentétesre váltja a forgáspont irányát"""

        if self.backward_direction == Direction.LEFT:
            self.backward_direction = Direction.RIGHT
        elif self.backward_direction == Direction.RIGHT:
            self.backward_direction = Direction.LEFT
        elif self.backward_direction == Direction.DOWN:
            self.backward_direction = Direction.UP
        elif self.backward_direction == Direction.UP:
            self.backward_direction = Direction.DOWN
