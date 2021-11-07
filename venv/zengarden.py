import numpy as np
import time
import random as rd
from copy import deepcopy

M, N = 12, 14
garden = np.zeros((M, N), dtype=int).astype(str)
rocks = 6
paveNum = 0
generations = 1

moveGenes = ['l', 'r']


class Monk():
    def __init__(self, state, fitness, starts, moves, generation):
        self.state = state
        self.fitness = fitness
        self.starts = starts # list
        self.moves = moves # list
        self.generation = generation


def generateGarden():
    global garden
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

    return value


def initState(monk: Monk):
    pass


def initGen():
    generation = []
    maxGenes = (M-2) + (N-2) + rocks

    for i in range(100):
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


if __name__ == '__main__':
    main()