from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware as _Firmware
from kmk.ps2matrix import PS2MatrixScanner
import board

class Firmware(_Firmware):
	debug_enabled = False
	matrix_scanner = PS2MatrixScanner
	col_pins = [board.D10, board.D11, 0, 0, 0, 0, 0, 0] # actually, PS/2 data lines
	row_pins = [board.D10, board.D11, \
                0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, \
                0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, \
                0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, \
                ]
	diode_orientation = 1

keyboard = Firmware()

def layer_changed(key, state, kc, coord_int, coord_raw):
    bits = 0
    for l in state.active_layers:
        if l == 1:
            bits |= PS2MatrixScanner.LED_NUM_LOCK
        elif l == 2:
            bits |= PS2MatrixScanner.LED_SCROLL_LOCK
    keyboard.matrix.set_led(bits)

mod0 = KC.TO(0)
mod1 = KC.TO(1)
mod2 = KC.MO(2)
mod0.after_press_handler(layer_changed)
mod1.after_press_handler(layer_changed)
mod2.after_press_handler(layer_changed)
mod2.after_release_handler(layer_changed)

XXX = KC.NO
___ = KC.TRNS

keyboard.keymap = [
    [ #  0 8       1 9       2 a       3 b       4 c       5 d       6 e      7 f     PS/2 keycodes
        XXX,      KC.F9,    XXX,      KC.F5,    KC.F3,    KC.F1,    KC.F2,    KC.F12   , # 00
        XXX,      KC.F10,   KC.F8,    KC.F6,    KC.F4,    KC.TAB,   KC.GRAVE, KC.NO    ,
        XXX,      KC.LALT,  KC.LSFT,  KC.INT2,  KC.LCTL,  KC.Q,     KC.N1,    KC.NO    , # 10
        XXX,      XXX,      KC.Z,     KC.S,     KC.A,     KC.W,     KC.N2,    KC.NO    ,
        XXX,      KC.C,     KC.X,     KC.D,     KC.E,     KC.N4,    KC.N3,    KC.INT6  , # 20
        XXX,      KC.SPACE, KC.V,     KC.F,     KC.T,     KC.R ,    KC.N5,    KC.NO    ,
        XXX,      KC.N,     KC.B,     KC.H,     KC.G,     KC.Y,     KC.N6,    KC.NO    , # 30
        XXX,      XXX,      KC.M,     KC.J,     KC.U,     KC.N7,    KC.N8,    KC.NO    ,
        XXX,      KC.COMMA, KC.K,     KC.I,     KC.O,     KC.N0,    KC.N9,    KC.NO    , # 40
        XXX,      KC.DOT,   KC.SLASH, KC.L,     KC.SCLN,  KC.P,     KC.MINUS, KC.NO    ,
        XXX,      KC.INT1,  KC.QUOT,  XXX,      KC.LBRC,  KC.EQL,   XXX,      KC.NO    , # 50
        KC.RALT,  KC.RSFT,  KC.ENTER, KC.RBRC,  XXX,      KC.BSLS,  XXX,      KC.LANG5 ,
        XXX,      KC.NUBS,  KC.LANG4, KC.LANG3, KC.INT4,  XXX,      KC.BKSP,  KC.INT5  , # 60
        XXX,      KC.END,   KC.INT3,  KC.LEFT,  KC.HOME,  KC.PCMM,  XXX,      KC.NO    ,
        KC.INS,   KC.DEL,   KC.DOWN,  KC.NO,    KC.RIGHT, KC.UP,    KC.ESC,   mod1     , # 70
        KC.F11,   KC.PENT,  KC.PGDN,  KC.PPLS,  KC.PMNS,  KC.PGUP,  mod2,     KC.NO    ,
        XXX,      XXX,      XXX,      KC.F7,    XXX,      KC.RCMD,  KC.LCMD,  KC.NO    , # 00 ext
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      KC.RALT,  XXX,      XXX,      KC.RCTL,  KC.MPRV,  XXX,      KC.NO    , # 10
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.LCMD  ,
        XXX,      KC.VOLD,  XXX,      KC.MUTE,  XXX,      XXX,      XXX,      KC.RCMD  , # 20
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.SEL   ,
        XXX,      XXX,      KC.VOLU,  XXX,      KC.MPLY,  XXX,      XXX,      KC.NO    , # 30
        XXX,      XXX,      XXX,      KC.MSTP,  XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 40
        XXX,      XXX,      KC.PSLS,  XXX,      XXX,      KC.MNXT,  XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 50
        XXX,      XXX,      KC.PENT,  XXX,      XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 60
        XXX,      KC.END,   XXX,      KC.LEFT,  KC.HOME,  XXX,      XXX,      KC.NO    ,
        KC.INS,   KC.DEL,   KC.DOWN,  XXX,      KC.RIGHT, KC.UP,    XXX,      KC.NO    , # 70
        XXX,      XXX,      KC.PGDN,  XXX,      KC.PSCR,  KC.PGUP,  KC.PAUSE, KC.NO    ,
    ],
    [ #  0 8       1 9       2 a       3 b       4 c       5 d       6 e      7 f     Num Lock
        XXX,      KC.F9,    XXX,      KC.F5,    KC.F3,    KC.F1,    KC.F2,    KC.F12   , # 00
        XXX,      KC.F10,   KC.F8,    KC.F6,    KC.F4,    KC.TAB,   KC.GRAVE, KC.NO    ,
        XXX,      KC.LALT,  KC.LSFT,  KC.INT2,  KC.LCTL,  KC.Q,     KC.N1,    KC.NO    , # 10
        XXX,      XXX,      KC.Z,     KC.S,     KC.A,     KC.W,     KC.N2,    KC.NO    ,
        XXX,      KC.C,     KC.X,     KC.D,     KC.E,     KC.N4,    KC.N3,    KC.INT6  , # 20
        XXX,      KC.SPACE, KC.V,     KC.F,     KC.T,     KC.R ,    KC.N5,    KC.NO    ,
        XXX,      KC.N,     KC.B,     KC.H,     KC.G,     KC.Y,     KC.N6,    KC.NO    , # 30
        XXX,      XXX,      KC.M,     KC.J,     KC.U,     KC.N7,    KC.N8,    KC.NO    ,
        XXX,      KC.COMMA, KC.K,     KC.I,     KC.O,     KC.N0,    KC.N9,    KC.NO    , # 40
        XXX,      KC.DOT,   KC.SLASH, KC.L,     KC.SCLN,  KC.P,     KC.MINUS, KC.NO    ,
        XXX,      KC.INT1,  KC.QUOT,  XXX,      KC.LBRC,  KC.EQL,   XXX,      KC.NO    , # 50
        KC.RALT,  KC.RSFT,  KC.ENTER, KC.RBRC,  XXX,      KC.BSLS,  XXX,      KC.LANG5 ,
        XXX,      KC.NUBS,  KC.LANG4, KC.LANG3, KC.INT4,  XXX,      KC.BKSP,  KC.INT5  , # 60
        XXX,      KC.P1,    KC.INT3,  KC.P4,    KC.P7,    KC.PCMM,  XXX,      KC.NO    ,      
        KC.P0,    KC.PDOT,  KC.P2,    KC.P5,    KC.P6,    KC.P8,    KC.ESC,   mod0     , # 70
        KC.F11,   KC.PENT,  KC.P3,    KC.PPLS,  KC.PMNS,  KC.P9,    mod2,     KC.NO    ,      
        XXX,      XXX,      XXX,      KC.F7,    XXX,      KC.RCMD,  KC.LCMD,  KC.NO    , # 00 ext
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      KC.RALT,  XXX,      XXX,      KC.RCTL,  KC.MPRV,  XXX,      KC.NO    , # 10
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.LCMD  ,
        XXX,      KC.VOLD,  XXX,      KC.MUTE,  XXX,      XXX,      XXX,      KC.RCMD  , # 20
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.SEL   ,
        XXX,      XXX,      KC.VOLU,  XXX,      KC.MPLY,  XXX,      XXX,      KC.NO    , # 30
        XXX,      XXX,      XXX,      KC.MSTP,  XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 40
        XXX,      XXX,      KC.PSLS,  XXX,      XXX,      KC.MNXT,  XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 50
        XXX,      XXX,      KC.PENT,  XXX,      XXX,      XXX,      XXX,      KC.NO    ,
        XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      XXX,      KC.NO    , # 60
        XXX,      KC.END,   XXX,      KC.LEFT,  KC.HOME,  XXX,      XXX,      KC.NO    ,
        KC.INS,   KC.DEL,   KC.DOWN,  XXX,      KC.RIGHT, KC.UP,    XXX,      KC.NO    , # 70
        XXX,      XXX,      KC.PGDN,  XXX,      KC.PSCR,  KC.PGUP,  KC.PAUSE, KC.NO    ,
    ],
    [ #  0 8      1 9       2 a       3 b       4 c       5 d       6 e       7 f     Scroll Lock
        ___,      KC.VOLD,   ___,     KC.MSTP,  KC.MRWD,  KC.F11,   KC.F12,   ___,     # 00
        ___,      KC.VOLU,  KC.MNXT,  KC.MPLY,  KC.MFFD,  ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 10
        ___,      ___,      ___,      KC.SLCK,  ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 20
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 30 
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 40
        ___,      ___,      ___,      ___,      ___,      KC.PAUSE, ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 50
        KC.CAPS,  ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 60
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      KC.NLCK,  # 70
        ___,      ___,      ___,      ___,      KC.PSCR,  ___,      ___,      ___,      
        ___,      ___,      ___,      KC.MPRV,  ___,      KC.SEL,   ___,      ___,     # 00 ext
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 10
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 20
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 30
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 40
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,     # 50
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      #60 
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      #70  
        ___,      ___,      ___,      ___,      ___,      ___,      ___,      ___,      
    ],
]

if __name__ == '__main__':
    keyboard.go()
