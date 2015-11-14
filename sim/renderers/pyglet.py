import os
import pyglet
from pyglet.gl import *

from sim.geometry import *
from sim.models import tile
from sim.models.tile_map import TileMap

from sim.models.action import *
from sim.models.terrain import *
from sim.models.resource import *
from sim.models.terrain_improvement import *
from sim.models.unit.peasant import Peasant
from sim.models.unit.ship import Ship

from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.building.fishing_hole import FishingHole
from sim.models.building.lumber_mill import LumberMill
from sim.models.building.iron_mine import IronMine
from sim.models.building.dock import Dock

class Camera:

	def __init__(self, tile_map):
		self.tile_map = tile_map
		self.view_rect = Rectangle(Point(0,0), tile_map.sz)
		self.minimum_tile_line_in_view = 10

	def convert_world_vector_to_view_vector(self, v):
		return (v / self.tile_map.sz) * self.view_rect.sz

	def convert_world_point_to_view_point(self, p):
		return (p / self.tile_map.sz) * self.view_rect.sz + self.view_rect.p

	def pan(self, v):
		scaled_v = self.convert_world_vector_to_view_vector(v)
		new_center = self.view_rect.clamp_point(self.view_rect.center + scaled_v)
		clamped_v = new_center - self.view_rect.center
		self.view_rect = Rectangle(self.view_rect.p + clamped_v, self.view_rect.sz)

	def zoom(self, z):
		min_sz = self.tile_map.tile_sz * self.minimum_tile_line_in_view
		min_z = max(*(min_sz / self.view_rect.sz))
		max_sz = self.tile_map.sz
		max_z = min(*(max_sz / self.view_rect.sz))
		clamped_z = max(min(z, max_z), min_z)
		self.view_rect = self.view_rect * clamped_z

	@property
	def ortho_matrix(self):
		return (self.view_rect.left, self.view_rect.right, self.view_rect.bottom, self.view_rect.top)

class HUD:

	def __init__(self, tile_map, window):
		self.tile_map = tile_map
		self.window = window
		self.status_box_rect = self.tile_map.bounds_rect.scale_y(0.20, center=False).scale_x(0.66)

	def should_draw(self):
		return self.tile_map.selected_unit is not None

	def get_status_text(self):
		u = self.tile_map.selected_unit
		return "{}".format(u.status)

class PygletEventHandler:

	def __init__(self, tile_map, camera):
		self.tile_map = tile_map
		self.camera = camera

	def on_mouse_press(self, x, y, button, modifiers):
		pt = self.camera.convert_world_point_to_view_point(Point(x, y))
		if button == pyglet.window.mouse.LEFT:
			unit = self.tile_map.get_unit_at_position(pt)
			if unit is None:
				self.tile_map.clear_unit_selection()
			else:
				self.tile_map.select_unit(unit)
		if button == pyglet.window.mouse.RIGHT:
			unit = self.tile_map.selected_unit
			if unit is not None:
				unit.clear_actions()
				unit.add_action(MoveToward(pt))

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.F:
			unit = self.tile_map.selected_unit
			if unit is not None:
				unit.clear_actions()
				unit.add_action(ConstructBuilding(CabbageFarm))

		if symbol == pyglet.window.key.C:
			unit = self.tile_map.selected_unit
			if unit is not None:
				unit.clear_actions()
				unit.add_action(Harvest(Wood))

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			self.camera.pan(Vector(-dx, -dy))

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if scroll_y != 0:
			self.camera.zoom(1.0 + (0.05 * -scroll_y))

=======
>>>>>>> interim-commit
class PygletRenderer:

	def __init__(self, tile_map, update_interval):
		self.tile_map = tile_map
		self.update_interval = update_interval
		self.window = pyglet.window.Window(int(self.tile_map.w), int(self.tile_map.h))
		self.image_registry = {}
		self.sprite_registry = {}
		pyglet.clock.schedule_interval(self.update, self.update_interval)
<<<<<<< afd9318a37e0c370f762c24943b43fe2b485355a
		self.clock = 0
		self.camera = Camera(tile_map)
		self.window.push_handlers(PygletEventHandler(self.tile_map, self.camera))
		self.hud = HUD(self.tile_map, self.window)



=======
		self.window.push_handlers(PygletEventHandler(tile_map))
>>>>>>> interim-commit

	def scale_sprite_to_tile_size(self, sprite):
		sprite.scale = min(
			self.tile_map.tile_sz.w / sprite.width,
			self.tile_map.tile_sz.w / sprite.height,
			)

	def run(self):
		pyglet.app.run()

	def update(self, dt):
		self.window.clear()
		self.clock += dt

		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()
		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()

		gluOrtho2D(*self.camera.ortho_matrix)

		self.update_terrain()
		self.update_terrain_improvements()
		self.update_buildings()
		self.update_units(dt)

		if not self.hud.should_draw():
			return

		glLoadIdentity()
		gluOrtho2D(0, self.window.width, 0, self.window.height)
		r = self.hud.status_box_rect

		pyglet.graphics.draw(
			4,
			pyglet.gl.GL_QUADS,
			('v2f', Pair.chain(r.ll, r.lr, r.ur, r.ul)),
			('c3f', (0.5,0.5,0.5)*4),
			)

		status_doc = pyglet.text.document.FormattedDocument()
		status_doc.text = self.hud.get_status_text()
		status_doc.set_style(0, -1, {'color': (255, 255, 255, 255)})
		layout = pyglet.text.layout.TextLayout(status_doc, r.w, r.h)
		layout.x = r.x
		layout.y = r.y
		layout.multiline = True
		layout.draw()

	def update_terrain(self):
		for pt in self.tile_map.tile_grid.get_grid_points_in_rect():
			terrain_id = "terrain{}".format(pt)
			if terrain_id not in self.sprite_registry:
				terrain = self.tile_map.tile_grid.get_tile(pt).terrain
				image = self.get_terrain_image(terrain)
				if image is None:
					continue
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[terrain_id] = sprite
			sprite = self.sprite_registry[terrain_id]
			(sprite.x, sprite.y) = self.tile_map.grid_coords_to_map_coords(pt)
			sprite.draw()

	def update_terrain_improvements(self):
		for pt in self.tile_map.tile_grid.get_grid_points_in_rect():
			terrain_improvement_id = "terrain_improvement{}".format(pt)
			if terrain_improvement_id not in self.sprite_registry:
				terrain_improvement = self.tile_map.tile_grid.get_tile(pt).terrain_improvement
				image = self.get_terrain_improvement_image(terrain_improvement)
				if image is None:
					continue
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[terrain_improvement_id] = sprite
			sprite = self.sprite_registry[terrain_improvement_id]
			(sprite.x, sprite.y) = self.tile_map.grid_coords_to_map_coords(pt)
			sprite.draw()

	def update_buildings(self):
		for building in self.tile_map.get_buildings():
			if building.building_id not in self.sprite_registry:
				image = self.get_building_image(building)
				if image is None:
					continue
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[building.building_id] = sprite
			sprite = self.sprite_registry[building.building_id]
			pt = self.tile_map.get_building_position(building)
			pt = pt - self.tile_map.tile_sz * 0.5
			(sprite.x, sprite.y) = pt
			sprite.draw()

	def update_units(self, dt):
		for unit in self.tile_map.get_units():
			unit.act(dt)
			if unit.unit_id not in self.sprite_registry:
				image = self.get_unit_image(unit)
				if image is None:
					continue
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[unit.unit_id] = sprite
			sprite = self.sprite_registry[unit.unit_id]
			pt = self.tile_map.get_unit_position(unit)
			pt = pt - self.tile_map.tile_sz * 0.5
			(sprite.x, sprite.y) = pt
			sprite.draw()
		if self.tile_map.selected_unit is not None:
			unit_selection_key = 'unit-selection'
			if unit_selection_key not in self.sprite_registry:
				image = self.load_image('selection.png', 'unit-selection-image')
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[unit_selection_key] = sprite
			sprite = self.sprite_registry[unit_selection_key]
			pt = self.tile_map.selected_unit.pt
			pt = pt - self.tile_map.tile_sz * 0.5
			(sprite.x, sprite.y) = pt
			sprite.draw()

	def get_terrain_image(self, terrain):
		if terrain is Forest:
			return self.load_image('forest.png', 'forest-terrain-image')
		elif terrain is Water:
			return self.load_image('water.png', 'water-terrain-image')
		elif terrain is Grass:
			return self.load_image('grass.png', 'grass-terrain-image')
		else:
			return self.load_image('plains.png', 'plains-terrain-image')

	def get_terrain_improvement_image(self, terrain_improvement):
		if terrain_improvement is Road:
			return self.load_image('road.jpg', 'road-improvement-image')
		elif terrain_improvement is IronOreDeposit:
			return self.load_image('iron_ore.png', 'iron-ore-improvement-image')
		else:
			return None

	def get_building_image(self, building):
		if isinstance(building, CabbageFarm):
			return self.load_image('cabbage.png', 'cabbage-building-image')
		elif isinstance(building, Dock):
			return self.load_image('dock.jpg', 'dock-building-image')
		elif isinstance(building, FishingHole):
			return self.load_image('fish.png', 'fish-building-image')
		elif isinstance(building, LumberMill):
			return self.load_image('lumbermill.png', 'lumber-building-image')
		elif isinstance(building, IronMine):
			return self.load_image('mine.jpg', 'iron-mine-building-image')
		else:
			return None

	def get_unit_image(self, unit):
		if isinstance(unit, Peasant):
			return self.load_image('peasant.png', 'peasant-unit-image')
		elif isinstance(unit, Ship):
			return self.load_image('ship.jpg', 'ship-unit-image')
		else:
			return None

	def load_image(self, path, key):
		if key not in self.image_registry:
			image = pyglet.image.load(os.path.join(os.getcwd(), 'images', path))
			self.image_registry[key] = image
		return self.image_registry[key]

