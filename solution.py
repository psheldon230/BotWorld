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
        self.numBlocks = random.randint(5, 15)
        self.positions = [(0, 0, 0)]
        

    
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
        map = prel()
        blockList = map.getBlocks()
        jointList = map.getJoints()
        pyrosim.Send_Cube(name="Block0", pos=blockList[0][1], size=[1, 1, 1], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        pyrosim.Send_Joint(name=str(jointList[0][0]), parent= "Block" + str(jointList[0][0][5]) , child = "Block" + str(jointList[0][0][12]) , type = "revolute", position = jointList[0][1],jointAxis = "1 0 0")
        for i in range(1, len(blockList)):
              pyrosim.Send_Cube(name="Block" + str(blockList[i][0][5]), pos=blockList[i][1], size=[1, 1, 1], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        for i in range(1, len(jointList)):
              pyrosim.Send_Joint(name=str(jointList[i][0]), parent= "Block" + str(jointList[i][0][5]) , child = "Block" + str(jointList[i][0][12]) , type = "revolute", position = jointList[i][1],jointAxis = "1 0 0")
        map.printBlockList()
        pyrosim.End()

        # pyrosim.Start_URDF("body.urdf")

        # randomNumbers = numpy.random.rand(3,1) + 0.5

        # if "Block0" in self.senseBlock:
        #     color = "Green"
        # else:
        #     color = "Blue"
        
        # pyrosim.Send_Cube(name="Block0", pos=[0,0,3] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 1.0 0 1.0"', colorName='"' + color + '"')
        # pyrosim.Send_Joint(name = "Block0_Block1" , parent= "Block0" , child = "Block1", type = "revolute", position = [randomNumbers[0][0] / 2,0,2],jointAxis = "0 1 0")
        # print(self.senseBlock)
        # for currBlock in range(1, self.numBlocks):
        #     randomNumbers = numpy.random.rand(3,1) + 0.5
        #     caseDir = random.randint(1, 4)
        #     oldJoint = [randomNumbers[0][0] / 2,0,2]
        #     if caseDir == 1: 
        #         if self.senseBlock.__contains__("Block" + str(currBlock)):
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[randomNumbers[0][0]/2,0,0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        #         else:
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[randomNumbers[0][0]/2,0,0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        #         #make joint if not last
        #           #make joint if not last
        #         if currBlock < self.numBlocks - 1:
        #             pyrosim.Send_Joint( name = "Block" + str(currBlock) + "_Block" + str(currBlock + 1) , parent= "Block" + str(currBlock) , child = "Block" + str(currBlock+ 1) , type = "revolute", position = [randomNumbers[0][0],0,0],jointAxis = "0 1 0")
        #     elif caseDir == 2:
        #          if self.senseBlock.__contains__("Block" + str(currBlock)):
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0,randomNumbers[0][0] /2,0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        #          else:
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0,randomNumbers[0][0] /2 ,0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        #         #make joint if not last
        #           #make joint if not last
        #          if currBlock < self.numBlocks - 1:
        #             pyrosim.Send_Joint( name = "Block" + str(currBlock) + "_Block" + str(currBlock + 1) , parent= "Block" + str(currBlock) , child = "Block" + str(currBlock+ 1) , type = "revolute", position = [0,randomNumbers[0][0],0],jointAxis = "0 1 0")
        #     elif caseDir == 3:
        #          if self.senseBlock.__contains__("Block" + str(currBlock)):
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0, 0, randomNumbers[0][0] /2] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        #          else:
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0, 0,randomNumbers[0][0] / 2] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        #         #make joint if not last
        #           #make joint if not last
        #          if currBlock < self.numBlocks - 1:
        #             pyrosim.Send_Joint( name = "Block" + str(currBlock) + "_Block" + str(currBlock + 1) , parent= "Block" + str(currBlock) , child = "Block" + str(currBlock+ 1) , type = "revolute", position = [ 0,0,randomNumbers[0][0]],jointAxis = "0 0 1")
        #     elif caseDir == 4:
        #          if self.senseBlock.__contains__("Block" + str(currBlock)):
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0, -randomNumbers[0][0] /2, 0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 1.0 0 1.0"', colorName='"Green"')
        #          else:
        #             pyrosim.Send_Cube(name="Block" + str(currBlock), pos=[0, -randomNumbers[0][0] /2, 0] , size=[randomNumbers[0][0],randomNumbers[1][0],randomNumbers[2][0]], colorCode='"0 0 1.0 1.0"', colorName='"Blue"')
        #         #make joint if not last
        #           #make joint if not last
        #          if currBlock < self.numBlocks - 1:
        #             pyrosim.Send_Joint( name = "Block" + str(currBlock) + "_Block" + str(currBlock + 1) , parent= "Block" + str(currBlock) , child = "Block" + str(currBlock+ 1) , type = "revolute", position = [ 0,-randomNumbers[0][0], 0],jointAxis = "0 0 1")





        # pyrosim.End()


        # pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])
        # pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5,0,1], jointAxis= "1 0 0")
        # pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0 ,0] , size=[1,.2 ,0.2])
        # pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [-1, 0,0], jointAxis = "0 1 0")
        # pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0, 0] , size=[0.2,0.2,1])
        
        # pyrosim.End()
        # pass

    def Create_Brain(self):
         pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        #  motorCount = 0
        #  for currBlock in range(self.numBlocks-1):
        #     motorCount += 1
        #     pyrosim.Send_Motor_Neuron(name= currBlock, jointName="Block" + str(currBlock)+ "_Block" + str(currBlock + 1))
        #  sensorCount = 0
        
        #  for currBlock in range(self.numBlocks):
        #     sensorTest = random.randint(0, 1)
        #     if sensorTest == 0:
        #         sensorCount += 1
        #         pyrosim.Send_Sensor_Neuron(name=sensorCount + motorCount, linkName= "Block" + str(currBlock))
        #         self.senseBlock.append("Block" + str(currBlock))

        #  self.weights = numpy.random.rand(sensorCount, motorCount) * 2 - 1

        #  for currentRow in range(sensorCount):
        #      for currentColumn in range(self.numBlocks - 1):
        #         pyrosim.Send_Synapse(sourceNeuronName = currentRow + self.numBlocks, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])

         pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
         self.myID = ID



        

