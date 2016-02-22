import sys
sys.path.append("../")

# Import
from apm import *
	
# Select server
server = 'http://byu.apmonitor.com'

# Application name
app = 'cstr'

# Clear previous application
apm(server,app,'clear all')

# Load model file
apm_load(server,app,'cstr.apm')

# Load time points for future predictions
csv_load(server,app,'cstr.csv')

# Load replay replay data for local use
data = csv.reader(open('replay.csv', 'r'))
#data = csv.reader(open('replay1.csv', 'r'))
#data = csv.reader(open('replay2.csv', 'r'))
#data = csv.reader(open('replay3.csv', 'r'))
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

#Parameters
FVs = 'v','rho','cp','mdelh','eoverr','k0','ua'
MVs = 'tc','q','caf','tf'

#Variables
SVs = 'ca','---'
CVs = 't','---'

# Set up variable classifications for data flow
for x in FVs: apm_info(server,app,'FV',x)
for x in MVs: apm_info(server,app,'MV',x)
for x in SVs: apm_info(server,app,'SV',x)
for x in CVs: apm_info(server,app,'CV',x)

# Options

# controller mode (1=simulate, 2=predict, 3=control)
#apm_option(server,app,'nlc.reqctrlmode',3)

# time units (1=sec,2=min,3=hrs,etc)
apm_option(server,app,'nlc.ctrl_units',2)
apm_option(server,app,'nlc.hist_units',2)

# set controlled variable error model type
apm_option(server,app,'nlc.cv_type',1)
apm_option(server,app,'nlc.ev_type',1)
apm_option(server,app,'nlc.reqctrlmode',2)

# read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1)

# turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',500)

# set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',10)


# Objective for Nonlinear Control

# Controlled variable (c)
apm_option(server,app,'t.sp',303)
apm_option(server,app,'t.sphi',305)
apm_option(server,app,'t.splo',300)
apm_option(server,app,'t.tau',10.0)
apm_option(server,app,'t.status',1)
apm_option(server,app,'t.fstatus',0)

# Manipulated variables (u)
apm_option(server,app,'tc.upper',300)
apm_option(server,app,'tc.dmax',10)
apm_option(server,app,'tc.lower',0)
apm_option(server,app,'tc.status',1)
apm_option(server,app,'tc.fstatus',1)

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',1)
solver_output = apm(server,app,'solve')
apm_option(server,app,'nlc.imode',6)

for isim in range(1, len_replay-1):
	print('')
	print('--- Cycle %i of %i ---' %(isim,len_replay-2))

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

	if (isim==1):
		# Open Web Viewer and Display Link
		print("Opening web viewer")
		url = apm_web(server,app)

	# Retrieve results (MEAS,MODEL,NEWVAL)
	# MEAS = FV, MV,or CV measured values
	# MODEL = SV & CV predicted values
	# NEWVAL = FV & MV optimized values
