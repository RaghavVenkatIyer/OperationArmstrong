import math
G=6.674e-11
c=3.0e8
M=float(input('Enter the mass of black hole (kilograms) : '))
r=float(input('Enter the distance of the person from the black hole (kilometers): '))
rinmeters=(10**-3)*r
r_s=(2*G*M)/c**2
print(r_s,'is the schwarzchild radius')
time=int(input('Enter 0 if you need to calculate fallers time(viewers time needs to be inputed), and enter 1 if you need to calculate viewers time(fallers time needs to be inputed) : '))
if time ==0:
    viewerstime=float(input('Enter the viewers time (seconds): '))
    t_faller = viewerstime * math.sqrt(1 - r_s / rinmeters)
    print(t_faller)
else:
    fallerstime=float(input('Enter the fallers time (seconds): '))
    t_viewer=fallerstime/math.sqrt(1-r_s/rinmeters)
    print(t_viewer)


