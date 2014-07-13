from nose.tools import *
from theme_converter.base import BaseConverter

def test_converter():
    converter = BaseConverter("~/renkoo")
    assert converter.path == '~/renkoo'
    assert converter.theme_name == 'renkoo'
    assert converter.plist == 'foo'