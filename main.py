import os
import constants as c
import parallelHillClimber
import time
import matplotlib.pyplot as plt
import pickle
import signal
#simply click run to evolve a creature!
with open("workingPhcs.pkl", "rb") as g:
    phcsW = pickle.load(g)
phcs = []
maxes = []
def find_max(maxes):
    max = 0
    maxi = -1
    for i in range (len(maxes)):
        if maxes[i][0] > max:
            max = maxes[i][0]
            maxi = i
    return maxi

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

 # define a function to handle the timeout
def handle_timeout(signum, frame):
    raise TimeoutError("Function timed out")

# set the timeout in seconds
timeout = 3

# set the signal handler for SIGALRM
# 
signal.signal(signal.SIGALRM, handle_timeout)   
firstTime = True
for i in range(c.numRuns):
   # run the function in a loop until it finishes within the timeout
    while True:
        try:
            # set the alarm to go off after the specified timeout
            signal.alarm(timeout)
            
            # call the function and catch the TimeoutError exception if it's raised
            phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
            
            # reset the alarm and break out of the loop if the function finishes within the timeout
            signal.alarm(0)
            break
            
        except TimeoutError:
            # if the function takes too long, reset the alarm and stop the function
            signal.alarm(0)
            print("Function took too long, stopping...")
            
            # rerun the function
            continue
    if firstTime:
        phc.Show_First()
        firstTime = False
    phc.Evolve()
    phcs.append(phc)
for i in range(len(phcs)):
    maxes.append(phcs[i].Show_Seed())

maxi = find_max(maxes)
phcs[maxi].Show_Best()
with open("bphcs.pkl", "wb") as f:
     pickle.dump(phcs, f)
     f.close()
with open("bmaxes.pkl", "wb") as g:
    pickle.dump(maxes, g)
create_graph(maxes, phcs)


