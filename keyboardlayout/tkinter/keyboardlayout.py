from collections import defaultdict
from typing import Tuple, Union, Optional, Dict

import tkinter as tk
import tkinter.font as tkf

from keyboardlayout.common import (
    KeyboardInfo,
    LayoutName,
    KeyInfo,
    Rect,
    TxtBase,
    HorizontalAnchor,
    VerticalAnchor,
    KeyboardLayoutInterface,
    LayoutConstant
)
from keyboardlayout import layouts
from keyboardlayout.key import Key
from keyboardlayout.tkinter.key import KEY_MAP


class TkTxt(TxtBase, tk.Label):
    """Contains text"""
    def __init__(
        self,
        master: Union[tk.Frame, tk.Tk],
        x: int,
        y: int,
        horizontal_anchor: HorizontalAnchor,
        vertical_anchor: VerticalAnchor,
        txt: str,
        font: tkf.Font,
        txt_color: str,
        color: str,
    ):
        super().__init__(
            master=master,
            text=txt,
            font=font,
            padx=0,
            pady=0,
            fg=txt_color,
            bg=color,
            bd=0,
        )

        txt_width = font.measure(txt)
        txt_height = font.metrics("linespace")
        xloc, yloc = self._get_position(
            horizontal_anchor,
            vertical_anchor,
            x,
            y,
            txt_width,
            txt_height
        )
        self.place(x=xloc, y=yloc)


class TkRect(tk.Frame):
    """Contains a filled rectangle"""
    def __init__(
        self,
        master: Union[tk.Frame, tk.Tk],
        r: Rect,
        color: str,
    ):
        super().__init__(
            master,
            bd=0,
            bg=color,
            height=r.height,
            width=r.width,
            padx=0,
            pady=0,
        )
        self.place(x=r.x, y=r.y)


class KeyboardLayout(tk.Frame, KeyboardLayoutInterface):
    """
    Makes a sprite group that stores a keyboard layout image

    Args:
        layout_name: must be a string in the LayoutName enum
        keyboard_info: the settings for the keyboard
        letter_key_size: the horizontal and vertical size in px of letter keys
        key_info: the settings for the keys
        overrides: Optional; a dict that lets one override key settings

    Attributes:
        _key_name_to_sprite_group (dict): a dict that goes from
            key_name (str) to pygame.sprite.Group instances
    """
    def __get_key_widgets(
        self,
        key: Key,
        loc: Tuple[int],
        key_info: KeyInfo,
    ):
        key_loc_to_rect = self._rect_by_key_and_loc[key]
        rect = key_loc_to_rect[loc]
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
        key_padding = key_info.margin//2

        """
        If there are multiple rects for a key
        Check if this is the min width one. If so then make the height taller
        """
        y_delta = 0
        height_delta = 0
        if len(key_loc_to_rect) == 2:
            locs = list(set(key_loc_to_rect))
            other_loc = locs[not locs.index(loc)]
            other_r = key_loc_to_rect[other_loc]
            if rect.width < other_r.width:
                below_other = rect.y > other_r.y
                if below_other:
                    y_delta = -key_info.margin
                    height_delta = key_info.margin
                else:
                    height_delta = key_info.margin

        r = Rect(
            x+key_padding,
            y+key_padding + y_delta,
            width-2*key_padding,
            height-2*key_padding + height_delta,
        )
        key_widgets = []
        bg_frame = TkRect(self, r, key_info.color)
        key_widgets.append(bg_frame)

        txt_info = self._txt_info_by_loc[loc]
        for txt_anchor, label_txt in txt_info.items():
            txt_pos_info = self._get_txt_pos_info(
                txt_anchor, x, y, key_info, rect)
            horizontal_anchor, vertical_anchor, xloc, yloc = txt_pos_info
            txt_label = TkTxt(
                self,
                xloc,
                yloc,
                horizontal_anchor,
                vertical_anchor,
                label_txt,
                key_info.txt_font,
                key_info.txt_color,
                key_info.color,
            )
            key_widgets.append(txt_label)

        return key_widgets

    def __init__(
        self,
        layout_name: LayoutName,
        keyboard_info: KeyboardInfo,
        letter_key_size: Tuple[int],
        key_info: KeyInfo,
        *,
        master: Union[tk.Frame, tk.Tk],
        overrides: Optional[Dict[str, KeyInfo]] = None
    ):
        layout = layouts.get_layout(layout_name)

        self._key_to_widget_list = defaultdict(list)

        max_width, max_height = self._get_max_size_and_set_instance_info(
            layout,
            keyboard_info,
            letter_key_size,
            key_info,
            layout_name
        )
        super().__init__(
            master=master,
            padx=0,
            pady=0,
            width=max_width,
            height=max_height,
        )
        self.rect = Rect(
            keyboard_info.position[0],
            keyboard_info.position[1],
            max_width - key_info.margin + 2*keyboard_info.padding,
            max_height - key_info.margin + 2*keyboard_info.padding,
        )
        self.widgets = []
        if keyboard_info.color:
            bg_frame = TkRect(self, self.rect, keyboard_info.color)
            self.widgets.append(bg_frame)

        for row_ind, row in enumerate(layout[LayoutConstant.ROWS]):
            for row_key_ind, row_key in enumerate(row[LayoutConstant.KEYS]):
                key_name = row_key[LayoutConstant.NAME]
                key = Key(key_name)
                used_key_info = key_info
                if overrides:
                    used_key_info = overrides.get(key_name, used_key_info)
                loc = (row_ind, row_key_ind)
                key_widgets = self.__get_key_widgets(
                    key,
                    loc,
                    used_key_info,
                )
                self.widgets.extend(key_widgets)
                self._key_to_widget_list[key].extend(key_widgets)
        self.pack()


    def update_key(
        self,
        key: Key,
        key_info: KeyInfo,
    ):
        """Update key_name's image using key_info"""
        actual_key = self._key_to_actual_key.get(key, key)
        key_widget_list = self._key_to_widget_list[actual_key]
        for key_widget in key_widget_list:
            self.widgets.remove(key_widget)
            key_widget.destroy()
        key_widget_list.clear()
        for loc in self._rect_by_key_and_loc[actual_key]:
            key_widgets = self.__get_key_widgets(
                actual_key,
                loc,
                key_info,
            )
            self.widgets.extend(key_widgets)
            key_widget_list.extend(key_widgets)

    def get_key(self, event: tk.Event) -> Optional[Key]:
        """
        keysym_num is set on most keys and is platform independent
        If keysym_num is 0, we should use keycode which is platform-dependent
        """
        number = event.keysym_num
        if number == 0:
            number = event.keycode
        try:
            key = KEY_MAP[number]
            actual_key = self._key_to_actual_key.get(key, key)
            self._key_to_widget_list[actual_key]
            return key
        except KeyError:
            return None
