# tuple of upper txt and lower text
rows = {
    # 'functions': {},
    # upper text, lower txt, key_name for key detection
    'numbers': [
        ('~', '`', '`'),
        ('!', '1', '1'),
        ('@', '2', '2'),
        ('#', '3', '3'),
        ('$', '4', '4'),
        ('%', '5', '5'),
        ('^', '6', '6'),
        ('&', '7', '7'),
        ('*', '8', '8'),
        ('(', '9', '9'),
        (')', '0', '0'),
        ('_', '-', '-'),
        ('+', '=', '='),
        ('Backspace', '', 'backspace'),
    ],
    'letters_1': [
        ('Tab', '', 'tab'),
        ('Q', '', 'q'),
        ('W', '', 'w'),
        ('E', '', 'e'),
        ('R', '', 'r'),
        ('T', '', 't'),
        ('Y', '', 'y'),
        ('U', '', 'u'),
        ('I', '', 'i'),
        ('O', '', 'o'),
        ('P', '', 'p'),
        ('{', '[', '['),
        ('}', ']', ']'),
        ('|', '\\', '\\'),
    ],
    'letters_2': [
        ('Caps Lock', '', 'caps lock'),
        ('A', '', 'a'),
        ('S', '', 's'),
        ('D', '', 'd'),
        ('F', '', 'f'),
        ('G', '', 'g'),
        ('H', '', 'h'),
        ('J', '', 'j'),
        ('K', '', 'k'),
        ('L', '', 'l'),
        (':', ';', ';'),
        ('"', "'", "'"),
        ('Enter', '', 'return'),
    ],
    'letters_3': [
        ('Shift', '', 'left shift'),
        ('Z', '', 'z'),
        ('X', '', 'x'),
        ('C', '', 'c'),
        ('V', '', 'v'),
        ('B', '', 'b'),
        ('N', '', 'n'),
        ('M', '', 'm'),
        ('<', ',', ','),
        ('>', '.', '.'),
        ('?', '/', '/'),
        ('Shift', '', 'right shift'),
    ],
    'spacebar_row': [
        ('Control', '', 'left control'),
        ('Win', '', 'left windows'),
        ('Alt', '', 'left alt'),
        ('', '', 'space bar'),
        ('Alt', '', 'right alt'),
        ('Wind', '', 'right windows'),
        ('Menu', '', 'menu'),
        ('Control', '', 'right control'),
    ],
    # 'uparrow': {'up arrow': '▲'},
}
row_locations = {
    'numbers': (0, 0),
    'letters_1': (0, 1),
    'letters_2': (0, 2),
    'letters_3': (0, 3),
    'spacebar_row': (0, 4),
} # in std key size coordinates? where 1, 1 is 1 letter key wide by 1 letter key tall
key_sizes = {
    'tab': (1.5, 1),
    'alt': (1.2, 1),
}
key_width_percent_remainder_sizes = {
    'caps lock': 45,
    'return': 55,
    'left shift': 46,
    'right shift': 54,
    'backspace': 100,
    'space bar': 100,
}
key_to_key_size = {
    'tab': 'tab',
    '\\': 'tab',
    'left control': 'tab',
    'right control': 'tab',
    'left alt': 'alt',
    'right alt': 'alt',
    'left windows': 'alt',
    'right windows': 'alt',
    'menu': 'alt',
}
# if key size is not defined, 1 key x by 1 key y size is assumed
