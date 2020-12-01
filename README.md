# keyboardlayout
A python library to display different keyboards.
The keyboard layouts are created with pygame sprites.
PRs with additional layouts or graphics backends are welcome.

If you need to show your users a graphic that shows a specific keyboard layout or a portion of a keyboard, this is the library for you.

## Features:
- qwerty + azerty included
- dynamically generate a pygame sprite group showing a keyboard
- customize the keyboard with sizes, colors, key margin, padding, font, location, etc
- modify a specific key with `update_key`

## Keyboard Layouts
qwerty
![qwerty](https://raw.githubusercontent.com/spacether/keyboardlayout/main/sample_images/qwerty.jpg)

azerty laptop
![azerty_laptop](https://raw.githubusercontent.com/spacether/keyboardlayout/main/sample_images/azerty_laptop.jpg)

## Installation
Make sure that you are using Python3
```
pip install keyboardlayout
```

## Usage
```
import keyboardlayout as kl
import pygame

layout_name = 'qwerty'
pygame.init()

key_size = 60
grey = pygame.Color('grey')
keyboard_info = kl.KeyboardInfo(
    position=(0, 0),
    padding=2,
    color=~grey
)
key_info = kl.KeyInfo(
    size=(key_size, key_size),  # width, height
    margin=10,
    color=grey,
    txt_color=~grey,  # invert grey
    txt_font=pygame.font.SysFont('Arial', key_size//4),
    txt_padding=(key_size//6, key_size//10)
)
keyboard_layout = kl.KeyboardLayout(
    layout_name,
    keyboard_info,
    key_info
)

screen = pygame.display.set_mode(
    (keyboard_layout.rect.width, keyboard_layout.rect.height))
screen.fill(pygame.Color('black'))

keyboard_layout.draw(screen)
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            running = False

pygame.quit()
```

## Local Installation
```
python3 -m venv venv
source venv/bin/activate
# if you want to edit the program and have the library use your edits
pip install -e .
# to install separately in your virtual environment
pip install .
```

## Test
```
python setup.py pytest
```

### Todo
- hook into different keyboard listeners
- produce docs?
