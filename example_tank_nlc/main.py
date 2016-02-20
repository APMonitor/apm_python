# Import
import sys
sys.path.append("../")

# Import
from apm import *
	
# Select server
server = 'http://byu.apmonitor.com'

# Application name
app = 'nlc'

# Clear previous application
apm(server,app,'clear all')

# Load model file
apm_load(server,app,'tank.apm')

# Load time points for future predictions
csv_load(server,app,'tank.csv')

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
FVs = 'kc','taui','taud','op_bias'
MVs = 'percent_open[1]','sp'
SVs = 'percent_open[2]','pv[1]','op[1]','pv[2]','op[2]', \
'inlet_flow[1]','outlet_flow[1]', \
'inlet_flow[2]','outlet_flow[2]', \
'proportional','integral','derivative', \
'error[1]','error[2]'
CVs = 'volume[1]','volume[2]'

# Set up variable classifications for data flow
for x in FVs: apm_info(server,app,'FV',x)
for x in MVs: apm_info(server,app,'MV',x)
for x in SVs: apm_info(server,app,'SV',x)
for x in CVs: apm_info(server,app,'CV',x)

# Options

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',6)

# controller mode (1=simulate, 2=predict, 3=control)
#apm_option(server,app,'nlc.reqctrlmode',3)

# time units (1=sec,2=min,3=hrs,etc)
apm_option(server,app,'nlc.ctrl_units',1)

# set controlled variable error model type
apm_option(server,app,'nlc.cv_type',1)
apm_option(server,app,'nlc.ev_type',1)
apm_option(server,app,'nlc.reqctrlmode',3)

# read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1)

# turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',500)

# set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',10)


# Objective for Nonlinear Control

# Controlled variable (c)
apm_option(server,app,'volume[1].sp',500)
apm_option(server,app,'volume[1].sphi',520)
apm_option(server,app,'volume[1].splo',480)
apm_option(server,app,'volume[2].sp',500)
apm_option(server,app,'volume[2].sphi',520)
apm_option(server,app,'volume[2].splo',480)
apm_option(server,app,'volume[1].tau',40.0)
apm_option(server,app,'volume[2].tau',40.0)
apm_option(server,app,'volume[1].status',1)
apm_option(server,app,'volume[2].status',0)
apm_option(server,app,'volume[1].fstatus',0)
apm_option(server,app,'volume[2].fstatus',0)

# Manipulated variables (u)
apm_option(server,app,'percent_open[1].upper',100)
apm_option(server,app,'percent_open[1].dmax',50)
apm_option(server,app,'percent_open[1].lower',0)
apm_option(server,app,'percent_open[1].status',1)
apm_option(server,app,'percent_open[1].fstatus',0)

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
	print("Finished Solving")
	
	# Retrieve results
	array = apm_sol(server,app)

	#if (isim==1):
	#	# Open Web Viewer and Display Link
	#	print("Opening web viewer")
	#	url = apm_web(server,app)

	# Retrieve results (MEAS,MODEL,NEWVAL)
	# MEAS = FV, MV,or CV measured values
	# MODEL = SV & CV predicted values
	# NEWVAL = FV & MV optimized values

print('--- Available Variables ---')
print(array.keys())

# Plotting
from matplotlib import pyplot
x = array['time']
print(x)
y = array['percent_open[1]']
pyplot.plot(x, y)
pyplot.xlabel('Time')
pyplot.ylabel('Percent Open')
pyplot.show()
