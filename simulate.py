import pybullet as p
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet_data
import time as t
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(100)
frontLegSensorValues = numpy.zeros(100)
for i in range(100):
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = 'Torso_BackLeg',
    controlMode = p.POSITION_CONTROL,
    targetPosition = 0.0,
    maxForce = 500)

    p.stepSimulation()
    t.sleep(1/60)
p.disconnect()
numpy.save("data/backLegSensorData.npy", backLegSensorValues)
numpy.save("data/frontLegSensorData.npy", frontLegSensorValues)