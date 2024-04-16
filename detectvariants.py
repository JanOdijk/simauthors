from optparse import OptionParser
from typing import List, Tuple
from collections import defaultdict
from xlsx import getxlsxdata, mkworkbook
from cleanauthors import  cleanauthors
from parameters import authorscol,  parblockcol, sessionslotcol, paperidcol, presenterscol
import itertools
from editdistance import distance

reportevery = 100000

space = ' '
namevariantsfullname = 'name_analysis.txt'

initialscore = 0.1
scorethreshold = (0.3, 0)
restscorethreshold = 0.3
missingnames_score = 0.1
missingnames_factor = 0.5


def isnoncontsublist(wrds1: List[str], wrds2: List[str]) -> bool:
    if wrds1 == []:
        return True
    if wrds2 == []:
        return False
    head1 = wrds1[0]
    head2 = wrds2[0]
    if head1 == head2:
        result = isnoncontsublist(wrds1[1:], wrds2[1:])
    else:
        result = isnoncontsublist(wrds1, wrds2[1:])
    return result
def detectvariants():

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="infilename", help="inputfile (MS Excel")
    parser.add_option("-s", "--sheet", dest="sheetname", help="WorkSheet name (default: the active worksheet")
    parser.add_option("-o", "--outfile", dest="outfullname", help=f"Filename to write the results to (default: {namevariantsfullname}")

    (options, args) = parser.parse_args()

    if options.infilename is None:
        print('Please specify an input filename using -f.')
        exit(-1)

    if options.outfullname is None:
        options.outfullname = namevariantsfullname

    # read the input file with the program
    header, data = getxlsxdata(options.infilename, sheetname=options.sheetname)

    cleanauthortuples = []
    for row in data:
        theauthors = row[authorscol]
        cleanauthortuples += cleanauthors(theauthors, includerestnames=True)

    # obtain frequencies
    famnamefrqdict = defaultdict(int)
    restnamefrqdict = defaultdict(int)
    tuplefrqdict = defaultdict(int)
    for famname, restnames in cleanauthortuples:
        famnamefrqdict[famname] += 1
        restnametuple = tuple(restnames)
        restnamefrqdict[restnametuple] += 1
        tuplefrqdict[(famname, restnametuple)] == 1


    # compare all names with each other
    resultlist = []
    counter = 0
    countercounter = 0
    tuplefrqdictkeys = [key for key in tuplefrqdict]
    for nametuple1, nametuple2 in itertools.combinations(tuplefrqdictkeys, 2):
        counter += 1
        if counter % reportevery == 0:
            print(counter, end='\t', flush=True)
            countercounter += 1
            if countercounter % 10 == 0:
                print('', flush=True)
        famname1, restname1 = nametuple1
        famname2, restname2 = nametuple2
        if famname1 == famname2:
            restnamescore = getrestnamescore(restname1, restname2)
            score = (0, restnamescore)
        else:
            famnamescore = relativedistance(famname1, famname2)
            restnamescore = getrestnamescore(restname1, restname2)
            score = (famnamescore, restnamescore)
        if score != (0, 0) and score < scorethreshold:
            resultlist.append((nametuple1, nametuple2, score))

    print(f'\n{counter} comparisons made')

    # sort the results by score, lowest to highest
    sortedresultlist = sorted(resultlist, key=lambda x: x[2], reverse=True)

    differentauthors = []
    likelyvariants = []
    variantsof = []
    variants = []
    for triple in sortedresultlist:
        nametuple1, nametuple2, score = triple
        famscore, restscore = score
        if famscore == 0:
            if restscore > restscorethreshold:
                differentauthors.append((nametuple1, nametuple2))
            else:
                likelyvariants.append((nametuple1, nametuple2))
        elif restscore <= restscorethreshold:
            famname1frq = famnamefrqdict[nametuple1[0]]
            famname2frq = famnamefrqdict[nametuple2[0]]
            if famname1frq > famname2frq:
                variantsof.append((nametuple2, nametuple1, famname2frq, famname1frq))
            elif famname2frq > famname1frq:
                variantsof.append((nametuple1, nametuple2, famname1frq, famname2frq))
            else:
                variants.append((nametuple1, nametuple2, famname1frq, famname2frq))
                # print(f'{nametuple1} and {nametuple2} are variants ({famname1frq} == {famname2frq})')


    with open(options.outfullname, 'w', encoding='utf8') as outfile:
        print('\n================\nMost likely different authors:', file=outfile)
        for nametuple1, nametuple2 in sorted(differentauthors):
            print(f'{nametuple1} v. {nametuple2}', file=outfile)
        print(f'\n================\nMost likely variants (same normalized family name):', file=outfile)
        for nametuple1, nametuple2 in sorted(likelyvariants):
            print(f'{nametuple1} v. {nametuple2}', file=outfile)
        print(f'\n================\nMost likely a variant of:', file=outfile)
        for nametuple1, nametuple2, famnamefrq1, famnamefrq2 in sorted(variantsof):
            print(f'{nametuple1} v. {nametuple2} ({famnamefrq1} v. {famnamefrq2})', file=outfile)
        print(f'\n================\nMost likely  variants of each other:', file=outfile)
        for nametuple1, nametuple2, famnamefrq1, famnamefrq2 in sorted(variants):
            print(f'{nametuple1} v. {nametuple2} ({famnamefrq1} == {famnamefrq2})', file=outfile)


def getrestnamescore(restname1: List[str], restname2: List[str]) -> float:
    newrestname1 = expandinitials(restname1, restname2)
    newrestname2 = expandinitials(restname2, restname1)
    if missingnames_factor* len(newrestname2) <= len(newrestname1) < len(newrestname2) and \
        isnoncontsublist(newrestname1, newrestname2):
        score = missingnames_score
    elif missingnames_factor * len(newrestname1) <= len(newrestname2) < len(newrestname1) and \
            isnoncontsublist(newrestname2, newrestname1):
        score = missingnames_score
    else:
        newrestname1str = space.join(newrestname1)
        newrestname2str = space.join(newrestname2)
        score = relativedistance(newrestname1str, newrestname2str)
    return score


def expandinitials(restname1, restname2):
    if len(restname1) == 0:
        return []
    head1 = restname1[0]
    if isinitial(head1):
        expansionfound = False
        for i,el in enumerate(restname2):
            if el[0] == head1[0]:
                newhead1 = el + '@'
                tail2 = restname2[i+1:]
                expansionfound = True
                break
        if not expansionfound:
            tail2 = restname2
            newhead1 = head1
        newtail1 = expandinitials(restname1[1:], tail2)
    else:
        newtail1 = expandinitials(restname1[1:], restname2)
        newhead1 = head1
    newrestname1 = [newhead1] + newtail1
    return newrestname1




def relativedistance(wrd1: str, wrd2: str) -> float:
    dist = distance(wrd1, wrd2)
    maxl = max(len(wrd1), len(wrd2))
    if maxl != 0:
        result = dist / maxl
    else:
        result = 0
    return result

def isinitialof(name1:str, name2:str) -> bool:
    result = name1 == name2[0] or name1 ==name2[0] + '.'
    return result

def isinitial(name:str) -> bool:
    result = len(name) == 1 or (len(name) == 2 and name[1] == '.')
    return result


if __name__ == '__main__':
    detectvariants()