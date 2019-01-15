from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.label import Label
import os

from kivyfilechooser import KivyFileChooserLayout

class ChooserTest(App):
    def build(self):
        self.top_layout = FloatLayout()
        self.msg_label= Label(text="LABEL")
        self.top_layout.add_widget(self.msg_label)
        self.chooser= KivyFileChooserLayout(ok=self.ok, cancel=self.cancel,
                                            filter=self.is_dir)
        for directory in ['/home']:
            self.chooser.add_entry(directory)
        self.popup = Popup(title="Choose Directories", content=self.chooser)
        self.top_layout.add_widget(self.popup)
        return self.top_layout

    def is_dir(self, directory, filename):
        return os.path.isdir(os.path.join(directory, filename))

    def ok(self, directories):
        print ("APP: OK", directories)
        self.top_layout.remove_widget(self.popup)
        self.msg_label.text = "DIRECTORIES: " + ', '.join(directories)

    def cancel(self, directories):
        print ("APP: CANCEL", directories)
        self.top_layout.remove_widget(self.popup)

Factory.register('KivyFileChooserLayout', cls=KivyFileChooserLayout)


if __name__ == '__main__':
    palmchooser_test_app = ChooserTest()
    palmchooser_test_app.run()
