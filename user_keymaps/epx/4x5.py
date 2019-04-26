from kmk.consts import DiodeOrientation,
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P

import adafruit_dotstar
import board
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led[0] = (255, 255, 255)

keyboard = Firmware()

keyboard.debug_enabled = True
keyboard.col_pins = (P.D13, P.A3, P.A4, P.A2)
keyboard.row_pins = (P.D7, P.D10, P.D9, P.D12, P.D11)
keyboard.diode_orientation = DiodeOrientation.ROWS # ROW2COL

# ------------- Morse handling ----------------------

morse_codes = {".-": KC.A, "-.": KC.N}

class Morse:
    def __init__(self):
        self.code = ""
        self.state = "OFF"
        self.pending_timeout = None

    def trans(self, new_state, kbd_state, arg):
        transition = self.state + "_" +	new_state
        if keyboard.debug_enabled:
            print("transition " + transition)
        m = getattr(self, transition, None)
        if not m:
            if keyboard.debug_enabled:
                print("        	Invalid transition")
            return
        self.state = new_state
        m(self, kbd_state, arg)

    def OFF_STARTING(self, kbd_state, arg):
        self.trans("ON", kbd_state, arg)

    def STARTING_ON(self, kbd_state, arg):
        self.code = ""
        self.pending_timeout = None

    def ON_OFF(self, kbd_state, arg):
        pass

    def TYPING_OFF(self, kbd_state, arg):
        pass

    def ON_ON(self, kbd_state, arg):
        kbd_state.tap_key(KC.SPC)

    def ON_TYPING(self, kbd_state, c):
        self.code += c
        self.start_typing_timeout(kbd_state)

    def TYPING_TYPING(self, kbd_state, c):
        self.code += c
        self.start_typing_timeout(kbd_state)

    def TYPING_ON(self, kbd_state, arg):
        self.stop_typing_timeout(kbd_state)
        if self.code not in morse_codes:
            if keyboard.debug_enabled:
                print("Invalid code " + self.code)
            self.code = ""
            return
        key = morse_codes[self.code]
        self.code = ""
        kbd_state.tap_key(key)

    def TYPING_TIMEOUT(self, kbd_state, arg):
        self.code = ""
        self.trans("ON", None)

    def TIMEOUT_ON(self, kbd_state, arg):
        pass

    def TYPING_CANCEL(self, kbd_state, arg):
        self.stop_typing_timeout(kbd_state)
        self.code = ""
        self.trans("ON", None)

    def CANCEL_ON(self, kbd_state, arg):
        pass

    def start_typing_timeout(self, kbd_state):
        self.stop_typing_timeout(kbd_state)
        self.pending_timeout = kbd_state.set_timeout(2000, self.timeout)

    def stop_typing_timeout(self, kbd_state):
        if self.pending_timeout is not None:
            kbd_state.cancel_timeout(self.pending_timeout)
        self.pending_timeout = None
   
    def turn_on(self, kbd_state):
       self.trans("STARTING", kbd_state)
 
    def turn_off(self, kbd_state):
       self.trans("OFF", kbd_state)

    def dot(self, kbd_state):
        self.trans("TYPING", kbd_state, ".")

    def dash(self, kbd_state):
        self.trans("TYPING", kbd_state, "-")
        
    def spc(self, kbd_state):
        self.trans("ON", kbd_state)

    def cancel(self, kbd_state):
        self.trans("CANCEL", None)

    def timeout(self):
        self.pending_timeout = None
        self.trans("TIMEOUT", None)

morse = Morse()

# ---------------------- Keymap ---------------------------------------------------------

def layer_changed(key, state, kc, coord_int, coord_raw):
    if not state.active_layers:
        return
    layer = state.active_layers[-1]
    led[0] = ((255, 0, 0), (0, 255, 0), (0, 0, 255))[layer]
    if layer == 2:
        morse.turn_on(state)
    else:
        morse.turn_off(state)

mod0 = KC.TO(0)
mod1 = KC.TO(1)
mod2 = KC.TO(2)
mod0.after_press_handler(layer_changed)
mod1.after_press_handler(layer_changed)
mod2.after_press_handler(layer_changed)

def dot_on(key, state, kc, coord_int, coord_raw):
    morse.dot(state)
    return False

def dash_on(key, state, kc, coord_int, coord_raw):
    morse.dash(state)
    return False

def mute(key, state, kc, coord_int, coord_raw):
    return False

def spc_on(key, state, kc, coord_int, coord_raw):
    morse.spc(state)
    return False

def cancel_morse(key, state, kc, coord_int, coord_raw):
    morse.cancel(state)
    return False

dot = KC.B.clone()
dot.before_press_handler(dot_on)
dot.before_release_handler(mute)

dash = KC.C.clone()
dash.before_press_handler(dash_on)
dash.before_release_handler(mute)

spc = KC.SPC.clone()
spc.before_press_handler(spc_on)

cancel = KC.D.clone()
cancel.before_press_handler(cancel_morse)
cancel.before_release_handler(mute)

keyboard.keymap = [
    [
        [KC.ESC, KC.VOLD, KC.VOLU, KC.BSPC],
        [KC.P7,  KC.P8,   KC.P9,   mod1],
        [KC.P4,  KC.P5,   KC.P6,   mod1],
        [KC.P1,  KC.P2,   KC.P3,   KC.PENT],
        [KC.P0,  KC.P0,   KC.PDOT, KC.PENT]
    ],
    [
        [KC.ESC,  KC.VOLD, KC.VOLU, KC.BSPC],
        [KC.HOME, KC.UP,   KC.PGUP, mod2],
        [KC.LEFT, KC.NO,   KC.RGHT, mod2],
        [KC.END,  KC.DOWN, KC.PGDN, KC.PENT],
        [KC.INS,  KC.INS,  KC.DEL,  KC.PENT]
    ],
    [
        [KC.ESC,  KC.VOLD, KC.VOLU, KC.BSPC],
        [cancel,  dot,     dash,    mod0],
        [cancel,  cancel,  cancel,  mod0],
        [KC.MPRV, KC.MNXT, KC.MSTP, KC.PENT],
        [spc,     spc,     KC.MPLY, KC.PENT]
    ]
]

if __name__ == '__main__':
    led[0] = (255, 255, 0)
    keyboard.go()

