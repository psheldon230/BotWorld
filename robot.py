from motor import MOTOR
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import constants as c

class ROBOT:
    def __init__(self):
        self.motor = dict()
        self.sensors = dict()
        self.nn = NEURAL_NETWORK("brain.nndf")
        self.robotId = p.loadURDF("body.urdf", [0, 0, 0.1])
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        pass

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, x):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Get_Value(x)
        pass

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motor[jointName] = MOTOR(jointName)
        pass

    def Act(self, x):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motor[jointName].Set_Value(self.robotId, desiredAngle)
                print(desiredAngle)
                print(neuronName)
                print(jointName)
        # for jointName in pyrosim.jointNamesToIndices:
        #     self.motor[jointName].Set_Value(self.robotId, x)
    def Think(self):
        self.nn.Update()
        self.nn.Print()
