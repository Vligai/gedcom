#Mark Mirthcouk Project 2
import sys, time
from collections import defaultdict
from datetime import date, timedelta
tags=["INDI","NAME","SEX","BIRT","DEAT","FAMC","FAMS","FAM","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]
d = {} # for individuals
d2 = {} # for families

months ={"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

def birth_before_death(birth,death):
	"""
	User Story US03: True means everything is ok and Birthday is before Death day
	"""
	if death == {}:
        	return True #nothing to worry about
    	if birth == {}:
        	return False #you need to have a birthday
	if birth["year"]>death["year"]:
		return False
	elif birth["year"]<death["year"]:
		return True
	elif months[birth["month"]]>months[death["month"]]:
		return False
	elif months[birth["month"]]<months[death["month"]]:
		return True
	elif birth["day"]>death["day"]:
		return False
	return True

def birth_before_marriage(birth,marr):
	"""
	User Story US02: True means everything is ok and Birthday is before marriage day
	"""
	if marr == {}:
        	return True #nothing to worry about
    	if birth == {}:
        	return False #you need to have a birthday
	if birth["year"]>marr["year"]:
		return False
	elif birth["year"]<marr["year"]:
		return True
	elif months[birth["month"]]>months[marr["month"]]:
		return False
	elif months[birth["month"]]<months[marr["month"]]:
		return True
	elif birth["day"]>marr["day"]:
		return False
	return True

def less_than_150(birth, death):
    """user story 07"""
    birth = date(birth["year"], birth["month"], birth["day"])
    end = date.today() if death == {} else date(death["year"], death["month"], death["day"])
    return (end - birth) < 150*timedelta(days=365)

def div_before_death(div, death):
    """user story 06"""
    if div == {}:
        return False
    if death == {}:
        return True
    return firstDateIsEarlier(div, death)

def firstDateIsEarlier(d1, d2):
    """
    Given dates in the form {"year":1970, "month": 01, "day": 01},
    return True if the first date is the earlier of the two
    """
    if len(str(d1["month"])) > 2 and str(d1["month"]) in months.keys():
        #replace GED month code with number
        d1["month"] = months[d1["month"]]
    if len(str(d2["month"])) > 2 and str(d2["month"]) in months.keys():
        #replace GED month code with number
        d2["month"] = months[d2["month"]]
    date1 = date(d1["year"], d1["month"], d1["day"])
    date2 = date(d2["year"], d2["month"], d2["day"])
    return date1 < date2

def marriage_before_divorce(mar, div):
    """
    user story 04
    Marriage should occur before divorce of spouses,
    and divorce can only occur after marriage
    """
    if div == {}:
        return True #nothing to worry about
    if mar == {}:
        return False #divorce without marriage doesn't work
    return firstDateIsEarlier(mar, div)

def marriage_before_death(mar, death):
    """
    user story 05
    Marriage should occur before death of either spouse
    """
    if mar == {}:
        return True #nothing to worry about
    if death == {}:
        return True #marriage without death is fine
    return firstDateIsEarlier(mar, death)

def birth_before_marriage_of_parents(birth, marriage_of_parents):
        """user story 08 - if born before marriage return True else return False"""
        '''check if birth date is given, if not return False'''
        if birth == {}:
                return False
        else:
                birth = date(birth["year"], birth["month"], birth["day"])
        '''check if marriage date(of parents) is given, if not return True'''
        if marriage_of_parents == {}:
                return True
        else:
                marriage_of_parents = date(marriage_of_parents["year"], marriage_of_parents["month"], marriage_of_parents["day"])
        if birth < marriage_of_parents:
                return True
        else:
                return False

def birth_before_death_of_parents(birth, death_of_parents):
        """user story 09 - if born before death of parents return true else return false"""
        '''check if birth date is given, if not return False'''
        if birth == {}:
                return False
        else:
                birth = date(birth["year"], birth["month"], birth["day"])
        '''check if death date(of parents) is given, if not return True'''
        if death_of_parents == {}:
                return True
        else:
                death_of_parents = date(death_of_parents["year"], death_of_parents["month"], death_of_parents["day"])
        if birth < death_of_parents:
                return True
        else:
                return False

def main(filename):
	with open(filename, 'r') as f:
		icurr=''
		birt=0
		deat=0
		marr=0
		div=0
		for line in f:
			if "HUSB" not in line and "WIFE" not in line and "CHIL" not in line:
				fam=0
			#print (line.strip())
			y = line.strip().split(" ")

			#print (y[0].strip())

			#if y[1].strip() in tags:
			#    print (y[1].strip())
			#elif len(y)>2 and y[2].strip() in tags:
			#	print (y[2].strip())
			#else:
			#	print ("Invalid tag")

			if len(y)>2 and y[2].strip()=="INDI":
				icurr=y[1].strip()
				d[icurr]={}
			elif len(y)>3 and y[1].strip()=="NAME":
				a=y[2].strip()+" "+ y[3].strip()
				d[icurr]["NAME"]=a
			elif len(y)>2 and y[1].strip()=="SEX":
				a=y[2].strip()
				d[icurr]["SEX"]=a
			elif len(y)>2 and y[1].strip()=="GIVN":
				a=y[2].strip()
				d[icurr]["GIVN"]=a
			elif len(y)>2 and y[1].strip()=="SURN":
				a=y[2].strip()
				d[icurr]["SURN"]=a
			elif len(y)>=2 and y[1].strip()=="BIRT":
				birt=1
			elif len(y)>2 and y[1].strip()=="DEAT":
				deat=1
			elif len(y)>4 and y[1].strip()=="DATE":
				day=y[2].strip()
				month=y[3].strip()
				year=y[4].strip()
				if birt==1:
					a={"day":day, "month":month,"year":year}
					d[icurr]["BIRT"]=a
					birt=0
				if deat==1:
					a={"day":day, "month":month,"year":year}
					d[icurr]["DEAT"]=a
					deat=0
				if marr==1:
					a={"day":day, "month":month,"year":year}
					d2[fcurr]["MARR"]=a
					marr=0
				if div==1:
					a={"day":day, "month":month,"year":year}
					d2[fcurr]["DIV"]=a
					div=0
			elif len(y)>2 and y[1].strip()=="FAMC":
				a=y[2].strip()
				d[icurr]["FAMC"]=a
			elif len(y)>2 and y[1].strip()=="FAMS":
				a=y[2].strip()
				d[icurr]["FAMS"]=a
			elif len(y)>2 and y[2].strip()=="FAM":
				fcurr=y[1].strip()
				d2[fcurr]={}
				fam=1
			elif len(y)>2 and fam==1:
				tag=y[1].strip()
				a=y[2].strip()
				d2[fcurr][tag]=a
			elif len(y)>1 and y[1].strip()=="MARR":
				marr=1
			elif len(y)>1 and y[1].strip()=="DIV":
				div=1
		print ("Printing individual ID's and name!")
		for key in sorted(d, key=lambda x: int(x[1:])):
			name=d[key]["NAME"]
			print (key,name)
		print ("Printing family ID's, husband name, and wife name!")
		for key2 in sorted(d2, key=lambda x: int(x[1:])):
			husb=d2[key2]["HUSB"]
			wife=d2[key2]["WIFE"]
			hname=d[husb]["NAME"]
			wname=d[wife]["NAME"]
			print (key2,hname," , ",wname)
if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename)
    else:
        print ("Usage: python project02.py <filename>")
