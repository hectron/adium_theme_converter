from theme_converter.base import BaseConverter

import os.path
import shutil

class DockConverter(BaseConverter):
    def get_default_theme_dir(self):
        return os.path.expanduser('~/.purple/smileys/%s' % self.theme_name)

    def save_theme(self, path):
        if not path: path = self.get_default_theme_dir()

        shutil.copytree(self.path, path)
        print 'Installed dock theme to: %s' % path