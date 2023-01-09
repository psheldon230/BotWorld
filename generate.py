import pyrosim.pyrosim as pyrosim
currpos = .5
def CreateWorld():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[0,0, 0.5] , size=[1, 1, 1])
    pyrosim.End()
def CreateRobot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0, 0.5] , size=[1, 1, 1])
    pyrosim.End()

CreateWorld()