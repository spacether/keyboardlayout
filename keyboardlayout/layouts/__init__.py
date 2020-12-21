from enum import Enum
from importlib import resources
import sys
from typing import Dict

import yaml

current_module = sys.modules[__name__]
YAML_EXTENSION = '.yaml'
# the key names come from keyboardlayout.keyconstant

def __generate_keyboard_layout_enum():
    layout_names = []
    for file_name in resources.contents(current_module):
        if file_name.endswith(YAML_EXTENSION):
            layout_names.append(file_name[:-len(YAML_EXTENSION)])

    layout_name_enum = Enum(
        'LayoutName',
        {layout_name.upper(): layout_name for layout_name in layout_names},
        type=str
    )
    layout_name_enum.__doc__ = (
        "An enum that holds the allowed layout names")
    return layout_name_enum

LayoutName = __generate_keyboard_layout_enum()


def get_layout(layout_name: LayoutName) -> Dict:
    if not isinstance(layout_name, LayoutName):
        raise ValueError(
            'Invalid input type, layout_name must be type LayoutName')
    layout_file_name = layout_name.value + YAML_EXTENSION
    stream = resources.read_text(current_module, layout_file_name)
    layout = yaml.safe_load(stream)
    return layout


class VerticalAnchor(Enum):
    """Enums used to set vertical text location"""
    TOP = 't'
    MIDDLE = 'm'
    BOTTOM = 'b'

class HorizontalAnchor(Enum):
    """Enums used to set horizontal text location"""
    LEFT = 'l'
    CENTER = 'c'
    RIGHT = 'r'

class LayoutConstant:
    """Constants used to acces data in keyboard layout yaml files"""
    KEY_SIZE = 'key_size'
    ROWS = 'rows'
    NAME = 'name'
    LOCATION = 'location'
    SIZE = 'size'
    TXT_INFO = 'txt_info'
    KEYS = 'keys'
