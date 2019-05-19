from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.ps2matrix import PS2MatrixScanner
import board

keyboard = Firmware()
keyboard.debug_enabled = False
keyboard.matrix_scanner = PS2MatrixScanner
keyboard.col_pins = [board.D10, board.D11] # actually, PS/2 data lines
keyboard.row_pins = [board.D10, board.D11]
keyboard.diode_orientation = 1

# TODO PS/2 leds
# (CircuitPython seems not to be able to receive USB HID events at the moment,
# so we cannot pass the LED event down to PS/2.)

# The map below relates PS/2 keycodes to USB HID keys. The translation from
# PS/2 codes to a 32x8 virtual matrix is carried out by PS2Protocol.
# Single-byte keycodes are directly mapped. Extended keycodes (E0,code) are
# or'ed 0x80. This works because most keycodes are 7-bit, and the few
# 8-bit ones are either single or extended, not both.
#
# Note to myself and others interested in ABNT2 layout:
# NUBS = \ key right to Left Shift (which is shortened)
# INT1 = RO = / key left to Right Shift (which is shortened, too)
# PCMM = additional decimal dot key in dotmap, above ENTER
# Also, the 0x5d key (BSLS, \ in US keyboard) is merely moved
#     from above the double-width RETURN to left side of
#     double-height RETURN, but the keycode is the same.

keyboard.keymap = [
    [ #   0 8       1 9       2 a       3 b       4 c       5 d       6 e      7 f     PS/2 keycodes
        [KC.NO,    KC.F9,    KC.NO,    KC.F5,    KC.F3,    KC.F1,    KC.F2,    KC.F12   ], # 00
        [KC.NO,    KC.F10,   KC.F8,    KC.F6,    KC.F4,    KC.TAB,   KC.GRAVE, KC.NO    ],
        [KC.NO,    KC.LALT,  KC.LSFT,  KC.INT2,  KC.LCTL,  KC.Q,     KC.N1,    KC.NO    ], # 10
        [KC.NO,    KC.NO,    KC.Z,     KC.S,     KC.A,     KC.W,     KC.N2,    KC.NO    ],
        [KC.NO,    KC.C,     KC.X,     KC.D,     KC.E,     KC.N4,    KC.N3,    KC.INT6  ], # 20
        [KC.NO,    KC.SPACE, KC.V,     KC.F,     KC.T,     KC.R ,    KC.N5,    KC.NO    ],
        [KC.NO,    KC.N,     KC.B,     KC.H,     KC.G,     KC.Y,     KC.N6,    KC.NO    ], # 30
        [KC.NO,    KC.NO,    KC.M,     KC.J,     KC.U,     KC.N7,    KC.N8,    KC.NO    ],
        [KC.NO,    KC.COMMA, KC.K,     KC.I,     KC.O,     KC.N0,    KC.N9,    KC.NO    ], # 40
        [KC.NO,    KC.DOT,   KC.SLASH, KC.L,     KC.SCLN,  KC.P,     KC.MINUS, KC.NO    ],
        [KC.NO,    KC.INT1,  KC.QUOT,  KC.NO,    KC.LBRC,  KC.EQL,   KC.NO,    KC.NO    ], # 50
        [KC.CAPS,  KC.RSFT,  KC.ENTER, KC.RBRC,  KC.NO,    KC.BSLS,  KC.NO,    KC.LANG5 ],
        [KC.NO,    KC.NUBS,  KC.LANG4, KC.LANG3, KC.INT4,  KC.NO,    KC.BKSP,  KC.INT5  ], # 60
        [KC.NO,    KC.P1,    KC.INT3,  KC.P4,    KC.P7,    KC.PCMM,  KC.NO,    KC.NO    ],
        [KC.P0,    KC.PDOT,  KC.P2,    KC.P5,    KC.P6,    KC.P8,    KC.ESC,   KC.NLCK  ], # 70
        [KC.F11,   KC.PPLS,  KC.P3,    KC.PMNS,  KC.PAST,  KC.P9,    KC.SLCK,  KC.NO    ],
        [KC.NO,    KC.NO,    KC.NO,    KC.F7,    KC.NO,    KC.RCMD,  KC.LCMD,  KC.NO    ], # 00 ext
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO    ],
        [KC.NO,    KC.RALT,  KC.NO,    KC.NO,    KC.RCTL,  KC.MPRV,  KC.NO,    KC.NO    ], # 10
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.LCMD  ],
        [KC.NO,    KC.VOLD,  KC.NO,    KC.MUTE,  KC.NO,    KC.NO,    KC.NO,    KC.RCMD  ], # 20
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.SEL   ],
        [KC.NO,    KC.NO,    KC.VOLU,  KC.NO,    KC.MPLY,  KC.NO,    KC.NO,    KC.NO    ], # 30
        [KC.NO,    KC.NO,    KC.NO,    KC.MSTP,  KC.NO,    KC.NO,    KC.NO,    KC.NO    ],
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO    ], # 40
        [KC.NO,    KC.NO,    KC.PSLS,  KC.NO,    KC.NO,    KC.MNXT,  KC.NO,    KC.NO    ],
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO    ], # 50
        [KC.NO,    KC.NO,    KC.PENT,  KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO    ],
        [KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO    ], # 60
        [KC.NO,    KC.END,   KC.NO,    KC.LEFT,  KC.HOME,  KC.NO,    KC.NO,    KC.NO    ],
        [KC.INS,   KC.DEL,   KC.DOWN,  KC.NO,    KC.RIGHT, KC.UP,    KC.NO,    KC.NO    ], # 70
        [KC.NO,    KC.NO,    KC.PGDN,  KC.NO,    KC.PSCR,  KC.PGUP,  KC.PAUSE, KC.NO    ],
    ],
]

if __name__ == '__main__':
    keyboard.go()
