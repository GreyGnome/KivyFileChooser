from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.lang import Builder
import os
from debug_print import Debug

debug = Debug(True)

Builder.load_file("kivyfilechooser.kv")

palmchooser_test_app = None

DEBUG = True

class RemoveButton(Button):
    def __init__(self, *args, **kwargs):
        self.associated_label = kwargs.pop("associated_label")
        self.directory = kwargs.pop("directory")
        super(RemoveButton, self).__init__(*args, **kwargs)


class DirectoryGridLayout(GridLayout):
    directories = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(DirectoryGridLayout, self).__init__(*args, **kwargs)

    def remove_dir(self, remove_button):
        self.directories.remove(remove_button.directory)
        self.remove_widget(remove_button.associated_label)
        self.remove_widget(remove_button)
        print ("Directories now:", self.directories)

    def add_dir(self, dir_list):
        """

        :param dir_list: A list with 1 string element in it (the directory) This
        is what the kv file supplies to this method, so we must accept the list
        argument.
        :return:
        """
        directory = dir_list[0]
        if not directory in self.directories:
            self.directories.append(directory)
            directory_label = Label(text=str(directory), halign="left",
                                    size_hint_x=0.9, size_hint_y=None, height=20)
            directory_label.bind(size=directory_label.setter('text_size'))
            remove_button = RemoveButton(text="X", size_hint_x=0.1, size_hint_y=None,
                                        height=20, associated_label=directory_label,
                                        directory=directory)
            remove_button.bind(on_release=self.remove_dir)
            self.add_widget(remove_button)
            self.add_widget(directory_label)
        else:
            debug.print ("Directory", directory, "already in the list")
        debug.print ("Directories: ", self.directories, type(self.directories))

    def on_directories(self, *args):
        debug.print ("self.directories: ", self.directories, " ARGS: ", *args)


class KivyFileChooserLayout(FloatLayout):
    """
    Example usage:

        self.chooser= KivyFileChooserLayout(ok=self.ok, cancel=self.cancel)
        for directory in ['/home/my_login/stuff']:
            self.chooser.add_dir(directory)
        self.popup = Popup(title="Choose Directories", content=self.chooser)
        self.top_layout.add_widget(self.popup)
    """
    loadfile = ObjectProperty(None)
    txt_inpt = ObjectProperty(None)

    initial_dirs = ListProperty([])

    def __init__(self, *args, **kwargs):
        self.chosen_dirs = ListProperty([])
        self.ok_method = kwargs.pop("ok", None)
        self.cancel_method = kwargs.pop("cancel", None)
        self._filter = kwargs.pop("filter", self.filter)
        super(KivyFileChooserLayout, self).__init__(*args, **kwargs)

    def filter(self, directory, filename):
        """

        :param directory: As specified at https://kivy.org/doc/stable/api-kivy.uix.filechooser.html,
        it is the first argument to your filter.
        :param filename: Likewise, this is the second argument.
        :return:
        """
        pass

    def cancel(self):
        grid = self.ids["directory_grid"]
        if self.cancel_method is not None:
            self.cancel_method(grid.directories)

    def ok(self):
        grid = self.ids["directory_grid"]
        if self.ok_method is not None:
            self.ok_method(grid.directories)

    def add_dir(self, directory):
        """

        :param directory: String which is a path to a directory.
        :return:
        """
        grid = self.ids["directory_grid"]
        # This must be a list because the kv file supplies a list to this method.
        grid.add_dir([directory])
