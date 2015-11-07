from sim.models.cargo_container import MixedCargoContainer

from uuid import uuid4
from textwrap import indent

class UnitException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Unit:
    movement_speed = 0
    display_char = ''
    name = ''
    strength = 0

    def __init__(self):
        self.container = MixedCargoContainer()
        self.container.set_weight_capacity(self.strength)
        self.moves_remaining = self.movement_speed
        self.tile_map = None
        self.building_factories = {}
        self.unit_id = uuid4()
        self.action_queue = []

    def __repr__(self):
        return '\n'.join([
            'unit_id:         {}'.format(self.unit_id),
            'movement_speed:  {}'.format(self.movement_speed),
            'moves_remaining: {}'.format(self.moves_remaining),
            #'current_path: {}'.format(', '.join(['({},{})'.format(x,y) for (x,y) in self.path ])),
            'container:\n{}'.format(indent(str(self.container), '  '))
            ])

    def set_tile_map(self, tile_map):
        # TODO: Maybe error check?
        self.tile_map = tile_map

    def act(self):
        if len(self.action_queue) == 0 or self.moves_remaining <= 0:
            return
        #print("Acting: {}".format(self.unit_id))
        self.action_queue.pop(0)()

    def add_building_factory(self, building_factory):
        if building_factory.product.name in self.building_factories:
            raise UnitException("A factory for that building has already been added")
        self.building_factories[building_factory.product.name] = building_factory

    def receive_cargo(self, resource_type, quantity):
        return self.container.load_cargo(resource_type, quantity)

    def deliver_cargo(self, resource_type, quantity):
        return self.container.unload_cargo(resource_type, quantity)

    def can_construct_building(self, building):
        if not building.name in self.building_factories:
            return False
        if not self.building_factories[building.name].can_consume(self.container):
            return False
        return True

    def construct_building(self, building):
        if building.name not in self.building_factories:
            raise UnitException("This unit cannot build that building")
        return self.building_factories[building.name].digest(self.container)

    #def find_shortest_path(tile_map, start, end, path=[]):
    #	path = path + [start]
    #	if start == end:
    #		return path
    #	if not graph.has_key(start):
    #		return None
    #	shortest = None
    #	for node in graph[start]:
    #		if node not in path:
    #			newpath = find_shortest_path(graph, node, end, path)
    #			if newpath:
    #				if not shortest or len(newpath) < len(shortest):
    #					shortest = newpath
    #	return shortest

    def add_path(self, final_x, final_y):
        if self.tile_map is None:
            raise UnitException("This unit has not been placed on the tile map yet!")
        #eventually this will calculate the lowest-cost path by something like Dijkstra's algorithm (above)
        #but for now it just goes in a straight line, starting with diagonal movement
        (current_x, current_y) = self.tile_map.get_unit_position(self)

        # TODO: rewrite this with a zipped range or something
        while current_x < final_x and current_y < final_y:
            self.add_action(self.move_unit_one, (1, 1))
            current_x += 1
            current_y += 1
        while current_x > final_x and current_y < final_y:
            self.add_action(self.move_unit_one, (-1, 1))
            current_x -= 1
            current_y += 1
        while current_x < final_x and current_y > final_y:
            self.add_action(self.move_unit_one, (1, -1))
            current_x += 1
            current_y -= 1
        while current_x > final_x and current_y > final_y:
            self.add_action(self.move_unit_one, (-1, -1))
            current_x -= 1
            current_y -= 1
        while current_x < final_x:
            self.add_action(self.move_unit_one, (1, 0))
            current_x += 1
        while current_y < final_y:
            self.add_action(self.move_unit_one, (0, 1))
            current_y += 1
        while current_x > final_x:
            self.add_action(self.move_unit_one, (-1, 0))
            current_x -= 1
        while current_y > final_y:
            self.add_action(self.move_unit_one, (0, -1))
            current_y -= 1

        assert (current_x == final_x)
        assert (current_y == final_y)

    def add_action(self, method, *args, **kwds):
        self.action_queue.append(lambda: method(*args, **kwds))

    def add_immediate_action(self, method, *args, **kwds):
        self.action_queue.insert(0, lambda: method(*args, **kwds))

    def clear_actions(self):
        self.action_queue = []

    def move_unit_one(self, move):
        x_move = move[0]
        y_move = move[1]
        if abs(x_move) > 1 or abs(y_move) > 1:
            raise UnitException("Must move 1 at a time in x and or y")

        # TODO: move this logic to tile_map
        (x, y) = self.tile_map.get_unit_position(self)
        new_x = x + x_move
        new_y = y + y_move
        if not self.tile_map.in_bounds(new_x, new_y):
            return

        raw_move_cost = self.tile_map.get_terrain(new_x, new_y).move_cost
        move_cost = raw_move_cost/(self.tile_map.get_terrain_improvement(new_x, new_y).movement_reduction)
        if self.moves_remaining - move_cost >= 0:
            self.tile_map.move_unit(self, x_move, y_move)
            self.moves_remaining -= move_cost

    def reset_moves_remaining(self):
        self.moves_remaining = self.movement_speed

