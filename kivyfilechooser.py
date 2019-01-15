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
        self.entry = kwargs.pop("entry")
        super(RemoveButton, self).__init__(*args, **kwargs)


class EntryGridLayout(GridLayout):
    entries = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(EntryGridLayout, self).__init__(*args, **kwargs)

    def remove_entry(self, remove_button):
        self.entries.remove(remove_button.entry)
        self.remove_widget(remove_button.associated_label)
        self.remove_widget(remove_button)
        print ("Entries now:", self.entries)

    def add_entry(self, entry_list):
        """

        :param entry_list: A list with 1 string element in it (the path) This
        is what the kv file supplies to this method, so we must accept the list
        argument.
        :return:
        """
        entry = entry_list[0]
        if not entry in self.entries:
            self.entries.append(entry)
            entry_label = Label(text=str(entry), halign="left",
                                    size_hint_x=0.9, size_hint_y=None, height=20)
            entry_label.bind(size=entry_label.setter('text_size'))
            remove_button = RemoveButton(text="X", size_hint_x=0.1, size_hint_y=None,
                                        height=20, associated_label=entry_label,
                                        entry=entry)
            remove_button.bind(on_release=self.remove_entry)
            self.add_widget(remove_button)
            self.add_widget(entry_label)
        else:
            debug.print ("entry", entry, "already in the list")
        debug.print ("entries: ", self.entries, type(self.entries))

    def on_entries(self, *args):
        debug.print ("self.entries: ", self.entries, " ARGS: ", *args)


class KivyFileChooserLayout(FloatLayout):
    """
    Example usage:

        self.chooser= KivyFileChooserLayout(ok=self.ok, cancel=self.cancel)
        for directory in ['/home/my_login/stuff']:
            self.chooser.add_entry(directory)
        self.popup = Popup(title="Choose entries", content=self.chooser)
        self.top_layout.add_widget(self.popup)
    """
    loadfile = ObjectProperty(None)
    txt_inpt = ObjectProperty(None)

    initial_entries = ListProperty([])

    def __init__(self, *args, **kwargs):
        self.chosen_entries = ListProperty([])
        self.ok_method = kwargs.pop("ok", None)
        self.cancel_method = kwargs.pop("cancel", None)
        self._filter = kwargs.pop("filter", self.filter)
        super(KivyFileChooserLayout, self).__init__(*args, **kwargs)

    def filter(self, entry, filename):
        """

        :param entry: As specified at https://kivy.org/doc/stable/api-kivy.uix.filechooser.html,
        it is the first argument to your filter.
        :param filename: Likewise, this is the second argument.
        :return:
        """
        pass

    def cancel(self):
        grid = self.ids["entry_grid"]
        if self.cancel_method is not None:
            self.cancel_method(grid.entries)

    def ok(self):
        grid = self.ids["entry_grid"]
        if self.ok_method is not None:
            self.ok_method(grid.entries)

    def add_entry(self, entry):
        """

        :param entry: String which is a path to a entry.
        :return:
        """
        grid = self.ids["entry_grid"]
        # This must be a list because the kv file supplies a list to this method.
        grid.add_entry([entry])
