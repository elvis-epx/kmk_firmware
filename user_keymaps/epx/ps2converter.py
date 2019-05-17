from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.ps2matrix import PS2MatrixScanner
import board

keyboard = Firmware()
keyboard.debug_enabled = True
keyboard.matrix_scanner = PS2MatrixScanner
keyboard.col_pins = [board.D10, board.D11] # actually, PS/2 data lines
keyboard.row_pins = [board.D10, board.D11]
keyboard.diode_orientation = 1

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
        [KC.A, KC.B, KC.C, KC.D,     KC.E, KC.F, KC.G, KC.H],
        [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8],
    ],
]

if __name__ == '__main__':
    keyboard.go()
