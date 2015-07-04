import sys
sys.path.append("../")

# Import APM package
from apm import *

# Solve optimization problem
sol = apm_solve('hs71',3)

print '--- Results of the Optimization Problem ---'
print 'x[1]: ', sol['x[1]']
print 'x[2]: ', sol['x[2]']
print 'x[3]: ', sol['x[3]']
print 'x[4]: ', sol['x[4]']
