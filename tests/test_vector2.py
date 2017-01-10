import unittest

from godot.bindings import Vector2


class TestVector2(unittest.TestCase):

    def test_base(self):
        v = Vector2()
        self.assertEqual(type(v), Vector2)
        v2 = Vector2(1, -2)
        self.assertEqual(type(v), Vector2)
        self.assertEqual(v2, Vector2(1, -2))
        self.assertNotEqual(v, v2)

    def test_instanciate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_x, expected_y in (
                [(), 0, 0],
                [(0.5, 0.5), 0.5, 0.5],
                [(1, 2), 1, 2],
                [(1,), 1, 0]):
            v = Vector2(*args)
            self.assertEqual(v.x, expected_x, msg=msg_tmpl % (v.x, expected_x, args))
            self.assertEqual(v.y, expected_y, msg=msg_tmpl % (v.y, expected_y, args))
            self.assertEqual(v.width, expected_x, msg=msg_tmpl % (v.width, expected_y, args))
            self.assertEqual(v.height, expected_y, msg=msg_tmpl % (v.height, expected_x, args))
        self.assertRaises(TypeError, Vector2, "a", 2)
        self.assertRaises(TypeError, Vector2, "a", 2)
        self.assertRaises(TypeError, Vector2, 1, "b")
        self.assertRaises(TypeError, Vector2, None, 2)

    def test_methods(self):
        v2 = Vector2()
        v = Vector2()
        # Don't test methods' validity but bindings one
        for field, ret_type, params in (
                ['abs', Vector2, ()],
                ['angle', float, ()],
                ['angle_to', float, (v2, )],
                ['angle_to_point', float, (v2, )],
                ['clamped', Vector2, (0.5, )],
                ['cubic_interpolate', Vector2, (v2, v2, v2, 0.5)],
                ['distance_squared_to', float, (v2, )],
                ['distance_to', float, (v2, )],
                ['dot', float, (v2, )],
                ['floor', Vector2, ()],
                ['get_aspect', float, ()],
                ['length', float, ()],
                ['length_squared', float, ()],
                ['linear_interpolate', Vector2, (v2, 0.5)],
                ['normalized', Vector2, ()],
                ['reflect', Vector2, (v2, )],
                ['rotated', Vector2, (0.5, )],
                ['slide', Vector2, (v2, )],
                ['snapped', Vector2, (v2, )],
                ['tangent', Vector2, ()]):
            self.assertTrue(hasattr(v, field), msg='Vector2 has no method `%s`' % field)
            method = getattr(v, field)
            self.assertTrue(callable(method))
            ret = method(*params)
            self.assertEqual(type(ret), ret_type, msg="`Vector2.%s` is expected to return `%s`" % (field, ret_type))

    def test_properties(self):
        v = Vector2()
        for field, ret_type in (
                ('height', float),
                ('width', float),
                ('x', float),
                ('y', float)):
            self.assertTrue(hasattr(v, field), msg='Vector2 has no property `%s`' % field)
            field_val = getattr(v, field)
            self.assertEqual(type(field_val), ret_type, msg="`Vector2.%s` is expected to be a `%s`" % (field, ret_type))


if __name__ == '__main__':
    unittest.main()
