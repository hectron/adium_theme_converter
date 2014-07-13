from theme_converter.base import BaseConverter

class CustomConverter(BaseConverter):
    def test_stuff(self):
        print(os.path.basename('~/'))

if __name__ == '__main__':
    c = CustomConverter('C:\\')
    print c.test_stuff()