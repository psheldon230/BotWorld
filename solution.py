import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time

class Solution:


    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = numpy.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    
    def Evaluate(self, directOrGUI):
    
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/simulate.py' " + directOrGUI + " " + str(self.myID) + " &")
        print("ID num is :" + str(self.myID))
        while not os.path.exists('fitness'+str(self.myID)+ '.txt'):
            time.sleep(0.08)
        fitness = open("fitness"+str(self.myID) + ".txt", "r")
        self.fitness = float(fitness.read())
        fitness.close()
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/simulate.py' " + directOrGUI + " " + str(self.myID) + " &")
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('/Users/peter/Desktop/CS 396/BotWorld/fitness'+str(self.myID)+ '.txt'):
            time.sleep(0.09)
        fitness = open("fitness"+str(self.myID) + ".txt", "r")
        self.fitness = float(fitness.read())
        fitness.close()
        os.system("rm fitness" +str(self.myID)+ ".txt")
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-3,3,0.5] , size=[1,1,1])
        pyrosim.End()
        pass


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[1,1,1])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5,0,-0.5] , size=[1,1,1])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5,0,1])    
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5,0,-0.5] , size=[1,1,1])
        pyrosim.End()
        pass

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
        pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = 2.0 )
        sensneurArr = [0, 1, 2]
        motorneurArr = [0, 1]
        for currentRow in sensneurArr:
            for currentColumn in motorneurArr:
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])

        #pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 10.0 )
        pyrosim.End()
    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID



        

