from kmk.consts import DiodeOrientation, LeaderMode, UnicodeMode
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.mcpmatrix import MCPDualMatrixScanner

class Firmware(_Firmware):
    # col, rows are I/O pins, 0x0..0xf = first MCP, 0xf..0x1f = second MCP
    col_pins = (0x14, 0x15, 0x13, 0x11, 0x19, 0x12, 0x18, 0x10, 0x07, \
                     0x08, 0x0e, 0x0b, 0x06, 0x0d, 0x09, 0x0c, 0x0a)
    row_pins = (0x1d, 0x1f, 0x1e, 0x1c, 0x1a, 0x1b)
    diode_orientation = DiodeOrientation.ROWS
    matrix_scanner = MCPDualMatrixScanner
    debug_enabled = False

keyboard = Firmware()

XXX = KC.NO
________ = KC.TRANSPARENT

keyboard.keymap = [
    [
        KC.ESC,   XXX,      KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,    KC.F6,    KC.F7,
            KC.F8,    KC.F9,    KC.F10,   KC.F11,   KC.F12,   KC.PSCR,  KC.SLCK,  KC.PAUSE,
        KC.GRV,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,    KC.N6,    KC.N7,    KC.N8,
            KC.N9,    KC.N0,    KC.MINUS, KC.EQUAL, KC.BKSP,  KC.INS,   KC.HOME,  KC.PGUP,
        KC.TAB,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,     KC.Y,     KC.U,     KC.I,
            KC.O,     KC.P,     KC.LBRC,  KC.RBRC,  KC.BSLS,  KC.DEL,   KC.END,   KC.PGDN,
        KC.LCTL,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,     KC.H,     KC.J,     KC.K,
            KC.L,     KC.SCLN,  KC.QUOT,  XXX,      KC.ENT,   XXX,      XXX,      XXX,
        KC.LSFT,  XXX,      KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,     KC.N,     KC.M,
            KC.COMMA, KC.DOT,   KC.SLASH, KC.RSFT,  XXX,      XXX,      KC.UP,    XXX,
        KC.LCTL,  KC.LALT,  KC.LWIN,  XXX,      XXX,      XXX,      XXX,      XXX,      KC.SPACE,
            XXX,      KC.RWIN,  KC.RALT,  KC.RCTL,  KC.MO(1), KC.LEFT,  KC.DOWN,  KC.RIGHT,
    ],
    [
        ________, ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, ________, ________, ________, ________, ________, ________, ________,
        ________, ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, ________, ________, ________, ________, KC.MPLY,  KC.MPLY,  KC.MPLY,
        ________, ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, ________, ________, ________, ________, KC.MPLY,  KC.MPLY,  KC.MPLY,
        KC.CAPS,  ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, ________, ________, ________, ________, ________, ________, ________,
        ________, ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, ________, ________, ________, ________, ________, KC.VOLU,  ________,
        ________, ________, ________, ________, ________, ________, ________, ________, ________, 
            ________, KC.APP, ________, ________, ________, KC.MPRV,  KC.VOLD,  KC.MNXT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
