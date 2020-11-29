rows = [
    # upper text, lower txt, key_name for key detection
    {
        "name": 'numbers',
        "location": (0, 0),
        "keys": [
            {
                "name": 'code not known',
                "txt_info": {'bc': '2'},
            },
            {
                "name": '1',
                "txt_info": {'tc': '1', 'bc': '&'},
            },
            {
                "name": '2',
                "txt_info": {'tl': '2', 'bl': 'é', 'br': '~'},
            },
            {
                "name": '3',
                "txt_info": {'tl': '3', 'bl': '"', 'br': '#'},
            },
            {
                "name": '4',
                "txt_info": {'tl': '4', 'bl': '\'', 'br': '{'},
            },
            {
                "name": '5',
                "txt_info": {'tl': '5', 'bl': '(', 'br': '['},
            },
            {
                "name": '6',
                "txt_info": {'tl': '6', 'bl': '-', 'br': '|'},
            },
            {
                "name": '7',
                "txt_info": {'tl': '7', 'bl': 'è', 'br': '`'},
            },
            {
                "name": '8',
                "txt_info": {'tl': '8', 'bl': '_', 'br': '\\'},
            },
            {
                "name": '9',
                "txt_info": {'tl': '9', 'bl': 'ç', 'br': '^'},
            },
            {
                "name": '0',
                "txt_info": {'tl': '0', 'bl': 'à', 'br': '@'},
            },
            {
                "name": '°',
                "txt_info": {'tl': '°', 'bl': ')', 'br': ']'},
            },
            {
                "name": '+',
                "txt_info": {'tl': '+', 'bl': '=', 'br': '}'},
            },
            {
                "name": 'backspace',
                "txt_info": {'tl': 'Backspace'},
            },
        ],
    },
    # {
    #     "name": 'letters_1',
    #     "location": (0, 1),
    #     "keys": [
    #         ('Tab', '', 'tab'),
    #         ('A', '', 'a'),
    #         ('Z', '', 'z'),
    #         ('E', '', 'e'),
    #         ('R', '', 'r'),
    #         ('T', '', 't'),
    #         ('Y', '', 'y'),
    #         ('U', '', 'u'),
    #         ('I', '', 'i'),
    #         ('O', '', 'o'),
    #         ('P', '', 'p'),
    #         ('¨', '^', '^'),
    #         ('£', '$ ¤', '$'),
    #         ('Entrée', '', 'return'),
    #     ],
    # },
    # {
    #     "name": 'letters_2',
    #     "location": (0, 2),
    #     "keys": [
    #         ('Caps Lock', '', 'caps lock'),
    #         ('Q', '', 'q'),
    #         ('S', '', 's'),
    #         ('D', '', 'd'),
    #         ('F', '', 'f'),
    #         ('G', '', 'g'),
    #         ('H', '', 'h'),
    #         ('J', '', 'j'),
    #         ('K', '', 'k'),
    #         ('L', '', 'l'),
    #         ('M', '', 'm'),
    #         ('%', 'ù', 'ù'),
    #         ('μ', "*", "*"),
    #         ('', '', 'return'),
    #     ],
    # },
    # {
    #     "name": 'letters_3',
    #     "location": (0, 3),
    #     "keys": [
    #         ('Shift', '', 'left shift'),
    #         ('>', '<', '<'),
    #         ('W', '', 'w'),
    #         ('X', '', 'x'),
    #         ('C', '', 'c'),
    #         ('V', '', 'v'),
    #         ('B', '', 'b'),
    #         ('N', '', 'n'),
    #         ('?', ',', ','),
    #         ('.', ';', ';'),
    #         ('/', ':', ':'),
    #         ('§', '!', '!'),
    #         ('Shift', '', 'right shift'),
    #     ],
    # },
    # {
    #     "name": 'spacebar_row',
    #     "location": (0, 4),
    #     "keys": [
    #         ('Ctr', '', 'left control'),
    #         ('Fn', '', 'function'),
    #         ('Win', '', 'left windows'),
    #         ('Alt', '', 'left alt'),
    #         ('', '', 'space bar'),
    #         ('AltGr', '', 'right alt'),
    #         ('Control', '', 'right control'),
    #     ],
    # },
    # {
    #     "name": 'lower arrows',
    #     "location": (11.2, 4.6),
    #     "keys": [
    #         ('◄', '', 'left arrow'),
    #         ('▼', '', 'down arrow'),
    #         ('►', '', 'right arrow'),
    #     ]
    # },
    # {
    #     "name": 'upper arrows',
    #     "location": (12.3, 4.0),
    #     "keys": [
    #         ('▲', '', 'up arrow'),
    #     ]
    # },
]
key_sizes = {
    'tab': (1.5, 1),
    'caps lock': (1.7, 1),
    'right shift': (2.3, 1),
    'left shift': (1.2, 1),
    'space bar': (5, 1.2),
    'left control': (1.2, 1.2),
    'alt': (1, 1.2),
    'arrow': (1.1, 0.6)
}
# 14.5 - 11 = 3.5 - 2.3 = 1.2
key_width_percent_remainder_sizes = {
    'return': 100,
}
key_to_key_size = {
    'right shift': 'right shift',
    'left shift': 'left shift',
    'caps lock': 'caps lock',
    'backspace': 'tab',
    'tab': 'tab',
    '\\': 'tab',
    'left control': 'left control',
    'function': 'alt',
    'left alt': 'alt',
    'left windows': 'alt',
    'space bar': 'space bar',
    'right alt': 'alt',
    'right control': 'alt',
    'left arrow': 'arrow',
    'down arrow': 'arrow',
    'right arrow': 'arrow',
    'up arrow': 'arrow',
}
# if key size is not defined, 1 key x by 1 key y size is assumed
