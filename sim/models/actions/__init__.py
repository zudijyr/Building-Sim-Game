from sim import SimException


class ActionException(SimException):
	pass


class Action:

	def __init__(self, *args, **kwds):
		self.elapsed_time = 0.0
		self.setup(*args, **kwds)

	def __repr__(self):
		return 'base_action'

	def setup(self, *args, **kwds):
		pass

	def is_possible(self, unit, dt):
		return True

	def execute(self, unit, dt):
		self._execute(unit, dt)
		self.elapsed_time += dt

	def _execute(self, unit, dt):
		pass

	def is_complete(self, unit, dt):
		return True

	def finish(self, unit, dt):
		pass

	def next_action(self, unit, dt):
		return self
