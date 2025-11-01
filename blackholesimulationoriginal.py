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
    
print('Compressed Length Calculator Machine')
lengthselection=int(input('Enter 0 if providing viewers length, enter 1 if providing fallers length'))
if lengthselection==0:
    viewersleng=float(input('Enter the viewers length '))
    fallerslength=viewersleng*math.sqrt(1-(r_s/r))
    print(fallerslength,'is the fallerslength')
else:
    fallerslen=float(input('Enter the fallers length'))
    viewerslength=fallerslen/(math.sqrt(1-(r_s/r)))
    print(viewerslength,'is the viewers length')
  
print('Gravitational Potential Energy Engine')
m=int(input('Enter the mass of the object near the black hole'))
gravitationalpotentialenergy=-((G*m*M)/r)
print(gravitationalpotentialenergy,'is the gravitational potential energy')

print('Acceleration required to hover at distance r from black hole calculator')
acceleration=G*M/r**2*math.sqrt(1-(r_s/r))
print(acceleration, 'is the acceleration required to hover above the black hole')

print('Orbital period near a black hole calculator')
orbitalperiod=2*math.pi*math.sqrt(r**3/(G*M))
print(orbitalperiod, 'is the orbital period of the black hole')

print('Tidal force calculator')
h=int(input('Enter the persons height'))
tidalforce=(2*G*M*h)/(r**3)
print(tidalforce, 'is the tidalforce')

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
k=str(input(''))
if k =='kill':
      print('This code has been terminated')
else:
      print('Thanks for using the simulator, have a nice day!')
