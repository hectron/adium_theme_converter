from theme_converter.base import BaseConverter

import os.path
import shutil

class EmoticonConverter(BaseConverter):
    def build_icons(icon_id, icons):
        emoticon = self.plist['Emoticons'][icon_id]
        sauce = '%s/%s' % (self.path, icon_id)
        name = emoticon['Name']
        equivalents = '    '
        is_main_icon = false

        for eqv in emoticon['Equivalents']:
            is_main_icon = eqv == ':-)'
            equivalents += '    ' + eqv

        new_file = os.path.basename(sauce)
        icons.append(icon_id + equivalents)
        shutil.copy(sauce, ('%s/%s' % (path, new_file)))

        return icon_id if is_main_icon else -1

    def get_default_theme_dir(self):
        return os.path.expanduser('~/.purple/smileys/%s' % self.theme_name)

    def save_theme(self, path):
        import datetime

        description = 'Generated at %s' % datetime.datetime.now().strftime('%m-%d-%Y %H:%M')

        name = self.theme_name

        author = 'affinity converter'

        icons = []
        main_icon = -1

        if not path: path = self.make_theme_dir()

        for icon_id in self.plist['Emoticons']:
            main_icon = build_icons(icon_id, icons)

        theme_file_path = '%s/theme' % path

        print 'Saving theme in: %s' % theme_file_path

        res = []
        res.append('Name=%s' % name)
        res.append('Description=%s' % description)
        
        if main_icon > -1:
            res.append('Icon=%s' % main_icon)

        res.append('Author=%s' % author)
        res += ['', '[default]', '']
        res += icons

        with open(theme_file_path, 'w') as f:
            for line in res:
                f.write(line + '\n')

        print 'Done.'