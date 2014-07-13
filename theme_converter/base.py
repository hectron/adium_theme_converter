#!/usr/bin/python

import optparse
import os.path
import shutil
import plistlib

class BaseConverter(object):
    def __init__(self, source_path, **kwargs):
        self.path = source_path
        self.theme_name = os.path.splitext(os.path.basename(source_path))[0]
        self.plist = plistlib.readPlist(self.find_p_list_file())

    def find_p_list_file(self):
        """ 
        Recursively checks the object's path for a file of type '.plist'. If
        one could not be found, it returns an empty string.

        Note, this just returns the FIRST .plist file it finds.
        """
        for root, dirs, files in os.walk(self.path, topdown = False):
            for directory in dirs:
                for name in files:
                    if name.lower().find('.plist') != -1:
                        return ('%s\\%s' % (root, name))

        print('Could not find a .plist file in path: %s' % self.path)
        return ''

    def save_theme(self, path):
        pass

    def get_default_theme_dir(self):
        pass

    def make_theme_dir(self):
        path = self.get_default_theme_dir()

        try:
            os.makedirs(path)
        except OSError:
            print('Cannot make directory: %s\n Do you have access to it?' % path)

        return path
