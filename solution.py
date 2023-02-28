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
        self.blockList = self.map.getBlocks()
        self.jointList = self.map.getJoints()
        self.numMotorNeurons =  len(self.blockList)
        self.numSensorNeurons = len(self.senseBlock)
        self.firstTime = True
        

    
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
        time.sleep(1)
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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        if "Block0" in self.senseBlock:
            pyrosim.Send_Cube(name="Block0", pos=self.blockList[0][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        else:
             pyrosim.Send_Cube(name="Block0", pos=self.blockList[0][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        pyrosim.Send_Joint(name=str(self.jointList[0][0]), parent= "Block" + str(self.jointList[0][0][5]) , child = "Block" + str(self.jointList[0][0][12]) , type = "revolute", position = self.jointList[0][1],jointAxis = self.jointList[0][2])
        for i in range(1, len(self.blockList)):
            if self.blockList[i][0] in self.senseBlock:
                pyrosim.Send_Cube(name="Block" + str(self.blockList[i][0][5:]), pos=self.blockList[i][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
            else:
                pyrosim.Send_Cube(name="Block" + str(self.blockList[i][0][5:]), pos=self.blockList[i][1], size=[c.blockSize, c.blockSize, c.blockSize], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        for i in range(1, len(self.jointList)):
              parent = self.jointList[i][0].split("_")
              parentNum = parent[0][5:]
              childNum = parent[1][5:]
              pyrosim.Send_Joint(name=str(self.jointList[i][0]), parent= "Block" + str(parentNum) , child = "Block" + str(childNum) , type = "revolute", position = self.jointList[i][1],jointAxis = self.jointList[i][2])
       #self.map.printBlockList()
        pyrosim.End()


    def Create_Brain(self):
         self.senseBlock.clear()
         jointList = self.map.getJoints()
         blockList = self.map.getBlocks()
         time.sleep(2)
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
                 self.numSensorNeurons += 1
                 pyrosim.Send_Sensor_Neuron(name=sensorCount + motorCount, linkName= block[0])
                 self.senseBlock.append(block[0])
         if self.firstTime:

            self.weights = numpy.random.rand(20, 20) * 2 - 1
            self.firstTime = False

         for currentRow in range(sensorCount):
            for currentColumn in range(len(blockList) - 1):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow + self.numBlocks, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])

         pyrosim.End()

    def Mutate(self):
        randnum = random.randint(0, 1)
        if randnum == 0:
            if len(self.senseBlock) <= 1:
                randomRow = 0
            else:
                randomRow = random.randint(0,self.numSensorNeurons-1)
            randomColumn = random.randint(0, self.numMotorNeurons- 1)
            self.weights[randomRow][randomColumn] = random.random() * 2 - 1
        else:
            found = False
            block = random.randint(0, len(self.blockList) -1)
            while not(found):
                found = True
                for joints in self.jointList:
                     if joints[0].__contains__(self.blockList[block][0] + "_"):
                        found = False
                        block = random.randint(0, len(self.blockList) -1)
                        break
            for joints in self.jointList:
                if joints[0].__contains__("_" + self.blockList[block][0]):
                    self.jointList.remove(joints)
            print("mutating now")
            self.numBlocks -= 1
            if self.blockList[block][0] in self.senseBlock:
                self.numSensorNeurons -= 1
                self.senseBlock.remove(self.blockList[block][0])
            self.blockList.remove(self.blockList[block])
            self.numMotorNeurons -= 1
            
            


                
                
            

    def Set_ID(self, ID):
         self.myID = ID



        

