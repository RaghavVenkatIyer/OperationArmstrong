import math
import numpy as np
G=6.674e-11
c=3.0e8
M=float(input("Enter the mass of black hole (kilograms): "))
r=float(input("Enter the distance of the person from the black hole (meters): "))
r_s=(2*G*M)/c**2
print(r_s, "is the Schwarzschild radius")
time = int(input("Enter 0 for faller’s time (input viewer’s time), or 1 for viewer’s time (input faller’s time): "))

if time == 0:
        viewerstime = float(input("Enter the viewer's time (seconds): "))
        t_faller = viewerstime * math.sqrt((1 - r_s / r))
        print(t_faller, "is the faller’s time")
else:
        fallerstime = float(input("Enter the faller’s time (seconds): "))
        t_viewer = fallerstime / math.sqrt(1 - r_s / r)
        print(t_viewer, "is the viewer’s time")

escapevelocity = math.sqrt((2 * G * M) / r)
print(escapevelocity, "is the escape velocity")

gravitationalacceleration = (G * M) / (r**2)
print(gravitationalacceleration, "is the gravitational acceleration near the black hole")

orbitalvelocity = math.sqrt((G * M) / r)
print(orbitalvelocity, "is the orbital velocity of an object")

gravitationalredshift = (1 / math.sqrt(1 - (r_s / r))) - 1
print(gravitationalredshift, "is the gravitational redshift")
    
print('Gravitational Potential Energy Engine')
m=int(input('Enter the mass of the object near the black hole'))
gravitationalpotentialenergy=-((G*m*M)/r)
print(gravitationalpotentialenergy,'is the gravitational potential energy')

print('Acceleration required to hover at distance r from black hole calculator')
acceleration=(G*M)/(r**2*math.sqrt(1-r_s/r))
print(acceleration, 'is the acceleration required to hover above the black hole')

print('Orbital period near a black hole calculator')
orbitalperiod=2*math.pi*math.sqrt(r**3/(G*M))
print(orbitalperiod, 'is the orbital period of the black hole')

print('Tidal force calculator')
h=int(input('Enter the persons height'))
tidalforce=(2*G*M*h)/(r**3)
print(tidalforce, 'is the tidalforce')

print('Usage of Special Relativistic Formulae')
print('Accretion Disk Physics Calculator')
print('Time Dilation for orbiting particle')
dtau_dt = math.sqrt(1 - 3*G*M/(r*c**2))
print(dtau_dt, "is the SR time dilation for an orbiting particle")

print('Local Orbital Velocity Calculator')
omega = math.sqrt(G*M / r**3)
v_local = (r * omega) / math.sqrt(1 - r_s/r)
print(v_local, "is the local orbital velocity seen by a stationary observer")

print('Lorentz Factor Calculation')
gamma = 1 / math.sqrt(1 - (v_local**2 / c**2))
print(gamma, "is the SR Lorentz factor of the orbiting particle")

print('Full observed frequency shift')
theta=int(input('Enter the angle between the velocity and observer line of sight'))
theta=math.radians(theta)
g_factor = math.sqrt(1 - r_s/r) / (gamma * (1 - (v_local/c) * math.cos(theta)))
print(g_factor, "is the total relativistic redshift factor")

print('All calculations are printed and are successful, below is the summary of results : ')
print(r_s,'is the schwarzchild radius')
print(escapevelocity,'is the escape velocity')
print(gravitationalacceleration,'is the gravitational acceleration')
print(orbitalvelocity,'is the orbital velocity')
print(gravitationalredshift,'is the gravitational redshift')
print(gravitationalpotentialenergy, 'is the gravitational potential energy')
print(acceleration,'is the acceleration')
print(orbitalperiod,'is the orbital period')
print(tidalforce,'is the tidal force')
print(g_factor,'is the total relativistic redshift factor')
print(gamma,'is the special relativistic time lorentz factor of an orbiting particle')
print(v_local, "is the local orbital velocity seen by a stationary observer")
print(dtau_dt, "is the GR time dilation for an orbiting particle")
k=str(input(''))
if k =='kill':
      print('This code has been terminated')
else:
      print('Thanks for using the simulator, have a nice day!')
