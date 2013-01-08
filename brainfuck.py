#!/usr/bin/python
from time import sleep

hw =  '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>'
hw += '++.>+.+++++++..+++.>++.<<+++++++++++++++.>.'
hw += '+++.------.--------.>+.>.'
# found on wikipedia

fibo =  '+++++++++++>+>>>>++++++++++++++++++++++++'
fibo += '++++++++++++++++++++>++++++++++++++++++++'
fibo += '++++++++++++<<<<<<[>[>>>>>>+>+<<<<<<<-]>>'
fibo += '>>>>>[<<<<<<<+>>>>>>>-]<[>++++++++++[-<-['
fibo += '>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<[>'
fibo += '>>+<<<-]>>[-]]<<]>>>[>>+>+<<<-]>>>[<<<+>>'
fibo += '>-]+<[>[-]<[-]]>[<<+>>[-]]<<<<<<<]>>>>>[+'
fibo += '+++++++++++++++++++++++++++++++++++++++++'
fibo += '++++++.[-]]++++++++++<[->-<]>++++++++++++'
fibo += '++++++++++++++++++++++++++++++++++++.[-]<'
fibo += '<<<<<<<<<<<[>>>+>+<<<<-]>>>>[<<<<+>>>>-]<'
fibo += '-[>>.>.<<<[-]]<<[>>+>+<<<-]>>>[<<<+>>>-]<'
fibo += '<[<+>-]>[<+>-]<<<-]'
# found http://esoteric.sange.fi/brainfuck/bf-source/prog/fibonacci.txt
# don't use this with the verbose option. just don't.

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
		self.outputStack.append(chr(self.array[self.cell]))
	
	def input(self):
		""" takes input from cli.  needs work. """
		i = raw_input('bf> ')
		if i:
			i = ord(i)
		else:
			i = 0
		self.array[self.cell] = i

	def find(self, ptr, direction):
		""" finds the matching bracket in either given direction """
		b = [None,'[',']']
		count = 1
		while count:
			ptr += direction
			if self.code[ptr] == b[direction]:
				count += 1
			elif self.code[ptr] == b[direction*-1]:
				count -= 1
		self.ptr = ptr

	def begin(self):
		""" matches opening bracket. """
		if not self.array[self.cell]:
			self.find(self.ptr, 1)
	
	def end(self):
		""" matches end bracket. """
		if self.array[self.cell]:
			self.find(self.ptr, -1)

	def debug(self):
		"""
		prints verbose information to the screen.

		verbose=2 : shows code progression (really cool)
		verbose=3 : shows array values     (awesome to debug with)
		verbose=6 : shows both 2 and 3, one on each line

		if logTo is set, it won't print to the screen, but to the file.
		if not set, it'll sleep on every step, which may lock up the
		python process itself until it's done.

		"""
		if not self.logTo:
			sleep(self.step)
		if self.verbose % 2 == 0:
			op = ''
			for x, c in enumerate(self.code):
				if x == self.ptr:
					op += '('+c+')'
				elif x == self.ptr+1:
					op += c
				else:
					op += ' '+c
			
			if self.logTo:
				self.debugStack.append(op)
			else:
				print op
		if self.verbose % 3 == 0:
			debugString = str(self.code[self.ptr]) + str(self.array)
			if self.logTo:
				self.debugStack.append(debugString)
			else:
				print debugString

	def compile(self):
		"""
		matches symbols to the handlers until it reaches the end of the code.

		if logTo is set, it prints the debugStack to the file, as well as the
		code output.

		"""
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
		
		if self.logTo:
			with open(self.logTo, 'w') as f:
				f.write('\n'.join(self.debugStack)+'\n\n')
				f.write(''.join(self.outputStack))

		print ''.join(self.outputStack)

	def clean(self):
		""" removes all non-brainfuck commands. """
		self.code = ''.join(filter(lambda x: x in '+-<>.,[]', self.code))

	def __init__(self, code=None, verbose=0, step=0, inFile=None, logTo=None):
		"""
		make the class and initialize the values used.

		code: string/list of code
		verbose: uses debugger on every step, see self.debug
		step: interval between debug outputs
		inFile: file name to read code from
		logTo: file to send output to

		use:
			x = Brainfuck(code)
			x = Brainfuck(f='bf.b')
			x = Brainfuck(code, verbose=6)
			x = Brainfuck(f='bf.bf', verbose=2)

			x = Brainfuck(f='bf.bf', logTo='bf.log', verbose=2)

			recommended with debugger use.
			x.clean()

			x.compile()

		"""

		self.code = code
		if inFile:
			with open(inFile, 'r') as b:
				self.code = b.read()
		self.verbose = verbose
		self.step = step
		self.logTo = logTo
		self.array = [0]
		self.cell = 0
		self.ptr = 0
		self.outputStack = list()
		self.debugStack = list()
