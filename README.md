# keyboardplotter
A python library to display different keyboards

## Installation
```
python3 -m venv venv
source venv/bin/activate
pip install pygame
python plotter.py
```

### Todo
- [DONE] change margin into padding and put it in the key image
- [DONE] add keyboard padding
- [DONE] add bg color
- [DONE] finish qwerty
- [DONE] fix height
- [DONE] Folds row location into rows definition for azerty
- [DONE] connect enter key on two rows
- [DONE] add azerty
- [DONE] add ability to color keys
- [DONE] Add margin into txt positioning
- [DONE] Add ability to offset keyboard to x,y location
- Move txt location into key definition
```
{
  "name": "q"
  "txt_info": {
    "tl/tc/tr": "text",
    "ml/mc/mr": "text",
    "bl/bc/br": "text",
  }
}
```
- Move key size into key definition
- Update qwerty file
- Change files to yaml
- hook into different keyboard listeners
- Simple tests
