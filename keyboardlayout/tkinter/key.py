from keyboardlayout.key import Key

import tkinter

"""
keysym_num is set on most keys and is platform independent
If keysym_num is 0, we should use keycode which is platform-dependent
"""
__KEY_TO_KL_KEY = {
    96: Key.K_BACKQUOTE,
    49: Key.K_1,
    50: Key.K_2,
    51: Key.K_3,
    52: Key.K_4,
    53: Key.K_5,
    54: Key.K_6,
    55: Key.K_7,
    56: Key.K_8,
    57: Key.K_9,
    48: Key.K_0,
    45: Key.K_MINUS,
    61: Key.K_EQUALS,
    65288: Key.K_BACKSPACE,
    65289: Key.K_TAB,
    113: Key.K_Q,
    119: Key.K_W,
    101: Key.K_E,
    114: Key.K_R,
    116: Key.K_T,
    121: Key.K_Y,
    117: Key.K_U,
    105: Key.K_I,
    111: Key.K_O,
    112: Key.K_P,
    91: Key.K_LEFTBRACKET,
    93: Key.K_RIGHTBRACKET,
    92: Key.K_BACKSLASH,
    65509: Key.K_CAPSLOCK,
    97: Key.K_A,
    115: Key.K_S,
    100: Key.K_D,
    102: Key.K_F,
    103: Key.K_G,
    104: Key.K_H,
    106: Key.K_J,
    107: Key.K_K,
    108: Key.K_L,
    59: Key.K_SEMICOLON,
    39: Key.K_SINGLEQUOTE,
    65293: Key.K_RETURN,
    131074: Key.K_LEFT_SHIFT, # macOs
    65505: Key.K_LEFT_SHIFT,
    122: Key.K_Z,
    120: Key.K_X,
    99: Key.K_C,
    118: Key.K_V,
    98: Key.K_B,
    110: Key.K_N,
    109: Key.K_M,
    44: Key.K_COMMA,
    46: Key.K_PERIOD,
    47: Key.K_FORWARDSLASH,
    131076: Key.K_RIGHT_SHIFT, # macOs
    65506: Key.K_RIGHT_SHIFT,
    262145: Key.K_LEFT_CONTROL, # macOs
    65507: Key.K_LEFT_CONTROL,
    1048584: Key.K_LEFT_META, # macOs
    65511: Key.K_LEFT_META,
    524320: Key.K_LEFT_ALT, # macOs
    65513: Key.K_LEFT_ALT,
    32: Key.K_SPACE,
    524352: Key.K_RIGHT_ALT, # macOs
    65514: Key.K_RIGHT_ALT,
    1048592: Key.K_RIGHT_META, # macOs
    65512: Key.K_RIGHT_META,
    7208976: Key.K_CONTEXT_MENU, # macOs
    1073741925: Key.K_CONTEXT_MENU,
    270336: Key.K_RIGHT_CONTROL,
    65508: Key.K_RIGHT_CONTROL, # macOs
    65362: Key.K_UP_ARROW,
    65364: Key.K_DOWN_ARROW,
    65361: Key.K_LEFT_ARROW,
    65363: Key.K_RIGHT_ARROW,
    # pygame.K_COLON: Key.K_COLON,
    # pygame.K_EXCLAIM: Key.K_EXCLAMATION,
    # 249: Key.K_U_GRAVE,
    # pygame.K_CARET: Key.K_CARET,
    # pygame.K_DOLLAR: Key.K_DOLLAR,
    # pygame.K_ASTERISK: Key.K_ASTERISK,
    # pygame.K_LESS: Key.K_LESSTHAN,
    # pygame.K_1: Key.K_AMPERSAND,
    # pygame.K_2: Key.K_E_ACUTE,
    # pygame.K_3: Key.K_DOUBLEQUOTE,
    # pygame.K_4: Key.K_SINGLEQUOTE,
    # pygame.K_5: Key.K_LEFTPAREN,
    # pygame.K_6: Key.K_MINUS,
    # pygame.K_7: Key.K_E_GRAVE,
    # pygame.K_8: Key.K_UNDERSCORE,
    # pygame.K_9: Key.K_C_CEDILLE,
    # pygame.K_0: Key.K_A_GRAVE,
    # pygame.K_RIGHTPAREN: Key.K_RIGHTPAREN,
    # pygame.K_EQUALS: Key.K_EQUALS,
}


def get_key(event: tkinter.Event) -> Key:
    number = event.keysym_num
    if number == 0:
        number = event.keycode
    return __KEY_TO_KL_KEY[number]
