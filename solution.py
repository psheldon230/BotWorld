import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
from preload import prel

class Solution:


    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.senseBlock = []
        self.numBlocks = c.numBlocks
        self.positions = [(0, 0, 0)]
        self.map = prel()
        

    
    def Evaluate(self, directOrGUI):
    
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/simulate.py' " + directOrGUI + " " + str(self.myID) + " &")
        print("ID num is :" + str(self.myID))
        while not os.path.exists('fitness'+str(self.myID)+ '.txt'):
            time.sleep(0.1)
        fitness = open("fitness"+str(self.myID) + ".txt", "r")
        self.fitness = float(fitness.read())
        fitness.close()
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/simulate.py' " + directOrGUI + " " + str(self.myID) + " 2&>1 &")
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('/Users/peter/Desktop/CS 396/BotWorld/fitness'+str(self.myID)+ '.txt'):
            time.sleep(1)
        fitness = open("fitness"+str(self.myID) + ".txt", "r")
        self.fitness = float(fitness.read())
        fitness.close()
        os.system("rm fitness" +str(self.myID)+ ".txt")
    
    def Create_World(self):
        
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
        pass


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        blockList = self.map.getBlocks()
        jointList = self.map.getJoints()
        if "Block0" in self.senseBlock:
            pyrosim.Send_Cube(name="Block0", pos=blockList[0][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        else:
             pyrosim.Send_Cube(name="Block0", pos=blockList[0][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        pyrosim.Send_Joint(name=str(jointList[0][0]), parent= "Block" + str(jointList[0][0][5]) , child = "Block" + str(jointList[0][0][12]) , type = "revolute", position = jointList[0][1],jointAxis = jointList[0][2])
        for i in range(1, len(blockList)):
            if blockList[i][0] in self.senseBlock:
                pyrosim.Send_Cube(name="Block" + str(blockList[i][0][5:]), pos=blockList[i][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
            else:
                pyrosim.Send_Cube(name="Block" + str(blockList[i][0][5:]), pos=blockList[i][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        for i in range(1, len(jointList)):
              parent = jointList[i][0].split("_")
              parentNum = parent[0][5:]
              childNum = parent[1][5:]
              pyrosim.Send_Joint(name=str(jointList[i][0]), parent= "Block" + str(parentNum) , child = "Block" + str(childNum) , type = "revolute", position = jointList[i][1],jointAxis = jointList[i][2])
        self.map.printBlockList()
        pyrosim.End()


    def Create_Brain(self):
         jointList = self.map.getJoints()
         blockList = self.map.getBlocks()
         pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
         motorCount = 0
         for i in range(0, len(jointList)):
             motorCount += 1
             pyrosim.Send_Motor_Neuron(name= i , jointName=jointList[i][0])
         sensorCount = 0
        
         for block in blockList:
             sensorTest = random.randint(0, 1)
             if sensorTest == 0:
                 sensorCount += 1
                 pyrosim.Send_Sensor_Neuron(name=sensorCount + motorCount, linkName= block[0])
                 self.senseBlock.append(block[0])

         self.weights = numpy.random.rand(sensorCount, motorCount) * 2 - 1

         for currentRow in range(sensorCount):
             for currentColumn in range(len(blockList) - 1):
                 pyrosim.Send_Synapse(sourceNeuronName = currentRow + c.numBlocks, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])

         pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
         self.myID = ID



        

