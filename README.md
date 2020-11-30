# keyboardlayout
A python library to display different keyboards.
The keyboard layouts are created with pygame sprites.
PRs with additional layouts or graphics backends are welcome.

If you need to show your users a graphic that shows a specific keyboard layout or a portion of a keyboard, this is the library for you.

## Installation
Make sure that you are using Python3
```
pip install keyboardlayout
```

## What you get
![qwerty](/sample_images/qwerty.png)

## Usage
```
import keyboardlayout
import pygame

layout_name = 'qwerty'
pygame.init()

position = (0, 0)
letter_key_size = (60, 60) # width, height
keyboard_padding = 2
key_margin = 10
key_color = pygame.Color('grey')
font_color = key_color.__invert__()

font_size = letter_key_size[0]//4
font = pygame.font.SysFont('Arial', font_size)
font_color = key_color.__invert__()
txt_padding = (letter_key_size[0]//6, letter_key_size[0]//10) # x, y
keyboard_layout = keyboardlayout.KeyboardLayout(
    layout_name,
    position,
    keyboard_padding,
    letter_key_size,
    key_margin,
    key_color,
    font_color,
    font,
    txt_padding,
    keyboard_color=font_color
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

### Todo
- Consolidate 2 color parameters into one dict input
- Dynamically make enum of different layout options
- Auto produce sample images
- Simple tests
- hook into different keyboard listeners
