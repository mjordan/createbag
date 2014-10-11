# Create Bag

A simple utility to allow users to create a Bag from a directory on their file system.

## Features so far

* Uses standard file/directory picker to allow user to select which directory to create Bag from.
* BagIt tags can be defined in a config file.

## Python dependencies

* [Python GTK+3](http://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html)
* [bagit](https://github.com/LibraryOfCongress/bagit-python)

## Usage

Until Create Bag is compiled into native binaries, invoke it from the command line like this:

`python createbag.py`

and click on "Choose a directory to create Bag from" and go. Note that the Bag is created in place, meaning that the directory is replaced with the Bagged version.


## To do

* Port to Windows and OS X native binaries
* Add error handling, etc.
