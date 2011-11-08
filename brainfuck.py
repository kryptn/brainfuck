from time import sleep

hw = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'



class Brainfuck(object):


	def increment(self):
		self.array[self.cell] += 1

	def decrement(self):
		self.array[self.cell] -= 1

	def left(self):
		if self.cell > 0:
			self.cell -= 1

	def right(self):
		if len(self.array) <= self.cell+1:
			self.array.append(0)
		self.cell += 1
	
	def output(self):
		self.stack.append(chr(self.array[self.cell]))
	
	def input(self):
		i = raw_input('bf> ')
		if i:
			i = ord(i)
		else:
			i = 0
		self.array[self.cell] = i

	def find(self, ptr, direction):
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
		if not self.array[self.cell]:
			self.find(self.ptr, 1)
	
	def end(self):
		if self.array[self.cell]:
			self.find(self.ptr, -1)

	def debug(self):
		sleep(self.step)
		if self.verbose % 2 == 0:
			print ''.join([ '('+c+')' if x == self.ptr else ' '+c+' ' for x, c in enumerate(self.code) ])
		if self.verbose % 3 == 0:
			print self.code[self.ptr], self.array

	def compile(self):
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
		self.code = ''.join(filter(lambda x: x in '+-<>.,[]', self.code))

	def __init__(self, code=None, verbose=0, step=0, f=None):
		if f:
			with open(f, 'r') as b:
				self.code = b.read()
		self.code = code
		self.array = [0]
		self.cell = 0
		self.ptr =  0
		self.verbose = verbose
		self.step = step
		self.stack = list()
		#self.compile()

bf = Brainfuck

#a = bf(hw, 2, .02)