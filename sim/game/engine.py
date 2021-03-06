import os
import pyglet

from pyglet.gl import glMatrixMode, glLoadIdentity, gluOrtho2D
from pyglet.gl import GL_PROJECTION, GL_MODELVIEW

from sim.game.hud import HUD
from sim.game.camera import Camera
from sim.game.event_handler import EventHandler

from sim.models.terrain import Forest, Water, Grass
from sim.models.terrain_improvement import Road, IronOreDeposit
from sim.models.unit.peasant import Peasant
from sim.models.unit.ship import Ship
from sim.models.unit import Unit

from sim.models.building.cabbage_farm import CabbageFarm
from sim.models.building.fishing_hole import FishingHole
from sim.models.building.lumber_mill import LumberMill
from sim.models.building.iron_mine import IronMine
from sim.models.building.dock import Dock


class Engine:

	def __init__(self, tile_map, update_interval):
		self.tile_map = tile_map
		self.update_interval = update_interval
		self.window = pyglet.window.Window(
			int(self.tile_map.w),
			int(self.tile_map.h),
			)
		self.hud = HUD(self.window)
		self.image_registry = {}
		self.sprite_registry = {}
		pyglet.clock.schedule_interval(self.update, self.update_interval)
		self.clock = 0
		self.camera = Camera(tile_map)
		event_handler = EventHandler(self.tile_map, self.camera, self.hud)
		self.window.push_handlers(event_handler)

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

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		gluOrtho2D(*self.camera.ortho_matrix)

		self.update_terrain()
		self.update_terrain_improvements()
		self.update_buildings(dt)
		self.update_units(dt)

		self.hud.draw(self.tile_map.selected_unit)

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
				tile = self.tile_map.tile_grid.get_tile(pt)
				terrain_improvement = tile.terrain_improvement
				image = self.get_terrain_improvement_image(terrain_improvement)
				if image is None:
					continue
				sprite = pyglet.sprite.Sprite(image, x=0, y=0)
				self.scale_sprite_to_tile_size(sprite)
				self.sprite_registry[terrain_improvement_id] = sprite
			sprite = self.sprite_registry[terrain_improvement_id]
			(sprite.x, sprite.y) = self.tile_map.grid_coords_to_map_coords(pt)
			sprite.draw()

	def update_buildings(self, dt):
		for building in self.tile_map.get_buildings():
			building.act(dt)
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
			pt = unit.pt - self.tile_map.tile_sz * 0.5
			(sprite.x, sprite.y) = pt
			sprite.draw()
		if self.tile_map.selected_unit is not None:
			if isinstance(self.tile_map.selected_unit, Unit):
				unit_selection_key = 'unit-selection'
				if unit_selection_key not in self.sprite_registry:
					image = self.load_image(
						'selection.png',
						'unit-selection-image',
						)
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
			return self.load_image(
				'iron_ore.png',
				'iron-ore-improvement-image',
				)
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
			image_path = os.path.join(os.getcwd(), 'images', path)
			image = pyglet.image.load(image_path)
			self.image_registry[key] = image
		return self.image_registry[key]
