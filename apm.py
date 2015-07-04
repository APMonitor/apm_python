# Import
import csv
import math
import os
import random
import string
import time
import urllib
import webbrowser
from contextlib import closing

def apm(server,app,aline):
    '''Send a request to the server \n \
       server = address of server \n \
       app      = application name \n \
       aline  = line to send to server \n'''
    try:
        # Web-server URL address
        url_base = string.strip(server) + '/online/apm_line.php'
        app = app.lower()
        app.replace(" ","")
        params = urllib.urlencode({'p':app,'a':aline})
        f = urllib.urlopen(url_base,params)
        # Send request to web-server
        response = f.read()
    except:
        response = 'Failed to connect to server'
    return response

def apm_load(server,app,filename):
    '''Load APM model file \n \
       server   = address of server \n \
       app      = application name \n \
       filename = APM file name'''
    # Load APM File
    f = open(filename,'r')
    aline = f.read()
    app = app.lower()
    app.replace(" ","")
    response = apm(server,app,' '+aline)
    return

def csv_load(server,app,filename):
    '''Load CSV data file \n \
       server   = address of server \n \
       app      = application name \n \
       filename = CSV file name'''
    # Load CSV File
    f = open(filename,'r')
    aline = f.read()
    app = app.lower()
    app.replace(" ","")
    response = apm(server,app,'csv '+aline)
    return

def apm_ip(server):
    '''Get current IP address \n \
       server   = address of server'''
    # get ip address for web-address lookup
    url_base = string.strip(server) + '/ip.php'
    f = urllib.urlopen(url_base)
    ip = string.strip(f.read())
    return ip

def apm_t0(server,app,mode):
    '''Retrieve restart file \n \
       server   = address of server \n \
       app      = application name \n \
       mode = {'ss','mpu','rto','sim','est','ctl'} '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/' + string.strip(mode) + '.t0'
    f = urllib.urlopen(url)
    # Send request to web-server
    solution = f.read()
    return solution

def apm_sol(server,app):
    '''Retrieve solution results\n \
       server   = address of server \n \
       app      = application name '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/results.csv'
    f = urllib.urlopen(url)
    # Send request to web-server
    solution = f.read()

    # Write the file
    sol_file = 'solution_' + app + '.csv'
    fh = open(sol_file,'w')
    # possible problem here if file isn't able to open (see MATLAB equivalent)
    fh.write(solution.replace('\r',''))
    fh.close()        

    # Use array package otherwise
    from array import array
    # Import CSV file from web server
    with closing(urllib.urlopen(url)) as f:
        reader = csv.reader(f, delimiter=',')
        y={}
        for row in reader:
            if len(row)==2:
                y[row[0]] = float(row[1])
            else:
                y[row[0]] = array('f', [float(col) for col in row[1:]])
    # Return solution
    return y


def apm_get(server,app,filename):
    '''Retrieve any file from web-server\n \
       server   = address of server \n \
       app      = application name '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/' + filename
    f = urllib.urlopen(url)
    # Send request to web-server
    file = f.read()
    # Write the file
    fh = open(filename,'w')
    fh.write(file.replace('\r',''))
    fh.close()
    return (file)

def apm_option(server,app,name,value):
    '''Load APM option \n \
       server   = address of server \n \
       app      = application name \n \
       name     = {FV,MV,SV,CV}.option \n \
       value    = numeric value of option '''
    aline = 'option %s = %f' %(name,value)
    app = app.lower()
    app.replace(" ","")
    response = apm(server,app,aline)
    return response

def apm_web(server,app):
    '''Open APM web viewer in local browser \n \
       server   = address of server \n \
       app      = application name '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address    
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/' + ip + '_' + app + '_oper.htm'
    webbrowser.open_new_tab(url)
    return url

def apm_web_var(server,app):
    '''Open APM web viewer in local browser \n \
       server   = address of server \n \
       app      = application name '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address    
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/' + ip + '_' + app + '_var.htm'
    webbrowser.open_new_tab(url)
    return url
    
def apm_web_root(server,app):
    '''Open APM root folder \n \
       server   = address of server \n \
       app      = application name '''
    # Retrieve IP address
    ip = apm_ip(server)
    # Web-server URL address    
    app = app.lower()
    app.replace(" ","")
    url = string.strip(server) + '/online/' + ip + '_' + app + '/'
    webbrowser.open_new_tab(url)
    return url

def apm_info(server,app,type,aline):
    '''Classify parameter or variable as FV, MV, SV, or CV \n \
       server   = address of server \n \
       app      = application name \n \
       type     = {FV,MV,SV,CV} \n \
       aline    = parameter or variable name '''
    x = 'info' + ' ' +  type + ', ' + aline
    app = app.lower()
    app.replace(" ","")
    response = apm(server,app,x)
    return response


def csv_data(filename):
    '''Load CSV File into Python
       A = csv_data(filename)

       Function csv_data extracts data from a comma
       separated value (csv) file and returns it
       to the array A'''
    try:
        f = open(filename, 'rb')
        reader = csv.reader(f)
        headers = reader.next()
        c = [float] * (len(headers))
        A = {}
        for h in headers:
            A[h] = []
        for row in reader:
            for h, v, conv in zip(headers, row, c):
                A[h].append(conv(v))
    except ValueError:
        A = {}
    return A

def csv_lookup(name,replay):
    '''Lookup Index of CSV Column \n \
       name     = parameter or variable name \n \
       replay   = csv replay data to search'''
    header = replay[0]
    try:
        i = header.index(string.strip(name))
    except ValueError:
        i = -1 # no match
    return i

def csv_element(name,row,replay):
    '''Retrieve CSV Element \n \
       name     = parameter or variable name \n \
       row      = row of csv file \n \
       replay   = csv replay data to search'''
    # get row number
    if (row>len(replay)): row = len(replay)-1
    # get column number
    col = csv_lookup(name,replay)
    if (col>=0): value = float(replay[row][col])
    else: value = float('nan')
    return value

def apm_tag(server,app,name):
    '''Retrieve options for FV, MV, SV, or CV \n \
       server   = address of server \n \
       app      = application name \n \
       name     = {FV,MV,SV,CV}.{MEAS,MODEL,NEWVAL} \n \n \
         Valid name combinations \n \
        {FV,MV,CV}.MEAS \n \
        {SV,CV}.MODEL \n \
        {FV,MV}.NEWVAL '''
    # Web-server URL address
    url_base = string.strip(server) + '/online/get_tag.php'
    app = app.lower()
    app.replace(" ","")
    params = urllib.urlencode({'p':app,'n':name})
    f = urllib.urlopen(url_base,params)
    # Send request to web-server
    value = eval(f.read())
    return value

def apm_meas(server,app,name,value):
    '''Transfer measurement to server for FV, MV, or CV \n \
       server   = address of server \n \
       app      = application name \n \
       name     = name of {FV,MV,CV} '''
    # Web-server URL address
    url_base = string.strip(server) + '/online/meas.php'
    app = app.lower()
    app.replace(" ","")
    params = urllib.urlencode({'p':app,'n':name+'.MEAS','v':value})
    f = urllib.urlopen(url_base,params)
    # Send request to web-server
    response = f.read()
    return response

def apm_solve(app,imode):
    '''
     APM Solver for simulation, estimation, and optimization with both
      static (steady-state) and dynamic models. The dynamic modes can solve
      index 2+ DAEs without numerical differentiation.
     
     y = apm_solve(app,imode)
    
     Function apm_solve uploads the model file (apm) and optionally
       a data file (csv) with the same name to the web-server and performs
       a forward-time stepping integration of ODE or DAE equations
       with the following arguments:
    
      Input:      app = model (apm) and data file (csv) name
                imode = simulation mode {1..7}
                                   steady-state  dynamic  sequential
                        simulate     1             4        7
                        estimate     2             5        8 (under dev)
                        optimize     3             6        9 (under dev)
    
     Output: y.names  = names of all variables
             y.values = tables of values corresponding to y.names
             y.nvar   = number of variables
             y.x      = combined variables and values but variable
                          names may be modified to make them valid
                          characters (e.g. replace '[' with '')
    '''

    # server and application file names
    server = 'http://byu.apmonitor.com'
    app = app.lower()
    app.replace(" ","")
    app_model = app + '.apm'
    app_data =  app + '.csv'

    # randomize the application name
    from random import randint
    app = app + '_' + str(randint(1000,9999))
    
    # clear previous application
    apm(server,app,'clear all')

    try:
        # load model file
        apm_load(server,app,app_model)
    except:
        msg = 'Model file ' + app + '.apm does not exist'
        print msg
        return []

    # check if data file exists (optional)
    try:
        # load data file
        csv_load(server,app,app_data)
    except:
        # data file is optional
        print 'Optional data file ' + app + '.csv does not exist'
        pass
    
    # default options
    # use or don't use web viewer
    web = False
    if web:
        apm_option(server,app,'nlc.web',2)
    else:
        apm_option(server,app,'nlc.web',0)

    # internal nodes in the collocation (between 2 and 6)
    apm_option(server,app,'nlc.nodes',3)
    # sensitivity analysis (default: 0 - off)
    apm_option(server,app,'nlc.sensitivity',0)
    # simulation mode (1=ss,  2=mpu, 3=rto)
    #                 (4=sim, 5=est, 6=nlc, 7=sqs)
    apm_option(server,app,'nlc.imode',imode)

    # attempt solution
    solver_output = apm(server,app,'solve')

    # check for successful solution
    status = apm_tag(server,app,'nlc.appstatus')

    if status==1:
        # open web viewer if selected
        if web:
            apm_web(server,app)
        # retrieve solution and solution.csv
        z = apm_sol(server,app)
        return z
    else:
        print solver_output
        print 'Error: Did not converge to a solution'
        return []
