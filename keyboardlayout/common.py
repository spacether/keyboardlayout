from typing import (
    Tuple,
    Optional,
    Union
)
from enum import Enum
from pathlib import Path
import os
from importlib import resources

import pygame
import yaml

from . import layouts
YAML_EXTENSION = '.yaml'

class TkinterColor(str):
    pass

def __generate_keyboard_layout_enum():
    layout_names = []
    for file_name in resources.contents(layouts):
        if file_name.endswith(YAML_EXTENSION):
            layout_names.append(file_name[:-len(YAML_EXTENSION)])

    layout_name_enum = Enum(
        'LayoutName',
        {layout_name.upper(): layout_name for layout_name in layout_names}
    )
    layout_name_enum.__doc__ = (
        "An enum that holds the allowed layout names")
    return layout_name_enum

LayoutName = __generate_keyboard_layout_enum()

class VerticalAnchor(Enum):
    """Enums used to set vertical text location"""
    TOP = 't'
    MIDDLE = 'm'
    BOTTOM = 'b'

class HorizontalAnchor(Enum):
    """Enums used to set horizontal text location"""
    LEFT = 'l'
    CENTER = 'c'
    RIGHT = 'r'

class LayoutYamlConstant:
    """Constants used to acces data in keyboard layout yaml files"""
    KEY_SIZE = 'key_size'
    ROWS = 'rows'
    NAME = 'name'
    LOCATION = 'location'
    SIZE = 'size'
    TXT_INFO = 'txt_info'
    KEYS = 'keys'


class Rect:
    """
    This class is internally used by keyboardlayout with tkinter to store
    rectangles

    Args:
        x: the left x position in pixels
        y: the top y position in pixels
        width: the width in pixels
        height: the height in pixels
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class KeyInfo:
    """
    The needed key inputs for KeyboardLayout

    Args:
        margin: the gap between keys in pixels.
            this should be an even number
        color: the key background color
        txt_color: the color used for key text
        txt_font: the font used to write key text
        txt_padding: x, y padding in pixes
            from the edges of the key background rectangle
    """
    def __init__(
        self,
        margin: int,
        color: Union[pygame.Color, TkinterColor],
        txt_color: Union[pygame.Color, TkinterColor],
        txt_font: pygame.font.SysFont,
        txt_padding: Tuple[int, int],
    ):
        self.margin = margin
        self.color = color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_padding = txt_padding


class KeyboardInfo:
    """
    The needed keyboard inputs for KeyboardLayout

    Args:
        position: x, y top left position in pixels
        padding: the padding used on all sides in pixels
        color: the background color to use
    """
    def __init__(
        self,
        position: Tuple[int, int],
        padding: int,
        color: Optional[Union[pygame.Color, TkinterColor]]=None
    ):
        self.position = position
        self.padding = padding
        self.color = color
