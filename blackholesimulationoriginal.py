import math
G=6.674e-11
c=3.0e8

M=float(input("Enter the mass of black hole (kilograms): "))
r=float(input("Enter the distance of the person from the black hole (meters): "))
r_s=(2*G*M)/c**2
print(r_s, "meters is the Schwarzschild radius")

time = int(input("Enter 0 for faller’s time (input viewer’s time), or 1 for viewer’s time (input faller’s time): "))

if time == 0:
        viewerstime = float(input("Enter the viewer's time (seconds): "))
        t_faller = viewerstime * math.sqrt((1 - r_s / r))
        print(t_faller, "seconds is the faller’s time")
else:
        fallerstime = float(input("Enter the faller’s time (seconds): "))
        t_viewer = fallerstime / math.sqrt(1 - r_s / r)
        print(t_viewer, "seconds is the viewer’s time")

escapevelocity = math.sqrt((2 * G * M) / r)
print(escapevelocity, "m/s is the escape velocity")

gravitationalacceleration = (G * M) / (r**2)
print(gravitationalacceleration, "m/s^2 is the gravitational acceleration near the black hole")

orbitalvelocity = math.sqrt((G * M) / r)
print(orbitalvelocity, "m/s is the orbital velocity of an object")

gravitationalredshift = (1 / math.sqrt(1 - (r_s / r))) - 1
print(gravitationalredshift, "(dimensionless) is the gravitational redshift")
    
print('Gravitational Potential Energy Engine')
m=int(input('Enter the mass of the object near the black hole'))
gravitationalpotentialenergy=-((G*m*M)/r)
print(gravitationalpotentialenergy,'joules is the gravitational potential energy')

print('Acceleration required to hover at distance r from black hole calculator')
acceleration=(G*M)/(r**2*math.sqrt(1-r_s/r))
print(acceleration, 'm/s^2 is the acceleration required to hover above the black hole')

print('Orbital period near a black hole calculator')
orbitalperiod=2*math.pi*math.sqrt(r**3/(G*M))
print(orbitalperiod, 'seconds is the orbital period of the black hole')

print('Tidal force calculator')
h=int(input('Enter the persons height'))
tidalforce=(2*G*M*h)/(r**3)
print(tidalforce, 'newtons per meter is the tidal force')

print('Deflection angle of light due to lensing')
alpha = 4 * G * M / (r * c**2)
print(alpha,'radians is the deflection angle of light')

print('Shapiro Time Delay Calculator')
r1 = float(input("Enter distance from the light source to the black hole (meters): "))
r2 = float(input("Enter distance from the black hole to the observer (meters): "))
shapiro_delay = (2 * G * M / c**3) * math.log((4 * r1 * r2) / (r**2))
print(shapiro_delay, "seconds is the Shapiro time delay or the delay that light faces when passing close to the black hole")

print('Usage of Special Relativistic Formulae')
print('Accretion Disk Physics Calculator')
print('Time Dilation for orbiting particle')
dtau_dt = math.sqrt(1 - 3*G*M/(r*c**2))
print(dtau_dt, "(dimensionless) is the SR time dilation for an orbiting particle")

print('Local Orbital Velocity Calculator')
omega = math.sqrt(G*M / r**3)
v_local = (r * omega) / math.sqrt(1 - r_s/r)
print(v_local, "m/s is the local orbital velocity seen by a stationary observer")

print('Lorentz Factor Calculation')
gamma = 1 / math.sqrt(1 - (v_local**2 / c**2))
print(gamma, "(dimensionless) is the SR Lorentz factor of the orbiting particle")

print('Full observed frequency shift')
theta=int(input('Enter the angle between the velocity and observer line of sight'))
theta=math.radians(theta)
g_factor = math.sqrt(1 - r_s/r) / (gamma * (1 - (v_local/c) * math.cos(theta)))
print(g_factor, "(dimensionless) is the total relativistic redshift factor")

print('All calculations are printed and are successful, below is the summary of results : ')
print(r_s,'meters is the schwarzchild radius')
print(escapevelocity,'m/s is the escape velocity')
print(gravitationalacceleration,'m/s^2 is the gravitational acceleration')
print(orbitalvelocity,'m/s is the orbital velocity')
print(gravitationalredshift,'(dimensionless) is the gravitational redshift')
print(gravitationalpotentialenergy, 'joules is the gravitational potential energy')
print(acceleration,'m/s^2 is the acceleration')
print(orbitalperiod,'seconds is the orbital period')
print(tidalforce,'newtons per meter is the tidal force')
print(g_factor,'(dimensionless) is the total relativistic redshift factor')
print(gamma,'(dimensionless) is the special relativistic time lorentz factor of an orbiting particle')
print(v_local, "m/s is the local orbital velocity seen by a stationary observer")
print(dtau_dt, "(dimensionless) is the GR time dilation for an orbiting particle")

k=str(input(''))
if k =='kill':
      print('This code has been terminated')
else:
      print('Thanks for using the simulator, have a nice day!')

