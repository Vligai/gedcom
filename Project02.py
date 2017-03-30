#Mark Mirthcouk Project 2
import sys, time, copy
from collections import defaultdict
from datetime import date, timedelta
tags=["INDI","NAME","SEX","BIRT","DEAT","FAMC","FAMS","FAM","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]
d = {} # for individuals
d2 = {} # for families

months ={"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

ERR_OBJ = {}
def addError(user_story, message):
    if not user_story in ERR_OBJ:
        ERR_OBJ[user_story] = []
    ERR_OBJ[user_story].append(message)

def printErrors(print_us_nums=True):
    if len(ERR_OBJ) == 0:
        print "No errors found"
        return
    print "\n+----------------------+"
    print "| Errors found in file |"
    print "+----------------------+"
    for user_story, msgLst in sorted(ERR_OBJ.iteritems()):
        #msgLst = ERR_OBJ[user_story]
        if print_us_nums:
            print "{0} errors:".format(user_story)
        for msg in msgLst:
            indent = ''
            if print_us_nums:
                indent = "-"
            print "{0:2}{1}".format(indent, msg)

def birth_before_death(birth,death):
    """
    User Story US03: True means everything is ok and Birthday is before Death day
    """
    if death == {}:
        return True
    if birth == {}:
        return False
    return firstDateIsEarlier(birth, death)

def birth_before_marriage(birth,marr):
    """
    User Story US02: True means everything is ok and Birthday is before marriage day
    """
    if marr == {}:
        return True
    if birth == {}:
        return False
    return firstDateIsEarlier(birth, marr)

def marriage_after_14(birth, marriage):
    """user story 10"""
    if len(str(birth["month"]))>2:
        birth["month"]=months[birth["month"]]
    birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    if marriage == {}:
        return False
    else:
        end = date(int(marriage["year"]), marriage["month"], int(marriage["day"]))
    return (end - birth) >= 14*timedelta(days=365)

def date_before_today(d):
    """user story 01"""
    if d == {}:
        return True
    today = date.today()
    today2={"day":today.day, "month":today.month,"year":today.year}
    return firstDateIsEarlier(d,today2)

def less_than_150(birth, death):
    """user story 07"""
    if len(str(birth["month"]))>2:
        birth["month"]=months[birth["month"]]
    birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    if death == {}:
        end = date.today()
    else:
        end = date(int(death["year"]), death["month"], int(death["day"]))
    return (end - birth) < 150*timedelta(days=365)

def div_before_death(div, death):
    """user story 06"""
    if death == {}:
        return True
    if div == {}:
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
    date1 = date(int(d1["year"]), d1["month"], int(d1["day"]))
    date2 = date(int(d2["year"]), d2["month"], int(d2["day"]))
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
    #print birth,marriage_of_parents
    if birth == {}:
        return False
    else:
        birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    '''check if marriage date(of parents) is given, if not return True'''
    if marriage_of_parents == {}:
        return True
    else:
        marriage_of_parents = date(int(marriage_of_parents["year"]), marriage_of_parents["month"], int(marriage_of_parents["day"]))
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
        birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    '''check if death date(of parents) is given, if not return True'''
    if death_of_parents == {}:
        return True
    else:
        death_of_parents = date(int(death_of_parents["year"]), death_of_parents["month"], int(death_of_parents["day"]))
    if birth < death_of_parents:
        return True
    else:
        return False

def correct_genders(husb, wife):
    """
    User story 21
    Check that husband is male and wife is female
    """
    if husb['SEX'] == 'M' and wife['SEX'] == 'F':
        return True
    return False

def unique_ids(d):
    """
    User story 22
    Check if a dictionary has all unique IDs

    Note: Python dictionaries don't allow duplicates, so the check and error
          message happens in the main function when parsing the file
    """
    return True

def no_bigamy(marr1,marr2,div1,div2):
    """
    User Story 11
    Marriage should not occur during marriage to another spouse
    """

    if firstDateIsEarlier(marr1,marr2):
    	if div1 == {}:
        	return False
    	if firstDateIsEarlier(marr2,div1):
        	return False

    if firstDateIsEarlier(marr2,marr1):
        if div2 == {}:
        	return False
    	if firstDateIsEarlier(marr1,div2):
        	return False

    return True

def sibling_spacing(birth_sib1, birth_sib2):
    """
    User Story 13
    Birth dates of siblings should be more than 8 months apart or less than 2
    days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the
    following calendar day)
    """

    if firstDateIsEarlier(birth_sib2,birth_sib1):
    # Makes the birth_sib1 first
        temp = birth_sib1
        birth_sib1 = birth_sib2
        birth_sib2 = temp

    if birth_sib1 == {}:
        return False
    else:
        birth_sib1 = date(int(birth_sib1["year"]), birth_sib1["month"], int(birth_sib1["day"]))
    if birth_sib2 == {}:
        return True
    else:
        birth_sib2 = date(int(birth_sib2["year"]), birth_sib2["month"], int(birth_sib2["day"]))

    if (birth_sib2-birth_sib1) < 8*timedelta(days=30) and birth_sib2-birth_sib1 > 2*timedelta(days=1):
        return False
    return True

def male_last_names(ind, fam):
    """User Story 16"""
    name = ind[fam["HUSB"]]["SURN"]
    for child in fam["CHIL"]:
        if ind[child]["SURN"] != name and ind[child]["SEX"] == "M":
            return False
    return True

def no_incest(ind, fam, start):
    sex = "HUSB" if ind[start]["SEX"] == "M" else "WIFE"
    other = "WIFE" if sex == "HUSB" else "HUSB"
    childsFams = []
    marr = {}
    descendants = []
    for famid in ind[start]["FAMIDS"]:
        if sex == "HUSB":
            marr[(fam[famid][sex], fam[famid][other])] = ''
        else:
            marr[(fam[famid][other], fam[famid][sex])] = ''
        descendants += fam[famid]["CHIL"]
    for id in descendants:
        for famid in ind[id]["FAMIDS"]:
            descendants += fam[famid]["CHIL"]
            if (fam[famid][sex], fam[famid][other]) in marr or (fam[famid][other], fam[famid][sex]) in marr:
                return False
    return True

def living_married(d,d2):
	livingmarriedpeople={}
	for key2 in d2:
		husb=d2[key2]["HUSB"]
	        wife=d2[key2]["WIFE"]
	        hdeat=d[husb]["DEAT"]
	        wdeat=d[wife]["DEAT"]
        	div=d2[key2]["DIV"]
		if div == {}: #not divorced
			if hdeat=={} and wdeat=={}: #both husbnad and wife are alive
				livingmarriedpeople[husb]=husb
				livingmarriedpeople[wife]=wife
	return livingmarriedpeople

def parseFile(filename, PRINT_USER_STORY_TESTS):
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
                if icurr in d:
                    msg = "Individual ID duplicate:{0}".format(icurr)
                    addError('US22', msg)
                    icurr = icurr + "500"
                d[icurr]={
                    "MARR":{},
                    "NAME":{},
                    "SEX":{},
                    "GIVN":{},
                    "SURN":{},
                    "BIRT":{},
                    "DEAT":{},
                    "FAMC":{},
                    "FAMS":{},
                    "DIV":{},
                    "FAMIDS":[] #for if they have marry multiple times
                    }
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
                if not isinstance(month, int):
                    month = months[month]
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
                if fcurr in d2:
                    msg = "Family ID duplicate:{0}".format(fcurr)
                    addError('US22', msg)
                    fcurr = fcurr + "500"
                d2[fcurr]={
                    "MARR":{},
                    # "NAME":{},
                    # "SEX":{},
                    # "GIVN":{},
                    # "SURN":{},
                    # "BIRT":{},
                    # "DEAT":{},
                    # "FAMC":{},
                    # "FAMS":{},
                    "DIV":{},
                    "CHIL":[]
                    }
                fam=1
            elif len(y)>2 and fam==1:
                tag=y[1].strip()
                a=y[2].strip()
                if tag =="CHIL":
                    d2[fcurr][tag].append(a)
                else:
                    d2[fcurr][tag]=a
                    d[a]["FAMIDS"].append(fcurr)
            elif len(y)>1 and y[1].strip()=="MARR":
                marr=1
            elif len(y)>1 and y[1].strip()=="DIV":
                div=1
    return d, d2



def main(filename, printUserStories, printDescriptions):
    PRINT_USER_STORY_TESTS = printUserStories
    PRINT_PERSON_OR_FAMILY_DESCRIPTION = printDescriptions
    ERR_LIST = {}

    print "+------------+"
    print "| Running... |"
    print "+------------+"

    d, d2 = parseFile(filename, PRINT_USER_STORY_TESTS)

    """
    interate over individuals
    """
    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print "\nIndividuals:"
        keyWidth = 6
        nameWidth = 25
        ind_table_hr = "+-{0:-<{kw}}-+-{1:-<{nw}}-+".format('', '', kw=keyWidth, nw=nameWidth) #horizontal table line
        print ind_table_hr
        print "| {0:{kw}} | {1:{nw}} |".format("Key", "Name", kw=keyWidth, nw=nameWidth)
        print ind_table_hr
    for key in sorted(d, key=lambda x: int(x[1:])):
        name=d[key]["NAME"]
        birt=d[key]["BIRT"]
        deat=d[key]["DEAT"]
        if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
            print "| {0:{kw}} | {1:{nw}} |".format(key, name, kw=keyWidth, nw=nameWidth)
        if not birth_before_death(birt,deat):
            msg = "Birth is not before death:{0}".format(name)
            addError("US03", msg)
        if not less_than_150(birt,deat):
            msg = "Greater than 150 years old: {0}".format(name)
            addError('US07', msg)
        if not date_before_today(birt):
            msg = "Date of {0}'s birth {1} is after today".format(name, birt)
            addError("US01", msg)
        if not date_before_today(deat):
            msg = "Date of {0}'s death {1} is after today".format(name,deat)
            addError("US01", msg)
    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print ind_table_hr

    """
    interate over families
    """
    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print "\nFamilies:"
        keyWidth = 6
        nameWidth = 25
        fam_table_hr = "+-{0:-<{kw}}-+-{1:-<{nw}}-+-{1:-<{nw}}-+".format('', '', kw=keyWidth, nw=nameWidth) #horizontal table line
        print fam_table_hr
        print "| {0:{kw}} | {1:{nw}} | {2:{nw}} |".format("Key", "Husband", "Wife", kw=keyWidth, nw=nameWidth)
        print fam_table_hr
    for key2 in sorted(d2, key=lambda x: int(x[1:])):
        husb=d2[key2]["HUSB"]
        wife=d2[key2]["WIFE"]
        hname=d[husb]["NAME"]
        wname=d[wife]["NAME"]
        hbirt=d[husb]["BIRT"]
        wbirt=d[wife]["BIRT"]
        hdeat=d[husb]["DEAT"]
        wdeat=d[wife]["DEAT"]
        marr=d2[key2]["MARR"]
        div=d2[key2]["DIV"]
        chil=d2[key2]["CHIL"]
        if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
            print "| {0:{kw}} | {1:{nw}} | {2:{nw}} |".format(key2, hname, wname, kw=keyWidth, nw=nameWidth)
        if not birth_before_marriage(hbirt,marr):
            msg = "Husbands Birth with key {0} has name {1} is not before marriage ".format(husb, hname)
            addError("US02", msg)
        if not birth_before_marriage(wbirt,marr):
            msg = "Wifes Birth with key {0} has name {1} is not before marriage ".format(wife, wname)
            addError("US02", msg)
        if not marriage_before_divorce(marr,div):
            msg = "Marriage with key {0} of {1} and {2} is not before divorce ".format(key2, hname, wname)
            addError("US04", msg)
        if not marriage_before_death(marr,hdeat):
            msg = "Marriage with key {0} of {1} and {2} is not before death of husband {3}: ".format(key2, hname, wname, hname)
            addError("US05", msg)
        if not marriage_before_death(marr,wdeat):
            msg = "Marriage with key {0} of {1} and {2} is not before death of wife {3} ".format(key2, hname, wname, wname)
            addError("US05", msg)
        if not div_before_death(div,hdeat):
            msg = "Divorce with key {0} of {1} and {2} is not before deathof husband {3} ".format(key2, hname, wname, hname)
            addError("US06", msg)
        if not div_before_death(div,wdeat):
            msg = "Divorce with key {0} of {1} and {2} is not before death of wife {3} ".format(key2, hname, wname, wname)
            addError("US06", msg)
        if not correct_genders(d[husb], d[wife]):
            msg = "Husband {0} is not male or wife {1} is not female".format(hname, wname)
            addError("US21", msg)
        if not marriage_after_14(hbirt,marr):
            msg = "Husbands Birth with key {0} has name {1} is not older than 14".format(husb, hname)
            addError("US10", msg)
        if not marriage_after_14(wbirt,marr):
            msg = "Wifes Birth with key {0} has name {1} is not older than 14".format(wife, wname)
            addError("US10", msg)
        if not date_before_today(marr):
            msg = "Date of {0} and {1} marriage {2} is after today".format(hname,wname,marr)
            addError("US01", msg)
        if not date_before_today(div):
            msg = "Date of {0} and {1} divorce {2} is after today".format(hname,wname,div)
            addError("US01", msg)
        if not male_last_names(d,d2[key2]):
            msg = "Family with key {0} doesn't have all male last names".format(key2)
            addError("US16", msg)

        for c in chil:
            name=d[c]["NAME"]
            birth=d[c]["BIRT"]
            if birth_before_marriage_of_parents(birth,marr):
                msg = "Birth of {0} is before marriage of {1},{2} ".format(name,hname,wname)
                addError('US08', msg)
            if birth_before_death_of_parents(birth,hdeat):
                msg = "Birth of {0} is before death of Dad: {1}".format(name,hname)
                addError('US09', msg)
            if birth_before_death_of_parents(birth,wdeat):
                msg = "Birth of {0} is before death of Mom: {1}".format(name,wname)
                addError('US09', msg)

        for c in chil:
            boolb=0
            for c2 in chil:
                if c==c2:
                    boolb=1
                elif boolb==1:
                    birth1=d[c]["BIRT"]
                    birth2=d[c2]["BIRT"]
                    if not sibling_spacing(birth1,birth2):
                        msg = "Sibling spacing between {0} and {1} is too small or too large".format(c,c2)
                        addError('US13', msg)

    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print fam_table_hr


    d3=sorted(d2, key=lambda x: int(x[1:]))
    for key2 in d3:
        boolb=0
    	for key3 in d3:
        	if key2==key3:
            		boolb=1
        	elif boolb==1:
            		husb1=d2[key2]["HUSB"]
            		wife1=d2[key2]["WIFE"]
		        hname1=d[husb1]["NAME"]
            		wname1=d[wife1]["NAME"]
            		marr1=d2[key2]["MARR"]
           		div1=d2[key2]["DIV"]

            		husb2=d2[key3]["HUSB"]
            		wife2=d2[key3]["WIFE"]
            		hname2=d[husb2]["NAME"]
            		wname2=d[wife2]["NAME"]
            		marr2=d2[key3]["MARR"]
            		div2=d2[key3]["DIV"]

            		if husb1==husb2 or wife1==wife2:
                		if not no_bigamy(marr1,marr2,div1,div2):
                    			msg = "Marriage with key {} of {} and {} overlaps with Marriage with key {} of {} and {}".format(key2,husb1,wife1,key3,wife2,husb2)
                    			addError('US11', msg)

    lm=living_married(d,d2)
    lm2=sorted(lm, key=lambda x: int(x[1:]))
    for key in lm2:
	name=d[key]["NAME"]
	msg = "Person with key {} has the name {} and is still alive and married".format(key,name)
	addError('US30', msg)

    if PRINT_USER_STORY_TESTS:
        printErrors()
    living_married(d,d2)#TAKE OUT

if __name__ == '__main__':
    print_user_stories = True
    print_descriptions = True
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename, print_user_stories, print_descriptions)
    else:
        print ("Usage: python project02.py <filename>")
