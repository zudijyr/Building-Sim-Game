import pyglet

from sim.geometry import Point, Vector
from sim.models.actions.move_toward import MoveToward


class EventHandler:

	def __init__(self, tile_map, camera, hud):
		self.tile_map = tile_map
		self.camera = camera
		self.hud = hud

	def on_mouse_press(self, x, y, button, modifiers):
		pt = self.camera.convert_world_point_to_view_point(Point(x, y))
		if button == pyglet.window.mouse.LEFT:
			unit = self.tile_map.get_unit_at_position(pt)
			if unit is None:
				self.tile_map.clear_unit_selection()
				self.hud.clear_action_gui()
			else:
				self.tile_map.select_unit(unit)
				self.hud.build_action_gui(unit)
		if button == pyglet.window.mouse.RIGHT:
			unit = self.tile_map.selected_unit
			if unit is not None:
				unit.clear_actions()
				unit.add_action(MoveToward(pt))
				if self.hud.selected_action is not None:
					unit.add_action(self.hud.selected_action)

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			self.camera.pan(Vector(-dx, -dy))

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if scroll_y != 0:
			self.camera.zoom(1.0 + (0.05 * -scroll_y))
