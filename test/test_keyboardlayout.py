import unittest
import typing

import pygame
import keyboardlayout


class TestKeyboardLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        key_size = 60
        grey = pygame.Color('grey')
        cls.key_info = keyboardlayout.KeyInfo(
            size=(key_size, key_size),  # width, height
            margin=10,
            color=grey,
            txt_color=~grey,  # invert grey
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        cls.keyboard_info = keyboardlayout.KeyboardInfo(
            position=(0, 0),
            padding=2,
            color=~grey
        )


    def test_writes_sample_keyboard_layouts_to_images(self):
        layout_names = ['qwerty', 'azerty_laptop']
        for layout_name in layout_names:
            pygame.display.set_caption(
                "{} keyboard layout".format(layout_name))

            keyboard = keyboardlayout.KeyboardLayout(
                layout_name,
                self.keyboard_info,
                self.key_info,
            )

            screen = pygame.display.set_mode(
                (keyboard.rect.width, keyboard.rect.height))
            screen.fill(pygame.Color('black'))

            keyboard.draw(screen)
            pygame.display.update()
            pygame.image.save(
                screen, "sample_images/{}.jpg".format(layout_name))

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

    def test_layout_num_sprites(self):
        num_sprites_by_layout = {
            keyboardlayout.LayoutName.QWERTY: 143,
            keyboardlayout.LayoutName.AZERTY_LAPTOP: 166,
        }
        for layout_name in keyboardlayout.LayoutName:
            keyboard = keyboardlayout.KeyboardLayout(
                layout_name,
                self.keyboard_info,
                self.key_info,
            )
            self.assertEqual(
                len(keyboard.sprites()),
                num_sprites_by_layout[layout_name]
            )


if __name__ == '__main__':
    unittest.main()
