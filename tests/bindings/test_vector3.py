import unittest

from godot.bindings import Vector3


class TestVector3(unittest.TestCase):

    def test_base(self):
        v = Vector3()
        self.assertEqual(type(v), Vector3)
        v2 = Vector3(1, -2, 5)
        self.assertEqual(type(v), Vector3)
        self.assertEqual(v2, Vector3(1, -2, 5))
        self.assertNotEqual(v, v2)

    def test_instanciate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_x, expected_y, expected_z in (
                [(), 0, 0, 0],
                [(0.5, 0.5, 0.5), 0.5, 0.5, 0.5],
                [(1,), 1, 0, 0],
                [(1, 1), 1, 1, 0],
                [(1, 2, 3), 1, 2, 3]):
            v = Vector3(*args)
            self.assertEqual(v.x, expected_x, msg=msg_tmpl % (v.x, expected_x, args))
            self.assertEqual(v.y, expected_y, msg=msg_tmpl % (v.y, expected_y, args))
            self.assertEqual(v.z, expected_z, msg=msg_tmpl % (v.z, expected_z, args))
        self.assertRaises(TypeError, Vector3, "a", 2, 3)
        self.assertRaises(TypeError, Vector3, "a", 2)
        self.assertRaises(TypeError, Vector3, 1, "b", 5)
        self.assertRaises(TypeError, Vector3, None, 2, "c")

    def test_methods(self):
        v = Vector3()
        # Don't test methods' validity but bindings one
        for field, ret_type, params in (
                ['abs', Vector3, ()],
                ['angle_to', float, (v, )],
                ['ceil', Vector3, ()],
                ['cross', Vector3, (v, )],
                ['cubic_interpolate', Vector3, (v, v, v, 0.5)],
                ['distance_squared_to', float, (v, )],
                ['distance_to', float, (v, )],
                ['dot', float, (v, )],
                ['floor', Vector3, ()],
                ['inverse', Vector3, ()],
                ['length', float, ()],
                ['length_squared', float, ()],
                ['linear_interpolate', Vector3, (v, 0.5)],
                ['max_axis', int, ()],
                ['min_axis', int, ()],
                ['normalized', Vector3, ()],
                ['reflect', Vector3, (v, )],
                ['rotated', Vector3, (v, 0.5)],
                ['slide', Vector3, (v, )],
                ['snapped', Vector3, (v, )]):
            self.assertTrue(hasattr(v, field), msg='`Vector3` has no method `%s`' % field)
            method = getattr(v, field)
            self.assertTrue(callable(method))
            ret = method(*params)
            self.assertEqual(type(ret), ret_type, msg="`Vector3.%s` is expected to return `%s`" % (field, ret_type))

    def test_properties(self):
        v = Vector3()
        for field, ret_type in (
                ('x', float),
                ('y', float),
                ('z', float)):
            self.assertTrue(hasattr(v, field), msg='`Vector3` has no property `%s`' % field)
            field_val = getattr(v, field)
            self.assertEqual(type(field_val), ret_type, msg="`Vector3.%s` is expected to be a `%s`" % (field, ret_type))
            for val in (0, 10, 10., 42.5):
                setattr(v, field, val)
                field_val = getattr(v, field)
                self.assertEqual(field_val, val, msg="`Vector3.%s` is expected to be equal to `%d`" % (field_val, val))

    def test_unary(self):
        v = Vector3(0, 1, 2)
        v2 = -v
        self.assertEqual(v2.x, 0)
        self.assertEqual(v2.y, -1)
        self.assertEqual(v2.z, -2)
        v3 = +v
        self.assertEqual(v3.x, 0)
        self.assertEqual(v3.y, 1)
        self.assertEqual(v3.z, 2)
        v = Vector3(0.0, 1.5, 2.5)
        v2 = -v
        self.assertEqual(v2.x, 0.0)
        self.assertEqual(v2.y, -1.5)
        self.assertEqual(v2.z, -2.5)
        v3 = +v
        self.assertEqual(v3.x, 0.0)
        self.assertEqual(v3.y, 1.5)
        self.assertEqual(v3.z, 2.5)


if __name__ == '__main__':
    unittest.main()
