from sim import SimException

import numpy
from decimal import Decimal

EPS = 10**-6

class GeometryException(SimException): pass

class Pair:
	lhs = '|'
	rhs = '|'

	def __init__(self, v0, v1):
		self.a = numpy.array([v0, v1])

	@classmethod
	def from_array(cls, array):
		if len(array) != 2:
			raise GeometryException("Can only be created from a 2d array")
		return cls(array[0], array[1])

	def __iter__(self):
		for i in (0, 1):
			yield self.a[i]

	def __repr__(self):
		return "{}{},{}{}".format(self.lhs, round(self.a[0], 6), round(self.a[1], 6), self.rhs)

	def __hash__(self):
		return self.__repr__().__hash__()

	def __eq__(self, other):
		return self.a[0] == other.a[0] and self.a[1] == other.a[1]

	def __add__(self, other):
		if isinstance(other, Pair):
			return self.from_array(self.a + other.a)
		else:
			return self.from_array(self.a + other)

	def __sub__(self, other):
		return self + -other

	def __mul__(self, other):
		if isinstance(other, Pair):
			return self.from_array(self.a * other.a)
		else:
			return self.from_array(self.a * other)

	def __truediv__(self, other):
		if isinstance(other, Pair):
			return self.from_array(self.a / other.a)
		else:
			return self.from_array(self.a / other)

	def __neg__(self):
		return self.from_array(-self.a)

class Point(Pair):
	lhs = '('
	rhs = ')'

	def __sub__(self, other):
		return Vector.from_array(super().__sub__(other).a)

	@property
	def x(self):
		return self.a[0]

	@property
	def y(self):
		return self.a[1]

	def near(self, other):
		return (self - other).M < EPS

class Vector(Pair):
	lhs = '<'
	rhs = '>'

	@property
	def i(self):
		return self.a[0]

	@property
	def j(self):
		return self.a[0]

	@property
	def M(self):
		"""
		Calculates the magnitude of the vector
		"""
		return numpy.linalg.norm(self.a)

	@property
	def u(self):
		"""
		Calculates the unit vector for this vector
		"""
		return self / self.M

class Size(Pair):
	lhs = '/'
	rhs = '/'

	@property
	def w(self):
		return self.a[0]

	@property
	def h(self):
		return self.a[1]

	@property
	def diag(self):
		return numpy.linalg.norm(self.a)

class Rectangle:

	def __init__(self, p, sz):
		self._p = p
		self._sz = sz

	def __repr__(self):
		return "[{} {}]".format(self.p, self.sz)

	def __contains__(self, pt):
		x_in_range = pt.x >= self.x and pt.x < self.x + self.w
		y_in_range = pt.y >= self.y and pt.y < self.y + self.h
		return x_in_range and y_in_range

	@property
	def p(self):
		return self._p

	@property
	def sz(self):
		return self._sz

	@property
	def x(self):
		return self.p.x

	@property
	def y(self):
		return self.p.y

	@property
	def w(self):
		return self.sz.w

	@property
	def h(self):
		return self.sz.h

