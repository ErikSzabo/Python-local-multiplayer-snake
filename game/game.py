import pygame
import winsound
from utils import Utils, Image
from game.food import Food, SuperFood

class Game:
    """Játékmenetet vezérlő osztály"""

    def __init__(self, players, display, grid_size):
        self.players = players
        self.highscore = 0
        self.grid_size = grid_size
        self.field_start_y = 80
        
        for i in range(display.height):
            if (self.field_start_y + i) % self.grid_size == 0:
                self.field_start_y = self.field_start_y + i
                break

        self.food = Food(display.width, display.height, grid_size, self.field_start_y, Image.food_image)
        self.super_food = SuperFood(display.width, display.height, grid_size, self.field_start_y, Image.super_food_image)
        
        self.food.recreate(self.players, self.super_food)
        
        highscores = Utils.load_highscores()
        if highscores != []:
            self.highscore = highscores[0].score

    def start_game(self, display):
        """
        Játékmenet kontrollore
        Paraméterek:
        display: DisplayMonitor
        """

        quit = False
        timer = pygame.time.Clock()
        while not quit:
            # 60 FPS
            timer.tick(60)

            # Event loop
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit = True
                
                if event.type == pygame.KEYDOWN:
                    for player in self.players:
                        player.controlled_move(event)

            for player in self.players:
                # ha nem mozdult gombokkal akkor mozdítsuk a kigyot a jelenlegi irányba tovább
                if not player.key_pressed:
                    player.move()
                
                # ha saját magába, vagy a falba ment, akkor a játéknak vége
                if player.detect_self_collision() or player.detect_wall_collision(display.width, display.height, self.field_start_y):
                    player.is_lost = True
                    quit = True
                    winsound.PlaySound("sounds/dead.wav", 1)
    
                # új highscore beállitása ha valamelyik player meghaladta az eddigi legmagasabbat
                if player.score > self.highscore:
                    self.highscore = player.score 

                # Alma felvétel kezelése
                if player.detect_food_collision(self.food):
                    self.food.recreate(self.players, self.super_food)
                    player.score += 1
                    player.length += 1
                    winsound.PlaySound("sounds/eat.wav", 1)

                # Szuper alma felvétel kezelése
                if player.detect_food_collision(self.super_food):
                    player.score += 5
                    player.length += 1
                    self.super_food.handle_collision()
                    winsound.PlaySound("sounds/eat.wav", 1)

                # Alapértékre állítás, nem nyomott irányváltoztató gombot
                player.key_pressed = False

                # Esetleges új sebességek beállítása
                player.calculate_velocity()
            
            # Kétjátékos módban ha egymásba mentek akkor a játéknak vége
            if len(self.players) > 1:
                j = len(self.players) - 1
                for i in range(len(self.players)):
                    if self.players[i].detect_enemy_collision(self.players[j]):
                        self.players[i].is_lost = True
                        quit = True
                        winsound.PlaySound("sounds/dead.wav", 1)
                    j -= 1

            # Szuper alma megfelelő számlálójának növelése
            self.super_food.update_counters()

            # Megnézzük és eltüntetjük a szuper almát ha kell
            self.super_food.check_for_remove()

            # Ha még nincs szuper almánk és idő van, 30% eséllyel spawnol egy
            self.super_food.check_for_spawn(self.players, self.food)      

            # újra rajzoljuk a képernyőt
            self.redraw(display)

    def redraw(self, display):
        """
        Újra rajzolja a képernyőt a játékállásnak megfelelően
        Paraméterek:
        display: DisplayMonitor
        """

        display.window.fill((20,20,20))

        for x in range(0, display.width+1, self.grid_size):
            pygame.draw.line(display.window, (30,30,30), (x, self.field_start_y), (x, display.height))
        for j in range(self.field_start_y, display.height+1, self.grid_size):
            pygame.draw.line(display.window, (30,30,30), (0, j), (display.width, j))
        
        self.food.draw(display.window)
        
        if self.super_food.visible:
            self.super_food.draw(display.window)

        for i in range(len(self.players)):
            self.players[i].draw(display.window)
       
        x = [display.real_width/4 * 3, display.real_width/4]
        for i in range(len(self.players)):
            Utils.text_printer(display.window, "{}: {}".format(self.players[i].name, self.players[i].score), 30, self.players[i].color, (x[i], 35))
            
        Utils.text_printer(display.window, "HIGHSCORE", 30, (200,200,200), (display.real_width / 2, 20))
        Utils.text_printer(display.window, str(self.highscore), 30, (200,200,200), (display.real_width / 2, 50))

        pygame.display.update()