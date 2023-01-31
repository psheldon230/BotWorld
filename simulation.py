from world import WORLD
from robot import ROBOT
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c
import time

class SIMULATION:
    def __init__(self, directOrGUI):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        p.setGravity(0,0,-9.8)
        self.robot = ROBOT()
        pass

    def Run(self):
        for x in range(c.iterations):
            if self.directOrGUI == "GUI":
             time.sleep(c.sleepTime)
            p.stepSimulation()
            self.robot.Sense(x)
            self.robot.Think()
            self.robot.Act(x)
        #numpy.save('data/outputBack.npy', backLegSensorValues)
        #numpy.save('data/outputFront.npy', frontLegSensorValues)
        pass
    def Get_Fitness(self):
       self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
        pass