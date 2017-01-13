import unittest

from godot.bindings import Object, Node, Viewport, EditorPlugin, OS, _OS, KEY_ESCAPE, OK, FAILED


class TestDynamicBindings(unittest.TestCase):

    def test_singletons(self):
        self.assertEqual(type(OS), _OS)
        self.assertTrue(callable(OS.get_main_loop))
        ml = OS.get_main_loop()
        self.assertTrue(isinstance(ml, Object))

    def test_constants(self):
        self.assertEqual(OK, 0)
        self.assertEqual(FAILED, 1)
        self.assertEqual(type(KEY_ESCAPE), int)

    def test_objects_unicity(self):
        # Main loop object is a Godot Object, calling `get_main_loop` from
        # python returns a different python wrapper on the same object each time.
        # However those wrappers should feel like they are the same object.
        ml = OS.get_main_loop()
        ml2 = OS.get_main_loop()
        self.assertEqual(ml, ml2)
        # Of course different objects should be different and equality
        # should not crash with bad given types
        self.assertNotEqual(ml, Object())
        self.assertNotEqual(ml, None)
        self.assertNotEqual(ml, "")
        self.assertNotEqual(ml, 42)

    def test_class(self):
        self.assertEqual(type(Node), type)

    def test_class_constants(self):
        self.assertTrue(hasattr(EditorPlugin, 'CONTAINER_TOOLBAR'))
        self.assertEqual(type(EditorPlugin.CONTAINER_TOOLBAR), int)

    def test_class_inheritance(self):
        self.assertTrue(issubclass(Node, Object))
        self.assertTrue(issubclass(Viewport, Node))
        self.assertTrue(issubclass(Viewport, Object))

    def test_class_methods(self):
        pass

    def test_class_signals(self):
        pass

    def test_class_properties(self):
        self.assertTrue(hasattr(Viewport, 'own_world'))
        v = Viewport()
        self.assertTrue(hasattr(v.own_world, bool))
        # self.assertTrue(v.own_world)
        # v.own_world = False
        # self.assertFalse(v.own_world)


if __name__ == '__main__':
    unittest.main()
