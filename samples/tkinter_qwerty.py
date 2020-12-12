import tkinter as tk
import tkinter.font as tkf
import keyboardlayout as kl
import keyboardlayout.tkinter as klt

def get_keyboard(window: tk.Tk, layout_name: kl.LayoutName) -> klt.KeyboardLayout:
    key_size = 60
    grey = '#bebebe'
    dark_grey = '#414141'
    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color=dark_grey
    )
    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color=dark_grey,
        txt_font=tkf.Font(family='Arial', size=key_size//4),
        txt_padding=(key_size//6, key_size//10)
    )
    letter_key_size = (key_size, key_size)  # width, height
    keyboard_layout = klt.KeyboardLayout(
        window,
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info
    )
    return keyboard_layout

def keyboard_example(layout_name: kl.LayoutName):
    window = tk.Tk()
    window.resizable(False, False)

    keyboard = get_keyboard(window, layout_name)
    window.mainloop()

if __name__ == "__main__":
    keyboard_example(kl.LayoutName.QWERTY)
