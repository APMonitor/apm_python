# Import
import sys
sys.path.append("../")

# Import
from apm import *
	
# Select server
server = 'http://xps.apmonitor.com'

# Application name
app = 'mhe'

# Clear previous application
apm(server,app,'clear all')

# Load model file
apm_load(server,app,'tank.apm')

# Load time points for future predictions
csv_load(server,app,'tank.csv')

# Load replay replay data for local use
#data = csv.reader(open('replay1.csv', 'r'))
#data = csv.reader(open('replay2.csv', 'r'))
data = csv.reader(open('replay3.csv', 'r'))
replay = []
for row in data:
	replay.append(row)
len_replay = len(replay)

# APM Variable Classification
# class = FV, MV, SV, CV
#   F or FV = Fixed value - parameter may change to a new value every cycle
#   M or MV = Manipulated variable - independent variable over time horizon
#   S or SV = State variable - model variable for viewing
#   C or CV = Controlled variable - model variable for control
FVs = 'gain','tau','v0'
MVs = 'percent_open','c1','c2'
SVs = 'inlet_flow','outlet_flow'
CVs = 'volume','vol_lin'

# Set up variable classifications for data flow
for x in FVs: apm_info(server,app,'FV',x)
for x in MVs: apm_info(server,app,'MV',x)
for x in SVs: apm_info(server,app,'SV',x)
for x in CVs: apm_info(server,app,'CV',x)

# Options

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',5)

# controller mode (1=simulate, 2=predict, 3=control)
#apm_option(server,app,'nlc.reqctrlmode',3)

# time units (1=sec,2=min,3=hrs,etc)
apm_option(server,app,'nlc.ctrl_units',1)

# set controlled variable error model type
apm_option(server,app,'nlc.cv_type',2)
apm_option(server,app,'nlc.ev_type',2)

# read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1)

# turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',500)

# set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',5)

# Objective for Estimation

# inlet valve parameter (c1 = max_flow)
# inlet_flow = c1 * percent_open
apm_option(server,app,'c1.status',1)
apm_option(server,app,'c1.dmax',0.01)
apm_option(server,app,'c1.mv_step_hor',100)
apm_option(server,app,'c1.fstatus',0)
apm_option(server,app,'c1.lower',0.2)
apm_option(server,app,'c1.upper',0.3)

# outlet drain parameter
# outlet_flow = c2 * SQRT(volume)
apm_option(server,app,'c2.status',1)
apm_option(server,app,'c2.mv_step_hor',100)
apm_option(server,app,'c2.dmax',0.01)
apm_option(server,app,'c2.fstatus',0)
apm_option(server,app,'c2.lower',0.1)
apm_option(server,app,'c2.upper',0.2)

apm_option(server,app,'volume.fstatus',1)
apm_option(server,app,'vol_lin.fstatus',1)

# Objective for Nonlinear Control

# Controlled variable (c)
#apm_option(server,app,'volume.sp',4.1)
#apm_option(server,app,'volume.tau',2.0)
#apm_option(server,app,'volume.status',1)

# Manipulated variables (u)
#apm_option(server,app,'percent_open.upper',100)
#apm_option(server,app,'percent_open.lower',0)
#apm_option(server,app,'percent_open.status',1)
#apm_option(server,app,'percent_open.fstatus',0)

for isim in range(1, 5):
	print('')
	print('--- Cycle %i of %i ---' %(isim,4))

	# allow server to process other requests
	time.sleep(0.1)

	for x in FVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print(response)
	for x in MVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print(response)
	for x in CVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print(response)

	# schedule a set point change at cycle 40
	#if (isim==4): apm_option(server,app,'volume.sp',50)

	# Run NLC on APM server
	solver_output = apm(server,app,'solve')
	print(solver_output)

	#if (isim==1):
	#	# Open Web Viewer and Display Link
	#	print "Opening web viewer"
	#	url = apm_web(server,app)

	# Retrieve results (MEAS,MODEL,NEWVAL)
	# MEAS = FV, MV,or CV measured values
	# MODEL = SV & CV predicted values
	# NEWVAL = FV & MV optimized values
	percent_open = apm_tag(server,app,'percent_open.newval')
	volume_meas = apm_tag(server,app,'volume.meas')
	volume_model = apm_tag(server,app,'volume.model')

	print('Percent_open: %f' %(percent_open))
	print('Measured volume: %f' %(volume_meas))
	print('Predicted volume: %f' %(volume_model))
