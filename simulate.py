import pybullet as p
import time as t
physicsClient = p.connect(p.GUI)
for i in range(1000):
    print(i)
    p.stepSimulation()
    t.sleep(1/60)
p.disconnect()