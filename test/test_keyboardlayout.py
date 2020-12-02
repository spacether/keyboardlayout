import unittest
import typing

import pygame
import keyboardlayout as kl


class TestKeyboardLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @staticmethod
    def get_infos():
        key_size = 60
        grey = pygame.Color('grey')
        key_info = kl.KeyInfo(
            size=(key_size, key_size),  # width, height
            margin=10,
            color=grey,
            txt_color=~grey,  # invert grey
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        keyboard_info = kl.KeyboardInfo(
            position=(0, 0),
            padding=2,
            color=~grey
        )
        return keyboard_info, key_info


    def test_writes_sample_keyboard_layouts_to_images(self):
        layout_names = ['qwerty', 'azerty_laptop']
        keyboard_info, key_info = self.get_infos()
        for layout_name in layout_names:
            pygame.display.set_caption(
                "{} keyboard layout".format(layout_name))

            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                key_info,
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
            keyboard_layout = kl.KeyboardLayout(
                'invalid_layout',
                None,
                None,
            )

    def test_layout_num_sprites(self):
        num_sprites_by_layout = {
            kl.LayoutName.QWERTY: 143,
            kl.LayoutName.AZERTY_LAPTOP: 166,
        }
        keyboard_info, key_info = self.get_infos()
        for layout_name in kl.LayoutName:
            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                key_info,
            )
            self.assertEqual(
                len(keyboard.sprites()),
                num_sprites_by_layout[layout_name]
            )

    def test_colored_example(self):
        color_pairs = [
            ('lightgoldenrod', 'orangered'),
            ('pink', 'deeppink'),
            ('cornflowerblue', 'darkblue'),
        ]
        keyboards = []
        layout_name = 'qwerty'
        key_size = 32
        y = 0
        for color_pair in color_pairs:
            key_color, other_color = [pygame.Color(c) for c in color_pair]
            key_info = kl.KeyInfo(
                size=(key_size, key_size),  # width, height
                margin=2,
                color=key_color,
                txt_color=other_color,  # invert grey
                txt_font=pygame.font.SysFont('Arial', key_size//4),
                txt_padding=(key_size//10, key_size//10),
            )
            keyboard_info = kl.KeyboardInfo(
                position=(0, y),
                padding=2,
                color=other_color
            )

            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                key_info,
            )
            keyboards.append(keyboard)
            y += keyboard.rect.height

        screen = pygame.display.set_mode(
            (keyboards[0].rect.width, y))
        screen.fill(pygame.Color('black'))

        for keyboard in keyboards:
            keyboard.draw(screen)
        pygame.display.update()
        pygame.image.save(
            screen, "sample_images/{}_colored.jpg".format(layout_name))


if __name__ == '__main__':
    unittest.main()
