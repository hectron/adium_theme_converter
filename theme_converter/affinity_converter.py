from theme_converter.sound_converter import SoundConverter
from theme_converter.emoticon_converter import EmoticonConverter
from theme_converter.dock_converter import DockConverter
from theme_converter.status_converter import StatusConverter

import optparse
import os.path
import mimetypes
import tempfile
import shutil
import zipfile

class AffinityConverter(object):
    Converters = {
        'sound': [SoundConverter, ['.adiumsoundset']],
        'emoticon': [EmoticonConverter, ['.adiumemoticonset']],
        'status': [StatusConverter, ['.adiumstatusicon', '.adiumstatusicons']],
        'dockbar': [DockConverter, ['.adiumicon']]
    }

    def Exit(message):
        """
        Deletes the temporary directory created in the process and prints the
        message given. This should generally be used for error messages.
        """
        global TMP_DIR_NAME

        try:
            if TMP_DIR_NAME: shutil.rmtree(TMP_DIR_NAME)
        except:
            pass

        print message

        exit()

    def unpack(path):
        """
        If it's an archive, unpack into temporary directory and return path.
        Else return the path.
        """
        if os.path.isdir(path):
            return os.path.normpath(path)
        elif os.path.isfile(path):
            mimetypes.init()
            file_type = mimetypes.guess_type(path)

            if file_type[0] in ['application/zip', 'application/x-zip-compressed']:
                tmp_dir = tempfile.mkdtemp(prefix = 'AffinityConverter', suffix = os.path.basename(path))
                zip = zipfile.ZipFile(path)
                zip.extractall(tmp_dir)
                global TMP_DIR_NAME
                TMP_DIR_NAME = tmp_dir

                for directory in os.listdir(tmp_dir):
                    if dir != '__MACOSX' and os.path.isdir('%s/%s' % (tmp_dir, directory)):
                        resdir = '%s/%s' % (tmp_dir, directory)

                try:
                    return resdir
                except:
                    Exit('Source file can not be unzipped. Is it a valid zip archive?')
            else:
                Exit('Source file is not zip archive')
        else:
            Exit('Source path is not a valid path. Path given: %s' % path)

    def parse_arguments():
        parser = optparse.OptionParse(usage = 'Usage: %prog [-o PATH] [-t auto|sound|status|emoticon|theme] [-s aif|mp3|wav] source_adium_theme')

        parser.add_option('-o', '--output', dest = 'output', help = 'write converted Pidgin theme to PATH, default: ~/.purple/themes/$THEMENAME/', metavar = 'PATH')
        parser.add_option('-t', '--type', dest = 'type', help = 'type of theme, options: auto, sound, status, emoticon, theme, default: auto', metavar = 'TYPE')
        parser.add_option('-s', '--sound-format', dest = 'sound_format', help = 'convert sound to: aif, wav, or mp3, default: mp3', metavar = 'SOUND_FORMAT')

        (options, args) = parser.parse_args()

        if len(args) > 1: parser.error('No file or directory specified')

        return (options, args[0])

    def detect_type(path):
        (root, extension) = os.path.splitext(path)
        extension = extension.lower()

        for type in Converters:
            if ext in Converters[type][1]:
                return type
        Exit('Unable to detect type of theme, select it manual with --type option!')

def valid_type(custom_type):
    return custom_type in ['dockbar', 'auto', 'sound', 'emoticon', 'status', None]

def valid_audio_format(audio_format):
    return audio_format in ['wav', 'aif', 'mp3', None]

if __name__ == '__main__':
    program = AffinityConverter()
    _TMP_DIR_NAME = ''
    (options, input_path) = parse_arguments()

    print options

    if not (valid_type(options.type) and valid_audio_format(options.sound_format)):
        Exit('Wrong type or sound format parameters. Try --help for available options')

    source = unpack(input_path)

    if not options.type or options.type == 'auto':
        options.type = detect_type(source)
        print 'Auto detect type of theme: %s' % options.type

    if not options.sound_format:
        options.sound_format = 'wav'

    converter = Converters[options.type][0](source_path = source, sound_format = options.sound_format)

    converter.save_theme(options.output)

    Exit('Success!')