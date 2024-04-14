from detectvariants import isnoncontsublist
import itertools

list1 = ['b', 'd']
list2 = ['a', 'b', 'c', 'd', 'e']
list3 = list2 + ['f', 'g']

permutations =[itertools.permutations(list3, i) for i in range(len(list3))]

for permutation in permutations:
    for tpl in permutation:
        list1 = list(tpl)
        result = isnoncontsublist(list1, list2)
        if result:
            print(list1, list2, result)

junk =0