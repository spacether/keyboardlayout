import argparse

import tkinter as tk
import tkinter.font as tkf

import keyboardlayout as kl
import keyboardlayout.tkinter as klt

grey = '#bebebe'
dark_grey = '#414141'
key_size = 60

def get_keyboard(
    window: tk.Tk,
    layout_name: kl.LayoutName,
    key_info: kl.KeyInfo
) -> klt.KeyboardLayout:
    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=dark_grey
    )
    letter_key_size = (key_size, key_size)  # width, height
    keyboard_layout = klt.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info,
        master=window
    )
    return keyboard_layout

def run_until_user_closes_window(
    window: tk.Tk,
    keyboard: klt.KeyboardLayout,
    released_key_info: kl.KeyInfo,
):
    pressed_key_info = kl.KeyInfo(
        margin=14,
        color='red',
        txt_color='white',
        txt_font=tkf.Font(family='Arial', size=key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    """
    in the azerty layout store the pressed state of the key ˆ (upper case ¨)
    because tkinter does not register a key up event for that key
    That key adds accents to the key pressed after this key
    """
    dead_key_pressed = False
    dead_key_keys = {kl.Key.CIRCUMFLEX, kl.Key.DIACRATICAL}

    def keyup(e):
        key = keyboard.get_key(e)
        if key is None:
            return
        keyboard.update_key(
            key, released_key_info)
        nonlocal dead_key_pressed
        if dead_key_pressed and key not in dead_key_keys:
            dead_key_pressed = False
            keyboard.update_key(
                kl.Key.CIRCUMFLEX, released_key_info)

    def keydown(e):
        key = keyboard.get_key(e)
        if key is None:
            return
        keyboard.update_key(key, pressed_key_info)
        if key in dead_key_keys:
            nonlocal dead_key_pressed
            dead_key_pressed = True

    keyboard.bind("<KeyPress>", keydown)
    keyboard.bind("<KeyRelease>", keyup)
    keyboard.focus_set()
    window.mainloop()


def keyboard_example(layout_name: kl.LayoutName):
    window = tk.Tk()
    window.resizable(False, False)

    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color=dark_grey,
        txt_font=tkf.Font(family='Arial', size=key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    keyboard = get_keyboard(window, layout_name, key_info)

    run_until_user_closes_window(window, keyboard, key_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'layout_name',
        nargs='?',
        type=kl.LayoutName,
        default=kl.LayoutName.QWERTY,
        help='the layout_name to use'
    )
    args = parser.parse_args()
    keyboard_example(args.layout_name)
