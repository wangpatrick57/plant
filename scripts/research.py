#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *

# Check for consistency using mapList1 and mapList2.
def checkForConsistentEdges(edges1, edges2, mapping1):
    consistentEdges = 0
    counter = 0
    for i in edges1[0]:
        for j in edges2[0]:
            ui = i[0]
            uj = i[1]
            vi = j[0]
            vj = j[1]
            if (((ui, vi) in mapping1 and (uj, vj) in mapping1) or ((ui, vj) in mapping1 and (uj, vi) in mapping1)):
                consistentEdges += 1
            counter += 1
    return consistentEdges

def addEdges(nameResult, lines1):
    numEdges = 0
    edges1 = set()
    for i in nameResult:
        if(i[0] in lines1 and i[1] in lines1):
            numEdges += 1
            edges1.add((i[0], i[1]))
    return [edges1, numEdges]

def organizeIntoList(fileName):
    openedFile = open(fileName, 'r')
    lines = []
    for line in openedFile:
        lines.append(map(str, line.strip().split()))
    openedFile.close()
    tempResult = list(map(list, zip(*lines)))
    tempResult1 = set()
    counter = 0
    for i in tempResult[0]:
        tempResult1.add((i,tempResult[1][counter]))
        counter += 1
    return list(tempResult1)

def firstAndSecondPass(res):

    dupeValues1 = dict()
    dupeValues2 = dict()
    finalList = list()

    initialCounter = 0
    for i in res[0]:
        if i != "0" and res[1][initialCounter] != "0":
            if i in dupeValues1:
                dupeValues1[i] += 1
            else: 
                dupeValues1[i] = 1
            if res[1][initialCounter] in dupeValues2:
                dupeValues2[res[1][initialCounter]] += 1
            else: 
                dupeValues2[res[1][initialCounter]] = 1
        initialCounter += 1
        secondInitialCounter = 0
    for i in res[0]:
        if i != "0" and res[1][secondInitialCounter] != "0":
            if not(dupeValues1[i] > 1 or int(dupeValues2[res[1][secondInitialCounter]]) > 1):
                finalList.append((i, res[1][secondInitialCounter]))
        secondInitialCounter += 1
    
    return finalList

def filter(name):

    finalList = list()

    tempResult = organizeIntoList(name)

    newLines = []
    for i in tempResult:
        newLines.append(map(str, i))
    result = list(map(list, zip(*newLines)))

    finalList = firstAndSecondPass(result)

    return finalList

# ----------------------------------------------------------------------------

mouseResult2 = organizeIntoList(get_graph_path('mouse'))
ratResult2 = organizeIntoList(get_graph_path('rat'))

mapping = filter("seeds.out")
mapping1 = set(mapping)
lines1 = set()
lines2 = set()
for i in mapping:
    lines1.add(i[0])
    lines2.add(i[1])

edges1 = addEdges(mouseResult2, lines1) # left valid edges
edges2 = addEdges(ratResult2, lines2) # right valid edges

consistentEdges1 = checkForConsistentEdges(edges1, edges2, mapping1)
totalConsistency = float(consistentEdges1) / max(edges1[1], edges2[1])

print("Edge consistency: " + str(totalConsistency))
