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
            self.output_is_col = True
            self.inputs = self.rows
            self.outputs = self.cols
        elif self.diode_orientation == DiodeOrientation.ROWS:
            self.output_is_col = False
            self.inputs = self.cols
            self.outputs = self.rows
        else:
            raise ValueError('Invalid DiodeOrientation: {}'.format(
                self.diode_orientation,
            ))

        output_mask = self.create_mask(self.outputs)
        self.set_iodir(0xffffffff ^ output_mask) # outputs are LO bits

        self.state = bytearray(len(self.inputs) * len(self.outputs))
        self.report = bytearray(3)

    def scan_for_changes(self):
        ba_idx = 0

        for oidx, opin in enumerate(self.outputs):
            # set one output pin LO
            bits = 0xffffffff ^ (1 << opin)
            self.set_gpio(bits)

            # get input pins and treat the result
            # LO = pressed, so we work on inverted value
            input_bits = 0xffffffff ^ self.get_gpio()

            for iidx, ipin in enumerate(self.inputs):
                new_val = (input_bits >> ipin) & 0x1
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    self.state[ba_idx] = new_val
                    if self.output_is_col:
                        self.report[0] = iidx
                        self.report[1] = oidx
                    else:
                        self.report[0] = oidx
                        self.report[1] = iidx
                    self.report[2] = new_val
                    return self.report

                ba_idx += 1

        return None
