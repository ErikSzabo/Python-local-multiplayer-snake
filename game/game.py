import pygame
import winsound
from utils import text_printer, load_highscores
from images import Image
from display import window
from surfaces import GameSurface, GameFieldSurface
from game.food import Food, SuperFood
from game.constants import Color


class Game:
    def __init__(self, players):
        highscores = load_highscores()
        self.highscore = highscores[0].score if highscores else 0
        self.players = players
        self.squares = (17, 15)
        self.game_surface: GameSurface = GameSurface(window)
        self.field: GameFieldSurface = GameFieldSurface(self.game_surface, self.squares)
        self.food = Food(self.field, Image.food_image)
        self.super_food = SuperFood(self.field, Image.super_food_image)
        self.food.recreate(self.players, self.super_food, self.field.grid_size)
        player_starting_xs = [self.field.grid_size * (i * 3 + 4) for i in range(len(self.players))]
        for i in range(len(self.players)):
            self.players[i].x = player_starting_xs[i]

    def start(self):
        """Játékmenet vezérlője."""

        end = False
        timer = pygame.time.Clock()
        pygame.event.set_allowed(pygame.KEYDOWN)

        while not end:
            # 60 FPS
            timer.tick(60)

            # Event loop
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        end = True
                
                if event.type == pygame.KEYDOWN:
                    for player in self.players:
                        player.controlled_move(event, self.field.grid_size)

            for player in self.players:
                # ha nem mozdult gombokkal akkor mozdítsuk a kigyot a jelenlegi irányba tovább
                if not player.key_pressed:
                    player.move(self.field.grid_size)
                
                # ha saját magába, vagy a falba ment, akkor a játéknak vége
                if player.detect_self_collision(self.field.grid_size) or player.detect_wall_collision(self.field):
                    player.is_lost = True
                    end = True
                    winsound.PlaySound("assets/sounds/dead.wav", 1)
    
                # új highscore beállitása ha valamelyik player meghaladta az eddigi legmagasabbat
                if player.score > self.highscore:
                    self.highscore = player.score 

                # Alma felvétel kezelése
                if player.detect_food_collision(self.food, self.field.grid_size):
                    self.food.recreate(self.players, self.super_food, self.field.grid_size)
                    player.score += 1
                    player.length += 1
                    winsound.PlaySound("assets/sounds/eat.wav", 1)

                # Szuper alma felvétel kezelése
                if player.detect_food_collision(self.super_food, self.field.grid_size):
                    player.score += 5
                    player.length += 1
                    self.super_food.handle_collision()
                    winsound.PlaySound("assets/sounds/eat.wav", 1)

                # Alapértékre állítás, nem nyomott irányváltoztató gombot
                player.key_pressed = False

                # Esetleges új sebességek beállítása
                player.calculate_velocity()
            
            # Kétjátékos módban ha egymásba mentek akkor a játéknak vége
            if len(self.players) > 1:
                j = len(self.players) - 1
                for i in range(len(self.players)):
                    if self.players[i].detect_enemy_collision(self.players[j], self.field.grid_size):
                        self.players[i].is_lost = True
                        end = True
                        winsound.PlaySound("assets/sounds/dead.wav", 1)
                    j -= 1

            # Szuper alma megfelelő számlálójának növelése
            self.super_food.update_counters()

            # Megnézzük és eltüntetjük a szuper almát ha kell
            self.super_food.check_for_remove()

            # Ha még nincs szuper almánk és idő van, 30% eséllyel spawnol egy
            self.super_food.check_for_spawn(self.players, self.food, self.field.grid_size)      

            # újra rajzoljuk a képernyőt
            self.redraw()

    def redraw(self):
        """Újra rajzolja a képernyőt a játékállásnak megfelelően."""

        self.game_surface.redraw(self.players, self.highscore)
        self.field.redraw()

        self.food.draw(self.field.surface)
        
        if self.super_food.visible:
            self.super_food.draw(self.field.surface)

        for i in range(len(self.players)):
            self.players[i].draw(self.field.surface)
        
        self.field.blit()
        self.game_surface.scaled_blit_to_parent()

        pygame.display.update()