from sim import SimException

import numpy

EPS = 10**-6


class GeometryException(SimException):
	pass


class Pair:
	lhs = '|'
	rhs = '|'

	def __init__(self, v0, v1):
		self.a = numpy.array([v0, v1]).astype(float)

	@classmethod
	def from_array(cls, array):
		if len(array) != 2:
			raise GeometryException("Can only be created from a 2d array")
		return cls(array[0], array[1])

	def __iter__(self):
		for i in (0, 1):
			yield self.a[i]

	def __repr__(self):
		return "{}{:.2f},{:.2f}{}".format(
			self.lhs,
			self.a[0],
			self.a[1],
			self.rhs
			)

	def __hash__(self):
		return self.__repr__().__hash__()

	def __eq__(self, other):
		return (
			abs(self.a[0] - other.a[0]) < EPS and
			abs(self.a[1] - other.a[1]) < EPS
			)

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

	def __tuple__(self):
		return (self.a[0], self.a[1])

	@staticmethod
	def chain(*args):
		chain = ()
		for pair in args:
			chain = chain + tuple(pair)
		return chain


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
		return self.a[1]

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
		# TODO: This should probably be adjusted to account for
		#       epsilon rounding erros
		x_in_range = pt.x >= self.x and pt.x < self.x + self.w
		y_in_range = pt.y >= self.y and pt.y < self.y + self.h
		return x_in_range and y_in_range

	def __eq__(self, other):
		return self.p == other.p and self.sz == other.sz

	def scale_x(self, scale_factor, center=True):
		new_w = self.w * scale_factor
		x_off = 0
		if center is True:
			x_off = (self.w - new_w)/2
		return Rectangle(self.p + Vector(x_off, 0), Size(new_w, self.h))

	def scale_y(self, scale_factor, center=True):
		new_h = self.h * scale_factor
		y_off = 0
		if center is True:
			y_off = (self.h - new_h)/2
		return Rectangle(self.p + Vector(0, y_off), Size(self.w, new_h))

	def scale(self, scale_factor, center=True):
		return self.scale_x(scale_factor, center).scale_y(scale_factor, center)

	def translate_x(self, dx):
		return self.translate(Vector(dx, 0.0))

	def translate_y(self, dy):
		return self.translate(Vector(0.0, dy))

	def translate(self, move_v):
		# TODO: test me
		return Rectangle(self.p + move_v, self.sz)

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

	@property
	def left(self):
		return self.x

	@property
	def right(self):
		return self.x + self.w

	@property
	def bottom(self):
		return self.y

	@property
	def ll(self):
		return self.p

	@property
	def lr(self):
		return self.p + Vector(self.w, 0)

	@property
	def ur(self):
		return self.p + self.sz

	@property
	def ul(self):
		return self.p + Vector(0, self.h)

	@property
	def top(self):
		return self.y + self.h

	def __mul__(self, scale_factor):
		return self.scale(scale_factor)

	@property
	def center(self):
		return Point(self.x + self.w / 2, self.y + self.h / 2)

	def clamp_point(self, pt):
		return Point(
			min(max(pt.x, self.x), self.right),
			min(max(pt.y, self.y), self.top),
			)
