import unittest
import omniValidator as ov 

class testGetSchema(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        

unittest.main()