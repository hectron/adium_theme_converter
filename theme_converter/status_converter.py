from theme_converter.base import BaseConverter

import os.path

class StatusConverter(BaseConverter):
    _available_statuses = {
        'Generic Available':'pidgin-status-available',
        'Free for Chat':'pidgin-status-chat',
        'Available for Friends Only':'',
        'Generic Away':'pidgin-status-away',
        'Extended Away':'pidgin-status-xa',
        'Away for Friends Only':'pidgin-status-away',
        'DND':'pidgin-status-busy',
        'Not Available':'pidgin-status-busy',
        'Occupied':'pidgin-status-busy',
        'BRB':'',
        'Busy':'pidgin-status-busy',
        'Phone':'pidgin-status-busy',
        'Lunch':'pidgin-status-busy',
        'Not At Home':'pidgin-status-xa',
        'Not At Desk':'pidgin-status-xa',
        'Not In Office':'pidgin-status-xa',
        'Vacation':'pidgin-status-xa',
        'Stepped Out':'pidgin-status-xa',
        'Idle And Away':'pidgin-status-busy',
        'Idle':'pidgin-status-busy',
        'Invisible':'pidgin-status-invisible',
        'Offline':'pidgin-status-offline',
        'Unknown':''
    }

    def get_default_theme_dir(self):
        return os.path.expanduser('~/.purple/themes/%s/purple/status-icon' % self.theme_name)

    def save_theme(self, path):
        import xml.etree.ElementTree
        import datetime

        _tree = xml.etree.ElementTree
        theme = _tree.Element('theme')
        description = _tree.SubElement(theme, 'description')
        description.text = 'Generated at %s in Affinity Status converter.' % datetime.datetime.now().strf('%m-%d-%Y %H:%M')

        theme.attrib = {
            'type': 'pidgin status icon',
            'name': self.theme_name,
            'author': 'affinity status converter'
        }

        icons = []

        if not path: path = self.make_theme_dir()
        new_path = '%s/16' % path
        
        try:
            os.mkdir(new_path)
        except OSError:
            print('Cannot make dir: %s\nMaybe the theme already exists?' % new_path)

        for icon_id in self.plist['List']:
            try:
                if self._available_statuses[icon_id]:
                    sauce = '%s/%s' % (self.path, self.plist['List'][icon_id])
                    target_file = os.path.basename(sauce)

                    icons.append(_tree.SubElement(theme, 'icon'))
                    icons[-1].attrib = {
                        'id': self._available_statuses[icon_id],
                        'file': target_file
                    }

                    icons.append(_tree.SubElement(theme, 'icon'))

                    icons[-1].attrib = {
                        'id': self._available_statuses[icon_id] + '-i',
                        'file': target_file
                    }

                    shutil.copy(sauce, '%s/%s' % (new_path, target_file))
                else:
                    print('Cannot find Adium\'s %s pidgin equivalent' % icon_id)
            except KeyError:
                print('Unknown Adium status icon id: %s' % icon_id)


        tree = _tree.ElementTree(theme)

        file_path = '%s/theme.xml' % path

        print('Saving theme.xml in: %s' % file_path)

        tree.write(file_path)

        os.system('xmllint --format "{0}" --output "{0}"'.format(file_path))