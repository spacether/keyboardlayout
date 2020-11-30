import typing
from types import ModuleType
from enum import Enum
from pathlib import Path
import yaml
import os

import pygame

CURRENT_WORKING_DIR = Path(__file__).parent.absolute()

def init_pygame_and_draw_keyboard(keyboard_layout: str):
    pygame.init()
    pygame.display.set_caption("{} keyboard layout".format(keyboard_layout))

    keyboard = get_keyboard(keyboard_layout, (0, 0))

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


class TxtAnchor(Enum):
    TOP_LEFT = 'tl'
    TOP_CENTER = 'tc'
    TOP_RIGHT = 'tr'
    MIDDLE_LEFT = 'ml'
    MIDDLE_CENTER = 'mc'
    MIDDLE_RIGHT = 'mr'
    BOTTOM_LEFT = 'bl'
    BOTTOM_CENTER = 'bc'
    BOTTOM_RIGHT = 'br'

class TxtSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        txt_anchor: TxtAnchor,
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

        first_word, second_word = txt_anchor.name.split('_')
        if first_word == 'TOP':
            yloc = y
        elif first_word == 'MIDDLE':
            yloc = y - txt_height//2
        elif first_word == 'BOTTOM':
            yloc = y - txt_height
        if second_word == 'LEFT':
            xloc = x
        elif second_word == 'CENTER':
            xloc = x - txt_width//2
        elif second_word == 'RIGHT':
            xloc = x - txt_width
        self.rect = pygame.Rect(xloc, yloc, txt_width, txt_height)

    def render_text(self):
        self.image = self.font.render(self.txt, 1, self.font_color)


class RectSprite(pygame.sprite.Sprite):
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
    def __init__(
        self,
        bg_sprites: pygame.sprite.Group,
        txt_sprites: pygame.sprite.Group
    ):
        self.bg_sprites = bg_sprites
        self.txt_sprites = txt_sprites



class KeyGroup(pygame.sprite.Group):
    def __init__(
        self,
        r: pygame.Rect,
        key_margin: int,
        color: pygame.Color,
        txt_info: typing.Dict[str, str],
        font: pygame.font.SysFont,
        font_color: pygame.Color,
        txt_xpadding: int,
        txt_ypadding: int,
    ):
        super().__init__()
        x, y, width, height = r.x, r.y, r.width, r.height
        key_padding = key_margin//2
        r = pygame.Rect(
            x+key_padding,
            y+key_padding,
            width-2*key_padding,
            height-2*key_padding,
        )
        bg_sprite = RectSprite(r, color)
        self.add(bg_sprite)

        for txt_anchor, label_txt in txt_info.items():
            txt_anchor = TxtAnchor(txt_anchor)
            first_word, second_word = txt_anchor.name.split('_')
            if first_word == 'TOP':
                yloc = y + key_padding + txt_ypadding
            elif first_word == 'MIDDLE':
                yloc = y + height//2
            elif first_word == 'BOTTOM':
                yloc = y + height - key_padding - txt_ypadding
            if second_word == 'LEFT':
                xloc = x + key_padding + txt_xpadding
            elif second_word == 'CENTER':
                xloc = x + width//2
            elif second_word == 'RIGHT':
                xloc = x + width - key_padding - txt_xpadding
            txt_sprite = TxtSprite(
                xloc,
                yloc,
                txt_anchor,
                label_txt,
                font,
                font_color
            )
            self.add(txt_sprite)


class KeyboardLayout(pygame.sprite.Group):
    @staticmethod
    def __max_width(
        letter_key_width: int,
        layout: ModuleType,
    ):
        max_width = 0
        key_size = layout['key_size']
        for row in layout['rows']:
            row_max_width = 0
            key_size = row.get('key_size', key_size)
            for row_key in row['keys']:
                key_xsize_keycoords, _ = row_key.get('size', key_size)
                key_width = letter_key_width * key_xsize_keycoords
                row_max_width += key_width
            if row_max_width > max_width:
                max_width = row_max_width
        return max_width

    @staticmethod
    def __max_height(
        letter_key_height: int,
        layout: ModuleType,
    ):
        height_max = 0
        key_size = layout['key_size']
        for row in layout['rows']:
            key_size = row.get('key_size', key_size)
            for row_key in row['keys']:
                _, key_ysize_keycoords = row_key.get('size', key_size)
                _, row_y_keycoords = row["location"]
                row_y = row_y_keycoords * letter_key_height
                key_height = letter_key_height * key_ysize_keycoords
                key_ymax = row_y + key_height
                if key_ymax > height_max:
                    height_max = key_ymax
        return height_max

    def __add_additional_sprites_to_key(
        self,
        key: Key,
        key_group: KeyGroup,
        key_margin: int,
        key_color: pygame.Color,
    ):
        txt_sprites = key_group.sprites()[1:]
        key.txt_sprites.add(txt_sprites)

        new_bg_sprite = key_group.sprites()[0]
        existing_bg_sprite = key.bg_sprites.sprites()[0]
        if existing_bg_sprite.rect.width < new_bg_sprite.rect.width:
            used_rect = existing_bg_sprite.rect
            used_y = used_rect.bottom
        else:
            used_rect = new_bg_sprite.rect
            used_y = used_rect.top - key_margin
        r = pygame.Rect(
            used_rect.left,
            used_y,
            used_rect.width,
            key_margin,
        )
        sticher_sprite = RectSprite(r, key_color)
        self.add([sticher_sprite])
        key.bg_sprites.add([new_bg_sprite, sticher_sprite])

    def __init__(
        self,
        position: typing.Tuple[int],
        layout_name: str,
        keyboard_padding: int,
        letter_key_width: int,
        letter_key_height: int,
        key_margin: int,
        key_color: pygame.Color,
        font_color: pygame.Color,
        font: pygame.font.SysFont,
        txt_xpadding: int,
        txt_ypadding: int,
        keyboard_color: typing.Optional[pygame.Color]=None
    ):
        super().__init__()
        layout_path = os.path.join(
            CURRENT_WORKING_DIR, 'keyboard_layouts', layout_name+'.yaml')
        stream = open(layout_path, 'r')
        layout = yaml.safe_load(stream)
        self._key_name_to_key = {}

        x, y = position
        xanchor = x + keyboard_padding
        yanchor = y + keyboard_padding
        if key_margin:
            xanchor += -key_margin//2
            yanchor += -key_margin//2
        xmax = 0
        ymax = 0
        max_width = self.__max_width(letter_key_width, layout)
        max_height = self.__max_height(letter_key_height, layout)
        self.rect = pygame.Rect(
            x,
            y,
            max_width - key_margin + 2*keyboard_padding,
            max_height - key_margin + 2*keyboard_padding,
        )
        if keyboard_color:
            bg_sprite = RectSprite(self.rect, keyboard_color)
            self.add(bg_sprite)
        key_size = layout['key_size']
        for row in layout['rows']:
            row_keys = row['keys']
            key_names = set(key['name'] for key in row_keys)

            row_x_keycoords, row_y_keycoords = row['location']
            key_x = xanchor + row_x_keycoords * letter_key_width
            row_y = yanchor + row_y_keycoords * letter_key_height
            key_size = row.get('key_size', key_size)
            for row_key in row_keys:
                key_name = row_key['name']

                key_xsize_keycoords, key_ysize_keycoords = (
                    row_key.get('size', key_size))
                key_width, key_height = (
                    letter_key_width*key_xsize_keycoords,
                    letter_key_height*key_ysize_keycoords
                )
                rect = pygame.Rect(key_x, row_y, key_width, key_height)
                key_group = KeyGroup(
                    rect,
                    key_margin,
                    key_color,
                    row_key['txt_info'],
                    font,
                    font_color,
                    txt_xpadding,
                    txt_ypadding
                )
                self.add(key_group.sprites())
                key_x += key_width
                key = self._key_name_to_key.get(key_name, None)
                if key is None:
                    bg_sprites = pygame.sprite.Group(key_group.sprites()[:1])
                    txt_sprites = pygame.sprite.Group(key_group.sprites()[1:])
                    key = Key(bg_sprites, txt_sprites)
                    self._key_name_to_key[key_name] = key
                else:
                    self.__add_additional_sprites_to_key(
                        key, key_group, key_margin, key_color)

    def update_key(
        self,
        key_name: str,
        bg_color: typing.Optional[pygame.Color] = None,
        font_color: typing.Optional[pygame.Color] = None,
    ):
        key = self._key_name_to_key[key_name]
        if bg_color:
            for bg_sprite in key.bg_sprites.sprites():
                bg_sprite.image.fill(bg_color)
        if font_color:
            for txt_sprite in key.txt_sprites.sprites():
                txt_sprite.font_color = font_color
                txt_sprite.render_text()


def get_keyboard(keyboard_layout: str, position: typing.List[int]):
    letter_key_width = 60
    letter_key_height = letter_key_width
    keyboard_padding = 2
    key_margin = 10
    key_color = pygame.Color('grey')
    font_color = key_color.__invert__()

    font_size = letter_key_width//4
    font = pygame.font.SysFont('Arial', font_size)
    font_color = key_color.__invert__()
    txt_xpadding = letter_key_width//6
    txt_ypadding = letter_key_width//10

    keyboard_layout = KeyboardLayout(
        position,
        keyboard_layout,
        keyboard_padding,
        letter_key_width,
        letter_key_height,
        key_margin,
        key_color,
        font_color,
        font,
        txt_xpadding,
        txt_ypadding,
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
