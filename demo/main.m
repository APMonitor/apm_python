% Clear local variables and plots
clc; clear all; close all

% Add APM libraries to path for session
addpath('../apm');

% Integrate model and return solution
y = apm_solve('demo',7);

% Retrieve the results
z = y.x; 

% Plot results
figure(1)
plot(z.time,z.x,'r-')
hold on
plot(z.time,z.y,'b--')
legend('x','y')
