import keyboardlayout as kl
import pygame

grey = pygame.Color('grey')
dark_grey = ~pygame.Color('grey')

released_color_info = kl.KeyColorInfo(
    color=grey,
    txt_color=dark_grey
)
pressed_color_info = kl.KeyColorInfo(
    color=pygame.Color('red'),
    txt_color=pygame.Color('white')
)

def get_keyboard(layout_name: str) -> kl.KeyboardLayout:
    key_size = 60
    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=~grey
    )
    key_info = kl.KeyInfo(
        size=(key_size, key_size),  # width, height
        margin=10,
        color=grey,
        txt_color=dark_grey,
        txt_font=pygame.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    keyboard_layout = kl.KeyboardLayout(
        layout_name,
        keyboard_info,
        key_info
    )
    return keyboard_layout

def run_until_user_closes_window(
    screen: pygame.Surface,
    keyboard: kl.KeyboardLayout
):
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
            if key_name not in keyboard._key_name_to_key:
                continue

            if event.type == pygame.KEYDOWN:
                keyboard.update_key(key_name, pressed_color_info)
            elif event.type == pygame.KEYUP:
                keyboard.update_key(
                    key_name, released_color_info)
            keyboard.draw(screen)
            pygame.display.update()

    pygame.display.quit()
    pygame.quit()

def keyboard_example(layout_name: str):
    pygame.init()
    # block events that we don't want
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])

    keyboard = get_keyboard(layout_name)

    screen = pygame.display.set_mode(
        (keyboard.rect.width, keyboard.rect.height))
    screen.fill(pygame.Color('black'))

    keyboard.draw(screen)
    pygame.display.update()
    run_until_user_closes_window(screen, keyboard)

if __name__ == "__main__":
    keyboard_example('qwerty')
