import numpy as np
import math
G=6.674e-11
c=3.0e8
M=float(input('Enter the mass of black hole : '))
r=float(input('Enter the distance of the person from the black hole : '))
r_s=(2*G*M)/c**2
print(r_s,'is the schwarzchild radius')
time=int(input('Enter 0 if you need to calculate fallers time(viewers time needs to be inputed), and enter 1 if you need to calculate viewers time(fallers time needs to be inputed) : '))
if time ==0:
    viewerstime=float(input('Enter the viewers time : '))
    t_faller = viewerstime * math.sqrt(1 - r_s / r)
    print(t_faller)
else:
    fallerstime=float(input('Enter the fallers time : '))
    t_viewer=fallerstime/math.sqrt(1-r_s/r)
    print(t_viewer)


