import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/'+'../..')
import seismograph

class FooTests(unittest.TestCase):
    def test_one(self):
        self.assertEqual('2 odd', '2 odd')

    def test_two(self):
        self.assertEqual('1', '1')

    def test_hello_world(self):
        self.assertEqual('2', '2')

if __name__ == '__main__':
    print("\n")
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(FooTests)
    # unittest.TextTestRunner(verbosity=2).run(suite)
