from enum import IntEnum
import pygame
from game.enums import Direction


class Snake:
    """Játékosokért felelős osztály"""

    def __init__(self, name, x, y, head_images, rotate_images, color, size, control):
        self.name = name
        self.x = x
        self.y = y
        self.head_images = head_images
        self.rotate_images = rotate_images
        self.color = color
        self.size = size
        self.score = 0
        self.length = 3
        self.direction = Direction.DOWN
        self.velocity = 3 + round(size / 20)
        self.key_pressed = False
        self.is_lost = False
        self.control = control
        self.body_rects = []
        self.rotate_parts = []
        self.rotate_points = []

    def calculate_velocity(self):
        """Beállítja a helyes sebességet kigyó(játékos) számára a pontszáma alapján"""

        score_breakpoints = [100, 90, 70, 50, 30, 20, 10]
        velocities = [10, 9, 8, 7, 6, 5, 4]
        for i in range(len(velocities)):
            velocities[i] = round(velocities[i] + (self.size / 20))

        for i in range(len(score_breakpoints)):
            if self.score >= score_breakpoints[i]:
                self.velocity = velocities[i]
                break

    def detect_wall_collision(self, win_width, win_height, first_y):
        """Visszatér igaz/hamis értékkel attől függően, hogy a játékos falnak ütközött-e"""

        if self.direction == Direction.LEFT:
            return self.x < 0
        elif self.direction == Direction.RIGHT:
            return self.x + self.size > win_width
        elif self.direction == Direction.DOWN:
            return self.y + self.size > win_height
        elif self.direction == Direction.UP:
            return self.y < first_y

    def detect_food_collision(self, apple):
        """
        Visszatér igaz/hamis értékkel attől függően, hogy a játékos almának ütközött-e
        Paraméterek:
        apple: alma, vagy szuper alma
        """

        head_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        apple_rect = pygame.Rect(apple.x, apple.y, apple.size, apple.size)
        return head_rect.colliderect(apple_rect)

    def detect_self_collision(self):
        """Visszatér igaz/hamis értékkel attől függően, hogy a játékos magába ütközött-e"""

        head_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        for body_rect in self.body_rects:
            if head_rect.colliderect(body_rect):
                return True
        return False

    def detect_enemy_collision(self, enemy_snake):
        """
        Visszatér igaz/hamis értékkel attől függően, hogy a játékos másik játékosba ütközött-e
        Paraméterek:
        enemy_snake: Másik játékos
        """

        enemy_head_rect = pygame.Rect(enemy_snake.x, enemy_snake.y, self.size, self.size)
        head_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if head_rect.colliderect(enemy_head_rect):
            return True
        for body_rect in enemy_snake.body_rects:
            if head_rect.colliderect(body_rect):
                return True
        return False

    def draw(self, window):
        """
        Kirajzolja a játékos kígyóját
        Paraméterek:
        window: erre rajzol
        """

        window.blit(self.head_images[self.direction], (self.x, self.y))
        for body_rect in self.body_rects:
            pygame.draw.rect(window, self.color, body_rect)
        for rotate_part in self.rotate_parts:
            window.blit(rotate_part.image, (rotate_part.x, rotate_part.y))

    def add_rotate_point(self, rotate_point):
        """
        Hozzáad egy forgáspontot a játékos forgáspontjaihoz
        Paraméterek:
        rotate_point: forgáspont
        """

        self.rotate_points.append(rotate_point)

    def get_reverse_direction(self):
        """Visszatér a játékos ellenkező irányával"""

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
        Elmozgatja a játékost irányítóbillentyűtől függően
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
            self.x -= self.x - self.x // self.size * self.size
        elif self.direction == Direction.RIGHT:
            self.x = self.x // self.size * self.size + self.size
        elif self.direction == Direction.DOWN:
            self.y = self.y // self.size * self.size + self.size
        elif self.direction == Direction.UP:
            self.y -= self.y - self.y // self.size * self.size

        rotate_point = RotatePoint(self.x, self.y, self.direction)
        rotate_point.reverse()
        self.add_rotate_point(rotate_point)

        self.direction = Direction(new_direction)
        self.move()
        self.key_pressed = True

    def move(self):
        """Mozgatja a játékost a jelenlegi irányába"""

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
        self.rotate_parts = []
        # 2. Felvesszük utolsó forgáspontként a kígyó fejét, mivel innen indulunk visszafele a rajzolásban
        self.rotate_points.append(RotatePoint(self.x, self.y, self.get_reverse_direction()))
        # 3. csak addig építjük tovább a testét amíg kell
        length_in_pixels = self.length * self.size

        # 4. Visszafele haladva a forgáspontok iránya mentén haladva elkezdjük felépíteni a kígyó testét téglalapokból
        i = 0
        for i in range(len(self.rotate_points) - 1, 0, -1):
            # Ha elfogyott a kívánt hossz, nem építjük tovább akkor sem, ha van még forgáspont
            if length_in_pixels == 0:
                break

            # Felvesszük a forgáspont kezdő koordinátáit és irányát
            start_x = self.rotate_points[i].x
            start_y = self.rotate_points[i].y
            to_direction = self.rotate_points[i].direction
            # Az előtte lévőét is
            end_x = self.rotate_points[i - 1].x
            end_y = self.rotate_points[i - 1].y
            end_direction = self.rotate_points[i - 1].direction

            # Iránytól, és maradék hossztól függően megépítjük a téglalapokat
            if to_direction == Direction.LEFT:
                if length_in_pixels > start_x - end_x:
                    body_rect = pygame.Rect(end_x, end_y, start_x - end_x, self.size)
                    self.body_rects.append(body_rect)
                    length_in_pixels -= start_x - end_x
                    self.__setup_rotate_part(to_direction, end_direction, end_x, end_y)
                else:
                    body_rect = pygame.Rect(start_x - length_in_pixels, start_y, length_in_pixels, self.size)
                    self.body_rects.append(body_rect)
                    length_in_pixels = 0
            elif to_direction == Direction.RIGHT:
                if length_in_pixels > end_x - start_x:
                    body_rect = pygame.Rect(start_x + self.size, start_y, end_x - start_x, self.size)
                    self.body_rects.append(body_rect)
                    length_in_pixels -= end_x - start_x
                    self.__setup_rotate_part(to_direction, end_direction, end_x, end_y)
                else:
                    body_rect = pygame.Rect(start_x + self.size, start_y, length_in_pixels, self.size)
                    self.body_rects.append(body_rect)
                    length_in_pixels = 0
            elif to_direction == Direction.DOWN:
                if length_in_pixels > end_y - start_y:
                    body_rect = pygame.Rect(start_x, start_y + self.size, self.size, end_y - start_y)
                    self.body_rects.append(body_rect)
                    length_in_pixels -= end_y - start_y
                    self.__setup_rotate_part(to_direction, end_direction, end_x, end_y)
                else:
                    body_rect = pygame.Rect(start_x, start_y + self.size, self.size, length_in_pixels)
                    self.body_rects.append(body_rect)
                    length_in_pixels = 0
            elif to_direction == Direction.UP:
                if length_in_pixels > start_y - end_y:
                    body_rect = pygame.Rect(end_x, end_y, self.size, start_y - end_y)
                    self.body_rects.append(body_rect)
                    length_in_pixels -= start_y - end_y
                    self.__setup_rotate_part(to_direction, end_direction, end_x, end_y)
                else:
                    body_rect = pygame.Rect(end_x, end_y - length_in_pixels + start_y - end_y, self.size,
                                            length_in_pixels)
                    self.body_rects.append(body_rect)
                    length_in_pixels = 0

        # 5. Ha még maradt testhossz, de nincs további forgáspont, mint viszonyítási alap
        if length_in_pixels > 0:
            start_x = self.rotate_points[i - 1].x
            start_y = self.rotate_points[i - 1].y
            to_direction = self.rotate_points[i - 1].direction
            if to_direction == Direction.LEFT:
                body_rect = pygame.Rect(start_x - length_in_pixels, start_y, length_in_pixels, self.size)
                self.body_rects.append(body_rect)
            elif to_direction == Direction.RIGHT:
                body_rect = pygame.Rect(start_x + self.size, start_y, length_in_pixels, self.size)
                self.body_rects.append(body_rect)
            elif to_direction == Direction.DOWN:
                body_rect = pygame.Rect(start_x, start_y + self.size, self.size, length_in_pixels)
                self.body_rects.append(body_rect)
            elif to_direction == Direction.UP:
                body_rect = pygame.Rect(start_x, start_y - length_in_pixels, self.size, length_in_pixels)
                self.body_rects.append(body_rect)

        # 6. A továbbiakban teljesen haszontalan forgáspontoktól megszabadulunk
        self.rotate_points = self.rotate_points[i - 1:]
        # 7. A fent hozzáadatot forgáspontot (fej) töröljük, mert később változni fog a koordinátája
        self.rotate_points.pop()

    def __setup_rotate_part(self, direction, other_direction, x, y):
        """
        Beállítja az adott forgáspontra szükséges képet
        Paraméterek:
        direction: kiinduló forgáspont iránya
        other_direction: cél forgáspont iránya
        x: cél forgáspont x koordinátája
        y: cél forgáspont y koordinátája
        """

        if direction == Direction.LEFT and other_direction == Direction.UP:
            rotate_part = RotatePart(x, y, self.rotate_images[3])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.LEFT and other_direction == Direction.DOWN:
            rotate_part = RotatePart(x, y, self.rotate_images[2])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.RIGHT and other_direction == Direction.UP:
            rotate_part = RotatePart(x, y, self.rotate_images[1])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.RIGHT and other_direction == Direction.DOWN:
            rotate_part = RotatePart(x, y, self.rotate_images[0])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.DOWN and other_direction == Direction.LEFT:
            rotate_part = RotatePart(x, y, self.rotate_images[1])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.DOWN and other_direction == Direction.RIGHT:
            rotate_part = RotatePart(x, y, self.rotate_images[3])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.UP and other_direction == Direction.LEFT:
            rotate_part = RotatePart(x, y, self.rotate_images[0])
            self.rotate_parts.append(rotate_part)
        elif direction == Direction.UP and other_direction == Direction.RIGHT:
            rotate_part = RotatePart(x, y, self.rotate_images[2])
            self.rotate_parts.append(rotate_part)


class RotatePart:
    """A forgáspontra helyezett képet és koordinátát tárolja"""

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image


class RotatePoint:
    """Forgáspontok létrehozásáért felelős osztály"""

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def reverse(self):
        """Ellentétesre váltja a forgáspont irányát"""

        if self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.LEFT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.UP
        elif self.direction == Direction.UP:
            self.direction = Direction.DOWN
