This example demonstrates the numerical integration of simple Differtial Algebraic Equations (DAEs) in MATLAB and Python. ODE stiff systems as well as high index (Index 2+) DAE systems are possible.

The directory contains a folder (apm) that contains the library of functions for working with APM. The model file (demo.apm) contains the following text:

Model                
  Parameters         
   tau = 5         
   K = 3  
   u 
  End Parameters     

  Variables          
   x = 0               
   y = 0                
  End Variables      

  Equations          
   tau * $x + x = K * u  
   y = 2 * x         
  End Equations      
End Model            

The data file (demo.csv) specifies the time points and any inputs to the model. In this case, the input 'u' is specified at the following time intervals:

time, u
0,    0
0.5,  0
1,    1
2,    1
3,    1
5,    1
8,    1
12,   1
15,   1
18,   1
21,   1
22,   1
25,   1
28,   1
30,   1

The function 'apm_solve' receives an input of the application name (in this case 'demo') and returns a structure with the results of the simulation. In this case, the solution is returned into a structure named 'z'.

y = apm_solve('demo');
z = y.x;

The structure contains all of the parameters and variables defined in the model file as well as the time points. A plot of 'time' and 'x' is provided with the demo and these are referenced as 'z.time' and 'z.x'.

The APMonitor Modeling Language (http://apmonitor.com) is optimization software for ODEs and DAEs. It is a full-featured modeling language with interfaces to MATLAB and Python. It is coupled with large-scale nonlinear programming solvers for parameter estimation, nonlinear optimization, simulation, and model predictive control. There is an active discussion group as well as regular webinars for those interested in large-scale modeling and simulation.
