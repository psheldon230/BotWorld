import os
import hillclimber
# counter = 0
# while counter < 5:
#     os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/generate.py'")
#     os.system("python3 '/Users/peter/Desktop/CS 396/BotWorld/BotWorld/simulate.py'")
#     counter = counter + 1

hc = hillclimber.hillclimber()
hc.Evolve()
hc.Show_Best()