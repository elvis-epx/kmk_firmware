from kmk.consts import DiodeOrientation
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.pins import Pin as P
from kmk.morse import Morse

import adafruit_dotstar
import board
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led[0] = (255, 255, 255)

class Firmware(_Firmware):
	debug_enabled = False
	col_pins = (P.D13, P.A3, P.A4, P.A2)
	row_pins = (P.D7, P.D10, P.D9, P.D12, P.D11)
	diode_orientation = DiodeOrientation.ROWS # ROW2COL

keyboard = Firmware()

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
        KC.ESC, KC.VOLD, KC.VOLU, KC.BSPC,
        KC.P7,  KC.P8,   KC.P9,   mod1,
        KC.P4,  KC.P5,   KC.P6,   mod1,
        KC.P1,  KC.P2,   KC.P3,   KC.PENT,
        KC.P0,  KC.P0,   KC.PDOT, KC.PENT,
    ],
    [
        KC.ESC,  KC.VOLD, KC.VOLU, KC.BSPC,
        KC.HOME, KC.UP,   KC.PGUP, mod2,
        KC.LEFT, KC.NO,   KC.RGHT, mod2,
        KC.END,  KC.DOWN, KC.PGDN, KC.PENT,
        KC.INS,  KC.INS,  KC.DEL,  KC.PENT
    ],
    [
        KC.ESC,  KC.VOLD, KC.VOLU, KC.BSPC,
        cancel,  dot,     dash,    mod0,
        cancel,  cancel,  cancel,  mod0,
        KC.MPRV, KC.MNXT, KC.MSTP, KC.PENT,
        spc,     spc,     KC.MPLY, KC.PENT
    ]
]

if __name__ == '__main__':
    led[0] = (255, 128, 128)
    keyboard.go()

