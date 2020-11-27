import typing

import pygame

def init_pygame(keyboard_layout: str) -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption("{} keyboard layout".format(keyboard_layout))

    width = 1100
    height = 300
    screen = pygame.display.set_mode((width,height))
    screen.fill(pygame.Color('black'))
    return screen

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
        txt = '',
        font=None,
        font_color=None,
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
        txt_xmargin: int,
        txt_ymargin: int,
    ):
        super().__init__()
        bg_sprite = RectSprite(x, y, width, height, color)
        self.add(bg_sprite)

        for i, label_txt in enumerate(label_pair):
            if not label_txt:
                continue
            xloc = x + txt_xmargin
            if i == 0:
                ytop = True
                yloc = y + txt_ymargin
            else:
                ytop = False
                yloc = y + height - txt_ymargin
            txt_sprite = TxtSprite(
                xloc,
                yloc,
                ytop,
                label_txt,
                font,
                font_color
            )
            self.add(txt_sprite)


def plot_keyboard(keyboard_layout: str, screen: pygame.Surface):
    keyboard_group = pygame.sprite.Group()

    letter_key_width = 60
    letter_key_height = 60
    gap = 10
    key_color = pygame.Color('grey')

    font_size = 15
    font = pygame.font.SysFont('Arial', font_size)
    font_color = key_color.__invert__()
    txt_xmargin = 11
    txt_ymargin = 8

    from keyboard_layouts import qwerty
    layout = qwerty
    for row_name, row_keys in layout.rows.items():
        row_x, row_y = layout.row_locations[row_name]
        key_x = row_x
        for i, label_info in enumerate(row_keys):
            key_name = label_info[-1]
            key_xsize_keycoords, key_ysize_keycoords = (
                layout.key_sizes.get(key_name, (1, 1))
            )
            key_width = letter_key_width * key_xsize_keycoords
            key_height = letter_key_height * key_ysize_keycoords
            key_group = KeyGroup(
                key_x,
                row_y,
                key_width,
                key_height,
                key_color,
                label_info[:2],
                font,
                font_color,
                txt_xmargin,
                txt_ymargin
            )
            keyboard_group.add(key_group.sprites())
            key_x += key_width + gap

    keyboard_group.draw(screen)
    pygame.display.update()


def example_plot_keyboard(keyboard_layout: str):
    screen = init_pygame(keyboard_layout)
    plot_keyboard(keyboard_layout, screen)
    run_until_window_closed()


if __name__=="__main__":
    example_plot_keyboard("qwerty")
