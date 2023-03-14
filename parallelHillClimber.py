import solution
import copy
import constants as c
import os
import time
import matplotlib.pyplot as plt
class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")

        self.nextAvailableID = 0
        self.parents = {}
        for i in range(0, c.populationSize):
            self.parents[i] = solution.Solution(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
        self.evolutionList = []
        for i in range(len(self.parents)):
            self.evolutionList.append([])
    def Evolve(self):
        # self.parent.Evaluate("GUI")
        self.Evaluate(self.parents)
        for currentGeneration in range(0, c.numberOfGenerations):
             self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
       

    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
    def Mutate(self):
        for i in self.children.keys():
            self.children[i].Mutate()
    def Select(self):
        for i in self.parents.keys():
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
            self.evolutionList[i].append(self.parents[i].fitness)
    def Print(self):
        for i in self.parents.keys():
            print("Parent Fitness:" + str(self.parents[i].fitness) + " Child Fitness:" + str(self.children[i].fitness))
            print("")
    def Show_Best(self):
        max= 0
        for i in self.parents.keys():
            if self.parents[i].fitness > self.parents[max].fitness:
                max = i
        print("")
        print("Best Fitness:")
        print(self.parents[max].fitness)
        print("")
        self.parents[max].Start_Simulation("GUI")
    def Show_Seed(self):
        max= 0
        for i in self.parents.keys():
            if self.parents[i].fitness > self.parents[max].fitness:
                max = i
        print(self.parents[max].fitness)
        return [self.parents[max].fitness, self.evolutionList[max]]
    def Show_First(self):
        self.parents[0].Start_Simulation("GUI")
        time.sleep(3)

    def Evaluate(self, solutions):
        for i in range(0, len(solutions.keys())):
           solutions[i].Start_Simulation("DIRECT")
        for i in range(0,len(solutions.keys())):
            solutions[i].Wait_For_Simulation_To_End()




        