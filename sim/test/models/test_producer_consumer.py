import unittest
from sim.models.resource import Fish, Wood, Cabbage
from sim.models.cargo_container import *
from sim.models.producer_consumer import *

class DummyProducerConsumer(ProducerConsumer):

    def digest(self):
        pass



class ProducerConsumerModelTest(unittest.TestCase):

    def test_add_resource_requirement_creates_a_new_requirement_for_a_specified_resource(self):
        dummy = DummyProducerConsumer()
        dummy.add_resource_requirement(Fish, 10)
        self.assertIn(Fish.name, dummy.resource_requirements.keys())
        self.assertEqual(dummy.resource_requirements[Fish.name]['load'], 10)
        self.assertIs(dummy.resource_requirements[Fish.name]['type'], Fish)

    def test_add_resource_requirement_raises_error_if_there_is_already_a_requirement_for_that_resource_type(self):
        dummy = DummyProducerConsumer()
        dummy.add_resource_requirement(Fish, 10)
        with self.assertRaises(ProducerConsumerException) as error_context:
            dummy.add_resource_requirement(Fish, 12)
        self.assertEqual(
            "A resource requirement of that type has already been added",
            error_context.exception.message
            )

    def test_can_consume_returns_true_if_the_supplied_container_holds_all_the_needed_requirements(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        dummy = DummyProducerConsumer()
        dummy.add_resource_requirement(Fish, 2)
        dummy.add_resource_requirement(Wood, 5)
        self.assertTrue(dummy.can_consume(tray))

    def test_can_consume_returns_false_if_the_supplied_container_lacks_all_the_needed_requirements(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        dummy1 = DummyProducerConsumer()
        dummy1.add_resource_requirement(Fish, 4)
        dummy1.add_resource_requirement(Wood, 5)
        self.assertFalse(dummy1.can_consume(tray))

        dummy2 = DummyProducerConsumer()
        dummy2.add_resource_requirement(Fish, 2)
        dummy2.add_resource_requirement(Wood, 5)
        dummy2.add_resource_requirement(Cabbage, 1)
        self.assertFalse(dummy2.can_consume(tray))

class ResourcePlantModelTest(unittest.TestCase):

    def test_add_resource_product_creates_a_new_product_for_a_specified_resource(self):
        plant = ResourcePlant()
        plant.add_resource_product(Fish, 10)
        self.assertIn(Fish.name, plant.resource_products.keys())
        self.assertEqual(plant.resource_products[Fish.name]['load'], 10)
        self.assertIs(plant.resource_products[Fish.name]['type'], Fish)

    def test_add_resource_product_raises_error_if_there_is_already_a_product_for_that_resource_type(self):
        plant = ResourcePlant()
        plant.add_resource_product(Fish, 10)
        with self.assertRaises(ProducerConsumerException) as error_context:
            plant.add_resource_product(Fish, 12)
        self.assertEqual(
            "A resource product of that type has already been added",
            error_context.exception.message
            )

    def test_can_produce_returns_true_if_the_supplied_container_has_the_necessary_capacity_for_the_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)
        plant = ResourcePlant()
        plant.add_resource_product(Fish, 2)
        plant.add_resource_product(Wood, 5)
        self.assertTrue(plant.can_produce(tray))

    def test_can_produce_returns_false_if_the_supplied_container_lacks_the_necessary_capacity_for_the_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        plant1 = ResourcePlant()
        plant1.add_resource_product(Fish, 2)
        plant1.add_resource_product(Wood, 6)
        self.assertFalse(plant1.can_produce(tray))

        plant2 = ResourcePlant()
        plant2.add_resource_product(Fish, 2)
        plant2.add_resource_product(Wood, 5)
        plant2.add_resource_product(Cabbage, 1)
        self.assertFalse(plant2.can_produce(tray))

    def test_digest_consumes_required_resources_and_produces_resource_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish,    10)
        tray.add_resource_slot(Wood,    10)
        tray.add_resource_slot(Cabbage, 10)
        tray.load_cargo(Fish,    3)
        tray.load_cargo(Wood,    5)
        tray.load_cargo(Cabbage, 4)

        plant = ResourcePlant()
        plant.add_resource_requirement(Fish, 3)
        plant.add_resource_requirement(Wood, 2)
        plant.add_resource_product(Cabbage, 6)
        plant.digest(tray)

        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    0)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    3)
        self.assertEqual(tray.cargo_slots[Cabbage.name]['load'], 10)

    def test_digest_does_nothing_if_the_cargo_container_cannot_unload_requirements_or_load_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish,    10)
        tray.add_resource_slot(Wood,    10)
        tray.add_resource_slot(Cabbage, 10)
        tray.load_cargo(Fish,    3)
        tray.load_cargo(Wood,    5)
        tray.load_cargo(Cabbage, 4)

        plant1 = ResourcePlant()
        plant1.add_resource_requirement(Fish, 4)
        plant1.add_resource_requirement(Wood, 2)
        plant1.add_resource_product(Cabbage, 6)
        plant1.digest(tray)
        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    3)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    5)
        self.assertEqual(tray.cargo_slots[Cabbage.name]['load'], 4)

        plant2 = ResourcePlant()
        plant2.add_resource_requirement(Fish, 3)
        plant2.add_resource_requirement(Wood, 2)
        plant2.add_resource_product(Cabbage, 7)
        plant2.digest(tray)
        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    3)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    5)
        self.assertEqual(tray.cargo_slots[Cabbage.name]['load'], 4)

class FactoryModelTest(unittest.TestCase):

    def test_set_product_sets_the_product_that_a_factory_will_produce(self):
        factory = Factory()
        factory.set_product(Fish)
        self.assertIs(factory.product, Fish)

    def test_set_product_raises_an_exception_if_the_product_has_already_been_set(self):
        factory = Factory()
        factory.set_product(Fish)
        with self.assertRaises(ProducerConsumerException) as error_context:
            factory.set_product(Fish)
        self.assertEqual(error_context.exception.message, "The product for this factory has already been set")

    def test_digest_consumes_required_resources_and_produces_a_new_instance_of_the_product_of_the_factory(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish,    10)
        tray.add_resource_slot(Wood,    10)
        tray.add_resource_slot(Cabbage, 10)
        tray.load_cargo(Fish,    3)
        tray.load_cargo(Wood,    5)
        tray.load_cargo(Cabbage, 4)

        factory = Factory()
        factory.add_resource_requirement(Fish, 3)
        factory.add_resource_requirement(Wood, 2)
        factory.set_product(Cabbage)
        result = factory.digest(tray)

        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    0)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    3)
        self.assertIsInstance(result, Cabbage)

