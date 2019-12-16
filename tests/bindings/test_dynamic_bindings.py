# import pytest

# from godot.bindings import (
#     Object,
#     Node,
#     Viewport,
#     Input,
#     LineEdit,
#     Engine,
#     _Engine,
#     KEY_ESCAPE,
#     OK,
#     FAILED,
# )


# class TestDynamicBindings:
#     def test_singletons(self):
#         assert isinstance(Engine, _Engine)
#         assert callable(Engine.get_main_loop)
#         ml = Engine.get_main_loop()
#         assert isinstance(ml, Object)

#     def test_constants(self):
#         assert OK == 0
#         assert FAILED == 1
#         assert isinstance(KEY_ESCAPE, int)

#     def test_objects_unicity(self):
#         # Main loop object is a Godot Object, calling `get_main_loop` from
#         # python returns a different python wrapper on the same object each time.
#         # However those wrappers should feel like they are the same object.
#         ml = Engine.get_main_loop()
#         ml2 = Engine.get_main_loop()
#         assert ml == ml2
#         # Of course different objects should be different and equality
#         # should not crash with bad given types
#         obj = Object()
#         assert ml != obj
#         assert ml != None  # noqa
#         assert ml != ""
#         assert ml != 42
#         # Don't forget to free the Godot Object
#         obj.free()

#     def test_class(self):
#         assert isinstance(Node, type)

#     def test_class_constants(self):
#         assert hasattr(Input, "MOUSE_MODE_VISIBLE")
#         assert isinstance(Input.MOUSE_MODE_VISIBLE, int)

#     def test_class_inheritance(self):
#         assert issubclass(Node, Object)
#         assert issubclass(Viewport, Node)
#         assert issubclass(Viewport, Object)

#     def test_class_methods(self):
#         assert hasattr(LineEdit, "is_secret")
#         v = LineEdit()
#         assert callable(v.is_secret)
#         assert v.is_secret() is False
#         assert callable(v.set_secret)
#         v.set_secret(True)
#         assert v.is_secret() is True

#     @pytest.mark.xfail(reason="Not implemented yet.")
#     def test_class_signals(self):
#         pass

#     def test_class_properties(self):
#         assert hasattr(LineEdit, "max_length")
#         v = LineEdit()
#         assert v.max_length == 0
#         v.max_length = 42
#         assert v.max_length == 42
