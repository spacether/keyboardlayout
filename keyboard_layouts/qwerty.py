# tuple of upper txt and lower text
rows = {
    # 'functions': {},
    'numbers': [
        ('~', '`'),
        ('!', '1'),
    ],
    # 'letters_1': {'left tab': 'tab'},
    # 'letters_2': {},
    # 'letters_3': {},
    # 'spacebar_row': {'fn': 'fn',... 'left': '◄', 'down': '▼', 'right': '►'},
    # 'uparrow': {'up arrow': '▲'},
}
row_locations = {'numbers': (0, 0)} # in std key size coordinates? where 1, 1 is 1 letter key wide by 1 letter key tall
key_sizes = {'tab': (1.5, 1), 'return': (2, 1), 'shift': (2, 1), 'command': (1.3, 1.1), 'tall': (1, 1.2), 'space bar': (6, 1)}
rows_to_key_size = {'spacebar_row': 'tall'}
keys_to_key_size = {'space bar': 'space bar', 'left command': 'command', 'right command': 'command'}
# if key size is not defined, 1 key x by 1 key y size is assumed
