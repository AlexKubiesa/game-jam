from enum import Enum, auto
from pygame.locals import *
import pygame.key


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


def get_controls(player_id):
    return __player_controls[player_id]


def get_button_pressed(controls):
    key_states = pygame.key.get_pressed()
    return {button: key_states[controls[button]] for button in Button}
