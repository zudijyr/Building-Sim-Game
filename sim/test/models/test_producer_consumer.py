import unittest
from sim.models.resource import Fish, Wood, Cabbage
from sim.models.cargo_container import *
from sim.models.producer_consumer import ProducerConsumer, ProducerConsumerException

class ProducerConsumerModelTest(unittest.TestCase):

    def test_add_resource_requirement_creates_a_new_requirement_for_a_specified_resource(self):
        prodcon = ProducerConsumer()
        prodcon.add_resource_requirement(Fish, 10)
        self.assertIn(Fish.name, prodcon.resource_requirements.keys())
        self.assertEqual(prodcon.resource_requirements[Fish.name]['load'], 10)
        self.assertIs(prodcon.resource_requirements[Fish.name]['type'], Fish)

    def test_add_resource_requirement_raises_error_if_there_is_already_a_requirement_for_that_resource_type(self):
        prodcon = ProducerConsumer()
        prodcon.add_resource_requirement(Fish, 10)
        with self.assertRaises(ProducerConsumerException) as error_context:
            prodcon.add_resource_requirement(Fish, 12)
        self.assertEqual(
            "A resource requirement of that type has already been added",
            error_context.exception.message
            )

    def test_add_resource_product_creates_a_new_product_for_a_specified_resource(self):
        prodcon = ProducerConsumer()
        prodcon.add_resource_product(Fish, 10)
        self.assertIn(Fish.name, prodcon.resource_products.keys())
        self.assertEqual(prodcon.resource_products[Fish.name]['load'], 10)
        self.assertIs(prodcon.resource_products[Fish.name]['type'], Fish)

    def test_add_resource_product_raises_error_if_there_is_already_a_product_for_that_resource_type(self):
        prodcon = ProducerConsumer()
        prodcon.add_resource_product(Fish, 10)
        with self.assertRaises(ProducerConsumerException) as error_context:
            prodcon.add_resource_product(Fish, 12)
        self.assertEqual(
            "A resource product of that type has already been added",
            error_context.exception.message
            )

    def test_can_consume_returns_true_if_the_supplied_container_holds_all_the_needed_requirements(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        prodcon = ProducerConsumer()
        prodcon.add_resource_requirement(Fish, 2)
        prodcon.add_resource_requirement(Wood, 5)
        self.assertTrue(prodcon.can_consume(tray))

    def test_can_consume_returns_false_if_the_supplied_container_lacks_all_the_needed_requirements(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        prodcon1 = ProducerConsumer()
        prodcon1.add_resource_requirement(Fish, 4)
        prodcon1.add_resource_requirement(Wood, 5)
        self.assertFalse(prodcon1.can_consume(tray))

        prodcon2 = ProducerConsumer()
        prodcon2.add_resource_requirement(Fish, 2)
        prodcon2.add_resource_requirement(Wood, 5)
        prodcon2.add_resource_requirement(Cabbage, 1)
        self.assertFalse(prodcon2.can_consume(tray))

    def test_can_produce_returns_true_if_the_supplied_container_has_the_necessary_capacity_for_the_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)
        prodcon = ProducerConsumer()
        prodcon.add_resource_product(Fish, 2)
        prodcon.add_resource_product(Wood, 5)
        self.assertTrue(prodcon.can_produce(tray))

    def test_can_produce_returns_false_if_the_supplied_container_lacks_the_necessary_capacity_for_the_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish, 10)
        tray.add_resource_slot(Wood, 10)
        tray.load_cargo(Fish, 3)
        tray.load_cargo(Wood, 5)

        prodcon1 = ProducerConsumer()
        prodcon1.add_resource_product(Fish, 2)
        prodcon1.add_resource_product(Wood, 6)
        self.assertFalse(prodcon1.can_produce(tray))

        prodcon2 = ProducerConsumer()
        prodcon2.add_resource_product(Fish, 2)
        prodcon2.add_resource_product(Wood, 5)
        prodcon2.add_resource_product(Cabbage, 1)
        self.assertFalse(prodcon2.can_produce(tray))

    def test_digest_consumes_required_resources_and_produces_resource_products(self):
        tray = SlottedCargoContainer()
        tray.add_resource_slot(Fish,    10)
        tray.add_resource_slot(Wood,    10)
        tray.add_resource_slot(Cabbage, 10)
        tray.load_cargo(Fish,    3)
        tray.load_cargo(Wood,    5)
        tray.load_cargo(Cabbage, 4)

        prodcon = ProducerConsumer()
        prodcon.add_resource_requirement(Fish, 3)
        prodcon.add_resource_requirement(Wood, 2)
        prodcon.add_resource_product(Cabbage, 6)
        prodcon.digest(tray)

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

        prodcon1 = ProducerConsumer()
        prodcon1.add_resource_requirement(Fish, 4)
        prodcon1.add_resource_requirement(Wood, 2)
        prodcon1.add_resource_product(Cabbage, 6)
        prodcon1.digest(tray)
        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    3)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    5)
        self.assertEqual(tray.cargo_slots[Cabbage.name]['load'], 4)

        prodcon2 = ProducerConsumer()
        prodcon2.add_resource_requirement(Fish, 3)
        prodcon2.add_resource_requirement(Wood, 2)
        prodcon2.add_resource_product(Cabbage, 7)
        prodcon2.digest(tray)
        self.assertEqual(tray.cargo_slots[Fish.name]['load'],    3)
        self.assertEqual(tray.cargo_slots[Wood.name]['load'],    5)
        self.assertEqual(tray.cargo_slots[Cabbage.name]['load'], 4)

