import unittest
import typing
from collections import namedtuple

import pygame
import keyboardlayout as kl


class TestKeyboardLayout(unittest.TestCase):
    sample_images_folder = "samples/images/"

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @staticmethod
    def get_infos():
        grey = pygame.Color('grey')
        key_size = 60
        letter_key_size = (key_size, key_size) # width, height
        key_info = kl.KeyInfo(
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
        return keyboard_info, letter_key_size, key_info


    def test_writes_sample_keyboard_layouts_to_images(self):
        layout_names = ['qwerty', 'azerty_laptop']
        keyboard_info, letter_key_size, key_info = self.get_infos()
        for layout_name in layout_names:
            pygame.display.set_caption(
                "{} keyboard layout".format(layout_name))

            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                letter_key_size,
                key_info,
            )

            screen = pygame.display.set_mode(
                (keyboard.rect.width, keyboard.rect.height))
            screen.fill(pygame.Color('black'))

            keyboard.draw(screen)
            pygame.display.update()
            pygame.image.save(
                screen, self.sample_images_folder + "{}.jpg".format(layout_name))


    def test_invalid_layout_name_raise_exception(self):
        with self.assertRaisesRegex(
            ValueError,
            "'invalid_layout' is not a valid LayoutName"
        ):
            keyboard_layout = kl.KeyboardLayout(
                'invalid_layout',
                None,
                None,
                None,
            )

    def test_layout_num_sprites(self):
        num_sprites_by_layout = {
            kl.LayoutName.QWERTY: 143,
            kl.LayoutName.AZERTY_LAPTOP: 166,
        }
        keyboard_info, letter_key_size, key_info = self.get_infos()
        for layout_name in kl.LayoutName:
            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                letter_key_size,
                key_info,
            )
            self.assertEqual(
                len(keyboard.sprites()),
                num_sprites_by_layout[layout_name]
            )

    def test_colored_example(self):
        TestCase = namedtuple('TestCase', 'key_color other_color overrides')
        test_cases = [
            TestCase(key_color='lightgoldenrod', other_color='orangered', overrides=None),
            TestCase(key_color='pink', other_color='deeppink', overrides=None),
            TestCase(key_color='cornflowerblue', other_color='darkblue', overrides=None),
        ]
        keyboards = []
        layout_name = 'qwerty'
        key_size = 32
        letter_key_size = (key_size, key_size)  # width, height
        y = 0
        for test_case in test_cases:
            key_color, other_color = [
                pygame.Color(c)
                for c in (test_case.key_color, test_case.other_color)
            ]
            key_info = kl.KeyInfo(
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
                letter_key_size,
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
            screen, self.sample_images_folder + "{}_colored.jpg".format(layout_name))


if __name__ == '__main__':
    unittest.main()
