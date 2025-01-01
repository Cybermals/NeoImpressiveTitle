from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget


# Classes
# =======
class FloatingWindow(DragBehavior, Widget):
    title_bar = ObjectProperty(None)
    title = StringProperty()
    background_panel = StringProperty()
    background_border = StringProperty()
    background_title = StringProperty()
    background_close_normal = StringProperty()
    background_close_down = StringProperty()

    def on_touch_down(self, touch):
        # Call base method
        super().on_touch_down(touch)

        # Check if the touch was inside this widget
        if self.collide_point(touch.x, touch.y):
            # Bring this widget to the top of the z-order by removing it from
            # its parent and adding it back to its original parent.
            parent = self.parent

            if parent is not None:
                self.parent.remove_widget(self)
                parent.add_widget(self)

            # The event has been handled, so prevent further processing of it.
            return True

        else:
            # Continue processing the event
            return False

    def on_close(self):
        # Remove this widget from its parent. If you need to reopen it later,
        # be sure to keep a reference to prevent it from being garbage
        # collected.
        self.parent.remove_widget(self)


Builder.load_file("ui/floating_window.kv")
