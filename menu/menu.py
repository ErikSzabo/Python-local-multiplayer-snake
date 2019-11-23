import pygame
from utils import Utils, Image

class Menu:
    def __init__(self):
        self.surface = pygame.Surface((800, 600))
        self.full_exit = False
        self.current_position = 0  # legfelső elem
        self.max_position = 4 # legalsó elem
        self.player_number_pos = 1
        self.player_num = 2
        self.player_names = ["", ""]

    def redraw(self, window):        
        window.fill((20,20,20))
        self.surface.fill((20,20,20))
        color = (100,100,100)
        colors = [(100,100,100), (100,100,100), (100,100,100), (100,100,100), (100,100,100)]
        for i in range(len(colors)):
            if i == self.current_position:
                if self.player_num == 2:
                    colors[i] = (138,127,64)
                else:
                    colors[i] = (138,127,64)

        Utils.text_printer(self.surface, "Python Snake", 80, (64,138,74), (self.surface.get_width()/2, 55))

        Utils.text_printer(self.surface, "Játék", 60, colors[0], (self.surface.get_width()/2, 175))

        center_rect = Image.menu_left_arrow.get_rect(center=(self.surface.get_width()/2 - 200, 270))
        self.surface.blit(Image.menu_left_arrow, center_rect)

        Utils.text_printer(self.surface, "{}".format(self.player_num), 60, colors[1], (self.surface.get_width()/2, 270))

        center_rect = Image.menu_right_arrow.get_rect(center=(self.surface.get_width()/2 + 200, 270))
        self.surface.blit(Image.menu_right_arrow, center_rect)

        Utils.text_printer(self.surface, "Játékos nevek...", 20, color, (self.surface.get_width()/2, 330))

        centery = 380
        for i in range(self.player_num):
            Utils.input_box(self.surface, 300, 60, centery, colors[i+2])
            Utils.text_printer(self.surface, self.player_names[i], 20, (0, 0, 0), (self.surface.get_width()/2, centery))
            center_rect = Image.menu_control[i].get_rect(center=(self.surface.get_width()/2 - 110, centery))
            self.surface.blit(Image.menu_control[i], center_rect)
            centery += 80

        Utils.text_printer(self.surface, "Kilépés", 60, colors[-1], (self.surface.get_width()/2, 540))
        
        s_center_rect = self.surface.get_rect(center=(window.get_width()/2, window.get_height()/2))
        window.blit(self.surface, s_center_rect)
        pygame.display.update()


    def navigation(self, key, window):
        if key == pygame.K_DOWN:
            if self.current_position < self.max_position:
                if self.player_num == 1 and self.current_position == self.max_position - 2:
                    self.current_position = self.max_position
                else:
                    self.current_position += 1
        elif key == pygame.K_UP:
            if self.current_position > 0:
                if self.player_num == 1 and self.current_position == self.max_position:
                    self.current_position -= 2
                else:
                    self.current_position -= 1
        elif key == pygame.K_RIGHT:
            if self.current_position == self.player_number_pos:
                if self.player_num == 1:
                    self.player_num += 1
        elif key == pygame.K_LEFT:
            if self.current_position == self.player_number_pos:
                if self.player_num == 2:
                    self.player_num -= 1
        elif key == pygame.K_RETURN:
            if self.current_position == 0:
                return True
            elif self.current_position == self.max_position:
                self.full_exit = True
                return True
        self.redraw(window)
        return False

    def name_input_handler(self, key, window, key_unicode = ""):
        if key == pygame.K_BACKSPACE:
            if self.current_position == 2:
                self.player_names[0] = self.player_names[0][0:len(self.player_names[0])-1]
            elif self.current_position == 3:
                self.player_names[1] = self.player_names[1][0:len(self.player_names[1])-1]
        else:
            if self.current_position == 2:
                self.player_names[0] += key_unicode
                self.redraw(window)
            elif self.current_position == 3:
                self.player_names[1] += key_unicode
        self.redraw(window)
