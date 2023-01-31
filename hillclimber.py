import solution
import copy
import constants as c
class hillclimber:

    def __init__(self):
        self.parent = solution.Solution()

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(0, c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
    def Mutate(self):
        self.child.Mutate()
    def Select(self):
       if self.parent.fitness > self.child.fitness:
        self.parent = self.child
    def Print(self):
        print("Parent Fitness:" + str(self.parent.fitness) + " Child Fitness:" + str(self.child.fitness))
    def Show_Best(self):
        self.parent.Evaluate("GUI")



        