import typing
from enum import Enum
from pathlib import Path
import yaml
import os
from collections import defaultdict

import pygame

LAYOUTS_DIR = Path(__file__).parent.absolute().joinpath("layouts")
YAML_EXTENSION = '.yaml'


def __generate_keyboard_layout_enum():
    layout_names = []
    for (_dir_path, _dir_names, file_names) in os.walk(LAYOUTS_DIR):
        for file_name in file_names:
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

class TxtSprite(pygame.sprite.Sprite):
    """A sprite that contains text"""
    def __init__(
        self,
        x: int,
        y: int,
        horizontal_anchor: HorizontalAnchor,
        vertical_anchor: VerticalAnchor,
        txt: str,
        font: pygame.font.SysFont,
        txt_color: pygame.Color,
    ):
        super().__init__()
        self.image = font.render(txt, 1, txt_color)

        txt_width = self.image.get_width()
        txt_height = self.image.get_height()

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
        self.rect = pygame.Rect(xloc, yloc, txt_width, txt_height)


class RectSprite(pygame.sprite.Sprite):
    """A sprite that contains a filled rectangle"""
    def __init__(
        self,
        r: pygame.Rect,
        color: pygame.Color,
    ):
        super().__init__()
        self.image = pygame.Surface([r.width, r.height])
        self.image.fill(color)
        self.rect = pygame.Rect(r.x, r.y, r.width, r.height)


class KeyInfo:
    """The needed key inputs for KeyboardLayout"""
    def __init__(
        self,
        margin: int,
        color: pygame.Color,
        txt_color: pygame.Color,
        txt_font: pygame.font.SysFont,
        txt_padding: typing.Tuple[int],
    ):
        self.margin = margin
        self.color = color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_padding = txt_padding


class KeyboardInfo:
    """The needed keyboard inputs for KeyboardLayout"""
    def __init__(
        self,
        position: typing.Tuple[int],
        padding: int,
        color: typing.Optional[pygame.Color]=None
    ):
        self.position = position
        self.padding = padding
        self.color = color


class KeyboardLayout(pygame.sprite.Group):
    """
    Makes a sprite group that stores a keyboard layout image

    Args:
        layout_name: must be a string in the LayoutName enum
        keyboard_info: the settings for the keyboard
        letter_key_size: the horizontal and vertical size in px of letter keys
        key_info: the settings for the keys
        overrides: Optional; a dict that lets one override key settings

    Attributes:
        _key_name_to_sprite_group (dict): a dict that goes from
            key_name (str) to pygame.sprite.Group instances
    """
    @staticmethod
    def __max_width(
        letter_key_width: int,
        layout: dict,
    ):
        max_width = 0
        key_size = layout[LayoutYamlConstant.KEY_SIZE]
        for row in layout[LayoutYamlConstant.ROWS]:
            row_max_width = 0
            key_size = row.get(LayoutYamlConstant.KEY_SIZE, key_size)
            for row_key in row[LayoutYamlConstant.KEYS]:
                key_xsize_keycoords, _ = row_key.get(
                    LayoutYamlConstant.SIZE, key_size)
                key_width = letter_key_width * key_xsize_keycoords
                row_max_width += key_width
            if row_max_width > max_width:
                max_width = row_max_width
        return max_width

    @staticmethod
    def __max_height(
        letter_key_height: int,
        layout: dict,
    ):
        height_max = 0
        key_size = layout[LayoutYamlConstant.KEY_SIZE]
        for row in layout[LayoutYamlConstant.ROWS]:
            key_size = row.get(LayoutYamlConstant.KEY_SIZE, key_size)
            for row_key in row[LayoutYamlConstant.KEYS]:
                _, key_ysize_keycoords = row_key.get(
                    LayoutYamlConstant.SIZE, key_size)
                _, row_y_keycoords = row[LayoutYamlConstant.LOCATION]
                row_y = row_y_keycoords * letter_key_height
                key_height = letter_key_height * key_ysize_keycoords
                key_ymax = row_y + key_height
                if key_ymax > height_max:
                    height_max = key_ymax
        return height_max

    def __get_key_sprites(
        self,
        key_name: str,
        loc: typing.Tuple[int],
        key_info: KeyInfo,
    ):
        key_loc_to_rect = self.__rect_by_key_name_and_loc[key_name]
        r = key_loc_to_rect[loc]
        x, y, width, height = r.x, r.y, r.width, r.height
        key_padding = key_info.margin//2

        """
        If there are multiple rects for a key
        Check if this is the mind width one. If so then make the height taller
        """
        y_delta = 0
        height_delta = 0
        if len(key_loc_to_rect) == 2:
            locs = list(set(key_loc_to_rect))
            other_loc = locs[not locs.index(loc)]
            other_r = key_loc_to_rect[other_loc]
            if r.width < other_r.width:
                below_other = r.y > other_r.y
                if below_other:
                    y_delta = -key_info.margin
                    height_delta = key_info.margin
                else:
                    height_delta = key_info.margin

        r = pygame.Rect(
            x+key_padding,
            y+key_padding + y_delta,
            width-2*key_padding,
            height-2*key_padding + height_delta,
        )
        key_sprites = []
        bg_sprite = RectSprite(r, key_info.color)
        key_sprites.append(bg_sprite)

        txt_sprites = []
        txt_info = self.__txt_info_by_loc[loc]
        for txt_anchor, label_txt in txt_info.items():
            vertical_anchor = VerticalAnchor(txt_anchor[:1])
            horizontal_anchor = HorizontalAnchor(txt_anchor[1:])
            if vertical_anchor is VerticalAnchor.TOP:
                yloc = y + key_padding + key_info.txt_padding[1]
            elif vertical_anchor is VerticalAnchor.MIDDLE:
                yloc = y + height//2
            elif vertical_anchor is VerticalAnchor.BOTTOM:
                yloc = y + height - key_padding - key_info.txt_padding[1]
            if horizontal_anchor is HorizontalAnchor.LEFT:
                xloc = x + key_padding + key_info.txt_padding[0]
            elif horizontal_anchor is HorizontalAnchor.CENTER:
                xloc = x + width//2
            elif horizontal_anchor is HorizontalAnchor.RIGHT:
                xloc = x + width - key_padding - key_info.txt_padding[0]
            txt_sprite = TxtSprite(
                xloc,
                yloc,
                horizontal_anchor,
                vertical_anchor,
                label_txt,
                key_info.txt_font,
                key_info.txt_color
            )
            key_sprites.append(txt_sprite)

        return key_sprites

    def __init__(
        self,
        layout_name: str,
        keyboard_info: KeyboardInfo,
        letter_key_size: typing.Tuple[int],
        key_info: KeyInfo,
        overrides: typing.Optional[typing.Dict[str, KeyInfo]] = None
    ):
        super().__init__()

        layout_name = LayoutName(layout_name)
        layout_path = LAYOUTS_DIR.joinpath(layout_name.value + YAML_EXTENSION)
        stream = open(layout_path, 'r')
        layout = yaml.safe_load(stream)
        self._key_name_to_sprite_group = defaultdict(pygame.sprite.Group)

        letter_key_width, letter_key_height = letter_key_size

        x, y = keyboard_info.position
        xanchor = x + keyboard_info.padding
        yanchor = y + keyboard_info.padding
        if key_info.margin:
            xanchor += -key_info.margin//2
            yanchor += -key_info.margin//2
        xmax = 0
        ymax = 0
        max_width = self.__max_width(letter_key_width, layout)
        max_height = self.__max_height(letter_key_height, layout)
        self.rect = pygame.Rect(
            x,
            y,
            max_width - key_info.margin + 2*keyboard_info.padding,
            max_height - key_info.margin + 2*keyboard_info.padding,
        )
        if keyboard_info.color:
            bg_sprite = RectSprite(self.rect, keyboard_info.color)
            self.add(bg_sprite)

        self.__rect_by_key_name_and_loc = defaultdict(dict)
        self.__txt_info_by_loc = {}
        key_size = layout[LayoutYamlConstant.KEY_SIZE]
        for row_ind, row in enumerate(layout[LayoutYamlConstant.ROWS]):
            row_x_keycoords, row_y_keycoords = row[LayoutYamlConstant.LOCATION]
            key_x = xanchor + row_x_keycoords * letter_key_width
            key_y = yanchor + row_y_keycoords * letter_key_height
            key_size = row.get(LayoutYamlConstant.KEY_SIZE, key_size)
            for row_key_ind, row_key in enumerate(row[LayoutYamlConstant.KEYS]):
                key_xsize_keycoords, key_ysize_keycoords = (
                    row_key.get(LayoutYamlConstant.SIZE, key_size))
                key_width, key_height = (
                    letter_key_width*key_xsize_keycoords,
                    letter_key_height*key_ysize_keycoords
                )
                rect = pygame.Rect(key_x, key_y, key_width, key_height)
                key_name = row_key[LayoutYamlConstant.NAME]
                loc = (row_ind, row_key_ind)
                self.__rect_by_key_name_and_loc[key_name][loc] = rect
                self.__txt_info_by_loc[loc] = (
                    row_key[LayoutYamlConstant.TXT_INFO])
                key_x += key_width

        for row_ind, row in enumerate(layout[LayoutYamlConstant.ROWS]):
            for row_key_ind, row_key in enumerate(row[LayoutYamlConstant.KEYS]):
                key_name = row_key[LayoutYamlConstant.NAME]
                used_key_info = key_info
                if overrides:
                    used_key_info = overrides.get(key_name, used_key_info)
                loc = (row_ind, row_key_ind)
                key_sprites = self.__get_key_sprites(
                    key_name,
                    loc,
                    used_key_info,
                )
                self.add(*key_sprites)
                self._key_name_to_sprite_group[key_name].add(*key_sprites)


    def update_key(
        self,
        key_name: str,
        key_info: KeyInfo,
    ):
        """Update the color and txt_color for key_name"""
        key_sprite_group = self._key_name_to_sprite_group[key_name]
        self.remove(key_sprite_group.sprites())
        key_sprite_group.empty()
        for loc in self.__rect_by_key_name_and_loc[key_name]:
            key_sprites = self.__get_key_sprites(
                key_name,
                loc,
                key_info,
            )
            self.add(*key_sprites)
            key_sprite_group.add(*key_sprites)
