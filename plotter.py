import pygame

def init_pygame(keyboard_layout: str) -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption("{} keyboard layout".format(keyboard_layout))

    width = 240
    height = 180
    screen = pygame.display.set_mode((width,height))
    screen.fill(pygame.Color('black'))
    return screen

def run_until_window_closed():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

class SpriteRect(pygame.sprite.Sprite):
    xloc_keyunits = 0.2
    ylocs_keyunits = [0.35, 0.9]

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        label_pair = (),
        font=None,
        font_color=None,
    ):
        # TODO extract text into its own sprite
        # TODO make KeyGroup into its own class that will make:
        # - background + text sprites
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = pygame.Rect(x, y, width, height)

        for i, label_txt in enumerate(label_pair):
            self.textSurf = font.render(label_txt, 1, font_color)
            txt_width = self.textSurf.get_width()
            txt_height = self.textSurf.get_height()
            self.image.blit(
                self.textSurf,
                [
                    width*self.xloc_keyunits - txt_width/2,
                    # height*self.ylocs_keyunits[i]
                    height*self.ylocs_keyunits[i] - txt_height
                ]
            )

def plot_keyboard(keyboard_layout: str, screen: pygame.Surface):
    keyboard_group = pygame.sprite.Group()

    key_width = 60
    key_height = 60
    gap = 10
    key_color = pygame.Color('grey')

    font_size = 15
    font = pygame.font.SysFont('Arial', font_size)
    font_color = key_color.__invert__()


    from keyboard_layouts import qwerty
    layout = qwerty
    for row_name, row_keys in layout.rows.items():
        row_x, row_y = layout.row_locations[row_name]
        for i, label_pair in enumerate(row_keys):
            key_x = row_x + i*key_width + i*gap
            key_rect = SpriteRect(
                key_x,
                row_y,
                key_width,
                key_height,
                key_color,
                label_pair,
                font,
                font_color
            )
            keyboard_group.add(key_rect)

    keyboard_group.draw(screen)
    pygame.display.update()


def example_plot_keyboard(keyboard_layout: str):
    screen = init_pygame(keyboard_layout)
    plot_keyboard(keyboard_layout, screen)
    run_until_window_closed()


if __name__=="__main__":
    example_plot_keyboard("qwerty")
