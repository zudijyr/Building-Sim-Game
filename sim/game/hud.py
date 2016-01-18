import os
import json

import pyglet
from pyglet.gl import glLoadIdentity, gluOrtho2D

from pyglet_gui.document import Document
from pyglet_gui.buttons import GroupButton
from pyglet_gui.containers import HorizontalContainer, VerticalContainer
from pyglet_gui.theme import Theme
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Label, Frame

from sim import SimException

from sim.models.actions.harvest import Harvest
from sim.models.actions.construct import Construct


class HUDException(SimException):
	pass


class HUD:

	def __init__(self, window):
		with open('etc/gui/theme.json') as theme_file:
			theme_dict = json.loads(theme_file.read())
		self.theme = Theme(
			theme_dict,
			resources_path=os.path.join(os.getcwd(), 'etc/gui/images')
			)
		self.window = window
		self.clear_action_gui()
		self.clear_status_gui()

	def handle_click(self, button_state, action):
		if button_state is not False:
			self.selected_action = action
		return True

	def clear_action_gui(self):
		self.selected_action = None
		self.action_gui_batch = None
		self.action_gui_manager = None

	def clear_status_gui(self):
		self.status_box = None
		self.status_gui_batch = None
		self.status_gui_manager = None

	def build_action_gui(self, unit):
		if unit is None:
			raise HUDException("Can't build action gui with a unit of None")

		harvest_content = [Label(text='Harvest')]
		for resource in unit.harvestable_resources:
			harvest_button = GroupButton(
				group_id='action-gui-buttons',
				label=resource.name,
				on_press=lambda x: self.handle_click(x, Harvest(resource, unit.container.remaining_capacity(resource))),
				)
			harvest_content.append(harvest_button)
		harvest_container = HorizontalContainer(harvest_content)

		building_content = [Label(text='Construct')]
		for building_factory in unit.building_factories.values():
			building_button = GroupButton(
				group_id='action-gui-buttons',
				label=building_factory.product.name,
				on_press=lambda x:
					self.handle_click(x, Construct(building_factory.product)),
				)
			building_content.append(building_button)
		construct_container = HorizontalContainer(building_content)

		action_container = VerticalContainer([
			harvest_container,
			construct_container,
			])
		self.action_gui_batch = pyglet.graphics.Batch()
		self.action_gui_manager = Manager(
			action_container,
			window=self.window,
			theme=self.theme,
			batch=self.action_gui_batch,
			)
		self.action_gui_manager.set_position(
			10,
			self.window.height - action_container.height - 10,
			)
		self.action_gui_manager.is_movable = False

	def build_status_gui(self):
		self.status_box = Document(
			pyglet.text.document.UnformattedDocument(),
			width=self.window.width*0.9,
			height=self.window.height/4,
			is_fixed_size=True,
			)
		status_frame = Frame(self.status_box)
		self.status_gui_batch = pyglet.graphics.Batch()
		self.status_gui_manager = Manager(
			status_frame,
			window=self.window,
			theme=self.theme,
			batch=self.status_gui_batch,
			)
		self.status_gui_manager.set_position(
			(self.window.width - status_frame.width)/2,
			10,
			)
		self.status_gui_manager.is_movable = False

	def draw(self, selected_unit):
		glLoadIdentity()
		gluOrtho2D(0, self.window.width, 0, self.window.height)
		if selected_unit is not None:
			if self.action_gui_batch is None:
				self.build_action_gui(selected_unit)
			self.action_gui_batch.draw()
			if self.status_gui_batch is None:
				self.build_status_gui()
			self.status_box.set_text(selected_unit.status)
			self.status_gui_batch.draw()
