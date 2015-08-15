# -*- coding:utf8 -*-
import random
import sys
balance = False

class Board:
	def __init__(self, (width, height)):
		self.width = width
		self.height = height
		self.data = [ [0 for j in range(0, width)] for i in range(0, height)]
	def get_row(self, row):
		return self.data[row][:]
	def get_col(self, col):
		ret = []
		for i in range(0, self.height):
			ret.append(self.data[i][col])
		return ret
	def get(self, (row, col)):
		return self.data[row][col]
	def get_width(self):
		return self.width
	def get_height(self):
		return self.height
	def set(self, (width, height), value):
		self.data[width][height] = value
	def set_row(self, row, value):
		self.data[row] = value
	def set_col(self, col, value):
		for i in range(0, self.height):
			self.data[i][col] = value[i]
	def to_image(self):
		pass
	def show(self):
		for i in self.data:
			for j in i:
				if j == 1:
					print '*',
				else:
					print ' ',
			print ''
		print '\n\n'
		
def j(n):
	ret = 1
	for i in range(1, n+1):
		ret *= i
	return ret
	
def c(m, n):
	return j(m)/j(n)/j(m-n)

def i2l(n):
	if n == 0:
		return [0]
	elif n == 1:
		return [1]
	else:
		return i2l(n/2) + [n%2]

def l2i(l):
	if len(l) == 1:
		return l[0]
	else:
		return l[len(l)-1] + 2*l2i(l[:len(l)-1])

def cc(m, n):
	ret = [1]*n + [0]*(m-n)
	while ret.index(1) != m - n:		
		yield ret
		k = l2i(ret)
		k -= 1
		while i2l(k).count(1) != n:
			k -= 1
		ret = i2l(k)
		ret = [0] * (m-len(ret)) + ret
	yield ret
	
def f(n, v):
	sum = len(v) - 1
	for i in v:
		sum += i
	return c(n - sum + len(v), len(v))

def ff(n, v):
	
	sum = len(v) - 1
	for i in v:
		sum += i
	mm = n - sum + len(v)
	nn = len(v)
	for ii in cc(mm, nn):
		s = 0
		i = ii[:]
		for k in range(0, len(v)):
			s = i.index(1, s)
			s += 1
			i[s:s] = [1] * (v[k] - 1)
			s += v[k] - 1
			if k != len(v) - 1:
				i[s:s] = [0]
				s += 1
		yield i

#def collosion(v, v_new):
#	for i, j in zip(v, v_new):
#		if i == 1 and j == 0:
#			return True
#	return False

def can_black(board, (m, n), r_values = None, c_values = None):
	row = board.get_row(m)
	row[n] = 1
	ret = 0
	if r_values:
		for kk in ff(board.get_width(), r_values):
			if is_new_step(row, kk, r_values):
				ret += 1
				break
	else:
		ret += 1
		
	col = board.get_col(n)
	col[m] = 1
	if c_values:
		for kk in ff(board.get_height(), c_values):
			if is_new_step(col, kk, c_values):
				ret += 1
				break
	else:
		ret += 1
	return ret == 2

def is_balance(values):
	l = len(values)
	for i in range(0, l/2):
		j = l - 1 - i
		if values[i] != values[j]:
			return False
	return True

def not_collosion_r(board, rowNo, newRow, valuse, w, h):
	if balance and (not is_balance(newRow)):
		return False
	row = board.get_row(rowNo)
	if not is_new_step(row, newRow, valuse):
		return False
	for i in range(0, len(row)):
		if row[i] == 0 and newRow[i] == 1:
			if not can_black(board, (rowNo, i), c_values = w[i]):
				return False
	return True
	
def not_collosion_c(board, colNo, newCol, valuse, w, h):
	col = board.get_col(colNo)
	if not is_new_step(col, newCol, valuse):
		return False
	for i in range(0, len(col)):
		if col[i] == 0 and newCol[i] == 1:
			if not can_black(board, (i, colNo), r_values = h[i]):
				return False
	return True
			
def is_new_step(v, v_new, values):
	if sum(v_new) > sum(values):
		return False
	for i, j in zip(v, v_new):
		if i == 1 and j == 0:
			return False
	return True
	
def choose(array):
	s = sum(array)
	c = random.randint(1, s)
	a = 0
	for i in range(len(array)):
		a += array[i]
		if a >= c:
			return i
			
def solve(w, h):
	global balance
	board = Board((len(w), len(h)))
	balance = is_balance(w)
	unfinished = 2
	count = 0
	wc = []
	hc = []
	for i in w:
		wc.append(sum(i)+len(i)-1)
	for i in h:
		hc.append(sum(i)+len(i)-1)	
	while unfinished > 0:
		count += 1
		unfinished -= 1
		for _i in range(0, board.get_width()):
			i = _i
			print 'The %d col' % i
			values = w[i]
			if count == 1 and sum(values)+len(values)-1 <= board.get_height():
				continue
			length = len(w[i])
			col = board.get_col(i)
			n = 0
			validValues = []
			test = [0] * board.get_height()
			for kk in ff(board.get_height(), values):
				if not_collosion_c(board, i, kk, values, w, h):
					n += 1
					validValues.append(kk)
					test = map(lambda x,y:x+y, test, kk)
			if i == 4:
				print n
			test = map(lambda x:1 if x==n and n > 0 else 0, test)
			if is_new_step(col, test, values) and test.count(1) > col.count(1):
				unfinished = 2
			test = map(lambda x,y:x|y, test, col)
			board.set_col(i, test)
			board.show()
		for _i in range(0, board.get_height()):
			i = _i
			print 'The %d row' % i
			values = h[i]
			if (not balance) and count == 1 and sum(values)+len(values)-1 <= board.get_width():
				continue
			length = len(h[i])
			row = board.get_row(i)
			n = 0
			validValues = []
			test = [0] * board.get_width()
			for kk in ff(board.get_width(), values):
				if not_collosion_r(board, i, kk, values, w, h):
					n += 1
					validValues.append(kk)
					test = map(lambda x,y:x+y, test, kk)
			test = map(lambda x:1 if x==n and n>0 else 0, test)
			if is_new_step(row, test, values) and test.count(1) > row.count(1):
				unfinished = 2
			test = map(lambda x,y:x|y, test, row)
			board.set_row(i, test)
			board.show()
			
	print '==================================================='	
	board.show()

w = []
h = []
lines = sys.stdin.readlines()
p = w
for i in lines:
	if i.isspace():
		p = h
		continue
	p.append(map(int, i.split()))
solve(w, h)
