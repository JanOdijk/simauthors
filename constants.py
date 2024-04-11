


newdata_authorcol = 0
newdata_rawauthorscol = 1
newdata_parblockcol = 2
newdata_sessioncol = 3
newdata_paperidcol = 4
newdata_cleanauthorscol = 5

# columns in the (commented) output files

comment1_l = "Comment1"
comment2_l = "Comment2"
rawauthor1_l = "RawAuthor1"
rawauthor2_l = "Rawauthor2"
severity_l = "Severity"
author_l =  "Author"
message_l = "Message"
parblock_l =  "Parblock"
pid1_l =  "PID1"
session1_l = "Session1"
pid2_l =  "PID2"
session2_l = "Session2"
nth_author1_l = "Nth Author1"
out_of1_l = "Out of1"
rawauthors1_l = "Raw Authors1"
nth_author2_l = "Nth Author2"
out_of2_l = "Out of2"
rawauthors2_l = "Raw Authors2"


outheader = [ comment1_l, comment2_l, rawauthor1_l, rawauthor2_l,severity_l,  author_l, message_l,  parblock_l,
           pid1_l, session1_l,  pid2_l, session2_l, nth_author1_l, out_of1_l, rawauthors1_l, nth_author2_l, out_of2_l,
              rawauthors2_l]

def getcol(label: str) -> int:
    result = outheader.index(label)
    return result
