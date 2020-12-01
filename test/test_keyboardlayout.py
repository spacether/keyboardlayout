import unittest
import typing

import pygame
import keyboardlayout

def get_keyboard(
    layout_name: str,
    position: typing.List[int]
) -> keyboardlayout.KeyboardLayout:

    key_size = 60
    grey = pygame.Color('grey')
    key_info = keyboardlayout.KeyInfo(
        size=(key_size, key_size),  # width, height
        margin=10,
        color=grey,
        txt_color=~grey,  # invert grey
        txt_font=pygame.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//10, key_size//10),
    )
    keyboard_info = keyboardlayout.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=~grey
    )
    keyboard_layout = keyboardlayout.KeyboardLayout(
        layout_name,
        keyboard_info,
        key_info,
    )
    return keyboard_layout


class TestKeyboardLayout(unittest.TestCase):
    @staticmethod
    def __init_pygame_and_draw_keyboard(layout_name: str):
        pygame.init()
        pygame.display.set_caption("{} keyboard layout".format(layout_name))

        keyboard = get_keyboard(layout_name, (0, 0))

        screen = pygame.display.set_mode(
            (keyboard.rect.width, keyboard.rect.height))
        screen.fill(pygame.Color('black'))

        keyboard.draw(screen)
        pygame.display.update()

        pygame.image.save(screen, "sample_images/{}.jpg".format(layout_name))

    def test_writes_sample_keyboard_layouts_to_images(self):
        layout_names = ['qwerty', 'azerty_laptop']
        for layout_name in layout_names:
            screen = self.__init_pygame_and_draw_keyboard(layout_name)

    def test_invalid_layout_name_raise_exception(self):
        with self.assertRaisesRegex(
            ValueError,
            "'invalid_layout' is not a valid LayoutName"
        ):
            keyboard_layout = keyboardlayout.KeyboardLayout(
                'invalid_layout',
                None,
                None,
            )


if __name__ == '__main__':
    unittest.main()
