
class DirectoryGridLayout(GridLayout):
    directories = ListProperty([])

    def __init__(self, *args, **kwargs):
        # self.bind(minimum_height=self.setter('height'))
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
