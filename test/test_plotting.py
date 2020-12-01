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

    key_size = 60
    grey = pygame.Color('grey')
    key_info = keyboardlayout.KeyInfo(
        size=(key_size, key_size),  # width, height
        margin=10,
        color=grey,
        txt_color=~grey,  # invert grey
        txt_font=pygame.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10),
    )
    keyboard_info = keyboardlayout.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=~grey
    )
    keyboard_layout = keyboardlayout.KeyboardLayout(
        layout_name,
        keyboard_info,
        key_info,
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
