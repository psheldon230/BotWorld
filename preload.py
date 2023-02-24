import random
import math
class prel:
    def __init__(self):
        self.blockList = []
        self.jointList = []
        self.relativeBlock = []
        self.relativeJoint = []
        self.numBlocks = 9
        self.blockList.append(["Block0", [0, 0, 1], -1])
        self.generateCreature()
        self.convertToRelative()
        
    def generateCreature(self):
        for i in range(0, self.numBlocks):
            self.generateBlock()


    def generateBlock(self):
        found = False
        chosenBlock = self.chooseBlock()
        chosenDir = self.chooseDir()
        counter = 0
        while not(found): 
            if counter == 5:
                chosenBlock = self.chooseBlock()
            found = True
            for block in self.blockList:
                if block[1] != chosenBlock[1]:
                    if (self.hasCollision(chosenBlock, self.newCoord(chosenDir, chosenBlock))):
                        found = False
                        chosenDir= self.chooseDir()
                        counter += 1
                        break
        newNum = str(len(self.blockList))
        newCoord = self.newCoord(chosenDir, chosenBlock)
        self.blockList.append(["Block" + newNum, newCoord, int(chosenBlock[0][5])])
        self.jointList.append(["Block" + str(chosenBlock[0][5]) + "_Block" + newNum, self.jointCoord(newCoord, chosenBlock[1]), chosenDir])
    def convertToRelative(self):
       self.relativeBlock.append([self.blockList[0][0], self.blockList[0][1]])
       self.relativeJoint.append([self.jointList[0][0], self.jointList[0][1], self.dirToVector(self.jointList[3])])
       for i in range(1, len(self.blockList)):
            self.relativeBlock.append([self.blockList[i][0], self.getBlockCoords(self.blockList[i])])
       for i in range(1, len(self.jointList)):
            self.relativeJoint.append([self.jointList[i][0], self.getJointCoords(self.jointList[i])])
    def getJointCoords(self, newCoords):
          firstParent = newCoords[0][5]
          oldParent = ["", [0, 0, 0], 0]
          for block in self.blockList:
            if "Block" + firstParent == block[0]:
                oldParent = self.blockList[int(block[2])]
                print("oldParent")
          parentName = "Block" + str(oldParent[0][5]) + "_" + "Block" + str(firstParent)
          parentJoint = ["", [0, 0, 0], 0]
          for joint in self.jointList:
             print(parentName)
             if parentName == joint[0]:
                print("helloooo")
                parentJoint = joint

          return [float(newCoords[1][0] - parentJoint[1][0]), float(newCoords[1][1] - parentJoint[1][1]), float(newCoords[1][2] - parentJoint[1][2])]

    def getBlockCoords(self, blockCoord):
        parentName = "Block" + str(blockCoord[2]) + "_" + "Block" + str(blockCoord[0][5])
        dir = None
        for joint in self.jointList:
            if joint[0] == parentName:
                dir = joint[2]
        if dir == 0:
            return [0.5, 0, 0]
        elif dir == 1:
            return [0, 0.5, 0]
        elif dir == 2:
            return [-0.5, 0, 0]
        elif dir == 3:
            return [0, -0.5, 0]
        elif dir == 4:
            return [0, 0, -0.5]
        elif dir ==5:
            return [0, 0, 0.5]
        
            
        

    def dirToVector(self, dir):
        if dir == 0:
            return " 0 0 1"
        if dir == 1:
            return "0 0 1"
        if dir == 2:
            return "0 0 1"
        if dir == 3:
            return " 0 0 1"
        if dir == 4:
            return " 1 0 0"
        if dir == 5:
            return " 1 0 0"           
    def hasCollision(self, block, newCoord):
        for block in self.blockList:
            if newCoord[2] <=0 or block[1] == newCoord:
                return True
        return False

    def jointCoord(self, newCoord, oldCoord):
        return[float(newCoord[0] + oldCoord[0]) / 2.0,float(newCoord[1] + oldCoord[1])/ 2.0,float(newCoord[2] + oldCoord[2]) / 2.0]
    

    def newCoord(self, dir, oldblock):
            if dir == 0:
                return [oldblock[1][0] + 1, oldblock[1][1], oldblock[1][2]]
            elif dir == 1:
                    return [oldblock[1][0], oldblock[1][1] + 1, oldblock[1][2]]
            elif dir == 2:
                    return [oldblock[1][0] - 1, oldblock[1][1], oldblock[1][2]]
            elif dir == 3:
                    return [oldblock[1][0], oldblock[1][1] -1, oldblock[1][2]]
            elif dir == 4:
                    return [oldblock[1][0], oldblock[1][1], oldblock[1][2] -1]
            elif dir == 5:
                    return [oldblock[1][0], oldblock[1][1], oldblock[1][2] +1]

    def chooseBlock(self):
        return self.blockList[random.randint(0, len(self.blockList)-1)]
    def chooseDir(self):
        return random.randint(0, 5)
    def getBlocks(self):
        return self.relativeBlock
    def getJoints(self):
        return self.relativeJoint
    def printBlockList(self):
        for block in self.blockList:
            print("--------")
            print(block[0] + " " + str(block[1]) + " " + str(block[2]))
            print("--------")

        for joint in self.jointList:
            print("--------")
            print(joint[0] + " " + str(joint[1]))
            print("--------")
        print("BEGGINING RELATIVE:")
        for block in self.relativeBlock:
                print("--------")
                print(str(block[0]) + " " + str(block[1]))
                print("--------")

        for joint in self.relativeJoint:
                print("--------")
                print(str(joint[0]) + " " + str(joint[1]))
                print("--------")



        



