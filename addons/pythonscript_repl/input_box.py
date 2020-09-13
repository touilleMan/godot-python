from godot import exposed, InputEventKey, KEY_UP, KEY_DOWN, LineEdit


@exposed(tool=True)
class InputBox(LineEdit):
    def _enter_tree(self):
        self.repl_node = self.get_parent().get_parent()

    def _gui_input(self, event):
        if isinstance(event, InputEventKey) and event.pressed:
            if event.scancode == KEY_UP:
                self.repl_node.up_pressed()
                self.accept_event()
            elif event.scancode == KEY_DOWN:
                self.repl_node.down_pressed()
                self.accept_event()
