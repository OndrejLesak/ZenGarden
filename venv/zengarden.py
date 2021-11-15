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
        self.starts = starts  # list
        self.moves = moves  # list
        self.generation = generation


def fitSort(k):
    return k.fitness


def generateGarden():
    global garden, blocked
    value = 1
    y, x = 0, 0

    # FRAME
    if y == 0 and x == 0:
        for x in range(N):
            if x == 0 or x == N - 1:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == 0 and x == N - 1:
        for y in range(M):
            if y == 0 or y == M - 1:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == M - 1 and x == N - 1:
        for x in range(N - 1, -1, -1):
            if x == N - 1 or x == 0:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    if y == M - 1 and x == 0:
        for y in range(M - 1, -1, -1):
            if y == M - 1 or y == 0:
                continue
            else:
                garden[y][x] = 's' + str(value)
                value += 1

    # de-represent corners
    garden[0][0] = ''
    garden[0][N-1] = ''
    garden[M-1][0] = ''
    garden[M-1][N-1] = ''

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

        # put starting postiions blocked by stones in blocked
        # if garden[y-1][x][0] == 's':
        #     blocked.append(garden[y-1][x])
        # if garden[y+1][x][0] == 's':
        #     blocked.append(garden[y+1][x])
        # if garden[y][x-1][0] == 's':
        #     blocked.append(garden[y][x-1])
        # if garden[y][x+1][0] == 's':
        #     blocked.append(garden[y][x+1])

    return value


def generation(n: int):
    generation = []
    maxGenes = (M - 2) + (N - 2) + rocks
    startGenes = (maxGenes // 3) * 2 - rd.randrange(0, 3)

    for i in range(n):  # generate n monks
        monk = Monk(deepcopy(garden), 0, [], [], generations)

        # SATRTING POSITION GENE GENERATION
        for i in range(startGenes):
            gene = 's' + str(rd.randrange(1, paveNum))
            if gene in monk.starts and gene not in blocked:
                while gene in monk.starts and gene not in blocked:
                    gene = 's' + str(rd.randrange(1, paveNum))

            monk.starts.append(gene)

        # MOVEMENT GENES
        for i in range(rd.randrange(1, maxGenes - len(monk.starts))):
            move = rd.randrange(0, len(moveGenes))
            monk.moves.append(moveGenes[move])

        generation.append(monk)

    return generation


def setWay(x, y): # sets the initial direction of the monk
    if x + 1 >= N:
        return 'l'
    if x - 1 < 0:
        return 'r'
    if y + 1 >= M:
        return 'u'
    if y - 1 < 0:
        return 'd'
    return None


def check_first(state, direction, x, y):
    if direction == 'd':
        if str(state[y+1][x]) == '0': return 1
    elif direction == 'u':
        if str(state[y - 1][x]) == '0': return 1
    elif direction == 'r':
        if str(state[y][x+1]) == '0': return 1
    elif direction == 'l':
        if str(state[y][x-1]) == '0': return 1
    return 0


def check_border(x, y):
    if x > N-1 or x < 0 or y > M-1 or y < 0:
        return 0
    return 1


def check(state, x, y):
    if (x < N-1 and x >= 0) and (y < M-1 and y >= 0):
        if state[y][x][0] == 's' or str(state[y][x]) == '0':
            return 1
    return 0


def rake(monk: Monk):
    used = set()
    direction = None
    pg = monk.state
    cnt = 1
    moveOrd = 0
    monk.fitness = (M - 2) * (N - 2) - rocks # initial fitness (all the available zeros)

    for pos in monk.starts:
        if pos not in used:
            y, x = np.where(pg == pos) # get coordinates
            x, y = int(x), int(y)
            direction = setWay(x, y)


            if check_first(pg, direction, x, y):  # check whether first tile is free

                while True:
                    if direction == 'd': # down
                        if not check_border(x, y+1):
                            break

                        y += 1
                        if pg[y][x][0] == 's':
                            used.add(pg[y][x])
                            break
                        if str(pg[y][x]) != '0': # add y-1 condition if starting position
                            y -= 1
                            if check(pg, x+1, y) and check(pg, x-1, y):
                                direction = monk.moves[moveOrd]
                                moveOrd += 1
                                if moveOrd >= len(monk.moves): moveOrd = 0
                                continue
                            elif check(pg, x+1, y): direction = 'r'
                            elif check(pg, x-1, y): direction = 'l'
                            else: return monk # if stuck
                            continue

                    elif direction == 'u': # up
                        if not check_border(x, y-1):
                            break

                        y -= 1
                        if pg[y][x][0] == 's':
                            used.add(pg[y][x])
                            break
                        if str(pg[y][x]) != '0':
                            y += 1
                            if check(pg, x+1, y) and check(pg, x-1, y):
                                direction = monk.moves[moveOrd]
                                moveOrd += 1
                                if moveOrd >= len(monk.moves): moveOrd = 0
                            elif check(pg, x + 1, y): direction = 'r'
                            elif check(pg, x - 1, y): direction = 'l'
                            else: return monk # if stuck
                            continue

                    elif direction == 'r': # right
                        if not check_border(x+1, y):
                            break

                        x += 1
                        if pg[y][x][0] == 's':
                            used.add(pg[y][x])
                            break
                        if str(pg[y][x]) != '0':
                            x -= 1
                            if check(pg, x, y-1) and check(pg, x, y+1):
                                direction = 'u' if monk.moves[moveOrd] == 'r' else 'd'
                                moveOrd += 1
                                if moveOrd >= len(monk.moves): moveOrd = 0
                            elif check(pg, x, y-1): direction = 'u'
                            elif check(pg, x, y+1): direction = 'd'
                            else: return monk # if stuck
                            continue

                    elif direction == 'l': # left
                        if not check_border(x-1, y):
                            break

                        x -= 1
                        if pg[y][x][0] == 's':
                            used.add(pg[y][x])
                            break
                        if str(pg[y][x]) != '0':
                            x += 1
                            if check(pg, x, y - 1) and check(pg, x, y + 1):
                                direction = 'u' if monk.moves[moveOrd] == 'r' else 'd'
                                moveOrd += 1
                                if moveOrd >= len(monk.moves): moveOrd = 0
                            elif check(pg, x, y - 1): direction = 'u'
                            elif check(pg, x, y + 1): direction = 'd'
                            else: return monk # if stuck
                            continue

                    pg[y][x] = cnt
                    monk.fitness -= 1
                cnt += 1

    return monk


def evolve(population):
    totalFit = 0

    # ASCENDING SORT OF THE POPULATION
    population.sort(key=fitSort)

    # TOTAL POPULATION FITNESS
    for monk in population:
        totalFit += monk.fitness

    return totalFit


def main():
    global paveNum

    paveNum = generateGarden()
    print(pandas.DataFrame(garden))
    monks = generation(100)

    for monk in monks:
        rake(monk)

    print(evolve(monks))

if __name__ == '__main__':
    main()