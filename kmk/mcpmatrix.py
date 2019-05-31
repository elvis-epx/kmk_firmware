from kmk.consts import DiodeOrientation
import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCPDualMatrixScanner:
    def create_mask(self, a):
        mask = 0
        for x in a:
            mask |= 1 << x
        return mask

    def cpl32(self, a):
        return 0xffffffff ^ a

    def set_iodir(self, v):
        # 0 = output
        self.mcp1.iodir = v & 0xffff
        # 1 = pull-up enabled
        self.mcp1.gppu = v & 0xffff
        self.mcp2.iodir = (v >> 16) & 0xffff
        self.mcp2.gppu = (v >> 16) & 0xffff
    
    def set_gpio(self, v):
        self.mcp1.gpio = v & 0xffff
        self.mcp2.gpio = (v >> 16) & 0xffff
    
    def get_gpio(self):
        return self.mcp1.gpio + (self.mcp2.gpio << 16)
    
    def __init__(
        self, cols, rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        *_args, **_kwargs
    ):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp1 = MCP23017(i2c)
        self.mcp2 = MCP23017(i2c, address=0x21)
        self.cols = cols
        self.rows = rows
        self.diode_orientation = diode_orientation

        # MCP23017 has pull-up only, so we pull-up inputs and scan by
        # zeroing outputs. Diode points *from* input *to* output
        if self.diode_orientation == DiodeOrientation.COLUMNS:
            self.translate_coords = True
            self.inputs = self.rows
            self.outputs = self.cols
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.translate_coords = False
            self.inputs = self.cols
            self.outputs = self.rows
        else:
            raise ValueError('Invalid DiodeOrientation: {}'.format(
                self.diode_orientation,
            ))

        output_mask = self.cpl32(self.create_mask(self.outputs))
        self.set_iodir(output_mask)

        self.state = bytearray(len(self.inputs) * len(self.outputs))
        self.report = bytearray(3)

    def scan_for_changes(self):
        ba_idx = 0
        any_changed = False

        for oidx, opin in enumerate(self.outputs):
            # set output pin LO
            bits = 0xffffffff ^ (1 << opin)
            self.set_gpio(bits)

            # get input pins and treat the result
            input_bits = self.get_gpio()

            for iidx, ipin in enumerate(self.inputs):
                if input_bits & (1 << ipin):
                    new_val = 0 # HI = released
                else:
                    new_val = 1 # LO = pressed
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    if self.translate_coords:
                        # output is col
                        self.report[0] = iidx
                        self.report[1] = oidx
                    else:
                        # output is row
                        self.report[0] = oidx
                        self.report[1] = iidx

                    self.report[2] = new_val
                    self.state[ba_idx] = new_val
                    return self.report

                ba_idx += 1

        return None
