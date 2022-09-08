import numpy as np
import copy

import visuals
import cube

class natselNN:
    def __init__(self):
        self.popSize = int
        self.hiddenAm = int
        self.elitePer = float
        self.breedPer = float
        self.mutateChance = float
        self.mutEff = int
        self.maxTurns = int
        self.gens = int

        self.streak = 0
        self.randAm = 1

        self.popFirst = np.empty(1)
        self.popSecond = np.empty(1)

    def startSelection(self, pop, hiddenLayers, ePer, bPer, mutCh, mutEf, maxT, genAm):
        self.popSize = pop
        self.hiddenAm = hiddenLayers
        self.elitePer = ePer
        self.breedPer = bPer
        self.maxTurns = maxT
        self.gens = genAm
        self.mutateChance = mutCh
        self.mutEff = mutEf

        self.createPop()
        baseCube = cube.cube()
        for n in range(genAm):
            elite = self.testPop(n)
            self.mutatePop(elite)


    def continueSelection(self):
        hi = 1

    def changeParams(self):
        hi = 0

    def createPop(self):
        self.popFirst = np.random.randn(self.popSize, self.hiddenAm, 55)
        self.popSecond = np.random.randn(self.popSize, 13, self.hiddenAm)

    def testPop(self, gen):
        baseCube = cube.cube()
        baseCube.randomCube(self.randAm)
        baseScore = baseCube.getScore()
        scores = np.zeros(self.popSize)
        moveList = np.zeros((self.popSize, self.maxTurns))
        futureMaxTurns = self.maxTurns
        for member in range(self.popSize):
            curCube = copy.deepcopy(baseCube)
            for curRound in range(self.maxTurns):
                cubeVector = np.append(curCube.state.reshape([54, 1]), [1])
                nodes = np.matmul(self.popFirst[member], cubeVector)
                move = np.argmax(np.matmul(self.popSecond[member], nodes))+1
                moveList[member, curRound] = move
                curCube = curCube.rotate(move)
                curScore = curCube.getScore()
                #if member == 0:
                    #visuals.showCube(curCube.state, gen, curRound+1)
                if curScore == 48:
                    curScore = 100+baseScore# curScore + self.maxTurns - curRound
                    #futureMaxTurns = min(self.maxTurns, curRound + 5)
                    break
            scores[member] = curScore - baseScore
        self.maxTurns = futureMaxTurns
        sortedPop = np.flip(np.argsort(scores))
        elite = sortedPop[0: int(self.elitePer * self.popSize)]
        print('\ngeneration: ' + str(gen+1) + '  (' + str(self.randAm) + ') \nscore: ' + str(int(max(scores))) + '   moves: ' + str(moveList[np.argmax(scores), :]))
        print(np.matmul(self.popSecond[member], nodes).astype(int))
        if max(scores) == 100:
            self.streak = self.streak + 1
        else:
            self.streak = 0

        if self.streak == 10:
            self.randAm = self.randAm + 1
            self.streak = 0

        return elite

    def mutatePop(self, elite):
        eliteAm = len(elite)
        breedAm = int(self.popSize * self.breedPer)
        newPop1 = np.empty([self.popSize, self.hiddenAm, 55])
        newPop2 = np.empty([self.popSize, 13, self.hiddenAm])

        for n in range(eliteAm):
            newPop1[n] = self.popFirst[elite[n]]
            newPop2[n] = self.popSecond[elite[n]]

        for n in range(breedAm):
            ances = np.random.randint(0, eliteAm, [2, 1])
            while ances[0] == ances[1]:
                ances = np.random.randint(0, eliteAm, [2, 1])

            parentFirst1 = self.popFirst[elite[ances[0]]].reshape(self.hiddenAm * 55)
            parentFirst2 = self.popFirst[elite[ances[1]]].reshape(self.hiddenAm * 55)
            child = np.empty(len(parentFirst1))
            for geneNum in range(len(parentFirst1)):
                chrom = np.random.randint(1, 3)
                if chrom == 1:
                    child[geneNum] = parentFirst1[geneNum]
                if chrom == 2:
                    child[geneNum] = parentFirst2[geneNum]
            newPop1[n + eliteAm] = child.reshape((self.hiddenAm, 55))

            parentSecond1 = self.popSecond[elite[ances[0]]].reshape(13 * self.hiddenAm)
            parentSecond2 = self.popSecond[elite[ances[1]]].reshape(13 * self.hiddenAm)
            child = np.empty(len(parentSecond1))
            for geneNum in range(len(parentSecond1)):
                chrom = np.random.randint(1, 3)
                if chrom == 1:
                    child[geneNum] = parentSecond1[geneNum]
                if chrom == 2:
                    child[geneNum] = parentSecond2[geneNum]
            newPop2[n + eliteAm] = child.reshape((13, self.hiddenAm))

        for n in range(self.popSize - eliteAm - breedAm):

            childFirst = self.popFirst[elite[np.random.randint(eliteAm)]].reshape(self.hiddenAm * 55)
            childSecond = self.popSecond[elite[np.random.randint(eliteAm)]].reshape(13 * self.hiddenAm)

            for gene in range(len(childFirst)):
                if abs(np.random.randn()) <= self.mutateChance:
                    childFirst[gene] = childFirst[gene] + np.random.randn() * self.mutEff


            for gene in range(len(childSecond)):
                if abs(np.random.randn()) <= self.mutateChance:
                    childSecond[gene] = childSecond[gene] + np.random.randn() * self.mutEff

            newPop1[n + eliteAm + breedAm] = childFirst.reshape(self.hiddenAm, 55)
            newPop2[n + eliteAm + breedAm] = childSecond.reshape(13, self.hiddenAm)

        self.popFirst = newPop1
        self.popSecond = newPop2


network = natselNN()
# self, pop, hiddenLayers, ePer, bPer, mutCh, mutEffect, maxT, genAm
network.startSelection(1000, 25, .1, .2, .01, 2, 50, 100000)
