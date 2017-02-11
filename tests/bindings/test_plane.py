import unittest

from godot.bindings import Plane, Vector3


class TestPlane(unittest.TestCase):

    def test_base(self):
        p = Plane()
        self.assertEqual(type(p), Plane)
        p2 = Plane(Vector3(), 4)
        self.assertEqual(type(p), Plane)
        p2 = Plane(Vector3(), Vector3(), Vector3())
        self.assertEqual(type(p), Plane)
        p2 = Plane(1, -2, 5, 4)
        self.assertEqual(type(p), Plane)
        self.assertEqual(p2, Plane(1, -2, 5, 4))
        self.assertNotEqual(p, p2)

    def test_instanciate(self):
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_x, expected_y, expected_z, expected_d in (
                [(), 0, 0, 0, 0],
                [(Vector3(2.0, 1.0, 3.0), 4.0), 2.0, 1.0, 3.0, 4.0],
                [(Vector3(1, 2, 3), Vector3(), Vector3(2, 2, 2)), -0.408248, 0.816497, -0.408248, 0],
                [(0.5, 0.5, 0.5, 0.5), 0.5, 0.5, 0.5, 0.5],
                [(1, 2, 3, 4), 1, 2, 3, 4]):
            p = Plane(*args)
            self.assertEqual(round(p.x, 6), expected_x, msg=msg_tmpl % (p.x, expected_x, args))
            self.assertEqual(round(p.y, 6), expected_y, msg=msg_tmpl % (p.y, expected_y, args))
            self.assertEqual(round(p.z, 6), expected_z, msg=msg_tmpl % (p.z, expected_z, args))
            self.assertEqual(round(p.d, 6), expected_d, msg=msg_tmpl % (p.d, expected_d, args))
        self.assertRaises(TypeError, Plane, "a", 2, 3, 4.)
        self.assertRaises(TypeError, Plane, "a", 2, 3.9)
        self.assertRaises(TypeError, Plane, 1, "b", 5, 5)
        self.assertRaises(TypeError, Plane, None, 2, "c", Vector3())

    def test_methods(self):
        p = Plane()
        # Don't test methods' validity but bindings one
        for field, ret_type, params in (
            ['center', Vector3, ()],
            ['distance_to', float, (Vector3(), )],
            ['get_any_point', Vector3, ()],
            ['has_point', bool, (Vector3(),)],
            ['has_point', bool, (Vector3(), 0.0)],
            ['intersect_3', Vector3, (Plane(), Plane())],
            ['intersects_ray', Vector3, (Vector3(), Vector3())],
            ['intersects_segment', Vector3, (Vector3(), Vector3())],
            ['is_point_over', bool, (Vector3(),)],
            ['normalized', Plane, ()],
            ['project', Vector3, (Vector3(),)]
        ):
            self.assertTrue(hasattr(p, field), msg='`Plane` has no method `%s`' % field)
            method = getattr(p, field)
            self.assertTrue(callable(method))
            ret = method(*params)
            self.assertEqual(type(ret), ret_type, msg="`Plane.%s` is expected to return `%s`" % (field, ret_type))

    def test_properties(self):
        p = Plane()
        for field, ret_type in (
                ('x', float),
                ('y', float),
                ('z', float),
                ('normal', Vector3),
                ('d', float)):
            self.assertTrue(hasattr(p, field), msg='`Plane` has no property `%s`' % field)
            field_val = getattr(p, field)
            self.assertEqual(type(field_val), ret_type, msg="`Plane.%s` is expected to be a `%s`" % (field, ret_type))
            val = None
            if field == 'normal':
                val = Vector3(10, 10, 10)
            else:
                val = 10.
            setattr(p, field, val)
            field_val = getattr(p, field)
            self.assertEqual(field_val, val, msg="`Plane.%s` is expected to be equal to `%s`" % (field_val, str(val)))


if __name__ == '__main__':
    unittest.main()
