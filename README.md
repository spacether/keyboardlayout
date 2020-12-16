# keyboardlayout
A python library to display different keyboards.
Works with pygame or tkinter.

If you need to show your users a graphic that shows a specific keyboard layout or a portion of a keyboard, this is the library for you.

## Features:
- shows a keyboard to the user
- keyboard layouts
  - qwerty
  - azerty laptop
- graphics backends
  - pygame (uses sprite groups)
  - tkinter (uses frames + labels)
- customize the keyboard with sizes, colors, key margin, padding, font, location, etc
- update a specific key with `update_key`
- can update key images when keys are pressed

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
import keyboardlayout.pygame as klp
import pygame

layout_name = kl.LayoutName.QWERTY
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
keyboard_layout = klp.KeyboardLayout(
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
- get tkinter pressed keys working so red looks correct
