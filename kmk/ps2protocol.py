from ps2io import Ps2

class PS2Protocol:
	def __init__(self, data_pin, clock_pin):
		self.keyboard = Ps2(data_pin, clock_pin)
		self.state = "IDLE"
		self.state_handler = self.H_IDLE
		self.matrix = bytearray(32)

	def poll(self):
		b = self.keyboard.get_byte()
		if b >= 0:
			# print("PS/2 code %02x" % b)
			self.state_handler(b)
		elif self.matrix_made(0xfe):
			# simulate Pause release (not reported by PS/2)
			self.matrix_break(0xfe)
		return self.matrix

	def matrix_make(self, code):
		row = (code >> 3) & 0x1f
		col = code & 0x7
		bit = 1 << col
		self.matrix[row] |= bit

	def matrix_made(self, code):
		row = (code >> 3) & 0x1f
		col = code & 0x7
		bit = 1 << col
		return self.matrix[row] & bit

	def matrix_break(self, code):
		row = (code >> 3) & 0x1f
		col = code & 0x7
		bit = 1 << col
		self.matrix[row] &= ~bit

	def matrix_reset(self):
		for i in range(0, 32):
			self.matrix[i] = 0

	def trans(self, new_state, arg=None):
		trans_method_name = "ST_" + self.state + "_" + new_state
		handler_name = "H_" + new_state
		trans_method = getattr(self, trans_method_name, None)
		handler = getattr(self, handler_name, self.null_handler)
		if not trans_method:
			# print("Invalid trans", trans_method_name)
			self.state = "IDLE"
			self.state_handler = self.H_IDLE
			self.ST_FORCE_IDLE(None)
		else:
			self.state = new_state
			self.state_handler = handler
			trans_method(arg)

	def null_handler(self, _):
		pass

	def ST_FORCE_IDLE(self, _):
		pass

	def H_IDLE(self, b):
		if b == 0xe0:
			self.trans("EXT")
		elif b == 0xe1:
			self.trans("PAUSE1")
		elif b == 0xf0:
			self.trans("BREAK")
		elif b == 0xaa: # self-test passed
			self.matrix_reset()
		elif b == 0xfc: # self-test failed
			self.matrix_reset()
		elif b == 0x00: # problem
			self.matrix_reset()
		elif b == 0x84: # alt printscreen
			self.matrix_make(0xfc)
		else:
			self.matrix_make(b)

	def ST_IDLE_BREAK(self, _):
		pass

	def ST_BREAK_IDLE(self, _):
		pass

	def ST_IDLE_EXT(self, _):
		pass

	def H_EXT(self, b):
		if b == 0x12 or b == 0x59:
			self.trans("IDLE")
		elif b == 0xf0:
			self.trans("EBREAK")
		elif b == 0x7e:
			self.trans("CTRLPAUSE1")
		else:
			self.matrix_make(0x80 | b)
			self.trans("IDLE")

	def ST_EXT_IDLE(self, _):
		pass

	def ST_EXT_CTRLPAUSE1(self, _):
		pass

	def H_CTRLPAUSE1(self, b):
		if b == 0xe0:
			self.trans("CTRLPAUSE2")
		else:
			self.trans("IDLE")

	def ST_CTRLPAUSE1_IDLE(self, _):
		pass

	def ST_CTRLPAUSE1_CTRLPAUSE2(self, _):
		pass

	def H_CTRLPAUSE2(self, b):
		if b == 0xf0:
			self.trans("CTRLPAUSE3")
		else:
			self.trans("IDLE")

	def ST_CTRLPAUSE2_CTRLPAUSE3(self, _):
		pass

	def ST_CTRLPAUSE2_IDLE(self, _):
		pass

	def H_CTRLPAUSE3(self, b):
		if b == 0x7e:
			self.matrix_make(0xfe)
		self.trans("IDLE")

	def ST_CTRLPAUSE3_IDLE(self, _):
		pass

	def ST_IDLE_PAUSE1(self, _):
		pass

	def H_PAUSE1(self, b):
		if b == 0x14:
			self.trans("PAUSE2")
		else:
			self.trans("IDLE")

	def ST_PAUSE1_IDLE(self, _):
		pass

	def ST_PAUSE1_PAUSE2(self, _):
		pass

	def H_PAUSE2(self, b):
		if b == 0x77:
			self.trans("PAUSE3")
		else:
			self.trans("IDLE")

	def ST_PAUSE2_IDLE(self, _):
		pass

	def ST_PAUSE2_PAUSE3(self, _):
		pass

	def H_PAUSE3(self, b):
		if b == 0xe1:
			self.trans("PAUSE4")
		else:
			self.trans("IDLE")

	def ST_PAUSE3_IDLE(self, _):
		pass

	def ST_PAUSE3_PAUSE4(self, _):
		pass

	def H_PAUSE4(self, b):
		if b == 0xf0:
			self.trans("PAUSE5")
		else:
			self.trans("IDLE")

	def ST_PAUSE4_IDLE(self, _):
		pass

	def ST_PAUSE4_PAUSE5(self, _):
		pass

	def H_PAUSE5(self, b):
		if b == 0x14:
			self.trans("PAUSE6")
		else:
			self.trans("IDLE")

	def ST_PAUSE5_IDLE(self, _):
		pass

	def ST_PAUSE5_PAUSE6(self, _):
		pass

	def H_PAUSE6(self, b):
		if b == 0xf0:
			self.trans("PAUSE7")
		else:
			self.trans("IDLE")

	def ST_PAUSE6_IDLE(self, _):
		pass

	def ST_PAUSE6_PAUSE7(self, _):
		pass

	def H_PAUSE7(self, b):
		if b == 0x77:
			self.matrix_make(0xfe)
		self.trans("IDLE")

	def ST_PAUSE7_IDLE(self, _):
		pass

	def H_BREAK(self, b):
		if b == 0x84: # alt prinscreen
			self.matrix_break(0xfc)
		elif b == 0xf0:
			self.matrix_reset()
		else:
			self.matrix_break(b)
		self.trans("IDLE")

	def H_EBREAK(self, b):
		if b == 0x12 or b == 0x59:
			pass
		else:
			self.matrix_break(0x80 | b)
		self.trans("IDLE")

	def ST_EXT_EBREAK(self, b):
		pass

	def ST_EBREAK_IDLE(self, _):
		pass
