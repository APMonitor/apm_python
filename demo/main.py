# load apm library
from apm import *

# Integrate model and return solution
z = apm_solve('demo',7);

# Plot results
import matplotlib
import matplotlib.pyplot as plt
plt.figure()
plt.plot(z['time'],z['x'],'r-')
plt.plot(z['time'],z['y'],'b--')
plt.legend(['x','y'])
plt.savefig('plot.png')
plt.show()

