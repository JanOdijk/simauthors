from typing import List
import unicodedata
import os
import csv

comma = ','
space = ' '
tab = '\t'

# exceptionsfile to specify ad-hoc conversions (e.g. Winhouwer -> Windhouwer)
exceptionsfilename = 'exceptions.txt'

exceptions = {}

if os.path.exists(exceptionsfilename):
    with open(exceptionsfilename, 'r', encoding='utf8') as exceptionsfile:
        exceptionsreader = csv.reader(exceptionsfile, delimiter=tab)
        for row in exceptionsreader:
            exceptions[row[0]] = row[1]



replace = {}
replace["Æ"] = "AE"
replace["Ð"] = "d"
replace["Ö"] = "OE"
replace["Ø"] = "O"
replace["Ü"] = "UE"
replace["Þ"] = "Th"
replace["\xDF"] = "ss"
# replace["\xE0"]="a"
replace["ä"] = "ae"
replace["å"] = "aa"
replace["æ"] = "ae"
replace["ð"] = "d"
replace["ö"] = "oe"
replace["ø"] = "o"
replace["ü"] = "ue"
replace["þ"] = "th"


def authors2list(authorstring: str) -> List[str]:
    newauthorstring = authorstring.replace(' and ', ', ')
    authorlist = newauthorstring.split(comma)
    strippedauthorlist = [name.strip() for name in authorlist]
    return strippedauthorlist

def cleanauthors(rawauthorstring: str) -> List[str]:
    rawauthorlist = authors2list(rawauthorstring)
    cleanfamilynames = []
    for name in rawauthorlist:
        nameparts = name.split(space)
        familyname = nameparts[-1]
        if familyname in exceptions:
            familyname = exceptions[familyname]
        familyname = deaccent(familyname)
        cleanfamilynames.append(familyname)
    return cleanfamilynames


def deaccent(name: str) -> str:
    deaccented_name = ''.join(char for char in unicodedata.normalize('NFD', name) if unicodedata.category(char) != 'Mn')
    deaccented_name = ''.join(replace[char] if char in replace else char for char in deaccented_name)
    return deaccented_name
