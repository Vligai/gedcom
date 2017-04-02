import sys, time, copy
from collections import defaultdict
from datetime import date, timedelta
from copy import deepcopy

#Code for user story checks
from validity_checks import *
from utility import *

tags=[\
    "INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM",\
    "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
months ={\
    "JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6,\
    "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
monthnames = {\
    1: "January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",\
    7:"July", 8:"August", 9:"September", 10:"October", 11:"November",\
    12:"December",}
US_MSG_OBJ = {} #user story message object

def addUSMsg(user_story, message):
    """
    Adds a user story message to the global dictionary of user story messages, US_MSG_OBJ
    US_MSG_OBJ is sorted by user story, a string in the form "US<number>"
    """
    if not user_story in US_MSG_OBJ:
        US_MSG_OBJ[user_story] = []
    US_MSG_OBJ[user_story].append(message)

def printUSMsgs(print_us_nums=True):
    """
    Prints messages from the global user story message dictionary, US_MSG_OBJ
    Sorted by user story numbers, with the option to print the numbers
    """
    if len(US_MSG_OBJ) == 0:
        print "No messages found"
        return
    print "\n+----------------------+"
    print "| User Story Messages  |"
    print "+----------------------+"
    for user_story, msgLst in sorted(US_MSG_OBJ.iteritems()):
        #msgLst = US_MSG_OBJ[user_story]
        if print_us_nums:
            print "{0} messages:".format(user_story)
        for msg in msgLst:
            indent = ''
            if print_us_nums:
                indent = "-"
            print "{0:2}{1}".format(indent, msg)
    return None

def print_date(ddate):
    """
    prints a date in the form "January 2, 2000"
    """
    if ddate == {}:
        return {}
    monthName = monthnames[ddate["month"]]
    dd = ddate["day"]
    yyyy = ddate["year"]
    return "{0} {1}, {2}".format(monthName, dd, yyyy)

def parseFile(filename):
    """
    Parse over a GEDCOM file
    Return a two dictionaries, one for individuals and one for families
    """
    with open(filename, 'r') as f:
        icurr=''
        birt=0
        deat=0
        marr=0
        div=0
        ind_dict = {}
        fam_dict = {}
        dup_prefix = 'dup_'

        longestFirstNameLength = 0
        longestLastNameLength = 0
        for line in f:
            if "HUSB" not in line and "WIFE" not in line and "CHIL" not in line:
                isFamilyLine = False
            y = line.strip().split(' ')

            line_part_count = len(y)

            if line_part_count>2 and y[2].strip()=="INDI":
                icurr=y[1].strip()
                if icurr in ind_dict:
                    icurr = dup_prefix + icurr
                ind_dict[icurr]={
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
            elif line_part_count>3 and y[1].strip()=="NAME":
                a=y[2].strip()+" "+ y[3].strip()

                ind_dict[icurr]["NAME"]=a
            elif line_part_count>2 and y[1].strip()=="SEX":
                a=y[2].strip()
                ind_dict[icurr]["SEX"]=a
            elif line_part_count>2 and y[1].strip()=="GIVN":
                a=y[2].strip()
                if len(a) > longestFirstNameLength:
                    longestFirstNameLength = len(a)
                ind_dict[icurr]["GIVN"]=a
            elif line_part_count>2 and y[1].strip()=="SURN":
                a=y[2].strip()
                if len(a) > longestLastNameLength:
                    longestLastNameLength = len(a)
                ind_dict[icurr]["SURN"]=a
            elif line_part_count>=2 and y[1].strip()=="BIRT":
                birt=1
            elif line_part_count>2 and y[1].strip()=="DEAT":
                deat=1
            elif line_part_count>4 and y[1].strip()=="DATE":
                day=y[2].strip()
                month=y[3].strip()
                if not isinstance(month, int):
                    month = months[month]
                year=y[4].strip()
                if birt==1:
                    a={"day":day, "month":month,"year":year}
                    ind_dict[icurr]["BIRT"]=a
                    birt=0
                if deat==1:
                    a={"day":day, "month":month,"year":year}
                    ind_dict[icurr]["DEAT"]=a
                    deat=0
                if marr==1:
                    a={"day":day, "month":month,"year":year}
                    fam_dict[fcurr]["MARR"]=a
                    marr=0
                if div==1:
                    a={"day":day, "month":month,"year":year}
                    fam_dict[fcurr]["DIV"]=a
                    div=0
            elif line_part_count>2 and y[1].strip()=="FAMC":
                a=y[2].strip()
                ind_dict[icurr]["FAMC"]=a
            elif line_part_count>2 and y[1].strip()=="FAMS":
                a=y[2].strip()
                ind_dict[icurr]["FAMS"]=a
            elif line_part_count>2 and y[2].strip()=="FAM":
                fcurr=y[1].strip()
                if fcurr in fam_dict:
                    fcurr = dup_prefix + fcurr
                fam_dict[fcurr]={
                    "MARR":{},
                    "DIV":{},
                    "CHIL":[]
                    }
                isFamilyLine = True
            elif line_part_count>2 and isFamilyLine:
                tag=y[1].strip()
                a=y[2].strip()
                if tag =="CHIL":
                    fam_dict[fcurr][tag].append(a)
                else:
                    fam_dict[fcurr][tag]=a
                    ind_dict[a]["FAMIDS"].append(fcurr)
            elif line_part_count>1 and y[1].strip()=="MARR":
                marr=1
            elif line_part_count>1 and y[1].strip()=="DIV":
                div=1
    def handleDups():
        #time to fix duplicate IDs
        #get list of IDs that aren't tagged as duplicates
        non_dup_ind_lst = [k for k in ind_dict.keys() \
            if k[:len(dup_prefix)]!=dup_prefix]
        #get list of IDs tagged as duplicates
        dup_ind_lst = [k for k in ind_dict.keys() \
            if k[:len(dup_prefix)]==dup_prefix]
        #get max non-duplicate ID
        ind_id_max = max([int(x[1:]) for x in non_dup_ind_lst])
        #swap key for new key
        for k in dup_ind_lst:
            #swap
            temp_obj = deepcopy(ind_dict[k])
            del ind_dict[k]
            new_k = "I{0}".format(ind_id_max+1)
            ind_dict[new_k] = temp_obj
            #log
            msg = "Individual ID duplicate '{0}' reassigned to '{1}'".format(k[len(dup_prefix):], new_k)
            addUSMsg('US22', msg)
            #increase counter
            ind_id_max = ind_id_max+1

        #same as above for families
        non_dup_fam_lst = [k for k in fam_dict.keys() \
            if k[:len(dup_prefix)]!=dup_prefix]
        dup_fam_lst = [k for k in fam_dict.keys() \
            if k[:len(dup_prefix)]==dup_prefix]
        fam_id_max = max([int(x[1:]) for x in non_dup_fam_lst])
        for k in dup_fam_lst:
            #swap
            temp_obj = deepcopy(fam_dict[k])
            del fam_dict[k]
            new_k = "F{0}".format(fam_id_max+1)
            fam_dict[new_k] = temp_obj
            #log
            msg = "Family ID duplicate '{0}' reassigned to '{1}'".format(k[len(dup_prefix):], new_k)
            addUSMsg('US22', msg)
            #increase counter
            fam_id_max = fam_id_max+1
    handleDups()
    return ind_dict, fam_dict

def main(filename, oldestRecentData, printUserStories, printDescriptions):
    RECENT_CUTOFF = oldestRecentData
    PRINT_USER_STORY_TESTS = printUserStories
    PRINT_PERSON_OR_FAMILY_DESCRIPTION = printDescriptions
    ERR_LIST = {}

    print "+------------+"
    print "| Running... |"
    print "+------------+"

    d, d2 = parseFile(filename)

    """
    interate over individuals
    """
    recent = {'births':[], 'deaths':[]}

    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        ind_print_tbl = {}
        fam_print_tbl = {}
        #define headers and initialize dictionary columns
        ind_table_headers = ["Key", "First", "Last", "Birth", "Death"]
        for h in ind_table_headers:
            ind_print_tbl[h] = []

        fam_table_headers = ["Key", "Husb", "Wife", "Marriage", "Divorce", "Children"]
        for h in fam_table_headers:
            fam_print_tbl[h] = []

    for key in sorted(d, key=lambda x: int(x[1:])):
        name=d[key]["NAME"]
        fname=d[key]['GIVN']
        lname=d[key]['SURN']
        birt=d[key]["BIRT"]
        deat=d[key]["DEAT"]
        if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
            strBirth = ""
            strDeath = ""
            if birt != {}:
                dateBirth = date(int(birt['year']), int(birt['month']), int(birt['day']))
                strBirth = str(dateBirth)
                if dateBirth > RECENT_CUTOFF:
                    msg = "Recent birth: {0} on {1}".format(name, strBirth)
                    addUSMsg('US35', msg)
            if deat != {}:
                dateDeath = date(int(deat['year']), int(deat['month']), int(deat['day']))
                strDeath = str(dateDeath)
                if dateDeath > RECENT_CUTOFF:
                    msg = "Recent death: {0} on {1}".format(name, strDeath)
                    addUSMsg('US36', msg)
            ind_print_tbl["Key"].append(key)
            ind_print_tbl["First"].append(fname)
            ind_print_tbl["Last"].append(lname)
            ind_print_tbl["Birth"].append(strBirth if strBirth else "")
            ind_print_tbl["Death"].append(strDeath if strBirth else "")
        if not birth_before_death(birt,deat):
            msg = "Birth is not before death:{0}".format(name)
            addUSMsg("US03", msg)
        if not less_than_150(birt,deat):
            msg = "Greater than 150 years old: {0}".format(name)
            addUSMsg('US07', msg)
        if not date_before_today(birt):
            msg = "Date of {0}'s birth {1} is after today".format(name,print_date(birt))
            addUSMsg("US01", msg)
        if not date_before_today(deat):
            msg = "Date of {0}'s death {1} is after today".format(name,print_date(deat))
            addUSMsg("US01", msg)
        if not sibling_marry(key, d, d2):
            msg = "{0} has married one of their siblings".format(name)
            addUSMsg("US18", msg)
        if not first_cousins(key, d, d2):
            msg = "{0} has married one of their first cousins".format(name)
            addUSMsg("US19", msg)

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
            strMarr = ""
            strDiv = ""
            if marr != {}:
                dateMarr = date(int(marr['year']), int(marr['month']), int(marr['day']))
                strMarr = str(dateMarr)
            if div != {}:
                dateDiv = date(int(div['year']), int(div['month']), int(div['day']))
                strDiv = str(dateDiv)
            fam_print_tbl["Key"].append(key2)
            fam_print_tbl["Husb"].append(husb)
            fam_print_tbl["Wife"].append(wife)
            fam_print_tbl["Marriage"].append(strMarr if strMarr else "")
            fam_print_tbl["Divorce"].append(strDiv if strDiv else "")
            fam_print_tbl["Children"].append(", ".join(chil) if len(chil)>0 else "")
        if not birth_before_marriage(hbirt,marr):
            msg = "Husbands Birth with key {0} has name {1} is not before marriage ".format(husb, hname)
            addUSMsg("US02", msg)
        if not birth_before_marriage(wbirt,marr):
            msg = "Wifes Birth with key {0} has name {1} is not before marriage ".format(wife, wname)
            addUSMsg("US02", msg)
        if not marriage_before_divorce(marr,div):
            msg = "Marriage with key {0} of {1} and {2} is not before divorce ".format(key2, hname, wname)
            addUSMsg("US04", msg)
        if not marriage_before_death(marr,hdeat):
            msg = "Marriage with key {0} of {1} and {2} is not before death of husband {3}: ".format(key2, hname, wname, hname)
            addUSMsg("US05", msg)
        if not marriage_before_death(marr,wdeat):
            msg = "Marriage with key {0} of {1} and {2} is not before death of wife {3} ".format(key2, hname, wname, wname)
            addUSMsg("US05", msg)
        if not div_before_death(div,hdeat):
            msg = "Divorce with key {0} of {1} and {2} is not before deathof husband {3} ".format(key2, hname, wname, hname)
            addUSMsg("US06", msg)
        if not div_before_death(div,wdeat):
            msg = "Divorce with key {0} of {1} and {2} is not before death of wife {3} ".format(key2, hname, wname, wname)
            addUSMsg("US06", msg)
        if not correct_genders(d[husb], d[wife]):
            msg = "Husband {0} is not male or wife {1} is not female".format(hname, wname)
            addUSMsg("US21", msg)
        if not marriage_after_14(hbirt,marr):
            msg = "Husbands Birth with key {0} has name {1} is not older than 14".format(husb, hname)
            addUSMsg("US10", msg)
        if not marriage_after_14(wbirt,marr):
            msg = "Wifes Birth with key {0} has name {1} is not older than 14".format(wife, wname)
            addUSMsg("US10", msg)
        if not date_before_today(marr):
            msg = "Date of {0} and {1} marriage {2} is after today".format(hname,wname,print_date(marr))
            addUSMsg("US01", msg)
        if not date_before_today(div):
            msg = "Date of {0} and {1} divorce {2} is after today".format(hname,wname,print_date(div))
            addUSMsg("US01", msg)
        if not male_last_names(d,d2[key2]):
            msg = "Family with key {0} doesn't have all male last names".format(key2)
            addUSMsg("US16", msg)

        for c in chil:
            name=d[c]["NAME"]
            birth=d[c]["BIRT"]
            if birth_before_marriage_of_parents(birth,marr):
                msg = "Birth of {0} is before marriage of {1},{2} ".format(name,hname,wname)
                addUSMsg('US08', msg)
            if birth_before_death_of_parents(birth,hdeat):
                msg = "Birth of {0} is before death of Dad: {1}".format(name,hname)
                addUSMsg('US09', msg)
            if birth_before_death_of_parents(birth,wdeat):
                msg = "Birth of {0} is before death of Mom: {1}".format(name,wname)
                addUSMsg('US09', msg)
        """Checking if siblings were born too close or too far apart"""
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
                        addUSMsg('US13', msg)


    """Checking for bigomy"""
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
                        addUSMsg('US11', msg)

    deadp=deceased(d)
    dp=sorted(deadp, key=lambda x: int(x[1:]))
    for key in dp:
        name=d[key]["NAME"]
        deat=d[key]["DEAT"]
        msg = "Person with key {} has the name {} and died on {}".format(key,name,print_date(deat))
        addUSMsg('US29', msg)


    lm=living_married(d,d2)
    lm2=sorted(lm, key=lambda x: int(x[1:]))
    for key in lm2:
        name=d[key]["NAME"]
        msg = "Person with key {} has the name {} and is still alive and married".format(key,name)
        addUSMsg('US30', msg)
    """Checking for people with same names and birthdates"""
    for key in sorted(d, key=lambda x: int(x[1:])):
        for key2 in sorted(d, key=lambda x: int(x[1:])):
            if key == key2:
                continue
            else:
                name1=d[key]["NAME"]
                name2=d[key2]["NAME"]
                birt1=d[key]["BIRT"]
                birt2=d[key2]["BIRT"]
                if not unique_name_bdate(name1, name2, birt1, birt2):
                    msg = "Person with key {} has the name {} is the same as person with key {} and name {} have the same birthday {}".format(key,name1,key2,name2,print_date(birt1))
                    addUSMsg('US23', msg)
    """Checking for people, who are married to their aunts/uncles"""
    for key in sorted(d, key=lambda x: int(x[1:])):
        a = aunts_uncles(key, d, d2)
        if a != []:
            for aa in a:
                name1=d[key]["NAME"]
                name2=d[aa]["NAME"]
                msg = "Person with key {} has the name {} and is married to their aunt or uncle with key {} and name {}".format(key,name1,aa,name2)
                addUSMsg('US20', msg)

    if PRINT_PERSON_OR_FAMILY_DESCRIPTION:
        printTable(ind_print_tbl, ind_table_headers, "Individuals")
        printTable(fam_print_tbl, fam_table_headers, "Families")
    if PRINT_USER_STORY_TESTS:
        printUSMsgs()

if __name__ == '__main__':
    print_user_stories = True
    print_descriptions = True
    recent_days = 30
    oldest_recent_date = (date.today() + timedelta(days=-30))
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename, oldest_recent_date, print_user_stories, print_descriptions)
    else:
        print ("Usage: python project02.py <filename>")
