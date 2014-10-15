# Create Bag

A simple utility to allow users to create a Bag from a directory on their file system.

This utility is not a replacement for a full-featured tool such as the Library of Congress's Bagger (included in their [Transfer Tools](http://sourceforge.net/projects/loc-xferutils/files/loc-bagger/)). Instead, its purpose is to hide the details of creating a Bag from the end user by providing a simple, familiar user interface. Settings for Bag creation are contained in a configuration file (that would be modified by a network administrator, for example).

## Features

* Runs on Linux and Windows (after installation of prerequisites). Will likely run on OS X as well - testers welcome.
* Uses standard Graphical User Interface file/directory browser to allow user to select which directory to create Bag from.
* Configuration options:
    * Definition of the title of the main application window and the file chooser window title
    * Definition of custom BagIt tags
    * Options to enable some auto-generated BagIt tags (currently Source-Directory and Source-User)
    * Choice of checksum algorithms (md5, sha1, sha256, and sha512)
    * The option to define a list of "shortcuts" (i.e., links to directories) that appear in the file chooser dialog box.
    * The ability to specify which configuration file to use (as a command-line parameter)

An important option is 'create_bag_in'. If this is not set, the Bag is created in the selected directory and its contents are rearranged into a Bag structure. The value of this option is set to '/tmp' by default; *Windows users will need to set it manually before running the utility.*


to copy the contents of the selected directory to specific destination directory before creating the Bag. Note that since the Bag is created from the copy, checksums are generated for the copies, not the original files.

## Dependencies

* Python 2.7.8, but should work with any recent version of Python
* [Python GTK+3](http://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html)
    * On Linux, Python bindings for GTK+3 should already be installed
    * On Windows, install the latest version from http://sourceforge.net/projects/pygobjectwin32/files/?source=navbar. When asked which packages to install, choose GTK+. No other packages in this distribution are necessary for Create Bag to run.
* [bagit](https://github.com/LibraryOfCongress/bagit-python)
    * On all platforms, install with `pip install bagit` 

## Usage

Command line usage is documented here. However, it is possible on both Linux and Windows to create operating-system-specific shortcuts, allowing end users to start the program by clicking or double clicking on a desktop icon.

Invoke the utility from the command line like this:

`python createbag.py`

Create Bag allows you to specify which configuration file to use, as a command-line argument. If run as above, with no argument, the script looks for the file 'config.cfg' in the same directory as the script. To indicate another location for the configuration file, run the script with the file's path as an argument, like this:

`python createbag.py /path/to/the/config.file`

When the utility starts, a small window with two buttons appears:

![Create a Bag](https://dl.dropboxusercontent.com/u/1015702/linked_to/createbag/createbag.png)

Clicking on the "Choose a directory to create Bag from" will open up a standard file/directory browser:

![Choose a directory](https://dl.dropboxusercontent.com/u/1015702/linked_to/createbag/choosefolder.png)

Choosing a directory and clicking on "Create Bag" will create the Bag, after which the following dialog box will appear:

![Bag created](https://dl.dropboxusercontent.com/u/1015702/linked_to/createbag/bagcreated.png)

Clicking on "OK" will take the user back to the startup window:

![Create a Bag](https://dl.dropboxusercontent.com/u/1015702/linked_to/createbag/createbag.png)

## To do

* Compile the utility into native Windows, OS X, and Linux binaries, at which point the utility will be invoked like any other Graphical User Interface application on those operating systems.
* Add better error handling (e.g., options for going back to main application window on Bag creation error, etc.).
* Add error logging, with log path as a configuration option.

Pull requests implementing these features are welcome.

## License

The Unlicense (http://unlicense.org/). Refer to the LICENSE file for more information.
