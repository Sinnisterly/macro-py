import win32con

class KeyTranslator:
    _special_keys = {
        # Mouse buttons
        0x01: "Left Click",
        0x02: "Right Click",
        0x04: "Middle Click",
        0x05: "X Button 1",
        0x06: "X Button 2",

        # Standard keys
        0x08: "Backspace",
        0x09: "Tab",
        0x0D: "Enter",
        0x10: "Shift", 
        0xA1: "Right Shift",
        0xA0: "Left Shift",
        0x11: "Ctrl",
        0xA2: "Left Ctrl",
        0xA3: "Right Ctrl",
        0x12: "Alt",
        0xA4: "Left Alt",
        0xA5: "Right Alt",
        0x13: "Pause",
        0x14: "Caps Lock",
        0x1B: "Esc",
        0x20: "Space",
        0x21: "Page Up",
        0x22: "Page Down",
        0x23: "End",
        0x24: "Home",
        0x25: "Left Arrow",
        0x26: "Up Arrow",
        0x27: "Right Arrow",
        0x28: "Down Arrow",
        0x29: "Select",
        0x2A: "Print",
        0x2B: "Execute",
        0x2C: "Print Screen",
        0x2D: "Insert",
        0x2E: "Delete",
        0x2F: "Help",
        0x91: "Scroll Lock",

        # Number row
        0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4",
        0x35: "5", 0x36: "6", 0x37: "7", 0x38: "8", 0x39: "9",

        # Alphabet
        0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E",
        0x46: "F", 0x47: "G", 0x48: "H", 0x49: "I", 0x4A: "J",
        0x4B: "K", 0x4C: "L", 0x4D: "M", 0x4E: "N", 0x4F: "O",
        0x50: "P", 0x51: "Q", 0x52: "R", 0x53: "S", 0x54: "T",
        0x55: "U", 0x56: "V", 0x57: "W", 0x58: "X", 0x59: "Y",
        0x5A: "Z",

        # Numeric keypad
        0x60: "Numpad 0", 0x61: "Numpad 1", 0x62: "Numpad 2", 0x63: "Numpad 3",
        0x64: "Numpad 4", 0x65: "Numpad 5", 0x66: "Numpad 6", 0x67: "Numpad 7",
        0x68: "Numpad 8", 0x69: "Numpad 9", 0x6A: "Numpad *", 0x6B: "Numpad +",
        0x6D: "Numpad -", 0x6E: "Numpad .", 0x6F: "Numpad /", 0x90: "Num Lock",

        # Function keys
        0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
        0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
        0x7C: "F13", 0x7D: "F14", 0x7E: "F15", 0x7F: "F16", 0x80: "F17", 0x81: "F18",
        0x82: "F19", 0x83: "F20", 0x84: "F21", 0x85: "F22", 0x86: "F23", 0x87: "F24",

        # OEM keys
        0xBA: ";", 0xBB: "=", 0xBC: ",", 0xBD: "-", 0xBE: ".", 0xBF: "/",
        0xC0: "`", 0xDB: "[", 0xDC: "\\", 0xDD: "]", 0xDE: "'",
        0xE2: "OEM 102",
        0xFE: "OEM Clear",

        # Media keys
        0xAD: "Volume Mute", 0xAE: "Volume Down", 0xAF: "Volume Up",
        0xB0: "Next Track", 0xB1: "Previous Track", 0xB2: "Stop Media",
        0xB3: "Play/Pause", 0xB4: "Launch Mail", 0xB5: "Launch Media Select",
        0xB6: "Launch Application 1", 0xB7: "Launch Application 2",

        # Browser keys
        0xA6: "Browser Back", 0xA7: "Browser Forward", 0xA8: "Browser Refresh",
        0xA9: "Browser Stop", 0xAA: "Browser Search", 0xAB: "Browser Favorites",
        0xAC: "Browser Home",

        # IME keys
        0x15: "IME Kana Mode", 0x16: "IME Hangul Mode", 0x17: "IME Junja Mode",
        0x18: "IME Final Mode", 0x19: "IME Hanja Mode", 0x1A: "IME Kanji Mode",
        0x1C: "IME Convert", 0x1D: "IME Non-Convert", 0x1E: "IME Accept",
        0x1F: "IME Mode Change",

        # Miscellaneous keys
        0xE7: "Packet", 0xF6: "Attention", 0xF7: "CrSel", 0xF8: "ExSel",
        0xF9: "Erase EOF", 0xFA: "Play", 0xFB: "Zoom", 0xFC: "NoName", 0xFD: "PA1",
    }

    _shifted_keys = {
        '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
        '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?', '`': '~',
    }

    _oem_keys = {
        ';:': 0xBA, '=+': 0xBB, ',<': 0xBC, '-_': 0xBD, '.>': 0xBE, '/?': 0xBF,
        '`~': 0xC0, '[{': 0xDB, '\\|': 0xDC, ']}': 0xDD, "'\"": 0xDE,
    }

    @staticmethod
    def vk_to_string(vk_code):
        if isinstance(vk_code, str):
            return vk_code  

        if vk_code in KeyTranslator._special_keys:
            return KeyTranslator._special_keys[vk_code]
        elif 32 <= vk_code <= 126:
            return chr(vk_code)
        else:
            return f"Key(0x{vk_code:02X})"

    @staticmethod
    def string_to_vk(key_string):
        special_keys_inverted = {v: k for k, v in KeyTranslator._special_keys.items()}
        if key_string in special_keys_inverted:
            return special_keys_inverted[key_string]
        elif key_string in KeyTranslator._shifted_keys.values():
            return special_keys_inverted[list(KeyTranslator._shifted_keys.keys())[list(KeyTranslator._shifted_keys.values()).index(key_string)]]
        elif key_string in KeyTranslator._oem_keys:
            return KeyTranslator._oem_keys[key_string]
        elif len(key_string) == 1:
            return ord(key_string.upper())
        elif key_string.startswith("Key(0x"):
            try:
                return int(key_string[5:-1], 16)
            except ValueError:
                print(f"Warning: Could not convert {key_string} to virtual key code")
                return None
        else:
            print(f"Warning: Unrecognized key string: {key_string}")
            return None

    @staticmethod
    def is_shift_key(vk_code):
        return vk_code in [0x10, 0xA0, 0xA1]

    @staticmethod
    def get_combination_string(vk_code, shift_pressed=False, ctrl_pressed=False, alt_pressed=False):
        parts = []
        if ctrl_pressed:
            parts.append("Ctrl")
        if alt_pressed:
            parts.append("Alt")
        if shift_pressed:
            parts.append("Shift")

        key_string = KeyTranslator.vk_to_string(vk_code)
        
        if shift_pressed and key_string in KeyTranslator._shifted_keys:
            key_string = KeyTranslator._shifted_keys[key_string]
        
        parts.append(key_string)
        return "+".join(parts)