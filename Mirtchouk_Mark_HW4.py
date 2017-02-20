import unittest
from Project02 import *

class TestStringMethods(unittest.TestCase):

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

    def test_birth_before_death4(self):
        self.assertEqual(birth_before_death(self.person6["BIRT"],self.person6["DEAT"]),False)



if __name__ == '__main__':
	main("Mirtchouk_Mark_Project02.ged")
	i=0
	for key in d:		
		if 'DEAT' in d[key]:
			if i==0:
				TestStringMethods.person0=d[key]
			if i==1:
				TestStringMethods.person1=d[key]
			i+=1
	TestStringMethods.person2={}
	TestStringMethods.person3={}
	TestStringMethods.person4={}
	TestStringMethods.person5={}
	TestStringMethods.person6={}
	for key in TestStringMethods.person0:
		TestStringMethods.person2[key]=TestStringMethods.person0[key]
		TestStringMethods.person3[key]=TestStringMethods.person0[key]
		TestStringMethods.person4[key]=TestStringMethods.person0[key]
		TestStringMethods.person5[key]=TestStringMethods.person0[key]
		TestStringMethods.person6[key]=TestStringMethods.person0[key]
	TestStringMethods.person2["BIRT"]={'year': '2013', 'day': '1', 'month': 'JUN'} 
	TestStringMethods.person3["BIRT"]={'year': '2015', 'day': '1', 'month': 'MAY'} 
	TestStringMethods.person4["BIRT"]={'year': '2015', 'day': '2', 'month': 'JUN'} 
	TestStringMethods.person5["BIRT"]={'year': '2099', 'day': '1', 'month': 'JUN'} 
	TestStringMethods.person6["BIRT"]={'year': '2017', 'day': '2', 'month': 'JUN'} 
	TestStringMethods.person6["DEAT"]={'year': '2017', 'day': '1', 'month': 'JUN'} 
	unittest.main()
