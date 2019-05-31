from kmk.consts import DiodeOrientation
import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCPDualMatrixScanner:
    def __init__(
        self, cols, rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        *_args, **_kwargs
    ):
        i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
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

        # Mask with pins employed for input, used during scan
        self.input_mask = 0
        for bit in self.inputs:
            self.input_mask |= 1 << bit

        # Set GPIO pins for input or output
        output_mask = 0xffffffff
        for bit in self.outputs:
            output_mask ^= 1 << bit
        # 0 = output, 1 = input
        self.mcp1.iodir = output_mask & 0xffff
        self.mcp2.iodir = output_mask >> 16
        # 0 = pull-up disabled, 1 = pull-up enabled
        self.mcp1.gppu = output_mask & 0xffff
        self.mcp2.gppu = output_mask >> 16

        # Optimization: pre-calculates bit masks for every pin
        self.minputs = [ (1 << pin) for pin in self.inputs ]
        self.moutputs = [ 0xffffffff ^ (1 << pin) for pin in self.outputs ]

        self.report = bytearray(3)
        self.state = [ 0 for _ in self.outputs ]
        self.last_output_1 = 0
        self.last_output_2 = 0

        # Instrumentation
        self.x = 0
        self.last_time = time.monotonic()

    def scan_for_changes(self):
        ba_idx = 0
        self.x += 1
        if self.x >= 500:
            now = time.monotonic()
            print(500 / (now - self.last_time))
            self.x = 0
            self.last_time = now

        for oidx, opinmask in enumerate(self.moutputs):
            # set one output pin LO
            output_1 = opinmask & 0xffff
            output_2 = opinmask >> 16
            # Sending commands to MCP is the big bottleneck, and only one
            # bit changes at a time, so the extra logic is worthwhile
            if output_1 != self.last_output_1:
                self.mcp1.gpio = output_1
                self.last_output_1 = output_1
            if output_2 != self.last_output_2:
                self.mcp2.gpio = output_2
                self.last_output_2 = output_2

            # get input pins and handle if something changed
            input_bits = self.mcp1.gpio | (self.mcp2.gpio << 16)
            # LO = pressed, but we prefer to think in terms of HI = pressed
            input_bits = (0xffffffff ^ input_bits) & self.input_mask

            if input_bits == self.state[oidx]:
                # Nothing changed
                continue

            for iidx, ipinmask in enumerate(self.minputs):
                new_val = input_bits & ipinmask
                old_val = self.state[oidx] & ipinmask

                if old_val != new_val:
                    if new_val:
                        self.state[oidx] |= ipinmask
                    else:
                        self.state[oidx] &= (0xffffffff ^ ipinmask)
                    if self.output_is_col:
                        self.report[0] = iidx
                        self.report[1] = oidx
                    else:
                        self.report[0] = oidx
                        self.report[1] = iidx
                    self.report[2] = new_val and 1 or 0
                    return self.report

                ba_idx += 1

            # should not happen
            self.state[oidx] = input_bits

        return None
