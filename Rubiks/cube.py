import numpy as np
import copy

import visuals as vis


class cube:

    def __init__(self):
        self.state = np.array
        self.score = 0

    def getState(self):
        return self.state

    def randomCube(self, rotMax):
        vals = np.matmul(np.arange(0, 6, 1, int).reshape(6, 1), np.ones([1, 9], int))
        self.state = vals.reshape([6, 3, 3])
        rotations = rotMax #np.random.randint(1, rotMax+1)
        for n in range(rotations):
            side = ((2*n) % 13)+1 #np.random.randint(1, 13)
            self.rotate(side)
        self.getScore()

    def getScore(self):
        self.score = -6
        for n in range(6):
            self.score = self.score + np.bincount(self.state[n].reshape(9))[self.state[n, 1, 1]]
        return self.score

    def rotate(self, move):
        if move == 13:
            return self
        direc = 1
        for n in range(6):
            if move == 1:
                self.state[0] = faceClockwise(self.state[0])
                self.rowLeft()

            if move == 2:
                self.state[0] = faceCounterClockwise(self.state[0])
                self.rowRight()

            move = move - 2

            if direc == 1:
                self.orientateLeft()
            if direc == -1:
                self.orientateRight()

            direc = direc * -1

        return self

    def rowLeft(self):
        temp = copy.deepcopy(self.state[1, 0])
        self.state[1, 0] = copy.deepcopy(self.state[4, 0])
        self.state[4, 0] = copy.deepcopy(self.state[3, 0])
        self.state[3, 0] = copy.deepcopy(self.state[2, 0])
        self.state[2, 0] = temp

    def rowRight(self):
        temp = copy.deepcopy(self.state[1, 0])
        self.state[1, 0] = copy.deepcopy(self.state[2, 0])
        self.state[2, 0] = copy.deepcopy(self.state[3, 0])
        self.state[3, 0] = copy.deepcopy(self.state[4, 0])
        self.state[4, 0] = temp

    def orientateLeft(self):
        temp1 = copy.deepcopy(self.state[0])
        temp2 = copy.deepcopy(self.state[2])
        self.state[0] = faceClockwise(copy.deepcopy(self.state[1]))
        self.state[1] = faceClockwise(copy.deepcopy(self.state[4]))
        self.state[4] = faceClockwise(faceClockwise(temp1))
        self.state[2] = copy.deepcopy(self.state[5])
        self.state[5] = faceClockwise(copy.deepcopy(self.state[3]))
        self.state[3] = faceCounterClockwise(temp2)

    def orientateRight(self):
        temp1 = copy.deepcopy(self.state[0])
        temp2 = copy.deepcopy(self.state[3])
        self.state[0] = faceCounterClockwise(copy.deepcopy(self.state[1]))
        self.state[1] = faceCounterClockwise(copy.deepcopy(self.state[2]))
        self.state[2] = faceCounterClockwise(faceCounterClockwise(temp1))
        self.state[3] = faceClockwise(copy.deepcopy(self.state[4]))
        self.state[4] = copy.deepcopy(self.state[5])
        self.state[5] = faceCounterClockwise(temp2)


def faceClockwise(face):
    row1 = copy.deepcopy(face[0])
    row2 = copy.deepcopy(face[1])
    row3 = copy.deepcopy(face[2])

    face[:, 2] = row1
    face[:, 1] = row2
    face[:, 0] = row3

    return face


def faceCounterClockwise(face):
    row1 = copy.deepcopy(face[0])
    row2 = copy.deepcopy(face[1])
    row3 = copy.deepcopy(face[2])

    face[:, 0] = np.flip(row1)
    face[:, 1] = np.flip(row2)
    face[:, 2] = np.flip(row3)

    return face



#testCube = cube()
#for n in range(100):
#    testCube.randomCube(1)
#vis.showCube(testCube)