from kivy.lang import Builder
from kivy.properties import AliasProperty, NumericProperty
from kivy.uix.widget import Widget


# Classes
# =======
class TexturedProgress(Widget):
    max = NumericProperty(100)
    value = NumericProperty(0)

    def get_value_normalized(self):
        return self.value / self.max

    value_normalized = AliasProperty(
        get_value_normalized,
        bind=["max", "value"]
    )


Builder.load_file("ui/textured_progress.kv")
