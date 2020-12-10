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
        layout_names = [kl.LayoutName.QWERTY, kl.LayoutName.AZERTY_LAPTOP]
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
                screen,
                self.sample_images_folder + "{}.jpg".format(layout_name.value)
            )

    def test_invalid_layout_name_raise_exception(self):
        with self.assertRaisesRegex(
            ValueError,
            "Invalid input type, layout_name must be type LayoutName"
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
            kl.LayoutName.AZERTY_LAPTOP: 165,
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
        TestCase = namedtuple(
            'TestCase', 'key_color keyboard_color overrides txt_color')
        key_size = 32
        margin = 2
        first_letter = kl.KeyInfo(
            margin=0,
            color=pygame.Color('cyan'),
            txt_color=pygame.Color('black'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        second_letter = kl.KeyInfo(
            margin=0,
            color=pygame.Color('magenta'),
            txt_color=pygame.Color('black'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        third_letter = kl.KeyInfo(
            margin=0,
            color=pygame.Color('yellow'),
            txt_color=pygame.Color('black'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        third_letter_small = kl.KeyInfo(
            margin=14,
            color=pygame.Color('yellow'),
            txt_color=pygame.Color('black'),
            txt_font=pygame.font.SysFont('Arial', key_size//4),
            txt_padding=(key_size//10, key_size//10),
        )
        overrides = {
            # spells HI!
            # H
            "q": first_letter,
            'a': first_letter,
            'z': first_letter,
            's': first_letter,
            'e': first_letter,
            'd': first_letter,
            'c': first_letter,
            # I
            't': second_letter,
            'y': second_letter,
            'u': second_letter,
            'h': second_letter,
            'b': second_letter,
            'n': second_letter,
            'm': second_letter,
            # !
            'o': third_letter,
            'l': third_letter,
            '.': third_letter_small,
        }
        test_cases = [
            TestCase(
                key_color='lightgoldenrod',
                keyboard_color='orangered',
                txt_color='orangered',
                overrides=None
            ),
            TestCase(
                key_color='pink',
                keyboard_color='deeppink',
                txt_color='deeppink',
                overrides=None
            ),
            TestCase(
                key_color='cornflowerblue',
                keyboard_color='darkblue',
                txt_color='darkblue',
                overrides=None
            ),
            TestCase(
                key_color='black',
                keyboard_color='grey20',
                txt_color='grey80',
                overrides=overrides
            ),
        ]
        keyboards = []
        letter_key_size = (key_size, key_size)  # width, height
        y = 0
        layout_name = kl.LayoutName.QWERTY
        for test_case in test_cases:
            key_info = kl.KeyInfo(
                margin=margin,
                color=pygame.Color(test_case.key_color),
                txt_color=pygame.Color(test_case.txt_color),
                txt_font=pygame.font.SysFont('Arial', key_size//4),
                txt_padding=(key_size//10, key_size//10),
            )
            keyboard_info = kl.KeyboardInfo(
                position=(0, y),
                padding=2,
                color=pygame.Color(test_case.keyboard_color)
            )

            keyboard = kl.KeyboardLayout(
                layout_name,
                keyboard_info,
                letter_key_size,
                key_info,
                test_case.overrides
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
            screen,
            self.sample_images_folder + "{}_colored.jpg".format(
                layout_name.value)
        )


if __name__ == '__main__':
    unittest.main()
