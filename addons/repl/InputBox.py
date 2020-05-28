from godot import exposed, export
from godot import *


@exposed(tool=True)
class InputBox(LineEdit):

    # segfaults
    # def _input(self, event):
    # if event is InputEventKey and event.pressed:
    # 	if event.scancode == KEY_UP:
    # 		print("UP was pressed")

    # also segfaults
    # def _gui_input(self, event):
    # 	pass

    def _enter_tree(self):
        self.had_focus = False

    def _process(self, _delta):
        # Hacky, but _input is segfaulting right now
        if Input.is_action_just_pressed("ui_up") and self.had_focus:
            self.get_parent().get_parent().up_pressed()

        if Input.is_action_just_pressed("ui_down") and self.had_focus:
            self.get_parent().get_parent().down_pressed()

        self.had_focus = self.has_focus()

    def _ready(self):
        pass
