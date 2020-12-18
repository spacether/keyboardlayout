from collections import defaultdict
from enum import Enum
from importlib import resources
import os
from pathlib import Path
from typing import (
    Tuple,
    Optional,
    Union
)

import yaml

from . import layouts
from .key import Key
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
        color: Union['pygame.Color', TkinterColor],
        txt_color: Union['pygame.Color', TkinterColor],
        txt_font: Union['pygame.font.SysFont', 'tkinter.font.Font'],
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
        color: Optional[Union['pygame.Color', TkinterColor]]=None
    ):
        self.position = position
        self.padding = padding
        self.color = color


class Rect:
    """
    This class is internally used by keyboardlayout to store
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


class TxtBase:
    @staticmethod
    def _get_position(
        horizontal_anchor: HorizontalAnchor,
        vertical_anchor: VerticalAnchor,
        x: int,
        y: int,
        txt_width: int,
        txt_height: int
    ):
        if vertical_anchor is VerticalAnchor.TOP:
            yloc = y
        elif vertical_anchor is VerticalAnchor.MIDDLE:
            yloc = y - txt_height//2
        elif vertical_anchor is VerticalAnchor.BOTTOM:
            yloc = y - txt_height
        if horizontal_anchor is HorizontalAnchor.LEFT:
            xloc = x
        elif horizontal_anchor is HorizontalAnchor.CENTER:
            xloc = x - txt_width//2
        elif horizontal_anchor is HorizontalAnchor.RIGHT:
            xloc = x - txt_width
        return xloc, yloc


class KeyboardLayoutBase:
    @staticmethod
    def _get_txt_pos_info(
        txt_anchor: str,
        x: int,
        y: int,
        key_info: KeyInfo,
        r: Rect
    ):
        key_padding = key_info.margin//2
        vertical_anchor = VerticalAnchor(txt_anchor[:1])
        horizontal_anchor = HorizontalAnchor(txt_anchor[1:])
        if vertical_anchor is VerticalAnchor.TOP:
            yloc = y + key_padding + key_info.txt_padding[1]
        elif vertical_anchor is VerticalAnchor.MIDDLE:
            yloc = y + r.height//2
        elif vertical_anchor is VerticalAnchor.BOTTOM:
            yloc = y + r.height - key_padding - key_info.txt_padding[1]
        if horizontal_anchor is HorizontalAnchor.LEFT:
            xloc = x + key_padding + key_info.txt_padding[0]
        elif horizontal_anchor is HorizontalAnchor.CENTER:
            xloc = x + r.width//2
        elif horizontal_anchor is HorizontalAnchor.RIGHT:
            xloc = x + r.width - key_padding - key_info.txt_padding[0]
        return horizontal_anchor, vertical_anchor, xloc, yloc

    def _get_max_size_and_set_info_dicts(
        self,
        layout: dict,
        keyboard_info: KeyboardInfo,
        letter_key_size: Tuple[int],
        key_info: KeyInfo,
    ):
        letter_key_width, letter_key_height = letter_key_size
        max_width = 0
        max_height = 0
        key_size = layout[LayoutYamlConstant.KEY_SIZE]
        self._rect_by_key_and_loc = defaultdict(dict)
        self._txt_info_by_loc = {}
        xanchor = keyboard_info.position[0] + keyboard_info.padding
        yanchor = keyboard_info.position[1] + keyboard_info.padding
        if key_info.margin:
            xanchor += -key_info.margin//2
            yanchor += -key_info.margin//2

        for row_ind, row in enumerate(layout[LayoutYamlConstant.ROWS]):
            row_max_width = 0
            row_x_keycoords, row_y_keycoords = row[LayoutYamlConstant.LOCATION]
            key_x = xanchor + row_x_keycoords * letter_key_width
            key_y = yanchor + row_y_keycoords * letter_key_height
            key_size = row.get(LayoutYamlConstant.KEY_SIZE, key_size)

            for row_key_ind, row_key in enumerate(row[LayoutYamlConstant.KEYS]):
                key_xsize_keycoords, key_ysize_keycoords = row_key.get(
                    LayoutYamlConstant.SIZE, key_size)

                key_width, key_height = (
                    letter_key_width*key_xsize_keycoords,
                    letter_key_height*key_ysize_keycoords
                )

                row_max_width += key_width

                row_y = row_y_keycoords * letter_key_height
                key_ymax = row_y + key_height
                if key_ymax > max_height:
                    max_height = key_ymax

                """
                does not include key margins
                drawn key rect will be smaller than this if mey_info.margin
                is set
                """
                rect = Rect(key_x, key_y, key_width, key_height)
                key_name = row_key[LayoutYamlConstant.NAME]
                key = Key(key_name)
                loc = (row_ind, row_key_ind)
                self._rect_by_key_and_loc[key][loc] = rect
                self._txt_info_by_loc[loc] = (
                    row_key[LayoutYamlConstant.TXT_INFO])
                key_x += key_width

            if row_max_width > max_width:
                max_width = row_max_width

        return max_width, max_height
