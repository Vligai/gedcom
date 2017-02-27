import unittest
from Project02 import *

class firstIsEarlierTests(unittest.TestCase):
    #equality and format comparisons
    # d_h = date high
    # d_l = date low
    d_l_leadZero = {"year":1900, "month":01, "day":02}
    d_l_noZero = {"year":1900, "month":1, "day":2}
    d_l_letter = {"year":1900, "month":"JAN", "day":2}
    d_h_leadZero = {"year":1900, "month":02, "day":02}
    d_h_noZero = {"year":1900, "month":2, "day":2}
    d_h_letter = {"year":1900, "month":"FEB", "day":2}
    def testFalseForEqual(self):
        self.assertEqual(firstDateIsEarlier(self.d_l_leadZero, self.d_l_noZero), False)
        self.assertEqual(firstDateIsEarlier(self.d_l_leadZero, self.d_l_letter), False)
        self.assertEqual(firstDateIsEarlier(self.d_l_noZero, self.d_l_letter), False)
        self.assertEqual(firstDateIsEarlier(self.d_l_noZero, self.d_l_leadZero), False)
        self.assertEqual(firstDateIsEarlier(self.d_l_letter, self.d_l_leadZero), False)
        self.assertEqual(firstDateIsEarlier(self.d_l_letter, self.d_l_noZero), False)
    def testCrossFormat(self):
        self.assertEqual(firstDateIsEarlier(self.d_l_leadZero, self.d_h_leadZero), True)
        self.assertEqual(firstDateIsEarlier(self.d_l_leadZero, self.d_h_noZero), True)
        self.assertEqual(firstDateIsEarlier(self.d_l_leadZero, self.d_h_letter), True)
        self.assertEqual(firstDateIsEarlier(self.d_h_leadZero, self.d_l_leadZero), False)
        self.assertEqual(firstDateIsEarlier(self.d_h_noZero, self.d_l_leadZero), False)
        self.assertEqual(firstDateIsEarlier(self.d_h_letter, self.d_l_leadZero), False)
    #date isolation comparisons
    d_base = {"year":1970, "month":4, "day":2}
    d_yearDown = {"year":1969, "month":4, "day":2}
    d_yearUp = {"year":1971, "month":4, "day":2}
    d_monthDown = {"year":1970, "month":3, "day":2}
    d_monthUp = {"year":1970, "month":5, "day":2}
    d_dayDown = {"year":1970, "month":4, "day":1}
    d_dayUp = {"year":1970, "month":4, "day":3}
    def testIsolateYear(self):
        self.assertEqual(firstDateIsEarlier(self.d_yearDown, self.d_base), True)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_yearDown), False)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_yearUp), True)
        self.assertEqual(firstDateIsEarlier(self.d_yearUp, self.d_base), False)
    def testIsolateMonth(self):
        self.assertEqual(firstDateIsEarlier(self.d_monthDown, self.d_base), True)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_monthDown), False)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_monthUp), True)
        self.assertEqual(firstDateIsEarlier(self.d_monthUp, self.d_base), False)
    def testIsolateDay(self):
        self.assertEqual(firstDateIsEarlier(self.d_dayDown, self.d_base), True)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_dayDown), False)
        self.assertEqual(firstDateIsEarlier(self.d_base, self.d_dayUp), True)
        self.assertEqual(firstDateIsEarlier(self.d_dayUp, self.d_base), False)
    def testNewYears(self):
        yearPrev = {"year":1999, "month":12, "day":31}
        yearNext = {"year":2000, "month":1, "day":1}
        self.assertEqual(firstDateIsEarlier(yearPrev, yearNext), True)
        self.assertEqual(firstDateIsEarlier(yearNext, yearPrev), False)

class UserStory02Tests(unittest.TestCase):

    def test_birth_before_death0(self):
        self.assertTrue(birth_before_death(self.person0["BIRT"],self.person0["DEAT"]))

    def test_birth_before_death1(self):
        self.assertTrue(birth_before_death(self.person1["BIRT"],self.person1["DEAT"]))

    def test_birth_before_death2(self):
        self.assertTrue(birth_before_death(self.person2["BIRT"],self.person2["DEAT"]))

    def test_birth_before_death3(self):
        self.assertTrue(birth_before_death(self.person3["BIRT"],self.person3["DEAT"]))

    def test_birth_before_death4(self):
        self.assertEqual(birth_before_death(self.person4["BIRT"],self.person1["DEAT"]),False)

    def test_birth_before_death5(self):
        self.assertEqual(birth_before_death(self.person5["BIRT"],self.person5["DEAT"]),False)

    def test_birth_before_death6(self):
        self.assertEqual(birth_before_death(self.person6["BIRT"],self.person6["DEAT"]),False)

    def test_birth_before_death6(self):
        self.assertTrue(birth_before_death({},{}))


class UserStory03Tests(unittest.TestCase):
    #note DEAT is just used as a date, and will ultimately be marriage dates
    def test_birth_before_death0(self):
        self.assertTrue(birth_before_marriage(self.person0["BIRT"],self.person0["DEAT"]))

    def test_birth_before_marriage1(self):
        self.assertTrue(birth_before_marriage(self.person1["BIRT"],self.person1["DEAT"]))

    def test_birth_before_marriage2(self):
        self.assertTrue(birth_before_marriage(self.person2["BIRT"],self.person2["DEAT"]))

    def test_birth_before_marriage3(self):
        self.assertTrue(birth_before_marriage(self.person3["BIRT"],self.person3["DEAT"]))

    def test_birth_before_marriage4(self):
        self.assertEqual(birth_before_marriage(self.person4["BIRT"],self.person1["DEAT"]),False)

    def test_birth_before_marriage5(self):
        self.assertEqual(birth_before_marriage(self.person5["BIRT"],self.person5["DEAT"]),False)

    def test_birth_before_marriage6(self):
        self.assertEqual(birth_before_marriage(self.person6["BIRT"],self.person6["DEAT"]),False)

    def test_birth_before_marriage6(self):
        self.assertTrue(birth_before_marriage({},{}))


class UserStory04Tests(unittest.TestCase):
    def test1(self):
        #no marriage or divorce is fine
        self.assertTrue(marriage_before_divorce({},{}))
    def test2(self):
        #marriage without divorce is fine
        m = {"year":2000, "month":1, "day":1}
        self.assertTrue(marriage_before_divorce(m,{}))
    def test3(self):
        #divorce without marriage is NOT fine
        d = {"year":2000, "month":"JAN", "day":1}
        self.assertFalse(marriage_before_divorce({},d))
    def test4(self):
        #both events, with marriage first is fine
        m = {"year":2000, "month":1, "day":1}
        d = {"year":2010, "month":"FEB", "day":1}
        self.assertTrue(marriage_before_divorce(m,d))
    def test5(self):
        #both events, with divorce first is NOT fine
        d = {"year":2000, "month":1, "day":1}
        m = {"year":2010, "month":1, "day":1}
        self.assertFalse(marriage_before_divorce(m,d))

class UserStory05Tests(unittest.TestCase):
    def test1(self):
        #no marriage or death is fine
        self.assertTrue(marriage_before_death({},{}))
    def test2(self):
        #marriage without death is fine
        m = {"year":2000, "month":1, "day":1}
        self.assertTrue(marriage_before_death(m,{}))
    def test3(self):
        #death without marriage is fine
        d = {"year":2000, "month":1, "day":1}
        self.assertTrue(marriage_before_death({},d))
    def test4(self):
        #both events, with marriage first is fine
        m = {"year":2000, "month":1, "day":1}
        d = {"year":2010, "month":1, "day":1}
        self.assertTrue(marriage_before_death(m,d))
    def test5(self):
        #both events, with death first is NOT fine
        d = {"year":2000, "month":1, "day":1}
        m = {"year":2010, "month":1, "day":1}
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
	main("Mirtchouk_Mark_Project02.ged")
        i=0
        for key in d:
                if 'DEAT' in d[key]:
                        if i==0:
                                UserStory02Tests.person0=d[key]
                                UserStory03Tests.person0=d[key]
                        if i==1:
				UserStory02Tests.person1=d[key]
				UserStory03Tests.person1=d[key]
                        i+=1
        UserStory02Tests.person2={}
        UserStory02Tests.person3={}
        UserStory02Tests.person4={}
        UserStory02Tests.person5={}
        UserStory02Tests.person6={}
        for key in UserStory02Tests.person0:
                UserStory02Tests.person2[key]=UserStory02Tests.person0[key]
                UserStory02Tests.person3[key]=UserStory02Tests.person0[key]
                UserStory02Tests.person4[key]=UserStory02Tests.person0[key]
                UserStory02Tests.person5[key]=UserStory02Tests.person0[key]
                UserStory02Tests.person6[key]=UserStory02Tests.person0[key]
        UserStory02Tests.person2["BIRT"]={'year': '2013', 'day': '1', 'month': 'JUN'}
        UserStory02Tests.person3["BIRT"]={'year': '2015', 'day': '1', 'month': 'MAY'}
        UserStory02Tests.person4["BIRT"]={'year': '2015', 'day': '2', 'month': 'JUN'}
        UserStory02Tests.person5["BIRT"]={'year': '2099', 'day': '1', 'month': 'JUN'}
        UserStory02Tests.person6["BIRT"]={'year': '2017', 'day': '2', 'month': 'JUN'}
        UserStory02Tests.person6["DEAT"]={'year': '2017', 'day': '1', 'month': 'JUN'}

        UserStory03Tests.person2={}
        UserStory03Tests.person3={}
        UserStory03Tests.person4={}
        UserStory03Tests.person5={}
        UserStory03Tests.person6={}
        for key in UserStory03Tests.person0:
                UserStory03Tests.person2[key]=UserStory02Tests.person0[key]
                UserStory03Tests.person3[key]=UserStory02Tests.person0[key]
                UserStory03Tests.person4[key]=UserStory02Tests.person0[key]
                UserStory03Tests.person5[key]=UserStory02Tests.person0[key]
                UserStory03Tests.person6[key]=UserStory02Tests.person0[key]
        UserStory03Tests.person2["BIRT"]={'year': '2013', 'day': '1', 'month': 'JUN'}
        UserStory03Tests.person3["BIRT"]={'year': '2015', 'day': '1', 'month': 'MAY'}
        UserStory03Tests.person4["BIRT"]={'year': '2015', 'day': '2', 'month': 'JUN'}
        UserStory03Tests.person5["BIRT"]={'year': '2099', 'day': '1', 'month': 'JUN'}
        UserStory03Tests.person6["BIRT"]={'year': '2017', 'day': '2', 'month': 'JUN'}
        UserStory03Tests.person6["DEAT"]={'year': '2017', 'day': '1', 'month': 'JUN'}
	unittest.main()
