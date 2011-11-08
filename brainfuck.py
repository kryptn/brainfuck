from time import sleep

hw = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'



class Brainfuck(object):

	def increment(self):
		""" adds one to cell value """
		self.array[self.cell] += 1

	def decrement(self):
		""" subtracts one from cell value """
		self.array[self.cell] -= 1

	def left(self):
		""" shifts current position to the left by one """
		if self.cell > 0:
			self.cell -= 1

	def right(self):
		""" shifts to the right """
		if len(self.array) <= self.cell+1:
			self.array.append(0)
		self.cell += 1
	
	def output(self):
		""" outputs to a list, printed at the end. needs work."""
		self.stack.append(chr(self.array[self.cell]))
	
	def input(self):
		""" also needs work """
		i = raw_input('bf> ')
		if i:
			i = ord(i)
		else:
			i = 0
		self.array[self.cell] = i

	def find(self, ptr, direction):
		""" finds the matching bracket in either given direction """
		b = [0,'[',']']
		count = 1
		while count:
			ptr += direction
			if self.code[ptr] == b[direction]:
				count += 1
			elif self.code[ptr] == b[direction*-1]:
				count -= 1
		self.ptr = ptr

	def begin(self):
		""" matches opening bracket. this and the next could be cleaned up """
		if not self.array[self.cell]:
			self.find(self.ptr, 1)
	
	def end(self):
		""" matches end bracket """
		if self.array[self.cell]:
			self.find(self.ptr, -1)

	def debug(self):
		""" verbose=2 for code pos, verbose=3 for array values, verbose=6 for both """
		sleep(self.step)
		if self.verbose % 2 == 0:
			print ''.join([ '('+c+')' if x == self.ptr else ' '+c+' ' for x, c in enumerate(self.code) ])
		if self.verbose % 3 == 0:
			print self.code[self.ptr], self.array

	def compile(self):
		""" matches symbols to the handlers, runs till it reaches the end of the code """
		names = {'+':'increment',
				 '-':'decrement',
				 '<':'left',
				 '>':'right',
				 '.':'output',
				 ',':'input',
				 '[':'begin',
				 ']':'end',}
		
		while len(self.code) > self.ptr:
			if self.code[self.ptr] in names.keys():
				getattr(self, names[self.code[self.ptr]])()
			if self.verbose:
				self.debug()
			self.ptr += 1
		
		print ''.join(self.stack)

	def clean(self):
		""" removes all non-brainfuck symbols """
		self.code = ''.join(filter(lambda x: x in '+-<>.,[]', self.code))

	def __init__(self, code=None, verbose=0, step=0, f=None, clean=False):
		"""
		code: string/list of code
		verbose: uses debugger on every step, see self.debug
		step: 0 for instant, 1 for one step a second.  takes floats
		f: file name to read code from
		clean: clean code of non-brainfuck symbols

		use:  (these should work)
			x = Brainfuck(code)
			x = Brainfuck(f='bf.b')
			x = Brainfuck(code, verbose=6)
			x = Brainfuck(f='bf.b', verbose=2, clean=True)

			x.compile()
		"""
		self.code = code
		if f:
			with open(f, 'r') as b:
				self.code = b.read()
		if clean:
			clean()
		self.array = [0]
		self.cell = self.ptr = 0
		self.stack = list()
		self.verbose = verbose
		self.step = step
		self.compile()
