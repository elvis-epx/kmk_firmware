from kmk.consts import DiodeOrientation,
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P

import adafruit_dotstar
import board
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led[0] = (255, 255, 255)

keyboard = Firmware()

keyboard.debug_enabled = False
keyboard.col_pins = (P.D13, P.A3, P.A4, P.A2)
keyboard.row_pins = (P.D7, P.D10, P.D9, P.D12, P.D11)
keyboard.diode_orientation = DiodeOrientation.ROWS # ROW2COL

# ---------------------- Keymap ---------------------------------------------------------

def layer_changed(key, state, kc, coord_int, coord_raw):
    if not state.active_layers:
        return
    layer = state.active_layers[-1]
    led[0] = ((255, 0, 0), (0, 255, 0), (0, 0, 255))[layer]

mod0 = KC.TO(0)
mod1 = KC.TO(1)
mod2 = KC.TO(2)
mod0.after_press_handler(layer_changed)
mod1.after_press_handler(layer_changed)
mod2.after_press_handler(layer_changed)

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
        [KC.HOME, KC.UP,   KC.PGUP,   mod2],
        [KC.LEFT, KC.NO,   KC.RGHT,   mod2],
        [KC.END,  KC.DOWN, KC.PGDN,   KC.PENT],
        [KC.INS,  KC.INS,  KC.DEL,    KC.PENT]
    ],
    [
        [KC.ESC,  KC.VOLD, KC.VOLU, KC.BSPC],
        [KC.SPC,  KC.B,    KC.C,    mod0],
        [KC.NO,   KC.NO,   KC.NO,   mod0],
        [KC.MPRV, KC.MNXT, KC.MSTP, KC.PENT],
        [KC.MUTE, KC.MUTE, KC.MPLY, KC.PENT]
    ]
]

if __name__ == '__main__':
    led[0] = (255, 0, 0)
    keyboard.go()

