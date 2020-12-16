from keyboardlayout.key import Key

import pygame


class PygameKey(int):
    pass


__KEY_TO_KL_KEY = {
    pygame.K_BACKQUOTE: Key.K_BACKQUOTE,
    pygame.K_1: Key.K_1,
    pygame.K_2: Key.K_2,
    pygame.K_3: Key.K_3,
    pygame.K_4: Key.K_4,
    pygame.K_5: Key.K_5,
    pygame.K_6: Key.K_6,
    pygame.K_7: Key.K_7,
    pygame.K_8: Key.K_8,
    pygame.K_9: Key.K_9,
    pygame.K_0: Key.K_0,
    pygame.K_MINUS: Key.K_MINUS,
    pygame.K_EQUALS: Key.K_EQUALS,
    pygame.K_BACKSPACE: Key.K_BACKSPACE,
    pygame.K_TAB: Key.K_TAB,
    pygame.K_q: Key.K_Q,
    pygame.K_w: Key.K_W,
    pygame.K_e: Key.K_E,
    pygame.K_r: Key.K_R,
    pygame.K_t: Key.K_T,
    pygame.K_y: Key.K_Y,
    pygame.K_u: Key.K_U,
    pygame.K_i: Key.K_I,
    pygame.K_o: Key.K_O,
    pygame.K_p: Key.K_P,
    pygame.K_LEFTBRACKET: Key.K_LEFTBRACKET,
    pygame.K_RIGHTBRACKET: Key.K_RIGHTBRACKET,
    pygame.K_BACKSLASH: Key.K_BACKSLASH,
    pygame.K_CAPSLOCK: Key.K_CAPSLOCK,
    pygame.K_a: Key.K_A,
    pygame.K_s: Key.K_S,
    pygame.K_d: Key.K_D,
    pygame.K_f: Key.K_F,
    pygame.K_g: Key.K_G,
    pygame.K_h: Key.K_H,
    pygame.K_j: Key.K_J,
    pygame.K_k: Key.K_K,
    pygame.K_l: Key.K_L,
    pygame.K_SEMICOLON: Key.K_SEMICOLON,
    pygame.K_QUOTEDBL: Key.K_DOUBLEQUOTE,
    pygame.K_RETURN: Key.K_RETURN,
    pygame.K_LSHIFT: Key.K_LEFT_SHIFT,
    pygame.K_z: Key.K_Z,
    pygame.K_x: Key.K_X,
    pygame.K_c: Key.K_C,
    pygame.K_v: Key.K_V,
    pygame.K_b: Key.K_B,
    pygame.K_n: Key.K_N,
    pygame.K_m: Key.K_M,
    pygame.K_COMMA: Key.K_COMMA,
    pygame.K_PERIOD: Key.K_PERIOD,
    pygame.K_SLASH: Key.K_FORWARDSLASH,
    pygame.K_RSHIFT: Key.K_RIGHT_SHIFT,
    pygame.K_LCTRL: Key.K_LEFT_CONTROL,
    pygame.K_LMETA: Key.K_LEFT_META,
    pygame.K_LALT: Key.K_LEFT_ALT,
    pygame.K_SPACE: Key.K_SPACE,
    pygame.K_RALT: Key.K_RIGHT_ALT,
    pygame.K_RMETA: Key.K_RIGHT_META,
    1073741925: Key.K_CONTEXT_MENU,
    pygame.K_RCTRL: Key.K_RIGHT_CONTROL,
    pygame.K_QUOTE: Key.K_SINGLEQUOTE,
    pygame.K_UP: Key.K_UP_ARROW,
    pygame.K_DOWN: Key.K_DOWN_ARROW,
    pygame.K_LEFT: Key.K_LEFT_ARROW,
    pygame.K_RIGHT: Key.K_RIGHT_ARROW,
    pygame.K_COLON: Key.K_COLON,
    pygame.K_EXCLAIM: Key.K_EXCLAMATION,
    249: Key.K_U_GRAVE,
    pygame.K_CARET: Key.K_CARET,
    pygame.K_DOLLAR: Key.K_DOLLAR,
    pygame.K_ASTERISK: Key.K_ASTERISK,
    pygame.K_LESS: Key.K_LESSTHAN,
    pygame.K_1: Key.K_AMPERSAND,
    pygame.K_2: Key.K_E_ACUTE,
    pygame.K_3: Key.K_DOUBLEQUOTE,
    pygame.K_4: Key.K_SINGLEQUOTE,
    pygame.K_5: Key.K_LEFTPAREN,
    pygame.K_6: Key.K_MINUS,
    pygame.K_7: Key.K_E_GRAVE,
    pygame.K_8: Key.K_UNDERSCORE,
    pygame.K_9: Key.K_C_CEDILLE,
    pygame.K_0: Key.K_A_GRAVE,
    pygame.K_RIGHTPAREN: Key.K_RIGHTPAREN,
    pygame.K_EQUALS: Key.K_EQUALS,
}


def get_key(key: PygameKey) -> Key:
    return __KEY_TO_KL_KEY[key]