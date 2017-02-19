import unittest
from Project02 import less_than_150

class classname(unittest.TestCase):
    def test1(self):
        birth = {"year":1950, "month":3, "day":23}
        self.assertTrue(less_than_150(birth,{}))
    def test2(self):
        birth = {"year":1850, "month":3, "day":23}
        self.assertFalse(less_than_150(birth,{}))
    def test3(self):
        birth = {"year":2010, "month":4, "day":3}
        self.assertTrue(less_than_150(birth,{}))
    def test4(self):
        birth = {"year":1950, "month":3, "day":23}
        death = {"year":1990, "month":3, "day":23}
        self.assertTrue(less_than_150(birth,death))
    def test5(self):
        birth = {"year":1850, "month":3, "day":23}
        death = {"year":2030, "month":3, "day":23}
        self.assertFalse(less_than_150(birth,death))

if __name__ == '__main__':
    unittest.main()
