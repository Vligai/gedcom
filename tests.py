import unittest
from Project02 import *

class UserStory04Tests(unittest.TestCase):
    def test1(self):
        #no marriage or divorce is fine
        self.assertTrue(marriage_before_divorce({},{}))
    def test2(self):
        #marriage without divorce is fine
        m = {"year":2000, "month":01, "day":01}
        self.assertTrue(marriage_before_divorce(m,{}))
    def test3(self):
        #divorce without marriage is NOT fine
        d = {"year":2000, "month":01, "day":01}
        self.assertFalse(marriage_before_divorce({},d))
    def test4(self):
        #both events, with marriage first is fine
        m = {"year":2000, "month":01, "day":01}
        d = {"year":2010, "month":01, "day":01}
        self.assertTrue(marriage_before_divorce(m,d))
    def test5(self):
        #both events, with divorce first is NOT fine
        d = {"year":2000, "month":01, "day":01}
        m = {"year":2010, "month":01, "day":01}
        self.assertFalse(marriage_before_divorce(m,d))

class UserStory05Tests(unittest.TestCase):
    def test1(self):
        #no marriage or death is fine
        self.assertTrue(marriage_before_death({},{}))
    def test2(self):
        #marriage without death is fine
        m = {"year":2000, "month":01, "day":01}
        self.assertTrue(marriage_before_death(m,{}))
    def test3(self):
        #death without marriage is fine
        d = {"year":2000, "month":01, "day":01}
        self.assertTrue(marriage_before_death({},d))
    def test4(self):
        #both events, with marriage first is fine
        m = {"year":2000, "month":01, "day":01}
        d = {"year":2010, "month":01, "day":01}
        self.assertTrue(marriage_before_death(m,d))
    def test5(self):
        #both events, with death first is NOT fine
        d = {"year":2000, "month":01, "day":01}
        m = {"year":2010, "month":01, "day":01}
        self.assertFalse(marriage_before_death(m,d))

class UserStory07Tests(unittest.TestCase):
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
        
class UserStory08Tests(unittest.TestCase):
    def test1(self): #person born after parents married
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":1999, "month":5, "day":20}
        self.assertFalse(birth_before_marriage_of_parents(birth, marriage))
    def test2(self): #not married, so the person is born before marriage of parents
        birth = {"year":2001, "month":11, "day":20}
        marriage = {}
        self.assertTrue(birth_before_marriage_of_parents(birth, marriage))
    def test3(self): #person born before parents married
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":2002, "month":5, "day":20}
        self.assertTrue(birth_before_marriage_of_parents(birth, marriage))
    def test4(self): #person born before parents married
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":2001, "month":12, "day":21}
        self.assertEqual(birth_before_marriage_of_parents(birth, marriage), True)
    def test5(self): #no birth date given
        birth = {}
        marriage = {"year":2001, "month":12, "day":21}
        self.assertEqual(birth_before_marriage_of_parents(birth, marriage), False)


class story09test(unittest.TestCase):
    def test1(self): #person born after parents died
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":1999, "month":5, "day":20}
        self.assertFalse(birth_before_death_of_parents(birth, marriage))
    def test2(self): #not dead, so the person is born before death of parents
        birth = {"year":2001, "month":11, "day":20}
        marriage = {}
        self.assertTrue(birth_before_death_of_parents(birth, marriage))
    def test3(self): #person born before parents death
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":2002, "month":5, "day":20}
        self.assertTrue(birth_before_death_of_parents(birth, marriage))
    def test4(self): #person born before parents death
        birth = {"year":2001, "month":11, "day":20}
        marriage = {"year":2001, "month":12, "day":21}
        self.assertEqual(birth_before_death_of_parents(birth, marriage), True)
    def test5(self): #no birth date given
        birth = {}
        marriage = {"year":2001, "month":12, "day":21}
        self.assertEqual(birth_before_death_of_parents(birth, marriage), False)
        
if __name__ == '__main__':
    unittest.main()
