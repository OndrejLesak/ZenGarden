import numpy as np
import time
import random as rd
from copy import deepcopy
import re
import pandas

M, N = 12, 14
garden = np.zeros((M, N), dtype=int).astype(str)
rocks = 6
paveNum = 0
generations = 1

moveGenes = ['l', 'r']
blocked = []


class Monk():
    def __init__(self, state, fitness, starts, moves, generation):
        self.state = state
        self.fitness = fitness
        self.starts = starts # list
        self.moves = moves # list
        self.generation = generation


def generateGarden():
    global garden, blocked
    value = 1
    y, x = 0, 0

    # FRAME
    if y == 0 and x == 0:
        for x in range(N):
            if x == 0 or x == N-1:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == 0 and x == N-1:
        for y in range(M):
            if y == 0 or y == M-1:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == M-1 and x == N-1:
        for x in range(N-1, -1, -1):
            if x == N-1 or x == 0:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == M-1 and x == 0:
        for y in range(M-1, -1, -1):
            if y == M-1 or y == 0:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    # PUT STONES (temporarily)
    # rocksNum = rocks
    # while rocksNum != 0:
    #     y = int(rd.randrange(1, M-1))
    #     x = int(rd.randrange(1, N-1))
    #
    #     garden[y][x] = -1
    #     rocksNum -= 1

        garden[2][6] = -1
        garden[3][2] = -1
        garden[4][5] = -1
        garden[5][3] = -1
        garden[7][9] = -1
        garden[7][10] = -1

        # if re.search('^s', garden[y-1][x]):
        #     blocked.append(garden[y-1][x])
        # if re.search('^s', garden[y+1][x]):
        #     blocked.append(garden[y+1][x])
        # if re.search('^s', garden[y][x-1]):
        #     blocked.append(garden[y][x-1])
        # if re.search('^s', garden[y][x+1]):
        #     blocked.append(garden[y][x+1])

    return value


def setWay(x, y):
    if x + 1 >= N:
        return 'l'
    if x - 1 < 0:
        return 'r'
    if y + 1 >= M:
        return 'u'
    if y - 1 < 0:
        return 'd'

    return None


def check_up(state, x, y):
    if re.search('^s', state[y-1][x]):
        return state[y-1][x]
    return False


def check_down(state, x, y):
    if re.search('^s', state[y + 1][x]):
        return state[y + 1][x]
    return False


def check_right(state, x, y):
    if re.search('^s', state[y][x+1]):
        return state[y][x+1]
    return False


def check_left(state, x, y):
    if re.search('^s', state[y][x - 1]):
        return state[y][x - 1]
    return False


def rake(monk: Monk):
    used = set()
    pg = monk.state
    finished = 0
    cnt = 1

    for pos in monk.starts:
        if pos not in used or pos not in blocked:
            y, x = np.where(pg == pos)
            y = int(y)
            x = int(x)
            way = setWay(x, y)

            # while finished == 0:
            if way == 'd':
                while True:
                    y += 1
                    pg[y][x] = cnt

                    if pg[y+1][x] == '-1' or pg[y+1][x] != '0':
                        break
                    elif re.search('^s', pg[y+1][x]):
                        used.add(pg[y+1][x])
                        break

            if way == 'u':
                while True:
                    y -= 1
                    pg[y][x] = cnt

                    if pg[y - 1][x] == '-1' or pg[y - 1][x] != '0':
                        break
                    elif re.search('^s', pg[y - 1][x]):
                        used.add(pg[y - 1][x])
                        break

            if way == 'l':
                while True:
                    x -= 1
                    pg[y][x] = cnt

                    if pg[y][x-1] == '-1' or pg[y][x-1] != '0':
                        break
                    elif re.search('^s', pg[y][x-1]):
                        used.add(pg[y][x-1])
                        break
                        
            if way == 'r':
                while True:
                    x += 1
                    pg[y][x] = cnt

                    if pg[y][x + 1] == '-1' or pg[y][x + 1] != '0':
                        break
                    elif re.search('^s', pg[y][x + 1]):
                        used.add(pg[y][x + 1])
                        break

            cnt += 1

        else:
            continue

    return monk


def generation(n: int):
    generation = []
    maxGenes = (M-2) + (N-2) + rocks

    for i in range(n): # generate n monks
        monk = Monk(deepcopy(garden), 0, [], [], generations)

        # GENE GENERATION
        for i in range((maxGenes // 3)*2 - rd.randrange(0, 3)):
            gene = 's' + str(rd.randrange(1, paveNum))
            if gene in monk.starts:
                while gene in monk.starts:
                    gene = 's' + str(rd.randrange(1, paveNum))

            monk.starts.append(gene)

        # MOVEMENT GENES
        for i in range(rd.randrange(1, maxGenes - len(monk.starts))):
            move = rd.randrange(0, len(moveGenes))
            monk.moves.append(moveGenes[move])

        generation.append(monk)

    return generation

def main():
    global paveNum

    paveNum = generateGarden()
    print(garden)
    print(pandas.DataFrame(rake(generation(100)[0]).state))

if __name__ == '__main__':
    main()