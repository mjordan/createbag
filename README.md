# Create Bag

A simple utility to allow users to create a Bag from a directory on their file system.

## Features so far

* Uses standard file/directory picker to allow user to select which directory to create Bag from.
* BagIt tags can be defined in a config file.
* Checksum algorithms can be defined in a config file.
* The option (set in the config file) to copy the contents of the selected directory to specific location before creating the Bag. Note that since the Bag is created from the copy, checksums are generated for the copies, not the original files.

## Python dependencies

* [Python GTK+3](http://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html)
    ** On Ubuntu Linux, all prerequisites should already be installed. 
    ** On Windows, install the latest version from http://sourceforge.net/projects/pygobjectwin32/files/?source=navbar. When asked which packages to install, choose GTK+. No other packages in this distribution are necessary for Create Bag to run.
* [bagit](https://github.com/LibraryOfCongress/bagit-python)
    ** On all platforms, install with `pip install bagit`. 

## Usage

Invoke the utility from the command line like this:

`python createbag.py`

Clicking on the "Choose a directory to create Bag from" will open up a standard file/directory chooser dialog box. Choose a directory and click on "Create Bag".

The goal is to compile the utility into native Windows, OS X, and Linux binaries, at which point the utility will be invoked like any other Graphical User Interface program on those operating systems.

## To do

* Port to Windows, OS X, and Linux native binaries
* Add better error handling
