import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class Solution:


    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

    
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
        pyrosim.Send_Cube(name="Box", pos=[3,0, 0.5] , size=[1,10,1])
        pyrosim.End()
        pass


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5,0,1], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0 ,0] , size=[1,.2 ,0.2])
        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [-1, 0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0, 0] , size=[0.2,0.2,1])
        
        pyrosim.End()
        pass

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 2 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "BackLeg_BackLowerLeg")
        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        #pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 10.0 )
        pyrosim.End()
    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
         self.myID = ID



        

