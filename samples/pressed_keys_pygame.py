import keyboardlayout as kl
import pygame
import argparse

grey = pygame.Color('grey')
dark_grey = ~pygame.Color('grey')

def get_keyboard(
    layout_name: str,
    key_size: int,
    key_info: kl.KeyInfo
) -> kl.KeyboardLayout:
    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=~grey
    )
    letter_key_size = (key_size, key_size)  # width, height
    keyboard_layout = kl.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info
    )
    return keyboard_layout

def run_until_user_closes_window(
    screen: pygame.Surface,
    keyboard: kl.KeyboardLayout,
    key_size: int,
    released_key_info: kl.KeyInfo,
):
    pressed_key_info = kl.KeyInfo(
        margin=20,
        color=pygame.Color('red'),
        txt_color=pygame.Color('white'),
        txt_font=pygame.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.key == pygame.K_ESCAPE:
                playing = False
                break

            key_name = pygame.key.name(event.key)
            print(event.key, key_name, event.scancode)
            if key_name not in keyboard._key_name_to_sprite_group:
                continue

            if event.type == pygame.KEYDOWN:
                keyboard.update_key(key_name, pressed_key_info)
            elif event.type == pygame.KEYUP:
                keyboard.update_key(
                    key_name, released_key_info)
            keyboard.draw(screen)
            pygame.display.update()

    pygame.display.quit()
    pygame.quit()

def keyboard_example(layout_name: str):
    pygame.init()
    # block events that we don't want
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])

    key_size = 60
    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color=dark_grey,
        txt_font=pygame.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    keyboard = get_keyboard(layout_name, key_size, key_info)

    screen = pygame.display.set_mode(
        (keyboard.rect.width, keyboard.rect.height))
    screen.fill(pygame.Color('black'))

    keyboard.draw(screen)
    pygame.display.update()
    run_until_user_closes_window(screen, keyboard, key_size, key_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'layout_name',
        nargs='?',
        type=str,
        default='qwerty',
        help='the layout_name to use'
    )
    args = parser.parse_args()
    keyboard_example(args.layout_name)
