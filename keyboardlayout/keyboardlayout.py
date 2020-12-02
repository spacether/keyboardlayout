import typing
from enum import Enum
from pathlib import Path
import yaml
import os

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
        font_color: pygame.Color,
    ):
        super().__init__()
        self.font_color = font_color
        self.txt = txt
        self.font = font
        self.render_text()

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

    def render_text(self):
        self.image = self.font.render(self.txt, 1, self.font_color)


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


class Key:
    """
    Contains a key's background sprites and text sprites.
    This class allows us to change the key color and text color.
    """
    def __init__(
        self,
        bg_sprites: pygame.sprite.Group,
        txt_sprites: pygame.sprite.Group
    ):
        self.bg_sprites = bg_sprites
        self.txt_sprites = txt_sprites


class KeyInfo:
    """The needed key inputs for KeyboardLayout"""
    def __init__(
        self,
        size: typing.Tuple[int],
        margin: int,
        color: pygame.Color,
        txt_color: pygame.Color,
        txt_font: pygame.font.SysFont,
        txt_padding: typing.Tuple[int],
    ):
        self.size = size
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
    The class that stores the keyboard layout.
    This is the class that developers will use.
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

    def __make_stitcher_sprite(
        self,
        existing_bg_sprite: pygame.sprite.Sprite,
        new_bg_sprite: pygame.sprite.Sprite,
        key_info: KeyInfo,
    ):
        if existing_bg_sprite.rect.width < new_bg_sprite.rect.width:
            used_rect = existing_bg_sprite.rect
            used_y = used_rect.bottom
        else:
            used_rect = new_bg_sprite.rect
            used_y = used_rect.top - key_info.margin
        r = pygame.Rect(
            used_rect.left,
            used_y,
            used_rect.width,
            key_info.margin,
        )
        sticher_sprite = RectSprite(r, key_info.color)
        return sticher_sprite

    @staticmethod
    def __get_key_sprites(
        r: pygame.Rect,
        key_info: KeyInfo,
        txt_info: typing.Dict[str, str],
    ):
        x, y, width, height = r.x, r.y, r.width, r.height
        key_padding = key_info.margin//2
        r = pygame.Rect(
            x+key_padding,
            y+key_padding,
            width-2*key_padding,
            height-2*key_padding,
        )
        sprites = []
        bg_sprite = RectSprite(r, key_info.color)
        sprites.append(bg_sprite)

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
            sprites.append(txt_sprite)

        return sprites

    def __init__(
        self,
        layout_name: str,
        keyboard_info: KeyboardInfo,
        key_info: KeyInfo,
    ):
        super().__init__()

        layout_name = LayoutName(layout_name)
        layout_path = LAYOUTS_DIR.joinpath(layout_name.value + YAML_EXTENSION)
        stream = open(layout_path, 'r')
        layout = yaml.safe_load(stream)
        self._key_name_to_key = {}

        letter_key_width, letter_key_height = key_info.size

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
        key_size = layout[LayoutYamlConstant.KEY_SIZE]
        for row in layout[LayoutYamlConstant.ROWS]:
            row_keys = row[LayoutYamlConstant.KEYS]
            key_names = set(key[LayoutYamlConstant.NAME] for key in row_keys)

            row_x_keycoords, row_y_keycoords = row[LayoutYamlConstant.LOCATION]
            key_x = xanchor + row_x_keycoords * letter_key_width
            key_y = yanchor + row_y_keycoords * letter_key_height
            key_size = row.get(LayoutYamlConstant.KEY_SIZE, key_size)
            for row_key in row_keys:
                key_xsize_keycoords, key_ysize_keycoords = (
                    row_key.get(LayoutYamlConstant.SIZE, key_size))
                key_width, key_height = (
                    letter_key_width*key_xsize_keycoords,
                    letter_key_height*key_ysize_keycoords
                )
                rect = pygame.Rect(key_x, key_y, key_width, key_height)
                key_sprites = self.__get_key_sprites(
                    rect,
                    key_info,
                    row_key[LayoutYamlConstant.TXT_INFO],
                )
                self.add(key_sprites)
                key_x += key_width
                key_name = row_key[LayoutYamlConstant.NAME]
                key = self._key_name_to_key.get(key_name, None)
                if key is None:
                    bg_sprites = pygame.sprite.Group(key_sprites[:1])
                    txt_sprites = pygame.sprite.Group(key_sprites[1:])
                    key = Key(bg_sprites, txt_sprites)
                    self._key_name_to_key[key_name] = key
                else:
                    new_bg_sprite = key_sprites[0]
                    key.txt_sprites.add(key_sprites[1:])
                    sticher_sprite = self.__make_stitcher_sprite(
                        key.bg_sprites.sprites()[0], new_bg_sprite, key_info)
                    self.add([sticher_sprite])
                    key.bg_sprites.add([new_bg_sprite, sticher_sprite])


    def update_key(
        self,
        key_name: str,
        bg_color: typing.Optional[pygame.Color] = None,
        font_color: typing.Optional[pygame.Color] = None,
    ):
        """Update the new bg_color and font_color for key_name"""
        key = self._key_name_to_key[key_name]
        if bg_color:
            for bg_sprite in key.bg_sprites.sprites():
                bg_sprite.image.fill(bg_color)
        if font_color:
            for txt_sprite in key.txt_sprites.sprites():
                txt_sprite.font_color = font_color
                txt_sprite.render_text()
