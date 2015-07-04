import sys
sys.path.append("../")

# Import
from apm import *

# Select server
server = 'http://byu.apmonitor.com'

# Set application name
app = str(random.randint(1,10000))

# Clear previous application
apm(server,app,'clear all')

# Load model file
apm_load(server,app,'distill_pid.apm')

# Load time points for future predictions
csv_load(server,app,'horizon_sim.csv')

# Load replay replay data for local use
data = csv.reader(open('replay_ctl.csv', 'rb'))
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
FVs = 'feed','x_feed','alpha','atray','acond','areb'
MVs = 'sp_x[1]','sp_x[32]'
SVs = 'rr','fbot','x[2]','x[5]','x[10]','x[15]', \
      'x[20]','x[25]','x[30]','x[31]'
CVs = 'x[1]','x[32]'

# Set up variable classifications for data flow
for x in FVs: apm_info(server,app,'FV',x)
for x in MVs: apm_info(server,app,'MV',x)
for x in SVs: apm_info(server,app,'SV',x)
for x in CVs: apm_info(server,app,'CV',x)

# Options

# time units (1=sec,2=min,3=hrs,etc)
apm_option(server,app,'nlc.ctrl_units',2)
apm_option(server,app,'nlc.hist_units',3)

# set controlled variable error model type
apm_option(server,app,'nlc.cv_type',1)
apm_option(server,app,'nlc.ev_type',1)

# controller mode (1=simulate, 2=predict, 3=control)
apm_option(server,app,'nlc.reqctrlmode',1)

# read discretization from CSV file
apm_option(server,app,'nlc.csv_read',1)

# turn on historization to see past results
apm_option(server,app,'nlc.hist_hor',200)

# set web plot update frequency
apm_option(server,app,'nlc.web_plot_freq',10)

# Measured Disturbances
apm_option(server,app,'feed.fstatus',1)
apm_option(server,app,'x_feed.fstatus',1)

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',1)
apm_option(server,app,'nlc.sensitivity',1)

# steady state solution
solver_output = apm(server,app,'solve')
print solver_output

# imode (1=ss, 2=mpu, 3=rto, 4=sim, 5=mhe, 6=nlc)
apm_option(server,app,'nlc.imode',4)
apm_option(server,app,'nlc.sensitivity',0)

for isim in range(1, len_replay):
	print ''
	print '--- Cycle %i of %i ---' %(isim,len_replay-1)

	# allow server to process other requests
	time.sleep(0.1)

	if (isim==2):
		# controller set-points
		apm_meas(server,app,'sp_x[1]',0.952)
		apm_meas(server,app,'sp_x[32]',0.019)

	if (isim==70):
		# set point change
		apm_meas(server,app,'sp_x[1]',0.9955)
		apm_meas(server,app,'sp_x[32]',0.0095)

	for x in FVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print response
	for x in MVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print response
	for x in CVs:
		value = csv_element(x,isim,replay)
		if (not math.isnan(value)):
			response = apm_meas(server,app,x,value)
			print response

	# Run NLC on APM server
	solver_output = apm(server,app,'solve')
	#print solver_output

	if (isim==1):
		# Open Web Viewer and Display Link
		print "Opening web viewer"
		url = apm_web(server,app)

