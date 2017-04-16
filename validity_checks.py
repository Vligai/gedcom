from datetime import date, timedelta

import copy

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
    """US17"""
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
    """
    US29: Returns all people that are dead (DEAT date not empty)
    """
    deadpeople={}
    for key in d:
        deat=d[key]["DEAT"]
        if deat !={}: #dead
            deadpeople[key]=key
    return deadpeople

def living_married(d,d2):
    """
    US30: Returns all people that are not divorced and both their husband/wife and themselves are alive
    """
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

def aunts_uncles(key, d, d2):
    """
    US 20: Aunts and uncles should not marry their nieces or nephews
    """
    dad = 0
    mom = 0
    daddad = 0
    mommom = 0
    dadmom = 0
    momdad = 0
    fam = []
    ans = []
    for key1 in d2:
        for key2 in d2[key1]["CHIL"]:
            if key == key2:
                husb=d2[key1]["HUSB"]
                wife=d2[key1]["WIFE"]
                dad = husb
                mom = wife
    for key1 in d2:
        for key2 in d2[key1]["CHIL"]:
            if dad == key2:
                husb=d2[key1]["HUSB"]
                wife=d2[key1]["WIFE"]
                daddad = husb
                momdad = wife
    for key1 in d2:
        for key2 in d2[key1]["CHIL"]:
            if mom == key2:
                husb=d2[key1]["HUSB"]
                wife=d2[key1]["WIFE"]
                dadmom = husb
                mommom = wife
    for key1 in d2:
        husb=d2[key1]["HUSB"]
        wife=d2[key1]["WIFE"]
        if husb == dadmom and wife == mommom:
            for chil in d2[key1]["CHIL"]:
                if chil == mom:
                    continue
                else:
                    fam.append(chil)
        if husb == daddad and wife == momdad:
            for chil in d2[key1]["CHIL"]:
                if chil == dad:
                    continue
                else:
                    fam.append(chil)
    for key1 in d2:
        husb=d2[key1]["HUSB"]
        wife=d2[key1]["WIFE"]
        mar = [husb,wife]
        for key2 in fam:
            if key in mar and key2 in mar:
                ans.append(key2)
    return ans

def unique_name_bdate(name1, name2, bdate1, bdate2):
    """
    US23: No more than one individual with the same name and birth
    date should appear in a GEDCOM file
    """
    if name1 == {} or name2 == {}:
        return True
    if bdate1 == {} or bdate2 =={}:
        return True
    if name1 == name2 and bdate1 == bdate2:
        return False
    return True
    
def sibling_marry(key, d, d2):
    """US18"""
    if d[key]["FAMC"] != {} and d[key]["FAMC"] in d2:
        siblings = []
        #for a in d2[d[key]["FAMC"]]["CHIL"]:
        #	siblings[a] = 
        for a in d2[d[key]["FAMC"]]["CHIL"]:
            siblings.append(a)
        #siblings = d2[d[key]["FAMC"]]["CHIL"]
        #print siblings
        #print key, siblings, d2[d[key]["FAMC"]]
        if key in siblings:
            siblings.remove(key)
        fam = d[key]["FAMIDS"]
        #print fam
        #print d2
        l = []
        for id in fam:
            if id in d2:
                l += [(d2[id]["HUSB"], d2[id]["WIFE"])]
        for sib in siblings:
            if d[key]["SEX"] == "M":
                test = (key, sib)
            else:
                test = (sib, key)
            if test in l:
                return False
    return True

def first_cousins(key, d, d2):
    """US19"""
    if d[key]["FAMC"] != {}:
        if d[key]["FAMC"] in d2:
            dad = d2[d[key]["FAMC"]]["HUSB"]
            mom = d2[d[key]["FAMC"]]["WIFE"]
            if d[mom]["FAMC"] != {} and d[mom]["FAMC"] in d2:
                momfam = []
                for a in d2[d[mom]["FAMC"]]["CHIL"]:
                    momfam.append(a)
            #momfam = d2[d[mom]["FAMC"]]["CHIL"]
            else:
                momfam = []
            if momfam != [] and mom in momfam:
                momfam.remove(mom)
            if d[dad]["FAMC"] != {} and d[dad]["FAMC"] in d2:
                dadfam = []
                for a in d2[d[dad]["FAMC"]]["CHIL"]:
                    dadfam.append(a)
                #dadfam = d2[d[dad]["FAMC"]]["CHIL"]
            else:
                dadfam = []
            if dadfam != [] and dad in dadfam:
                dadfam.remove(dad)
        cousin = []
        l = []
        for k in momfam + dadfam:
            for f in d[k]["FAMIDS"]:
                if "dup" not in f:
                    cousin += [d2[f]["CHIL"]]
        for id in d[key]["FAMIDS"]:
            if "dup" not in id:
                l += [(d2[id]["HUSB"], d2[id]["WIFE"])]
        for c in cousin:
            if d[key]["SEX"] == "M":
                test = (key, c)
            else:
                test = (c, key)
            if test in l:
                return False
    return True

def makedate(d1):
    """
    creates dates to be sorted for order_sibling()
    """
    if len(str(d1["month"])) > 2 and str(d1["month"]) in months.keys():
        #replace GED month code with number
        d1["month"] = months[d1["month"]]
    return date(int(d1["year"]), d1["month"], int(d1["day"]))

def order_sibling(fid, d, d2):
    """us28"""
    if fid not in d2:
        return []
    children = d2[fid]["CHIL"]
    if children != []:
        sorted(children, key=lambda id: makedate(d[id]["BIRT"]))
        return children
    return []

def corresponding(id, d, d2):
    """us26"""
    head = d[id]["FAMIDS"]
    born = d[id]["FAMS"]
    print "us26"
    print id, born
    for fid in head:
        if fid not in d2:
            return False
        f = d2[fid]
        if f["HUSB"] != id and f["WIFE"] != id:
            return False
    
    if born != {} and id not in d2[born]["CHIL"]:
        return False
    return True

def individual_age(birth):
    """US27: Include person's current age when listing individuals"""
    age = 0
    if birth == {}:
        return age
    else:
        birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    today = date.today()
    age = today - birth
    return abs(int(int(age.days)/365.25))

def individual_age_from_marr(birth,marr):
    """US27: Include person's current age when listing individuals"""
    age = 0
    if birth == {}:
        return age
    else:
        birth = date(int(birth["year"]), birth["month"], int(birth["day"]))
    if marr == {}:
        return age
    else:
    	marr = date(int(marr["year"]), marr["month"], int(marr["day"]))
    age = marr - birth
    return abs(int(int(age.days)/365.25))

def unique_fam(wife1, husb1, wife2, husb2, marr1, marr2):
    """
    US24: No more than one family with the same spouses
    by name and the same marriage date should appear in a GEDCOM file
    """
    if wife1 == {} or wife2 == {}:
        return True
    if husb1 == {} or husb2 =={}:
        return True
    if marr1 == {} or marr2 =={}:
        return True
    if wife1 == wife2 and husb1 == husb2 and marr1 == marr2:
        return False
    return True

def large_age_diff(famid,d,d2):

	if famid not in d2:
		return False
        husb=d2[famid]["HUSB"]
        wife=d2[famid]["WIFE"]
        hbirt=d[husb]["BIRT"]
        wbirt=d[wife]["BIRT"]
        marr=d2[famid]["MARR"]
	hage = individual_age_from_marr(hbirt,marr)
	wage = individual_age_from_marr(wbirt,marr)
	if hage > (wage * 2) or wage > (hage * 2):
		return True
	return False

def unique_name_bdate_fam(name1, name2, bdate1, bdate2):
    """
    US25: No more than one child with the same name and birth
    date should appear in a family
    """
    if name1 == {} or name2 == {}:
        return True
    if bdate1 == {} or bdate2 =={}:
        return True
    if name1 == name2 and bdate1 == bdate2:
        return False
    return True
