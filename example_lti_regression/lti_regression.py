import sys
sys.path.append("../")

import numpy as np
from apm import *

######################################################
# Configuration
######################################################
# number of terms
ny = 3 # output coefficients
nu = 3 # input coefficients
# number of inputs
ni = 2
# number of outputs
no = 2
# load data and parse into columns
data = np.loadtxt('data_no_headers.csv',delimiter=',')
######################################################

# generate time-series model
sysid(data,ni,nu,ny)
