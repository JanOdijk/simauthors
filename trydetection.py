from detectvariants import getrestnamescore, expandinitials


testtuples = [(['john', 'f.', 'robert', 'bobby'],
               ['j.', 'fitgerald', 'r', 'bob']),
              (['r.'], ['robert']),
              (['gregoire'], ['gregoire', 'de'])]

def tryme():
    for rn1, rn2 in testtuples:
        newrn1 = expandinitials(rn1, rn2)
        newrn2 = expandinitials(rn2, rn1)
        print(f'{rn1} + {rn2} ==>\n {newrn1} + {newrn2}')

    for rn1, rn2 in testtuples:
        result = getrestnamescore(rn1, rn2)
        print(f'{rn1} v. {rn2}: {result}')

if __name__ == '__main__':
    tryme()