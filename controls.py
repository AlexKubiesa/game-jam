from enum import Enum, auto
from pygame.locals import *


class Button(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SHOOT = auto()


__player_controls = {
    1: {
        Button.UP: K_w,
        Button.DOWN: K_s,
        Button.LEFT: K_a,
        Button.RIGHT: K_d,
        Button.SHOOT: K_SPACE
    },

    2: {
        Button.UP: K_UP,
        Button.DOWN: K_DOWN,
        Button.LEFT: K_LEFT,
        Button.RIGHT: K_RIGHT,
        Button.SHOOT: K_KP0
    }
}


def get_controls(player_index):
    return __player_controls[player_index]
