from optparse import OptionParser
import os
from typing import List
import csv
from collections import defaultdict
from xlsx import getxlsxdata, mkworkbook
from cleanauthors import authors2list, cleanauthors
from parameters import authorscol,  parblockcol, sessionslotcol, paperidcol, presenterscol
from constants import getcol as gc, \
    comment1_l, comment2_l, rawauthor1_l, rawauthor2_l, severity_l,  author_l, message_l,  parblock_l, \
    pid1_l, session1_l,  pid2_l, session2_l, nth_author1_l, out_of1_l, rawauthors1_l, nth_author2_l, out_of2_l, \
    rawauthors2_l, newdata_authorcol, newdata_rawauthorscol, newdata_parblockcol, newdata_sessionslotcol, \
    newdata_paperidcol, newdata_cleanauthorscol, newdata_presentingauthorscol, outheader

tab = '\t'
comma = ','
semicolon = ';'
commentstr1 = "comments1"
commentstr2 = "comments2"
rawauthorslabel = 'rawauthors'
cleanauthorslabel = 'cleanauthors'
sessionlabel = 'session'
presentingauthorslabel = 'presentingauthors'

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

def getcleanauthors(rawauthors: str) -> list:
    pass

def getauthorn(name: str, namelist: List[str]):
    result = namelist.index(name) + 1
    return result

def getauthor(i: int, namelist):
    result = namelist[i-1]
    return result

def mkcomid(author, pid1, session1, pid2, session2):
    result = f'{author}-{pid1}-{session1}-{pid2}-{session2}'
    return result

def getcomments(commentsfilename: str) -> dict:
    # read the comments from the commentsfile
    comments = defaultdict(lambda: defaultdict(str))
    if os.path.exists(commentsfilename):
        with open(commentsfilename, 'r', encoding='utf8') as commentsfile:
            commentsreader = csv.reader(commentsfile, delimiter=tab)
            for row in commentsreader:
                thekey = row[0]
                comments1 = row[1]
                comments2 = row[2]
                comments[thekey][commentstr1] = comments1
                comments[thekey][commentstr2] = comments2
    return comments

def getpreviouscomments(previousfilename: str, comments: dict) -> dict:
    # read the comments in from the previous file and add them to the comments
    if os.path.exists(previousfilename):
        header, data = getxlsxdata(previousfilename)
        for row in data:
            if row[gc(comment1_l)] != '' or row[gc(comment2_l)] != '':

                thecomid = mkcomid(row[gc(author_l)], row[gc(pid1_l)], row[gc(session1_l)], row[gc(pid2_l)], row[gc(session2_l)])
                comments[thecomid][commentstr1] = row[gc(comment1_l)]
                comments[thecomid][commentstr2] = row[gc(comment2_l)]
    return comments

def storecomments(comments, commentsfilename) -> None:
    # store old and new comments in a revised commentsfile
    with open(commentsfilename, 'w', encoding='utf8', newline='') as commentsfile:
        commentswriter = csv.writer(commentsfile, delimiter=tab)
        for comid in comments:
            row = [comid, comments[comid][commentstr1], comments[comid][commentstr2]]
            commentswriter.writerow(row)

def getpresentingauthors(rawauthors: str, presenters: str) -> str:
    rawpresenterlist = presenters.split(semicolon) if presenters != '' else []
    presenterlist = [int(pres.strip()) for pres in rawpresenterlist]
    newrawauthors = rawauthors.replace(' and ', comma)
    rawauthorlist = newrawauthors.split(comma)
    presentingauthorlist = [rawauthorlist[i-1] for i in presenterlist]
    presentingauthorlist += [rawauthor for i, rawauthor in enumerate(rawauthorlist) if i+1 not in presenterlist]
    presentingauthors = comma.join(presentingauthorlist)
    return presentingauthors

def simauthors():
    parser = OptionParser()
    parser.add_option("-c", "--commentsfile", dest="commentsfilename", help="Comments file name")
    parser.add_option("-p", "--previousfile", dest="previousfilename", help="previous output file name")
    parser.add_option("-f", "--file", dest="infilename", help="inputfile (MS Excel")
    parser.add_option("-s", "--sheet", dest="sheetname", help="WorkSheet name (default: the active worksheet")
    parser.add_option("-o", "--outfile", dest="outfullname", help="Filename to write the results to (default: authoranalysis.xlsx")

    (options, args) = parser.parse_args()

    outfilenamebase = 'authoranalysis'
    if options.commentsfilename is None:
        options.commentsfilename = 'comments.txt'

    if options.outfullname is None:
        options.outfullname = f'{outfilenamebase}.xlsx'

    if options.previousfilename is None:
        options.previousfilename = f'{outfilenamebase}-annotated.xlsx'

    # read the comments from the commentsfile
    comments = getcomments(options.commentsfilename)

    # read the comments in from the previous file and add them to comments
    comments = getpreviouscomments(options.previousfilename, comments)


    # store old and new comments in a revised commentsfile
    storecomments(comments, options.commentsfilename)

    # read the input file with the program
    header, data = getxlsxdata(options.infilename, sheetname=options.sheetname)

    newdata = []
    for row in data:
        rawauthors = row[authorscol]
        parblock = row[parblockcol]
        session = row[sessionslotcol]
        paperid = row[paperidcol]
        presenters = str(row[presenterscol]) if presenterscol != -1 else ''
        rawpresentingauthors = getpresentingauthors(rawauthors, presenters)
        authorlist = cleanauthors(rawpresentingauthors)
        for author in authorlist:
            newrow = [author, rawauthors, parblock, session, paperid,  authorlist, rawpresentingauthors,]
            newdata.append(newrow)



    mainarray = nested_dict(4, str)
    for row in newdata:
        mainarray[row[newdata_authorcol]][row[newdata_parblockcol]][row[newdata_paperidcol]][rawauthorslabel] = authors2list(row[newdata_rawauthorscol])
        mainarray[row[newdata_authorcol]][row[newdata_parblockcol]][row[newdata_paperidcol]][cleanauthorslabel] = row[newdata_cleanauthorscol]
        mainarray[row[newdata_authorcol]][row[newdata_parblockcol]][row[newdata_paperidcol]][sessionlabel] = row[newdata_sessionslotcol]
        mainarray[row[newdata_authorcol]][row[newdata_parblockcol]][row[newdata_paperidcol]][presentingauthorslabel] \
            = authors2list(row[newdata_presentingauthorscol])

    outdata = []
    for author in mainarray:
       for parblock in mainarray[author]:
           if len(mainarray[author][parblock]) > 1:
               doneset = set()
               for pid1 in mainarray[author][parblock]:
                   for pid2 in mainarray[author][parblock]:
                       if pid1 != pid2 & pid2 not in doneset:
                            pid1dict = mainarray[author][parblock][pid1]
                            pid2dict = mainarray[author][parblock][pid2]
                            authorlist1 = pid1dict[cleanauthorslabel]
                            outof1: int = len(authorlist1)
                            author1n: int = getauthorn(author, authorlist1)
                            rawauthorlist1 = pid1dict[presentingauthorslabel]
                            rawauthor1 = getauthor(author1n, rawauthorlist1)
                            authorlist2  = pid2dict[cleanauthorslabel]
                            outof2: int = len(authorlist2)
                            author2n: int = getauthorn(author, authorlist2)
                            rawauthorlist2 = pid2dict[presentingauthorslabel]
                            rawauthor2 = getauthor(author2n, rawauthorlist2)
                            session1 = pid1dict[sessionlabel]
                            session2 = pid2dict[sessionlabel]

                            thecomid = mkcomid(author,pid1, session1, pid2, session2)
                            comment1 = comments[thecomid][commentstr1] if thecomid in comments else ''
                            comment2 = comments[thecomid][commentstr2] if thecomid in comments else ''
                            newrow = [comment1, comment2, rawauthor1, rawauthor2]

                            if session1 != session2:
                                severity = 'Warning'
                                message = 'has multiple papers in different sessions in parblock'
                            else:
                                severity = 'Message'
                                message = 'has multiple papers in the same session in parblock'

                            rawauthors1 = comma.join(mainarray[author][parblock][pid1][rawauthorslabel])
                            rawauthors2 = comma.join(mainarray[author][parblock][pid2][rawauthorslabel])
                            presentingauthors1 = comma.join(mainarray[author][parblock][pid1][presentingauthorslabel])
                            presentingauthors2 = comma.join(mainarray[author][parblock][pid2][presentingauthorslabel])
                            newrow += [severity, author, message, parblock,pid1, session1, pid2, session2]
                            newrow += [author1n, outof1, presentingauthors1, author2n, outof2, presentingauthors2,
                                       rawauthors1, rawauthors2]
                            outdata.append(newrow)

               doneset.add(pid1)

    # write the outheader and outdata to  an Excel output file

    wb = mkworkbook(options.outfullname, [outheader], outdata, freeze_panes=(1,0))
    wb.close()

    junk = 0


if __name__ == '__main__':
    simauthors()