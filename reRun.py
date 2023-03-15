import pickle
import parallelHillClimber
import matplotlib.pyplot as plt
with open("bphcs.pkl", "rb") as f:
    phcs = pickle.load(f)
with open("bmaxes.pkl", "rb") as g:
    maxes = pickle.load(g)

def create_graph(maxes, phcs):
        for i in range(len(phcs)):
            plt.plot(maxes[i][1], label="Seed {}".format(i + 1))

        # Setting the title and axis labels
        plt.title('Evolutionary Fitness vs Generations')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()

        # Displaying the plot
        plt.show()

def find_max(maxes):
    max = 0
    maxi = -1
    for i in range (len(maxes)):
        if maxes[i][0] > max:
            max = maxes[i][0]
            maxi = i
    return maxi
   

create_graph(maxes ,phcs)
maxi = find_max(maxes)

phcs[maxi].Show_Best()


