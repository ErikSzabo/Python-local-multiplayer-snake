import pygame
from game.constants import Color
from utils import Utils, Stat


class EndScreen:
    """
    Eredmény kijelző képernyőért felelős osztály.
    Attribútumok:
        players: Snake objektumokból álló játékos lista
        highscores: Stat objektumokból álló toplista
    """

    def __init__(self, players):
        self.players = players
        self.highscores = Utils.load_highscores()
        self.__add_players_to_highscores()
        self.highscores.sort(key=lambda highscores: highscores.score, reverse=True)
        Utils.save_highscores(self.highscores)

    def draw(self, window):
        """
        Újra rajzolja az ablakot.
        Paraméterek:
            window: pygame surface amire rajzolni kell
        """

        window.fill(Color.BACKGROUND)

        if len(self.players) > 1:
            if self.players[0].is_lost and self.players[1].is_lost:
                if self.players[0].score == self.players[1].score:
                    Utils.text_printer(window, "Döntetlen!", 40, Color.WHITE, (window.get_width() / 2, 60))
                else:
                    name = self.players[0].name if self.players[0].score > self.players[1].score else self.players[1].name
                    Utils.text_printer(window, "Nyertes: {}".format(name), 40, Color.WHITE, (window.get_width() / 2, 60))
            elif self.players[0].is_lost:
                Utils.text_printer(window, "Nyertes: {}".format(self.players[1].name), 40, Color.WHITE, (window.get_width()/2, 60))
            elif self.players[1].is_lost:
                Utils.text_printer(window, "Nyertes: {}".format(self.players[0].name), 40, Color.WHITE, (window.get_width()/2, 60))
        else:
            Utils.text_printer(window, "{}: {}".format(self.players[0].name, self.players[0].score), 50, Color.WHITE, (window.get_width()/2, 60))

        Utils.text_printer(window, "TOPLISTA", 60, Color.TEXT, (window.get_width()/2, 120))

        y = 180
        i = 0
        while i < 10 and i < len(self.highscores):
            Utils.text_printer(window, "{} - {}".format(self.highscores[i].name, self.highscores[i].score), 25, Color.TEXT, (window.get_width()/2, y))
            y += 40
            i += 1

        pygame.display.update()

    def __add_players_to_highscores(self):
        """
        Ha a játékosok megfelelnek a követelményeknek, akkor hozzáadja őket a toplistához.
        Követelmények:
            Ha még nincs 10 ember a toplistában akkor: pontszám > 0
            Ha van már 10 ember akkor: pontszám > 0 és az utolsónál több pont
            Ha már benne van a toplistában: Az előzőnél nagyobb pontszám
        """
        for player in self.players:
            already_in = False
            if player.score <= 0:
                continue
            for record in self.highscores:
                if player.name == record.name:
                    already_in = True
                    if player.score > record.score:
                        record.score = player.score
            if not already_in and len(self.highscores) < 10:
                stat = Stat(player.name, player.score)
                self.highscores.append(stat)
            elif not already_in and player.score > self.highscores[-1].score:
                stat = Stat(player.name, player.score)
                self.highscores.append(stat)