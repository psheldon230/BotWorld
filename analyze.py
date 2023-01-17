import matplotlib.pyplot
import numpy
backLegSensorValues = numpy.load("data/sensordata.npy")
print(backLegSensorValues)
matplotlib.pyplot.plot(backLegSensorValues)
matplotlib.pyplot.show()