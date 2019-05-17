from kmk.ps2protocol import PS2Protocol

class PS2MatrixScanner:
	def __init__(self, cols, *args, **kwargs):
		self.k = PS2Protocol(cols[0], cols[1])
		self.state = bytearray(32)
		self.report = bytearray(3)

	def scan_for_changes(self):
		matrix = self.k.poll()
		for row in range(0, 32):
			if matrix[row] == self.state[row]:
				continue
			self.report[0] = row
			for col in range(0, 7):
				bit = 1 << col
				if (matrix[row] & bit) == (self.state[row] & bit):
					continue
				self.report[1] = col
				if matrix[row] & bit: # press
					self.state[row] |= bit
					self.report[2] = True
				else: # release
					self.state[row] &= ~bit
					self.report[2] = False
				return self.report
