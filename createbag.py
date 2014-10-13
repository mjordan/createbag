"""
Simple GUI tool to create a Bag from a filesystem folder.

@todo:
  - Add error handling around the call to bagit and copying
    into 'create_bag_in' value.
"""

import ConfigParser
import sys
import os
import shutil
import bagit
from gi.repository import Gtk

# Get config file location and parse the file.
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    config_file = './config.cfg'

config = ConfigParser.ConfigParser({'add_source_directory_tag': False})
config.optionxform = str
config.read(config_file)

# Get tags from config file.
bagit_tags = {}
tags = config.options('Tags')
for tag in tags:
    bagit_tags[tag] = config.get('Tags', tag)

# Get checksum algorithms from config file.
bagit_checksums = []
if config.has_option('Checksums', 'algorithms'):
    checksums_string = config.get('Checksums', 'algorithms', 'md5')
    bagit_checksums = [algo.strip() for algo in checksums_string.split(',')]
else:
    bagit_checksums = ['md5']


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

        if response == Gtk.ResponseType.OK:
            if config.getboolean('Other', 'add_source_directory_tag'):
                bagit_tags['Source-Directory'] = folder_picker_dialog.get_filename()

            # If the 'create_bag_in' config option is set, create the Bag from a
            # copy of the selected folder.
            if config.has_option('Other', 'create_bag_in'):
                relativized_picker_path = os.path.relpath(folder_picker_dialog.get_filename(), '/')
                bag_dir = os.path.join(config.get('Other', 'create_bag_in'), relativized_picker_path)
                shutil.rmtree(bag_dir, True)
                shutil.copytree(folder_picker_dialog.get_filename(), bag_dir)
            # If it's not set, create the Bag in the selected directory.
            else:
                bag_dir = folder_picker_dialog.get_filename()

            bag = bagit.make_bag(bag_dir, bagit_tags, 1, bagit_checksums)
            confirmation_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Bag created")
            confirmation_dialog.format_secondary_text(
                "The Bag for folder %s has been created." % bag_dir)
            confirmation_dialog.run()
            confirmation_dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("Operation cancelled")

        folder_picker_dialog.destroy()


win = FolderChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
