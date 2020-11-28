import typing
from types import ModuleType

import pygame

def init_pygame_and_draw_keyboard(keyboard_layout: str):
    pygame.init()
    pygame.display.set_caption("{} keyboard layout".format(keyboard_layout))

    keyboard = get_keyboard(keyboard_layout)

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

class TxtSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        ytop: bool,
        txt: str,
        font: pygame.font.SysFont,
        font_color: pygame.Color,
    ):
        super().__init__()
        self.image = font.render(txt, 1, font_color)

        txt_width = self.image.get_width()
        txt_height = self.image.get_height()

        xloc = x
        if ytop:
            yloc = y
        else:
            yloc = y - txt_height
        self.rect = pygame.Rect(xloc, yloc, txt_width, txt_height)


class RectSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
    ):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)


class KeyGroup(pygame.sprite.Group):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        label_pair: typing.Tuple[str],
        font: pygame.font.SysFont,
        font_color: pygame.Color,
        txt_xpadding: int,
        txt_ypadding: int,
    ):
        super().__init__()
        bg_sprite = RectSprite(x, y, width, height, color)
        self.add(bg_sprite)

        for i, label_txt in enumerate(label_pair):
            if not label_txt:
                continue
            xloc = x + txt_xpadding
            if i == 0:
                ytop = True
                yloc = y + txt_ypadding
            else:
                ytop = False
                yloc = y + height - txt_ypadding
            txt_sprite = TxtSprite(
                xloc,
                yloc,
                ytop,
                label_txt,
                font,
                font_color
            )
            self.add(txt_sprite)


class KeyboardLayout(pygame.sprite.Group):
    __letter_key_size_keycoords = (1, 1)

    @classmethod
    def __get_remainder_x(
        cls,
        xmax: int,
        letter_key_width: int,
        key_margin: int,
        key_names: typing.List[str],
        layout: ModuleType
    ):
        if (
            any(key_name in layout.key_width_percent_remainder_sizes
                for key_name in key_names
            )
        ):
            used_width = 0
            for key_name in key_names:
                if key_name in layout.key_width_percent_remainder_sizes:
                    continue
                key_xsize_keycoords, _ = layout.key_sizes.get(
                    key_name, cls.__letter_key_size_keycoords)
                key_width = letter_key_width * key_xsize_keycoords
                used_width += key_width
            remainder_x = xmax - used_width - (len(key_names) - 1) * key_margin
            return remainder_x
        return None

    @classmethod
    def __get_key_width_height(
        cls,
        key_name: str,
        remainder_x: typing.Optional[int],
        letter_key_width: int,
        letter_key_height: int,
        layout: ModuleType,
    ):
        key_xsize_keycoords, key_ysize_keycoords = (
            layout.key_sizes.get(key_name, cls.__letter_key_size_keycoords)
        )
        key_width_percent_remainder = (
            layout.key_width_percent_remainder_sizes.get(key_name, None)
        )
        if key_width_percent_remainder is None:
            key_width = letter_key_width * key_xsize_keycoords
        else:
            key_width = remainder_x*(key_width_percent_remainder/100)
        key_height = letter_key_height * key_ysize_keycoords
        return key_width, key_height

    def __init__(
        self,
        layout_name: str,
        letter_key_width: int,
        letter_key_height: int,
        key_margin: int,
        key_color: pygame.Color,
        font_color: pygame.Color,
        font: pygame.font.SysFont,
        txt_xpadding: int,
        txt_ypadding: int,
    ):
        super().__init__()
        layout = __import__(
            'keyboard_layouts.{}'.format(layout_name),
            fromlist=['']
        )
        keys = []

        x = 0
        y = 0
        xmax = 0
        ymax = 0
        for i, (row_name, row_keys) in enumerate(layout.rows.items()):
            key_names = set(key[-1] for key in row_keys)
            remainder_x = self.__get_remainder_x(
                xmax, letter_key_width, key_margin, key_names, layout)

            row_x_keycoords, row_y_keycoords = layout.row_locations[row_name]
            key_x = x
            row_y = y + row_y_keycoords * letter_key_height + key_margin*i
            for j, label_info in enumerate(row_keys):
                key_name = label_info[-1]
                key_width, key_height = self.__get_key_width_height(
                    key_name,
                    remainder_x,
                    letter_key_width,
                    letter_key_height,
                    layout,
                )
                key_group = KeyGroup(
                    key_x,
                    row_y,
                    key_width,
                    key_height,
                    key_color,
                    label_info[:2],
                    font,
                    font_color,
                    txt_xpadding,
                    txt_ypadding
                )
                self.add(key_group.sprites())
                key_x += key_width + key_margin
                x_right, y_bot = key_group.sprites()[0].rect.bottomright
                if x_right > xmax:
                    xmax = x_right
                if y_bot > ymax:
                    ymax = y_bot
        self.rect = pygame.Rect(0, 0, xmax, ymax)


def get_keyboard(keyboard_layout: str):
    letter_key_width = 60
    letter_key_height = 60
    key_margin = 2
    # key_margin = 10
    key_color = pygame.Color('grey')
    font_color = key_color.__invert__()

    font_size = 15
    font = pygame.font.SysFont('Arial', font_size)
    font_color = key_color.__invert__()
    txt_xpadding = 11
    txt_ypadding = 8

    keyboard_layout = KeyboardLayout(
        keyboard_layout,
        letter_key_width,
        letter_key_height,
        key_margin,
        key_color,
        font_color,
        font,
        txt_xpadding,
        txt_ypadding,
    )
    return keyboard_layout


if __name__=="__main__":
    screen = init_pygame_and_draw_keyboard('qwerty')
    run_until_window_closed()
