import sys
sys.path.append("../")

# Import
from apm import *
	
# Select server
server = 'http://byu.apmonitor.com'

# Application name
app = 'diabetic'

# Clear previous application
apm(server,app,'clear all')

# Load model file
apm_load(server,app,'diabetic.apm')

# Load time points for future predictions
csv_load(server,app,'diabetic.csv')

# Load replay replay data for local use
data = csv.reader(open('control.csv', 'r'))
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
FVs = 'kc','taui','taud','op_bias'
MVs = 'u','d'
SVs = 'x','i','q[1]','q[2]','g_gut'
CVs = 'g','g_target'

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

# set controlled variable error model type
apm_option(server,app,'nlc.cv_type',1)
apm_option(server,app,'nlc.ev_type',1)
apm_option(server,app,'nlc.reqctrlmode',3)

# read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1)

# read discretization from CSV file
apm_option(server,app,'nlc.spc_chart',3)

# turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',500)
apm_option(server,app,'nlc.hist_units',3)

# set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',2)


# Objective for Nonlinear Control

# Controlled variable (c)
apm_option(server,app,'g.sp',100)
apm_option(server,app,'g.sphi',120)
apm_option(server,app,'g.splo',60)
apm_option(server,app,'g.tau',40.0)
apm_option(server,app,'g.status',0)
apm_option(server,app,'g.fstatus',0)

apm_option(server,app,'g_target.sp',83)
apm_option(server,app,'g_target.sphi',82)
apm_option(server,app,'g_target.splo',78)
apm_option(server,app,'g_target.tau',40.0)
apm_option(server,app,'g_target.status',1)
apm_option(server,app,'g_target.fstatus',0)

# Manipulated variables (u)
apm_option(server,app,'u.upper',20)
apm_option(server,app,'u.dmax',2)
apm_option(server,app,'u.lower',0)
apm_option(server,app,'u.status',1)
apm_option(server,app,'u.fstatus',0)

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',1)

# Steady State Solution
solver_output = apm(server,app,'solve')
print(solver_output)

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
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

	#if (isim==1):
		# Open Web Viewer and Display Link
	#	print("Opening web viewer")
	#	url = apm_web(server,app)

	# Retrieve results (MEAS,MODEL,NEWVAL)
	# MEAS = FV, MV,or CV measured values
	# MODEL = SV & CV predicted values
	# NEWVAL = FV & MV optimized values
