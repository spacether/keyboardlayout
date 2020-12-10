import tkinter as tk
import tkinter.font as tkf
from keyboardlayout import HorizontalAnchor, VerticalAnchor


class TkTxt(tk.Label):
    """Contains text"""
    def __init__(
        self,
        master: tk.Frame,
        x: int,
        y: int,
        horizontal_anchor: HorizontalAnchor,
        vertical_anchor: VerticalAnchor,
        txt: str,
        font: tkf.Font,
        txt_color: str,
    ):
        super().__init__(
            master=master,
            text=txt,
            bg="red",
            font=font,
            padx=0,
            pady=0,
            fg=txt_color
        )

        txt_width = font.measure(txt)
        txt_height = font.metrics("linespace")

        if vertical_anchor is VerticalAnchor.TOP:
            yloc = y
        elif vertical_anchor is VerticalAnchor.MIDDLE:
            yloc = y - txt_height//2
        elif vertical_anchor is VerticalAnchor.BOTTOM:
            yloc = y - txt_height
        if horizontal_anchor is HorizontalAnchor.LEFT:
            xloc = x
        elif horizontal_anchor is HorizontalAnchor.CENTER:
            xloc = x - txt_width//2
        elif horizontal_anchor is HorizontalAnchor.RIGHT:
            xloc = x - txt_width
        self.place(x=xloc, y=yloc)


class TkRect(tk.Frame):
    """Contains a filled rectangle"""
    def __init__(
        self,
        master: tk.Frame,
        r: Rect,
        color: str,
    ):
        super().__init__(
            master,
            bd=0,
            bg=color,
            height=r.height,
            width=r.width
        )
        self.place(x=r.x, y=r.y)

window = tk.Tk()
window.resizable(False, False)


keyboard_bg = TkRect(
    window,
    Rect(0, 0, 150, 150),
    'grey'
)
keyboard_bg.pack()

size = 10
font = tkf.Font(family='Arial', size=size)
txt = "I'm at (0, 0)"
label1 = TkTxt(
    keyboard_bg,
    0,
    0,
    HorizontalAnchor.LEFT,
    VerticalAnchor.TOP,
    txt,
    font,
    'black'
)
r = Rect(25, 25, 20, 10)
rect = TkRect(
    keyboard_bg,
    r,
    'blue'
)
# label1 = tk.Label(master=frame, text=text, bg="red", font=font, padx=0, pady=0)

label2 = tk.Label(master=keyboard_bg, text="I'm at (50, 50)", bg="yellow")
label2.place(x=50, y=50)

window.mainloop()
