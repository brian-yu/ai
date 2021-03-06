import sys
from random import randint

cellPaths = {}
for i in range(64):
    paths = [[] for j in range(8)]
    for j in range(64):
        jrow = int(j/8)
        jcol = j%8
        irow = int(i/8)
        icol = i%8
        #same row to the right
        if jrow == irow and jcol > icol:
            paths[1].append(j)
        #same col upward
        elif jcol == icol and jrow > irow:
            paths[2].append(j)
        #diagonals
        elif abs(jrow - irow) == abs(jcol - icol):
            #SW
            if jrow > irow and jcol < icol:
                paths[6].append(j)
            #SE
            if jrow > irow and jcol > icol:
                paths[7].append(j)
        k = abs(j-63)
        krow = int(k/8)
        kcol = k%8
        irow = int(i/8)
        icol = i%8
        #same row to the left
        if krow == irow and kcol < icol:
            paths[0].append(k)
        #same col downward
        elif kcol == icol and krow < irow:
            paths[3].append(k)
        #diagonals
        elif abs(krow - irow) == abs(kcol - icol):
            #NW
            if krow < irow and kcol < icol:
                paths[4].append(k)
            #NE
            if krow < irow and kcol > icol:
                paths[5].append(k)
    paths = [path for path in paths if path]
    cellPaths[i] = paths

oppositeSide = {"X": "O", "O":"X"}

i = [i for i in range(64)]
rl = [pos for arr in [[j for j in range(64) if j%8 == abs(i-7)] for i in range(8)] for pos in arr]
rr = [pos for arr in [[abs(j-63) for j in range(64) if abs(j-63)%8 == i] for i in range(8)] for pos in arr]
r2 = [pos for arr in [[abs(j-63) for j in range(64) if int(abs(j-63)/8) == abs(i-7)] for i in range(8)] for pos in arr]
fx = [pos for arr in [[j for j in range(64) if int(j/8) == abs(i-7)] for i in range(8)] for pos in arr]
fy = [pos for arr in [[abs(j-63) for j in range(64) if int(abs(j-63)/8) == i] for i in range(8)] for pos in arr]
fd = [pos for arr in [[abs(j-63) for j in range(64) if abs(j-63)%8 == abs(i-7)] for i in range(8)] for pos in arr]
fo = [pos for arr in [[j for j in range(64) if int(j%8) == i] for i in range(8)] for pos in arr]

trans = {"i":i, "rl":rl, "rr":rr, "r2":r2, "fx":fx, "fy":fy, "fd":fd, "fo":fo}

def findPossible(board, side):
    global cellPaths, oppositeSide

    opposite = oppositeSide[side]
    allPos = [pos for pos in range(64) if board[pos] == side]
    possible = set()

    for pos in allPos:
        for path in cellPaths[pos]:
            valid = False
            for pathPos in path:
                if board[pathPos] == opposite:
                    valid = True
                    continue
                elif board[pathPos] == side:
                    break
                elif board[pathPos] == '.':
                    if valid:
                        possible.add(pathPos)
                    break
    return possible

def negascout(board, depth, alpha, beta, side):
    possible = {}
    possible['X'], possible['O'] = findPossible(board, 'X'), findPossible(board, 'O')
    opposite = oppositeSide[side]

    if depth == 0 or (len(possible['X']) == 0 and len(possible['O']) == 0):
        return board.count(side)
    first = True
    for pos in possible[side]:
        child = flipBoard(board, pos, side)
        if first == True:
            first = False
            score = -negascout(child, depth-1, -alpha-1, -alpha, opposite)
            if alpha < score < beta:
                score = -negascout(child, depth-1, -beta, -alpha, opposite)
        else:
            score = -negascout(child, depth-1, -beta, -alpha, opposite)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return alpha

def alphabeta(board, depth, alpha, beta, onside, side):
    possible = {}
    possible['X'], possible['O'] = findPossible(board, 'X'), findPossible(board, 'O')
    opposite = oppositeSide[side]
    if depth == 0 or (len(possible['X']) == 0 and len(possible['O']) == 0):
        return board.count(side)
    if onside:
        v = float("-inf")
        for pos in possible[side]:
            child = flipBoard(board, pos, side)
            v = max(v, alphabeta(child, depth -1, alpha, beta, False, side))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float("inf")
        for pos in possible[opposite]:
            child = board[:pos] + opposite + board[pos+1:]
            v = min(v, alphabeta(child, depth-1, alpha, beta, True, side))
            beta = min(v, beta)
            if beta <= alpha:
                break
        return v

def nextMove(board, side, possible):

    movePos = None
    ab = {}
    for pos in possible:
        #child = board[:pos] + side + board[pos+1:]
        child = flipBoard(board, pos, side)
        ab[pos] = alphabeta(child, 4, float("-inf"), float("inf"), True, side)
    movePos = max(ab.keys(), key=(lambda key: ab[key]))
    return movePos

def flipBoard(board, move, side):
    opposite = oppositeSide[side]
    board = board[:move] + side + board[move+1:]
    flip = []
    paths = [path for path in cellPaths[move] if board[path[0]] == opposite]
    for path in cellPaths[move]:
        temp = []
        valid = False
        for pos in path:
            if board[pos] == '.':
                break
            elif board[pos] == side:
                valid = True
                break
            else:
                temp.append(pos)
        if valid:
            flip += temp
    for pos in flip:
        board = board[:pos] + side + board[pos+1:]

    return board

board = sys.argv[1]
side = sys.argv[2]

print(nextMove(board,side,findPossible(board, side)))