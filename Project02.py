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
                if PRINT_USER_STORY_TESTS:
                    if icurr in d:
                        print "US22:\tIndividual ID duplicate:{0}".format(icurr)
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
                    "DIV":{}
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
                if PRINT_USER_STORY_TESTS:
                    if fcurr in d2:
                        print "US22:\tIndividual ID duplicate:{0}".format(fcurr)
                d2[fcurr]={
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
            elif len(y)>1 and y[1].strip()=="MARR":
                marr=1
            elif len(y)>1 and y[1].strip()=="DIV":
                div=1
    return d, d2


def main(filename, printUserStories, printDescriptions):
    PRINT_USER_STORY_TESTS = printUserStories
    PRINT_PERSON_OR_FAMILY_DESCRIPTION = printDescriptions

    d, d2 = parseFile(filename, PRINT_USER_STORY_TESTS)

    if True: #to match indentation for easy formatting
        print "+-------------------------------------------------+"
        print "| Running...                                      |"
    if PRINT_USER_STORY_TESTS or PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print "| Looking at individual and family information    |"
    if PRINT_USER_STORY_TESTS:
        print "|   - Printing information on user story tests    |"
    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        print "|   - Printing individual and family descriptions |"
    if True: #same as above, for formatting
        print "+-------------------------------------------------+"


    """
    interate over individuals
    """
    for key in sorted(d, key=lambda x: int(x[1:])):
        name=d[key]["NAME"]
        birt=d[key]["BIRT"]
        deat=d[key]["DEAT"]
        if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
            print "The lovely person with the key %s has the wonderful name %s"%(key,name)
        if PRINT_USER_STORY_TESTS:
            if not birth_before_death(birt,deat):
                print "US03:\tBirth is not before death: ",name
            if not less_than_150(birt,deat):
                print "US07:\tGreater than 150 years old: ",name

    """
    interate over families
    """
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
            print "The lovely marriage with the key %s happened betwwen the handsome %s and the beautiful %s"%(key2,hname,wname)
        if PRINT_USER_STORY_TESTS:
            if not birth_before_marriage(hbirt,marr):
                print "US02:\tHusbands Birth with key %s has name %s is not before marriage "%(husb, hname)
            if not birth_before_marriage(wbirt,marr):
                print "US02:\tWifes Birth with key %s has name %s is not before marriage "%(wife, wname)
            if not marriage_before_divorce(marr,div):
                print "US04:\tMarriage with key %s of %s and %s is not before divorce "%(key2, hname, wname)
            if not marriage_before_death(marr,hdeat):
                print "US05:\tMarriage with key %s of %s and %s is not before death of husband %s: "%(key2, hname, wname, hname)
            if not marriage_before_death(marr,wdeat):
                print "US05:\tMarriage with key %s of %s and %s is not before death of wife %s "%(key2, hname, wname, wname)
            if not div_before_death(div,hdeat):
                print "US06:\tDivorce with key %s of %s and %s is not before deathof husband %s "%(key2, hname, wname, hname)
            if not div_before_death(div,wdeat):
                print "US06:\tDivorce with key %s of %s and %s is not before death of wife %s "%(key2, hname, wname, wname)
            if not correct_genders(d[husb], d[wife]):
                print "US21:\tMarriage gender error: husband {0} is not male or wife {1} is not female".format(hname, wname)

        for c in chil:
            name=d[c]["NAME"]
            birth=d[c]["BIRT"]
            if PRINT_USER_STORY_TESTS:
                if birth_before_marriage_of_parents(birth,marr):
                    print "US08:\tBirth of %s is before marriage of %s,%s "%(name,hname,wname)
                if birth_before_death_of_parents(birth,hdeat):
                    print "US09:\tBirth of %s is before death of Dad: %s"%(name,hname)
                if birth_before_death_of_parents(birth,wdeat):
                    print "US09:\tBirth of %s is before death of Mom: %s"%(name,wname)

if __name__ == '__main__':
    print_user_stories = True
    print_descriptions = False
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename, print_user_stories, print_descriptions)
    else:
        print ("Usage: python project02.py <filename>")
