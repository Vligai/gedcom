from datetime import date, timedelta

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

def deceased(d):
    """US29"""
    deadpeople={}
    for key in d:
        deat=d[key]["DEAT"]
        if deat !={}: #dead
            deadpeople[key]=key
    return deadpeople

def living_married(d,d2):
    """US30"""
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