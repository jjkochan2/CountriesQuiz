# imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# define layout
class MyLayout(BoxLayout):

    # define what runs when the layout is created
    def __init__(self, **kwargs):

        # run the BoxLayout init?
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.points = 0

        self.label = Label(text=f"Points: {self.points}", font_size=32)
        self.button = Button(text="Click me")

        self.button.bind(on_press=self.on_button_click)

        self.add_widget(self.label)
        self.add_widget(self.button)

    def on_button_click(self, instance):
        self.points += 1
        self.label.text = f"Points: {self.points}"

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    MyApp().run()