#Mark Mirthcouk Project 2
import sys
tags=["INDI","NAME","SEX","BIRT","DEAT","FAMC","FAMS","FAM","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]

def main(filename):
	with open(filename, 'r') as f:
		for line in f:
			print line.strip()
	            	y = line.strip().split(" ")

        	    	print y[0].strip()

            		if y[1].strip() in tags:
           			print y[1].strip()
	            	elif len(y)>2 and y[2].strip() in tags:
        	    		print y[2].strip()
            		else:
            			print "Invalid tag"

if __name__ == '__main__':
	if len(sys.argv) == 2:
        	filename= sys.argv[1]
        	main(filename)
    	else:
        	print "Usage: python project02.py <filename>"
