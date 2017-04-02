def printTable(tobj, title=""):
    """
    Prints a table
    tobj is a dictionary of column headers as keys, holding lists of cell values for each column
    """
    #define the order columns should print in
    customOrdering = ['Key', 'First', 'Last', 'Birth', 'Death', 'Husb', 'Wife', 'Marriage', 'Divorce', 'Children']
    #check for at least 1 column
    if len(tobj.keys()) < 1:
        raise ValueError("Table must contain at least 1 column")
        return
    #check that all columns have same # of rows
    rowCount = len(tobj[tobj.keys()[0]])
    if len(filter(lambda x: x!=rowCount, [len(tobj[k]) for k in tobj])) != 0:
        raise ValueError("All columns must have the same number of rows")
    if rowCount == 0:
        tobj = {k:["None"] for k in tobj}
    #create dictionary of column headers and longest widths
    maxSizeLst = {k:len(max(tobj[k], key=len)) for k in tobj}
    maxSizeLst = {k:max(maxSizeLst[k], len(k)) for k in maxSizeLst}
    #create horizontal rule string
    hr = "+-" + "-+-".join(["-"*(maxSizeLst[k]) for k in sorted(maxSizeLst, key=lambda word: customOrdering.index(word))]) + "-+"
    #create header string
    header = "| " + " | ".join(["{0:{w}}".format(k, w=maxSizeLst[k]) for k in sorted(tobj, key=lambda word: customOrdering.index(word))]) + " |"
    #print header
    print title+":" if len(title)>0 else title
    print hr
    print header
    print hr
    #print row data
    for i in range(rowCount):
        line = "| " + " | ".join(["{0:{w}}".format(tobj[k][i], w=maxSizeLst[k]) for k in sorted(tobj, key=lambda word: customOrdering.index(word))]) + " |"
        print line
    #print bottom hr
    print hr


if __name__ == "__main__":
    testTable = {
        "col1": ["v1long", "v2", "v3"],
        "col2": ["v1", "v2reallyreallylong", "v3"],
        "col3": ["v1", "v2", "v3kindalong"]
    }
    printTable(testTable, "Test table")
    printTable({"col1": [],"col2": [],"col3": []})
