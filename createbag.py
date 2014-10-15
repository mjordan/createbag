"""
Simple GUI tool to create a Bag from a filesystem folder.
"""

import ConfigParser
import sys
import os
import shutil
import getpass
import bagit
import platform
if platform.system() != 'Darwin':
    from gi.repository import Gtk
else:
    # Sets up Cocoadialog for error message popup on OSX
    class cocoaPopup:

    # Change CD_BASE to reflect the location of Cocoadialog on your system
        CD_BASE = "~/.createbag/"
        CD_PATH = os.path.join(CD_BASE, "CocoaDialog.app/Contents/MacOS/CocoaDialog")

        def __init__(self, title, message, button):
            template = "%s msgbox --title '%s' --text '%s' --button1 '%s'"
            self.pipe = os.popen(template % (cocoaPopup.CD_PATH, title, message, button), "w")
    
    def cocoaError():    
        if __name__ == "__main__":
            popup = cocoaPopup("Error","Sorry, you can't create a bag here -- you may want to change the config file so that bags are always created in a different output directory, rather than in situ.","OK")
            if popup == "1":
                popup.close()
                
    def cocoaSuccess(bag_dir):    
        if __name__ == "__main__":
            popup = cocoaPopup("Success!","Bag created at %s" % bag_dir,"OK")
            if popup == "1":
                popup.close()

# Get config file location and parse the file.
if platform.system() != 'Darwin':
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = './config.cfg'
else:
    if len(sys.argv) > 2:
        config_file = sys.argv[2]
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

# Get shortcuts from config file.
if config.has_option('Shortcuts', 'shortcuts'):
    filechooser_shortcuts = [shortcut.strip() for shortcut in config.get('Shortcuts', 'shortcuts').split(',')]
else:
    filechooser_shortcuts = []

# Get checksum algorithms from config file.
bagit_checksums = []
if config.has_option('Checksums', 'algorithms'):
    checksums_string = config.get('Checksums', 'algorithms', 'md5')
    bagit_checksums = [algo.strip() for algo in checksums_string.split(',')]
else:
    bagit_checksums = ['md5']


# Don't let the utility create a Bag in its own directory.
def directory_check(chosenFolder):
    if config.has_option('Other', 'create_bag_in'):
        relativized_picker_path = os.path.relpath(chosenFolder, '/')
        bag_dir = os.path.join(config.get('Other', 'create_bag_in'), relativized_picker_path)
        if os.path.dirname(os.path.realpath(__file__)) == bag_dir:
            if platform.system() != 'Darwin':
                FolderChooserWindow.GtkError(win)
            else:
                cocoaError()
    else:
        if os.path.dirname(os.path.realpath(__file__)) == chosenFolder:
            if platform.system() != 'Darwin':
                FolderChooserWindow.GtkError(win)
            else:
                cocoaError()

def make_bag(chosenFolder):
    if config.getboolean('Other', 'add_source_directory_tag'):
        bagit_tags['Source-Directory'] = chosenFolder

    if config.getboolean('Other', 'add_source_user_id_tag'):
        bagit_tags['Source-User'] = getpass.getuser()                

    # If the 'create_bag_in' config option is set, create the Bag from a
    # copy of the selected folder.
    if config.has_option('Other', 'create_bag_in'):
        relativized_picker_path = os.path.relpath(chosenFolder, '/')
        bag_dir = os.path.join(config.get('Other', 'create_bag_in'), relativized_picker_path)
        try:
            shutil.rmtree(bag_dir, True)
            shutil.copytree(chosenFolder, bag_dir)
        except (IOError, os.error) as shutilerror:
            if platform.system() != 'Darwin':
                FolderChooserWindow.GtkError(win)
            else:
                cocoaError()

    # If it's not set, create the Bag in the selected directory.
    else:
        bag_dir = chosenFolder

    try:
        bag = bagit.make_bag(bag_dir, bagit_tags, 1, bagit_checksums)
    except (bagit.BagError, Exception) as e:
        if platform.system() != 'Darwin':
            FolderChooserWindow.GtkError(win)
        else:
            cocoaError()
    return bag_dir


if platform.system() != 'Darwin':
    class FolderChooserWindow(Gtk.Window):

        def __init__(self):
            Gtk.Window.__init__(self, title = config.get('Other', 'main_window_title', 'Create a Bag'))
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

        def GtkError(self):
            not_allowed_message = "\n\nYou are not allowed to run the program on that directory."
            error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK, "Sorry...")
            error_dialog.format_secondary_text(not_allowed_message)
            error_dialog.run()
            error_dialog.destroy()
            raise SystemExit

        def on_folder_clicked(self, widget):
            folder_picker_dialog = Gtk.FileChooserDialog(
                config.get('Other', 'file_chooser_window_title', 'Create a Bag - Choose a folder to create Bag from'),
                self, Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                "Create Bag", Gtk.ResponseType.OK))
            folder_picker_dialog.set_default_size(800, 400)
            folder_picker_dialog.set_create_folders(False)
            for filechooser_shortcut in filechooser_shortcuts:
                print filechooser_shortcut
                folder_picker_dialog.add_shortcut_folder(filechooser_shortcut)

            response = folder_picker_dialog.run()

            if response == Gtk.ResponseType.OK:

                directory_check(folder_picker_dialog.get_filename())

                bag_dir = make_bag(folder_picker_dialog.get_filename())

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
    
else:
    directory_check(sys.argv[1])
    bag_dir = make_bag(sys.argv[1])
    cocoaSuccess(bag_dir)

#try:
#    shutil.rmtree('/tmp/createbag')
#except:
#    pass
