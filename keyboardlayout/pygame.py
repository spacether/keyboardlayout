from collections import defaultdict
from importlib import resources
import typing

import pygame
import yaml

from keyboardlayout.common import (
    TxtBase,
    KeyboardLayoutBase,
    YAML_EXTENSION,
    LayoutName,
    HorizontalAnchor,
    VerticalAnchor,
    KeyboardInfo,
    KeyInfo,
    LayoutYamlConstant
)
from keyboardlayout import layouts


class PgTxt(TxtBase, pygame.sprite.Sprite):
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
        xloc, yloc = self._get_position(
            horizontal_anchor,
            vertical_anchor,
            x,
            y,
            txt_width,
            txt_height
        )
        self.rect = pygame.Rect(xloc, yloc, txt_width, txt_height)


class PgRect(pygame.sprite.Sprite):
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


class KeyboardLayout(KeyboardLayoutBase, pygame.sprite.Group):
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
    def __get_key_sprites(
        self,
        key_name: str,
        loc: typing.Tuple[int],
        key_info: KeyInfo,
    ):
        key_loc_to_rect = self._rect_by_key_name_and_loc[key_name]
        rect = key_loc_to_rect[loc]
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
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
            if rect.width < other_r.width:
                below_other = rect.y > other_r.y
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
        bg_sprite = PgRect(r, key_info.color)
        key_sprites.append(bg_sprite)

        txt_sprites = []
        txt_info = self._txt_info_by_loc[loc]
        for txt_anchor, label_txt in txt_info.items():
            txt_pos_info = self._get_txt_pos_info(
                txt_anchor, x, y, key_info, rect)
            horizontal_anchor, vertical_anchor, xloc, yloc = txt_pos_info
            txt_sprite = PgTxt(
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
        layout_name: LayoutName,
        keyboard_info: KeyboardInfo,
        letter_key_size: typing.Tuple[int],
        key_info: KeyInfo,
        overrides: typing.Optional[typing.Dict[str, KeyInfo]] = None
    ):
        super().__init__()

        if not isinstance(layout_name, LayoutName):
            raise ValueError(
                'Invalid input type, layout_name must be type LayoutName')
        layout_file_name = layout_name.value + YAML_EXTENSION
        stream = resources.read_text(layouts, layout_file_name)
        layout = yaml.safe_load(stream)

        self._key_name_to_sprite_group = defaultdict(pygame.sprite.Group)

        letter_key_width, letter_key_height = letter_key_size

        x, y = keyboard_info.position
        max_width, max_height = self._get_max_size_and_set_info_dicts(
            layout,
            keyboard_info,
            letter_key_size,
            key_info
        )
        self.rect = pygame.Rect(
            x,
            y,
            max_width - key_info.margin + 2*keyboard_info.padding,
            max_height - key_info.margin + 2*keyboard_info.padding,
        )
        if keyboard_info.color:
            bg_sprite = PgRect(self.rect, keyboard_info.color)
            self.add(bg_sprite)

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
        """Update key_name's image using key_info"""
        key_sprite_group = self._key_name_to_sprite_group[key_name]
        self.remove(key_sprite_group.sprites())
        key_sprite_group.empty()
        for loc in self._rect_by_key_name_and_loc[key_name]:
            key_sprites = self.__get_key_sprites(
                key_name,
                loc,
                key_info,
            )
            self.add(*key_sprites)
            key_sprite_group.add(*key_sprites)
