# keyboardlayout
A python library to display different keyboards.
Works with pygame or tkinter
PRs with additional layouts or graphics backends are welcome.

If you need to show your users a graphic that shows a specific keyboard layout or a portion of a keyboard, this is the library for you.

## Features:
- qwerty + azerty included
- graphics backends: pygame + tkinter
- pygame: dynamically generate a sprite group showing a keyboard
- tkinter: dynamically generate a frmae containing frames and labels
- customize the keyboard with sizes, colors, key margin, padding, font, location, etc
- update a specific key with `update_key`

## Documentation
https://spacether.github.io/keyboardlayout/

## Examples
#### qwerty with colors
![qwerty colored](https://raw.githubusercontent.com/spacether/keyboardlayout/master/samples/images/qwerty_colored.jpg)

#### qwerty
![qwerty](https://raw.githubusercontent.com/spacether/keyboardlayout/master/samples/images/qwerty.jpg)

#### azerty laptop
![azerty_laptop](https://raw.githubusercontent.com/spacether/keyboardlayout/master/samples/images/azerty_laptop.jpg)

## Installation
Make sure that you are using Python3
```
pip install keyboardlayout
```

## Samples
- [pygame, qwerty](https://github.com/spacether/keyboardlayout/tree/master/samples/pygame_qwerty.py)
- [pygame, pressed keys](https://github.com/spacether/keyboardlayout/tree/master/samples/pygame_pressed_keys.py)
- [tkinter, qwerty](https://github.com/spacether/keyboardlayout/tree/master/samples/tkinter_qwerty.py)
- [tkinter, pressed keys](https://github.com/spacether/keyboardlayout/tree/master/samples/tkinter_pressed_keys.py)

## Usage
### pygame example
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
    margin=10,
    color=grey,
    txt_color=~grey,  # invert grey
    txt_font=pygame.font.SysFont('Arial', key_size//4),
    txt_padding=(key_size//6, key_size//10)
)
letter_key_size = (key_size, key_size)  # width, height
keyboard_layout = kl.KeyboardLayout(
    layout_name,
    keyboard_info,
    letter_key_size,
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
# make and activate virtual env
python3 -m venv venv
source venv/bin/activate

# if you want to edit the program and have the library use your edits
make develop

# to install separately in your virtual environment
make install
```

## Test
```
make test
```

## TODO
- change key for key_info in yaml file to keysym_number values (windows)
- get pygame pressed keys working
- get tkinter pressed keys working
