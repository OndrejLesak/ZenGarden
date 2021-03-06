import numpy as np
import time
import random as rd
from copy import deepcopy

# settings - replace with settings dictionary
M, N = 12, 14 # shape is always +2 for each axis due to outline of the garden (6x8 = 8x10)
rocks = 8
sample = 1
selection = 'TOURNAMENT'
mutateChance = 0.1
population_size = 100
max_generations = 300

# global variables
garden = np.zeros((M, N), dtype=int).astype(str)
paveNum = 0
gen = 1
ftp = None

# global structures
moveGenes = ['l', 'r']


class Monk():
    def __init__(self, state, fitness, starts, moves, generation, isStuck = False):
        self.state = state
        self.fitness = fitness
        self.starts = starts  # list
        self.moves = moves  # list
        self.generation = generation
        self.isStuck = isStuck


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
    garden[0][0] = ' '
    garden[0][N-1] = ' '
    garden[M-1][0] = ' '
    garden[M-1][N-1] = ' '

    if sample == 1:
        garden[2][6] = -1
        garden[3][2] = -1
        garden[4][5] = -1
        garden[5][3] = -1
        garden[7][9] = -1
        garden[7][10] = -1
    else:
        # PUT STONES (temporarily)
        rocksNum = rocks
        while rocksNum != 0:
            y = int(rd.randrange(1, M - 1))
            x = int(rd.randrange(1, N - 1))

            garden[y][x] = -1
            rocksNum -= 1

    return value


def generation(n: int):
    generation = []
    maxGenes = (M - 2) + (N - 2) + rocks
    startGenes = (maxGenes // 3) * 2 - rd.randrange(0, 3)

    for i in range(n):  # generate n monks
        monk = Monk(deepcopy(garden), 0, [], [], 1)

        # STARTING POSITION GENE GENERATION
        for i in range(startGenes):
            gene = 's' + str(rd.randrange(1, paveNum))
            if gene in monk.starts:
                while gene in monk.starts:
                    gene = 's' + str(rd.randrange(1, paveNum))

            monk.starts.append(gene)

        # MOVEMENT GENES
        for i in range((maxGenes - len(monk.starts)) // 2):
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
    monk.fitness = 0 # initial fitness (all the available zeros)

    for pos in monk.starts:
        if pos not in used:
            y, x = np.where(pg == pos) # get coordinate
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
                            else:
                                monk.fitness = int(monk.fitness * 0.2)
                                monk.isStuck = True
                                return monk # if stuck
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
                            else:
                                monk.fitness = int(monk.fitness * 0.2)
                                monk.isStuck = True
                                return monk # if stuck
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
                            else:
                                monk.fitness = int(monk.fitness * 0.2)
                                monk.isStuck = True
                                return monk # if stuck
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
                            else:
                                monk.fitness = int(monk.fitness * 0.2)
                                monk.isStuck = True
                                return monk # if stuck
                            continue

                    pg[y][x] = cnt
                    monk.fitness += 1
                cnt += 1

    return monk


def evolve(population):
    totalFit = 0
    stated = []
    newPopulation = []

    # ascending sort of the population
    population.sort(key=fitSort, reverse=True)

    if '0' not in population[0].state and not population[0].isStuck: # correct result check
        return population[0]

    # total population fitness
    for monk in population:
        totalFit += monk.fitness

    bestFit = population[0].fitness
    worstFit = population[-1].fitness
    average = totalFit/population_size

    wtf(bestFit, average, worstFit)

    # choose parents to be passed to the new generation
    parents = round(population_size * 0.1) + 5
    for i in range(parents):
        if selection == 'ROULETTE':
            newPal = roulette(population, totalFit)
            if newPal in newPopulation:
                while newPal in newPopulation:
                    newPal = roulette(population, totalFit)

        if selection == 'TOURNAMENT':
            newPal = tournament(population)
            if newPal in newPopulation:
                while newPal in newPopulation:
                    newPal = tournament(population)

        newPal.isStuck = False
        newPopulation.append(newPal)

    # cross-over chromosomes
    i = 0
    while i < parents-2:
        for j in range(i+1, parents-1):
            if len(newPopulation) >= population_size: break

            mutate = True if rd.random() <= mutateChance else False # can the next child mutate?
            newPal = geneCrossover(newPopulation[i], newPopulation[j], newPopulation, mutate)

            newPopulation.append(newPal)
        i += 1

    population.clear()
    for monk in newPopulation:
        if monk.fitness != 0:
            population.append(monk)
        else:
            population.append(rake(monk))

    return None


def geneCrossover(chromosome1, chromosome2, newPopulation, mutate = False):
    proportion_starts = rd.randint(1, (len(chromosome1.starts) // 2))
    proportion_moves = rd.randint(1, (len(chromosome1.moves) // 2))
    newStarts = chromosome1.starts[0: proportion_starts]
    newMoves = chromosome1.moves[0: proportion_moves] + chromosome2.moves[proportion_moves: len(chromosome2.moves)]

    for i in range(proportion_starts, len(chromosome2.starts)): # add part of the second chromosome
        if chromosome2.starts[i] in newStarts:

           for j in range(proportion_starts):
               if chromosome2.starts[j] not in newStarts:
                   newStarts.append(chromosome2.starts[j])
                   break
        else:
            newStarts.append(chromosome2.starts[i])

    newChrom = Monk(deepcopy(garden), 0, newStarts, newMoves, chromosome1.generation + 1)

    if mutate is True:
        for i in range(rd.randint(1, 2)):
            gene_to_mutate = rd.randint(0, len(newChrom.starts)-1)
            mutated = 's' + str(rd.randint(1, paveNum-1))

            if mutated == newChrom.starts[gene_to_mutate]: # if new mutation is the same as mutated gene
                while mutated == newChrom.starts[gene_to_mutate]:
                    mutated = 's' + str(rd.randint(1, paveNum-1))

        newChrom.starts[gene_to_mutate] = mutated
    return newChrom


def tournament(population):
    first = rd.randint(0, len(population)-1)
    second = rd.randint(0, len(population)-1)

    if first == second: # preventing from competing against itself
        while first == second:
            second = rd.randint(0, len(population)-1)

    if population[first].fitness > population[second].fitness:
        return population[first]
    else:
        return population[second]


def roulette(population, totalFit):
    ratio = rd.randint(0, totalFit)
    sum = 0

    for monk in reversed(population):
        sum += monk.fitness
        if sum >= ratio:
            return monk


def print_garden(zahrada):
    for i in range(M):
        for j in range(N):
            # Skaly
            if str(zahrada[i][j]) == '-1':
                print("\033[47m    \033[00m", end="")
            # Hranica zahrady
            elif zahrada[i][j][0] == 's':
                print("\033[43m    \033[00m", end="")
            # Pohrabane policka
            elif str(zahrada[i][j]) != '0':
                print("\033[92m{}\033[00m".format(zahrada[i][j].rjust(3, ' ')), end=" ")
            # Nepohrabane policka
            else:
                print(zahrada[i][j].rjust(3, ' '), end=" ")
        print()
    print()


def wtf(best, average, worst):
    print(f'{gen}\t{best}\t{average}\t{worst}', file=ftp)


def main():
    global paveNum, gen, ftp
    ftp = open('output.txt', 'w')
    ftp.close()

    ftp = open('output.txt', 'a')

    paveNum = generateGarden()

    print_garden(garden)
    monks = generation(population_size)

    for monk in monks:
        rake(monk)

    while gen <= max_generations:
        population = evolve(monks)
        if population != None:
            break

        gen += 1

    print_garden(monks[0].state)
    print(f'Generation: {gen-1}')

    ftp.close()

if __name__ == '__main__':
    main()