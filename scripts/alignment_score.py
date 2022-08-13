import sys
import os

def scrape_input(path: str, delim: str = " ", get_nodes: bool = False)-> list: 
    file = open(path, "r")
    lines = file.readlines()
    rlist = []
    for line in lines:
        if get_nodes:
            rlist.extend(
                line.strip("\n").split(delim)[1:] # get all the nodes and discard the index value
            )
        else:
            rlist.append(
                line.strip("\n").split(delim)[0] # only get index value
            )
    return rlist

def alignment_score(indexA: list, indexB: list, match: int, miss: int, gap: int):
    matrix = [[0]*(len(indexA) + 1) for i in range(0, len(indexB) + 1)] # empty matrix
    rowval = [x for x in indexB]
    rowval.insert(0, -1)
    colval = [x for x in indexA]
    colval.insert(0, -1)
    left = 0
    up = 0
    diag = 0
    
    # create matrix for all possibilites
    for i in range(0, len(indexB) + 1):
        for j in range(0, len(indexA) + 1):
            if rowval[i] == -1 and colval[j] == -1:
                matrix[i][j] = 0
            elif rowval[i] == -1 or colval[j] == -1:
                matrix[i][j] = gap*j if rowval[i] == -1 else gap*i
            else:
                left = matrix[i][j-1] + gap
                up = matrix[i-1][j] + gap
                diag = (match if rowval[i] == colval[j] else miss) + matrix[i-1][j-1]
                matrix[i][j] = max(left, up, diag)
    print_matrix(matrix)
    i = len(indexB)
    j = len(indexA)
    score = 0
    alist = []
    blist = []
    # start in bottom right corner and move up / left / diagonal
    while i >= 0 and j >= 0:
        left = matrix[i][j-1]
        up = matrix[i-1][j]
        diag = matrix[i-1][j-1]
        if (rowval[i] == colval[j]):
            score += match
            alist.append(colval[j])
            blist.append(rowval[i])
            i -= 1
            j -= 1
            # print("match")
        else:
            temp = sorted([left, up, diag], reverse=True)
            if temp[0] == up:
                alist.append("-")
                blist.append(rowval[i])
                i -= 1
                score += gap
                # print("up")
            elif temp[0] == left:
                alist.append(colval[j])
                blist.append("-")
                j -= 1
                score += gap
                # print("left")
            else:
                score += miss
                alist.append(colval[j])
                blist.append(rowval[i])
                i -= 1
                j -= 1
                # print("diag")
    alist.reverse()
    alist = alist[1:]
    blist.reverse()
    blist = blist[1:]

    # display alignment
    print(alist)
    print(blist)

    return score - 1


def print_matrix(matrix: list):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            end = "\n" if j == len(matrix[0]) - 1 else " "
            print(matrix[i][j], end=end)
        



if __name__ == "__main__":
    # pathA = sys.argv[1]
    # pathB = sys.argv[2]
    print(alignment_score(
        "A T G C T".split(" "),
        "A G C T".split(" "),
        match=1,
        miss=-1,
        gap=-2,
    ))
