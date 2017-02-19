#Mark Mirthcouk Project 2
import sys
from collections import defaultdict
tags=["INDI","NAME","SEX","BIRT","DEAT","FAMC","FAMS","FAM","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]
d = {} # for individuals
d2 = {} # for families

def birth_before_death(birth,death):
	if birth["year"]>death["year"]:
		return False
	if birth["month"]>death["month"]:
		return False
	if birth["day"]>=death["day"]:
		return False
	return True

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
			print line.strip()
	            	y = line.strip().split(" ")

        	    	print y[0].strip()

            		if y[1].strip() in tags:
           			print y[1].strip()
	            	elif len(y)>2 and y[2].strip() in tags:
        	    		print y[2].strip()
            		else:
            			print "Invalid tag"

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
		print "Printing individual ID's and name!"
		for key in sorted(d, key=lambda x: int(x[1:])):
			name=d[key]["NAME"]
			print key,name
		print "Printing family ID's, husband name, and wife name!"
		for key2 in sorted(d2, key=lambda x: int(x[1:])):
			husb=d2[key2]["HUSB"]
			wife=d2[key2]["WIFE"]
			hname=d[husb]["NAME"]
			wname=d[wife]["NAME"]
			print key2,hname," , ",wname
if __name__ == '__main__':
	if len(sys.argv) == 2:
        	filename= sys.argv[1]
        	main(filename)
    	else:
        	print "Usage: python project02.py <filename>"
