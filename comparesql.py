from typing import List

def getColums(a: List[List]):
    columns=[]
    ncols=0
    for irow in range(len(a)):
        arow=a[irow]
        ncols=len(arow)
        break
    for icol in range(ncols):
        columns.append([])

    for irow in range(len(a)):
        arow=a[irow]
        for icol in range(len(arow)):
           columns[icol].append(arow[icol])
    return columns

def colsAreEqual(a,b):
    aso=a
    aso.sort()
    bso=b
    bso.sort()
    for irow in range(len(aso)):
        if aso[irow] != bso[irow]:
            return False
    return True

def compare(ao: List[List], refo: List[List]):
    a=getColums(ao)
    ref=getColums(refo)
    if len(ref)>len(a):
        print(len(ref),' ',len((a)))
        return False
    if len(ref) == 0:
        return len(a)==0
    if len(ref[0])!=len(a[0]):
        return False
    
    for colref in ref:
        found=False
        for cola in a:
            if colsAreEqual(colref,cola):
                found=True
                break
        if not found:
            return False
    return True 