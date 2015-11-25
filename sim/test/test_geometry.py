import unittest
import numpy
from sim.geometry import *

class GeometryTest(unittest.TestCase):

	def test_pair_init_creates_a_instance_that_wraps_a_2d_numpy_array(self):
		p = Pair(2, 3)
		self.assertEqual(p.a[0], 2)
		self.assertEqual(p.a[1], 3)

	def test_pair_from_array_creates_an_instance_from_a_2d_numpy_array(self):
		p = Pair.from_array(numpy.array([2, 3]))
		self.assertIsInstance(p, Pair)
		self.assertEqual(p.a[0], 2)
		self.assertEqual(p.a[1], 3)

	def test_pair_from_array_raises_exception_if_argument_is_not_a_2d_array(self):
		with self.assertRaises(GeometryException) as error_context:
			p = Pair.from_array(numpy.array([2, 3, 5]))
		self.assertEqual(error_context.exception.message, "Can only be created from a 2d array")

	def test_pair_iter_allows_a_pair_to_be_iterable(self):
		p = Pair(2, 3)
		(v0, v1) = p
		self.assertEqual(v0, 2)
		self.assertEqual(v1, 3)

	def test_pair_hash_allows_a_pair_to_be_hashable(self):
		p = Pair(2, 3)
		d = { p: 'pair' }
		self.assertEqual(d[p], 'pair')

	def test_pair_repr_returns_a_string_representation_of_a_pair(self):
		p = Pair(2, 3)
		self.assertEqual("{}".format(p), '|2.00,3.00|')

	def test_pair_eq_returns_true_if_two_pairs_have_the_same_values_in_order(self):
		p1 = Pair(2, 3)
		p2 = Pair(2, 3)
		self.assertTrue(p1 == p2)

	def test_pair_add_returns_a_new_pair_that_is_the_sum_of_two_others(self):
		p1 = Pair(2, 3)
		p2 = Pair(7, 9)
		self.assertEqual(p1 + p2, Pair(9, 12))

	def test_pair_add_returns_a_translated_pair_that_is_the_sum_of_the_original_and_a_scalar(self):
		p1 = Pair(2, 3)
		self.assertEqual(p1 + 5, Pair(7, 8))

	def test_pair_sub_returns_a_new_pair_that_is_the_difference_of_two_others(self):
		p1 = Pair(2, 3)
		p2 = Pair(7, 9)
		self.assertEqual(p1 - p2, Pair(-5, -6))

	def test_pair_mul_returns_a_scaled_pair_that_is_the_product_of_the_original_and_a_scalar(self):
		p1 = Pair(2, 3)
		self.assertEqual(p1 * 5, Pair(10, 15))

	def test_pair_mul_returns_a_new_pair_that_is_the_product_of_two_others(self):
		p1 = Pair(2, 3)
		p2 = Pair(7, 9)
		self.assertEqual(p1 * p2, Pair(14, 27))

	def test_pair_truediv_returns_a_new_pair_that_is_the_quotient_of_two_others(self):
		p1 = Pair(2, 3)
		p2 = Pair(7, 9)
		self.assertEqual(p1 / p2, Pair(2/7, 3/9))

	def test_pair_neg_returns_a_new_pair_that_is_the_quotient_of_two_others(self):
		p1 = Pair(2, 3)
		self.assertEqual(-p1, Pair(-2, -3))

	def test_tuple_method_allows_a_pair_to_be_cast_as_a_tuple(self):
		p1 = Pair(2, 3)
		self.assertEqual(tuple(p1), (2, 3))

	def test_pair_chain_strings_pairs_together_into_a_single_tuple(self):
		p1 = Pair(2, 3)
		p2 = Pair(4, 5)
		p3 = Pair(6, 7)
		self.assertEqual(Pair.chain(p1, p2, p3), (2, 3, 4, 5, 6, 7))



	def test_point_sub_returns_a_vector_difference_between_the_two_points(self):
		p1 = Point(2, 3)
		p2 = Point(7, 9)
		p3 = p1 - p2
		self.assertEqual(p3, Vector(-5, -6))
		self.assertIsInstance(p3, Vector)

	def test_point_near_returns_true_if_a_point_is_near_to_another(self):
		p1 = Point(2, 3)
		p2 = Point(2.0000000001, 3.0000000001)
		self.assertTrue(p1.near(p2))



	def test_vector_M_returns_the_magnitude_of_a_vector(self):
		v = Vector(3, 4)
		self.assertEqual(5, v.M)

	def test_vector_u_returns_the_unit_vector_for_the_given_vector(self):
		v = Vector(3, 4)
		self.assertEqual(v.u, Vector(3/5, 4/5))

	def test_vector_i_and_j_property_return_elements_of_vector(self):
		v = Vector(3, 4)
		self.assertEqual(v.i, 3)
		self.assertEqual(v.j, 4)



	def test_size_w_and_h_properties_return_elements_of_size(self):
		sz = Size(3, 4)
		self.assertEqual(sz.w, 3)
		self.assertEqual(sz.h, 4)

	def test_size_diag_property_returns_the_diagonal_of_the_size(self):
		sz = Size(3, 4)
		self.assertEqual(sz.diag, 5)



	def test_rectangle_repr_returns_a_string_representation_of_the_rectangle(self):
		p = Point(2,3)
		sz = Size(3,4)
		self.assertTrue("{}".format(Rectangle(p, sz)), "[(2.00,3.00) /3.00,4.00/]")

	def test_rectangle_contains_returns_true_if_a_point_is_in_or_on_a_rectangles_boundary(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertTrue(Point(3, 4) in r)
		self.assertTrue(Point(2, 4) in r)
		self.assertTrue(Point(3, 3) in r)
		self.assertFalse(Point(5, 4) in r)
		self.assertFalse(Point(3, 7) in r)
		self.assertFalse(Point(1, 2) in r)

	def test_clamp_point_moves_a_point_outside_the_rectangle_to_the_nearest_border(self):
		r = Rectangle(Point(-2,-3), Size(5,7))
		self.assertEqual(r.clamp_point(Point(-5, 0)), Point(-2, 0))
		self.assertEqual(r.clamp_point(Point(0, -6)), Point(0, -3))
		self.assertEqual(r.clamp_point(Point(6, 0)), Point(3, 0))
		self.assertEqual(r.clamp_point(Point(0, 8)), Point(0, 4))
		self.assertEqual(r.clamp_point(Point(100, 100)), Point(3, 4))

	def test_scale_x_returns_a_rectangle_with_its_width_multiplied_by_a_scale_factor_centered_on_the_same_center_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale_x(3), Rectangle(Point(2-(9-3)/2, 3), Size(9, 4)))

	def test_scale_x_with_center_set_to_false_returns_a_rectangle_with_its_width_multiplied_by_a_scale_factor_anchored_to_the_same_point_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale_x(3, center=False), Rectangle(Point(2, 3), Size(9, 4)))

	def test_scale_y_returns_a_rectangle_with_its_height_multiplied_by_a_scale_factor_centered_on_the_same_center_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale_y(3), Rectangle(Point(2, 3-(12-4)/2), Size(3, 12)))

	def test_scale_y_with_center_set_to_false_returns_a_rectangle_with_its_height_multiplied_by_a_scale_factor_anchored_to_the_same_point_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale_y(3, center=False), Rectangle(Point(2, 3), Size(3, 12)))

	def test_scale_returns_a_rectangle_with_its_width_and_height_multiplied_by_a_scale_factor_centered_on_the_same_center_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale(3), Rectangle(Point(2-(9-3)/2, 3-(12-4)/2), Size(9, 12)))

	def test_scale_with_center_set_to_false_returns_a_rectangle_with_its_width_and_height_multiplied_by_a_scale_factor_anchored_to_the_same_point_as_the_source_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.scale(3, center=False), Rectangle(Point(2, 3), Size(9, 12)))

	def test_translate_x_returns_a_rectangle_that_has_been_translated_by_distance_in_x(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.translate_x(2), Rectangle(Point(4,3), Size(3,4)))

	def test_translate_y_returns_a_rectangle_that_has_been_translated_by_distance_in_y(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.translate_y(3), Rectangle(Point(2,6), Size(3,4)))

	def test_translate_returns_a_rectangle_that_has_been_translated_over_a_vector(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.translate(Vector(2, 3)), Rectangle(Point(4,6), Size(3,4)))

	def test_ll_lr_ur_ul_properties_return_the_corner_points_of_the_rectangle(self):
		r = Rectangle(Point(2,3), Size(3,4))
		self.assertEqual(r.ll, Point(2, 3))
		self.assertEqual(r.lr, Point(5, 3))
		self.assertEqual(r.ur, Point(5, 7))
		self.assertEqual(r.ul, Point(2, 7))


