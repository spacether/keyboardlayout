# 2.0.0
- Breaking: KeyboardLayout layout_name input type changed from str to LayoutName enum
- Fixed typo in readme code sample
- Python samples renamed to include pygame_ or tkinter_ prefix
- Adds init docstrings to KeyboardInfo, KeyInfo
- Adds Rect class used by the KeyboardLayoutInterface
- Adds a Key enum to store all possible keys for each backend
- Breaking: Changes update_key to ingest the Key enum
- Adds get_key method to get the key constant that is used to update keys
- Breaking KeyboardLayout class must now be imported from the pygame or tkinter submodules
- Breaking: pygame removed from the dependency list, if using the pygame backend
  the developer must install it into their environment

# 1.0.0
- qwerty + azerty included
- dynamically generate a pygame sprite group showing a keyboard
- customize the keyboard with sizes, colors, key margin, padding, font, location, etc
- override the default KeyInfo by passing in overrides
- update a specific key with update_key
