# simauthors
Software to find potential conflicts for authors when presenting papers or posters in parallel sessions in a conference. It can also be used to detect potential conflicts between author and persons with a special role in a session, such as the chair, technical assistance, etc. See the section [*Special roles*](#special-roles)

Note that it can only suggest plausible conflicts but it cannot guarantee that all conflicts will be detected.

The software can only detect potential conflicts, it can**NOT** resolve them, and it can**NOT** create a conference programme without (or with the least number of) conflicts.

> We use the term *program* for a piece of software and the term *programme* for a conference programme

This program is needed because proper names are natural language objects and thus show many of the problems when one tries to use natural language for effective communication (for which it is, mildly put, not optimal). In particular, a major problem is that a lot of variation is allowed. This program would be a lot simpler and perhaps even unnecessary if author identifiers were in use. See section [*Author identifiers*](#author-identifiers)


# Global Procedure

The procedure that the *simauthors* software supports is as follows:
1. The programme committee makes a conference programme. It stores it in a file as described in the section [*Presuppositions*](#presuppositions)
2. The *simauthors* program is run to detect potential author conflicts
3. The programme committee annotates the output of the *simauthors* program and identifies the real conflicts. If no conflicts are found, the procedure stops. 
4. The programme committee  revises the program to avoid the identified conflicts. and repeats the procedure from item *2*. 

Note that there is no guarantee that all conflicts can be resolved and thus no guarantee that this procedure stops. 

In most cases one can only take into account conflicts with the first or second author of a paper. In some cases the authors have indicated that the presenter will be a specific author. One can specify this in the conference programme file. (See the [*Presenters*](#presenters) section).

In cases where not all conflicts can be resolved, the programme committee has to make a decision to finalise the conference programme. 

# Presuppositions

It is assumed that the conference consists of one or more of *blocks*. Each block consist of one or more *session slots*. A *session slot* can contain one or more *session*s (multiple sessions especially in the case of posters and demos). A *session*  is a list of *presentations* (e.g. oral presentations, posters, demonstrations) based on an accepted submission (paper) of one or more *authors*. Each presentation requires the presence of at least one of the authors. 

If a block consists of multiple session slots, these session slots occur in parallel and the block is a *parallel block* (abbreviated as *parblock*).

Each parallel block and each session slot  must have a unique identifier to be assigned by the program committee.
Each submission must have a unique identifier.

The programme committee must create an Excel workbook in which it defines the program, and this Excel workbook must contain a worksheet with all and only the accepted submissions and with at least the following columns:

* *paperid*: unique id of the accepted submission
* *sessionslotid*: unique id of the session slot in which the presentation will be held
* parblock: the id of the parallel block that the session slot *sessionslotid* belongs to
* *authors*: the authors of the submission. This is a string that contains the author names separated from each other by comma or *" and "* 


One can specify the (zero-based!) column numbers of these columns in the file parameters.py. The header labels of these columns can have any value.

Any number of other columns can be present in the file. 

Such a file can be created by export from the START conference management system by adding columns for *sessionslotid* and *parblock* (*paperid* and *authors* are present in such files.

> Usually the parblock is uniquely determined by the session slot id. In the past we added parblocks automatically in the programme file by an Excel formula that looked up the parblock for a session slot in a table in a separate sheet. This is necessary anyway to generate different formats of the program after it has been established from this file. But it would nevertheless be desirable to be able to specify such a mapping table in a separate file. That is currently not the case. 

## Presenters

> *Warning*: this is a new feature of the 2024 version, and has not yet been tested extensively

The input file may also have an additional colum:

* *Presenters*: here one can list the author index(es) of the presenter(s) of the paper. If there are multiple, they must be separated by *semicolon*. 

The *author index* is an integer (1-based) that specifies the position of the author in the author list. Thus the first author has author index 1, the second 2, the eighth 8, etc. 

This is useful if the authors have specified who is/are going to present the paper (especially if they are not the first or second author of the paper).

The computation of potential conflicts is then done on the basis of a *presenting authors list*, which contains the presenters, followed by the other authors in the original order.

# Dependencies

The *simauthors* program requires the following modules:

* openpyxl
* XlsxWriter

They can be installed in the usual way:

```commandline
pip install openpyxl
pip install XlsxWriter
````

# Basic Usage

For basic usage one runs the program *simauthors.py* on the commandline with two parameters

* -f \<input filename\> (a MS Excel file)
* -s sheetname (if absent the active worksheet will be selected)

The program reads the data in the sheet with name *sheetname* in the input file.

It is presupposed that the top row of the sheet is  a header.

## The output generated

The program generates an output file that is called *authoranalysis.xlsx* (other names can be specified via parameters). This is a MS Excel workbook with a single worksheet that contains the following columns:

* *Comment1*: initially empty, a column to make annotations (see below))
* *Comment2*: initially empty, a column to make annotations (see below))
* *RawAuthor1*: the name of an author for which there potentially is a conflict
* *Rawauthor2*: the name of the author that the conflict is with. This is often the same name as *RawAuthor1* , but it might also be a variant of the *RawAuthor1* name (e.g. *J. Doe* instead of *John Doe*, or *Hans Schaeffer* instead of *Hans Schäffer*), but it might also be the name of a person with the same family name but with a different first name (e.g. *Arturo Calvo* v. *Adela Martinez Calvo*), These most probably refer to two different persons. See the section [*Comparing Names*](#comparing-names) for more details.
* *Severity*: the severity of the conflict: can be 
  * *Message*: if the conflict arises within the same session
  * *Warning*: if the conflict arises between two different sessions in the same parblock
* *Author*: a version of the family name of the authors that led to the identification of a potential conflict. It differs from the original family name (= usually the last token in the full name) in several respects as described in [*Comparing Names*](#comparing-names).
* *Message*: a message that describes the potential conflict
* *Parblock*: the parblock id that it concerns
* *PID1*: the paper id of the first paper
* *Session1*: the session id of the paper with id *PID1*
* *PID2*: the paper id of the second paper
* *Session2*: the session id of the paper with id *PID2*
* *Nth Author1*: the index of the author in the list of presenting authors for *PID1* (e.g. first author = 1, second author = 2, ... eight author = 8, etc.). This is interesting information because a conflict between two authors who are e.g. 7th and 8th author is not very problematic. In the past we tried to avoid conflicts only for the first and the second author.
* *Out of1*: the number of authors of paper *PID1* 
* *Presenting Authors1*: a string with the comma-separated  authors of *PID1* in *presenter order*
* *Nth Author2*: the index of the author in the list of authors for *PID2* 
* *Out of2*: the number of authors of paper *PID1* 
* *Presenting authors2*: a string with the comma-separated  authors of *PID1* in *presenter order*
* *Raw Authors1*: the original string with authors for paper *PID1* 
* *Raw Authors2*: the original string with authors for paper *PID2* 

One can inspect this file to identify real conflicts. The MS Excel sheet has AutoFilter on, so one can easily select e.g. only the warnings.  

## Annotating the *authoranalysis* file

It is recommended though not necessary to annotate the *authoranalysis* file. Making annotations will make it easier to identify real conflicts and may save time in later runs in the global procedure.

Annotating is done as follows: 

* Save a copy of the *authoranalysis.xlsx* under the name *authoranalysis-annotated.xlsx*. 
* Add annotations to the latter file by editing the columns with header *Comment1* and *Comment2*. 
  * It is recommended to use the *Comment1* column for a limited number of keywords so that one can easily select for them. 
  * The *Comment2* column can be used to clarify the keyword selected in the *Comment1* column.

In many cases one only has to annotate those entries that are not actually a conflict. Then the only keyword for *Column1* is *no problem*. Potential conflicts can be non-conflicts for many reasons. We list the most frequent ones here:

* *different first name*: the authors are actually two different authors because they have different first names
*  *high author index(es)*: the potential conflict is not important because  the author indexes of at least one of the conflicting authors is high (> 2)


Making such annotations allows one to easily select the potential conflicts that really are conflicts.

The programme committee must now come up with  different conference programme that avoids the conflicts observed, and then run the *simauthors* program again (see the section [*Global procedure*](#global-procedure)). If any of the potential conflicts that have already been annotated reappears the annotations made will reappear as well, so that these do not have to be looked into again.   

The annotations are stored in a file called *comments.txt*. Remove it when you start a programme for a new conference. 

# Special roles

The *simauthor* program can also be used to detect potential conflicts for people with special roles in a section such as a chair, technical assistants, etc. This can be done by creating a new row in the conference programme file, with parblock and sessionslot filled,   with the names of these persons in the authors column and  an arbitrary id in the paperid column (e.g. *O13_chair*). The title column can contain the word *Chair*.
The example file contains these for chairs from row 757.

# Comparing names

Names are compared as follows:
* First the family name is identified. This is usually the last token in the full name
* The family name is normalized
  * diacritics are removed from characters by removing the non spacing marks after  normalisation to  the Unicode NFD norm 
  * certain non-ascii characters are replaced by common  variants consisting of multiple ASCII symbols (e.g. *ä* is replaced by *ae*)

The first and middle names are ignored because taking them into account will lead to missing potential conflicts. 

## Exceptions

Name variants that cannot be dealt with by the procedure described above can be added to the exception file *exceptions.txt* with their substitutions. This is a tab-separated value file without a header.

The script *detectvariants.py* can be used to analyse the names in the conference programme file and entries for the exception file might be detected in this way.

## The script *detectvariants*

The *detectvariants* script analyses all names in the conference programme file. It compares each name to each other name, and categorizes the name pairs in a number of classes. We list these classes here and illustrate with examples from the LREC 2016 program file.

* the normalized names differ significantly both for the family name and the rest of the name and are considered to be names of different persons. This is the majority and they are not reported in the output 
* in the two names the normalized family names differ slightly: one name is most likely a variant of the other. The most frequent one is considered the correct one. Such examples should be added to the exception dictionary.
  * ('bhattacharya', ('pushpak',)) v. ('bhattacharyya', ('pushpak',)) (2 v. 4)
*  in the two names the normalized family names differ slightly: the two names are variants. They have the same frequency, so it is unclear which of these, if any,  is the correct one. Such examples should be added to the exception dictionary.
  * ('mititelu', ('verginica', 'barbu')) v. ('mitetelu', ('verginica',)) (1 == 1)
* in the two names the normalized family names are identical, but the rests of the names differ significantly. The two names most likely refer to different persons. This list must be checked thoruoghly to see whether n=i contains no variants of the same name.
   *  ('zhang', ('yue',)) v. ('zhang', ('ziqi',))
*  in the two names the normalized family names are identical, but the rests of the names differ slightly. the two names are most likely variants
   * ('mccrae', ('john', 'philip')) v. ('mccrae', ('john',))

The program writes the  output to a file called *name_analysis.txt*.

The program mostly works with relative edit distance (Levenshtein distance) to compare names.

> *Relative edit distance* is edit distance divided by the maximum of the lengths of the compared sequences.

It has set thresholds to determine the difference between "differing significantly" v. "differing slightly".
It is important to detect as many potential variants as possible. For example, with the current settings the program finds these as variants:
* ('zhang', ('xiaojun',)) v. ('zhang', ('jiajun',))

It is not certain that this is correct, but it is safer to treat them as variants of the same person than as two different persons.


The program has special measures to deal with:
* missing names in case of multiple non family names. Thus, these are considered  variants:
  *  ('clergerie', ('eric', 'villemonte', 'de', 'la')) v. ('clergerie', ('eric', 'de', 'la')) 
* abbreviated first names(initials) v. full first names also lead to variants (if not too different in other respects)
   *   ('gaizauskas', ('r.',)) v. ('gaizauskas', ('robert',))


##  Parameters of *detectvariants*

The following parameters are used in the script:

* initialscore = 0.1. the relative edit distance of an initial and a  full name starting with the initial's first character is set to this value.
* scorethreshold = (0.3, 0): two names are considered names of different persons if the relative edit distance of the family names has a difference of at least the first value of this tuple and the relative edit distance of the rests of the names are at least the second value in this tuple.  
* restscorethreshold = 0.3: the non-familynames are considered significantly different if the relative edit distance of the non-familynames is at least this value
* missingnames_score = 0.1. if there are missing names, the script gives this value as relative edit distance .
* missingnames_factor = 0.5. The number of missing name parts in a name must be less than this factor times the length of the name parts of the other name. 

These values have been set experimentally. They may have to be adapted for other conference programs.

> Note that the variants of the names we encountered here actually occur as different entries in the LREC 2016 proceedings if the papers were accepted, e.g.  (http://www.lrec-conf.org/proceedings/lrec2016/authors.html), for *Bhattacharyya* / *Bhattacharya*

# Full parameter overview

@@to be added@@

# Author identifiers

As stated before, systematic use of author identifiers would avoid many of the problems that a programme commitee is currently faced with. There are several author identifiers systems that are independent of specific conferences, international open ones such as e.g. ORCID, commercial ones such as ResearcherID, and national ones such as DAI (in the Netherlands). The problems with such systems are

* not every author has such an author ID
* even if they have it they have to enter it and make no mistakes with it

Perhaps a simpler and better solution is that the conference management system assigns author ids. This requires that *every* author is registered in the conference management system (not just the submitting author), but that should not be too difficult because almost every author is a submitting author in time. But it also requires checks when researchers register under different affiliations, e-mailaddresses and different  variants of their names. 

# Desired Extensions

* score to indicate plausibility of realness of the potential conflict
* proper dealing with name suffixes such as I, II, III, junior, senior
* specification of a session slot - parblock mapping in an external file.
* support for author identifiers

# Issues

Some Excel sheets cause the *openpyxl* module to report a warning:

```
UserWarning: Unknown extension is not supported and will be removed
  warn(msg)
````
This warning does not affect the functioning of the program. See https://stackoverflow.com/questions/54976991/python-openpyxl-userwarning-unknown-extension-issue

# History

The first version of  this program was written around 2006 as a batch file calling multiple scripts in a pipeline. The scripts were written  in a commercial version of AWK called Thomson AWK (TAWK, see http://www.tasoft.com/tawk.html). An upgraded version (V2.0) was made around 2014.  

The current Python version is a translation of the batch of awk scripts into a small number of Python modules. It was written in April 2024.

# Author
Jan Odijk, Utrecht University j.odijk@uu.nl

# License

BSD 3-Clause License. See separate LICENSE document.