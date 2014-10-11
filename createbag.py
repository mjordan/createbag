"""
Simple tool to create a Bag from a filesystem folder.

@todo:
  - Add error handling around the call to bagit.
  - Get working on Windows.
"""

import ConfigParser
import bagit
from gi.repository import Gtk

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read('config.cfg')

# Get tags from config file.
bagit_tags = {}
tags = config.options('Tags')
for tag in tags:
    bagit_tags[tag] = config.get('Tags', tag)

class FolderChooserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Create a Bag")
        self.set_border_width(10)
        self.move(200, 200)

        box = Gtk.Box(spacing=6)
        self.add(box)
       
        choose_folder_button = Gtk.Button("Choose a folder to create Bag from")
        choose_folder_button.connect("clicked", self.on_folder_clicked)
        box.add(choose_folder_button)

        quit_button = Gtk.Button("Quit")
        quit_button.connect("clicked", Gtk.main_quit)
        box.add(quit_button)

    def on_folder_clicked(self, widget):
        folder_picker_dialog = Gtk.FileChooserDialog("Please choose a folder to create a Bag from", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Create Bag", Gtk.ResponseType.OK))
        folder_picker_dialog.set_default_size(800, 400)
        folder_picker_dialog.set_create_folders(False)

        response = folder_picker_dialog.run()
        if config.getboolean('Other', 'add_source_directory_tag'):
            bagit_tags['Source-Directory'] = folder_picker_dialog.get_filename()
        if response == Gtk.ResponseType.OK:
            bag = bagit.make_bag(folder_picker_dialog.get_filename(), bagit_tags)
            confirmation_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Bag created")
            confirmation_dialog.format_secondary_text(
                "The Bag for folder %s has been created." % folder_picker_dialog.get_filename())
            confirmation_dialog.run()
            confirmation_dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("Operation cancelled")

        folder_picker_dialog.destroy()


win = FolderChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
