from kmk.keys import KC

morse_codes = {
    ".-": KC.A,
    "-...": KC.B,
    "-.-.": KC.C,
    "-..": KC.D,
    ".": KC.E,
    "..-.": KC.F,
    "--.": KC.G,
    "....": KC.H,
    "..": KC.I,
    ".---": KC.J,
    "-.-": KC.K,
    ".-..": KC.L,
    "--": KC.M,
    "-.": KC.N,
    "---": KC.O,
    ".--.": KC.P,
    "--.-": KC.Q,
    ".-.": KC.R,
    "...": KC.S,
    "-": KC.T,
    "..-": KC.U,
    "...-": KC.V,
    ".--": KC.W,
    "-..-": KC.X,
    "-.--": KC.Y,
    "--..": KC.Z,
    ".----": KC.N1,
    "..---": KC.N2,
    "...--": KC.N3,
    "....-": KC.N4,
    ".....": KC.N5,
    "-....": KC.N6,
    "--...": KC.N7,
    "---..": KC.N8,
    "----.": KC.N9,
    "-----": KC.N0,
    "--..--": KC.COMM,
    ".-.-.-": KC.DOT,
    "-..-.": KC.SLSH,
    ".----.": KC.QUOT,
    "-.--.-": KC.LBRC,
    "-.--.": KC.RBRC,
    "-....-": KC.MINS,
    "-...-": KC.EQL
}

class Morse:
    def __init__(self):
        self.code = ""
        self.state = "OFF"
        self.pending_timeout = None

    def trans(self, new_state, kbd_state, arg):
        transition = self.state + "_" +	new_state
        if kbd_state.config.debug_enabled:
            print("transition " + transition)
        m = getattr(self, transition, None)
        if not m:
            if kbd_state.config.debug_enabled:
                print("        	Invalid transition")
            return
        self.state = new_state
        m(kbd_state, arg)

    def OFF_STARTING(self, kbd_state, arg):
        self.trans("ON", kbd_state, arg)

    def STARTING_ON(self, kbd_state, arg):
        self.code = ""
        self.pending_timeout = None

    def ON_OFF(self, kbd_state, arg):
        pass

    def OFF_OFF(self, kbd_state, arg):
        pass

    def TYPING_OFF(self, kbd_state, arg):
        self.stop_typing_timeout(kbd_state)
        pass

    def ON_ON(self, kbd_state, arg):
        kbd_state.tap_key(KC.SPC)

    def ON_TYPING(self, kbd_state, c):
        self.code += c
	if len(self.code) > 10:
	    self.code = "f"
        self.start_typing_timeout(kbd_state)

    def TYPING_TYPING(self, kbd_state, c):
        self.code += c
	if len(self.code) > 10:
	    self.code = "f"
        self.start_typing_timeout(kbd_state)

    def TYPING_ON(self, kbd_state, arg):
        self.stop_typing_timeout(kbd_state)
        if self.code not in morse_codes:
            if kbd_state.config.debug_enabled:
                print("Invalid code " + self.code)
            self.code = ""
            return
        key = morse_codes[self.code]
        self.code = ""
        kbd_state.tap_key(key)

    def TYPING_TIMEOUT(self, kbd_state, arg):
        self.code = ""
        self.trans("ON", kbd_state, arg)

    def TIMEOUT_ON(self, kbd_state, arg):
        pass

    def TYPING_CANCEL(self, kbd_state, arg):
        self.stop_typing_timeout(kbd_state)
        self.code = ""
        self.trans("ON", kbd_state, arg)

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
       self.trans("STARTING", kbd_state, None)
 
    def turn_off(self, kbd_state):
       self.trans("OFF", kbd_state, None)

    def dot(self, kbd_state):
        self.trans("TYPING", kbd_state, ".")

    def dash(self, kbd_state):
        self.trans("TYPING", kbd_state, "-")
        
    def spc(self, kbd_state):
        self.trans("ON", kbd_state, None)

    def cancel(self, kbd_state):
        self.trans("CANCEL", kbd_state, None)

    def timeout(self):
        self.pending_timeout = None
        self.trans("TIMEOUT", None, None)
