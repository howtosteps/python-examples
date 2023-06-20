import unittest

class TestMethods(unittest.TestCase):
    def test_assertion(self):
        self.assertEqual('FOO','FOO')

if __name__=='__main__':
    print ("starting ...")
    unittest.main()
    print ("finished ....")
            