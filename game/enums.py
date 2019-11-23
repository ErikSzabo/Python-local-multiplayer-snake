import enum
import pygame
pygame.init()


class Direction(enum.IntEnum):
    """Irányokat tároló enum"""

    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


class Color:
    BACKGROUND = (20, 20, 20)
    GREEN = (64, 138, 74)
    ORANGE = (138, 127, 64)
    WHITE = (200, 200, 200)
    TEXT = (100, 100, 100)
    LINE = (30, 30, 30)