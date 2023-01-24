import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.frequency = c.frequency
        self.amplitude = c.amplitude
        self.offset = c.phaseOffset
        self.Prepare_To_Act()
        pass

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,jointName = self.jointName ,controlMode = p.POSITION_CONTROL,targetPosition =desiredAngle,maxForce = c.maxForce)
        pass