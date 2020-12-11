import tkinter as tk
import tkinter.font as tkf
import keyboardlayout as kl
import keyboardlayout.tkinter as klt

def get_keyboard(window: tk.Frame, layout_name: kl.LayoutName) -> klt.KeyboardLayout:
    key_size = 60
    grey = 'grey'
    keyboard_info = kl.KeyboardInfo(
        position=(0, 0),
        padding=2,
        color='dark grey'
    )
    key_info = kl.KeyInfo(
        margin=10,
        color=grey,
        txt_color='dark grey',
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

def run_until_user_closes_window():
    window.mainloop()
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.display.quit()
    #             running = False
    #
    # pygame.quit()

def keyboard_example(layout_name: kl.LayoutName):
    window = tk.Tk()
    window.resizable(False, False)

    keyboard = get_keyboard(window, layout_name)
    # keyboard.pack()

    # screen = pygame.display.set_mode(
    #     (keyboard.rect.width, keyboard.rect.height))
    # screen.fill(pygame.Color('black'))
    # keyboard.draw(screen)
    # pygame.display.update()
    window.mainloop()

if __name__ == "__main__":
    keyboard_example(kl.LayoutName.QWERTY)
