from kmk.consts import DiodeOrientation,
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P

keyboard = Firmware()

keyboard.col_pins = (P.D13, P.A3, P.A4, P.A2)
keyboard.row_pins = (P.D7, P.D10, P.D9, P.D12, P.D11)
keyboard.diode_orientation = DiodeOrientation.ROWS # ROW2COL

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        [KC.A, KC.B, KC.C, KC.D],
        [KC.E, KC.F, KC.G, KC.H],
        [KC.I, KC.J, KC.K, KC.L],
        [KC.M, KC.N, KC.O, KC.P],
        [KC.Q, KC.R, KC.S, KC.T]
    ]
]

if __name__ == '__main__':
    keyboard.go()
