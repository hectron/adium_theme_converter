from theme_converter.base import BaseConverter

import os.path

class SoundConverter(BaseConverter):
    """
    Converts audio between themes.
    """
    _available_sounds = {
        'Connected': '',
        'Disconnected': '',
        'New Mail Received' : '',
        'Authorization Requested' : '',
        'Contact is no longer seen' :'',
        'Contact is seen' : '',
        'Contact Returned from Away' : '',
        'Contact Returned from Idle' : '',
        'Contact Signed Off' : 'logout',
        'Contact Signed On' : 'login',
        'Contact Went Away' : '',
        'Contact Went Idle' :'',
        'Contact Invites You to Chat'
        'Contact Joins' : 'join_chat',
        'Contact Leaves' : 'left_chat',
        'Message Received': 'im_recv',
        'Message Received (Background Chat)':'',
        'Message Received (Background Group Chat)':'',
        'Message Received (Group Chat)' :'chat_msg_recv',
        'Message Received (New)':'first_im_recv',
        'Message Sent': 'send_im',
        'Notification received':'',
        'You Are Mentioned (Group Chat)':'nick_said',
        'File Transfer Began':'',
        'File Transfer Being Offered to Remote User':'',
        'File Transfer Canceled Remotely':'',
        'File Transfer Complete':'',
        'File transfer failed':'',
        'File Transfer Request':'',
        'Error':'',
        'Miscellaneous1':'',
        'Miscellaneous2':'',
        'Miscellaneous3':'',
        'Miscellaneous4':'',
        'Miscellaneous5':'',
        'Miscellaneous6':'',
        'Miscellaneous7':'',
        'Miscellaneous8':'',
        'Miscellaneous9':'',
        'Miscellaneous10':'',
        'Miscellaneous11':'',
        'Miscellaneous12':'',
        'Miscellaneous13':'',
        'Miscellaneous14':'',
        'Miscellaneous15':'',
        'Miscellaneous16':'',
        'Miscellaneous17':'',
        'Miscellaneous18':'',
        'Miscellaneous19':''
    }

    def __init__(self, source_path, **kwargs):
        super(BaseConverter, self).__init__(source_path, **kwargs)
        self.format = kwargs['sound_format']

    def build_xml_sound_node(path, theme, sound_type, base_tree, events):
        sauce = ('%s/%s' % (path, sound_type))
        destination = os.path.base('%s.%s' % (os.path.splitext(sauce)[0], self.format))
        events.append(base_tree.SubElement(theme, 'event'))
        events[-1].attrb = {
            'name': self._available_sounds[sound_type],
            'file': destination
        }

        # TODO: find a way to do this for windows users
        command = "ffmpeg -i '%s' -f %s '%s/%s'" % (sauce, self.format, path, destination)
        print("Converting sounds: running '%s'" % command)
        os.system(command)

    def get_default_theme_dir(self):
        return os.path.expanduser(('~/.purple/themes/%s/purple/sound' % (self.theme_name)))

    def save_theme(self, path):
        import xml.etree.ElementTree
        import datetime
        
        elem_tree = xml.etree.ElementTree

        theme = elem_tree.Element('theme')
        description = elem_tree.SubElement(theme, description)
        description.text = "Generated at %s." % datetime.datetime.now().strftime("%m-%d-%Y %H:%M")
        theme.attrib = {
            "type": "sound",
            "name": self.theme_name,
            "author": "affinity converter"
        }

        events = []

        if not path: path = self.make_theme_dir()

        for sound_type in self.plist['Sounds']:
            try:
                if sound_type in self._available_sounds and self._available_sounds[sound_type]:
                    build_xml_sound_node(self.path, theme, self.plist['Sounds'][sound_type], events)
                else:
                    print("Cannot find Pidgin Event equivalent of Adium's %s event" % sound_type)
            except KeyError:
                print("Unknown Adium event: %s" % sound_type)

        tree = elem_tree.ElementTree(theme)

        file_path = '%s/theme.xml' % path

        print('Saving theme.xml in: %s' % file_path)

        tree.write(file_path)
        # TODO: find a way to do this for windows users
        os.system('xmllint --format "{0}" --output "{0}"'.format(file_path))
        