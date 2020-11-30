import typing
from types import ModuleType
from enum import Enum
from pathlib import Path
import yaml
import os

import pygame
import keyboardlayout

CURRENT_WORKING_DIR = Path(__file__).parent.absolute()

def init_pygame_and_draw_keyboard(layout_name: str):
    pygame.init()
    pygame.display.set_caption("{} keyboard layout".format(layout_name))

    keyboard = get_keyboard(layout_name, (0, 0))

    screen = pygame.display.set_mode(
        (keyboard.rect.width, keyboard.rect.height))
    screen.fill(pygame.Color('black'))

    keyboard.draw(screen)
    pygame.display.update()

def run_until_window_closed():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def get_keyboard(
    layout_name: str,
    position: typing.List[int]
) -> keyboardlayout.KeyboardLayout:
    letter_key_size = (60, 60) # width, height
    keyboard_padding = 2
    key_margin = 10
    key_color = pygame.Color('grey')
    font_color = key_color.__invert__()

    font_size = letter_key_size[0]//4
    font = pygame.font.SysFont('Arial', font_size)
    font_color = key_color.__invert__()
    txt_padding = (letter_key_size[0]//6, letter_key_size[0]//10)

    keyboard_layout = keyboardlayout.KeyboardLayout(
        layout_name,
        position,
        keyboard_padding,
        letter_key_size,
        key_margin,
        key_color,
        font_color,
        font,
        txt_padding,
        keyboard_color=font_color
    )
    # keyboard_layout.update_key(
    #     "return",
    #     bg_color=pygame.Color('white'),
    #     font_color=pygame.Color('red')
    # )
    return keyboard_layout


if __name__=="__main__":
    layout_name = 'qwerty'
    # layout_name = 'azerty_laptop'
    screen = init_pygame_and_draw_keyboard(layout_name)
    run_until_window_closed()
