from cleanauthors import deaccent


teststr = "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"

for char in teststr:
    result = deaccent(char)
    print(char,result)

result = deaccent(teststr)
print(len(teststr), len(result))
print(result)