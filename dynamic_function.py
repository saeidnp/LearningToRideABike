from math import *
def dynamicFunction(r,theta,g,l,v,I,m): #TODO: fix the inputs
    num = -v**2/r * cos(theta) + l*sin(theta)*cos(theta)* v**2/r**2 + g*sin(theta) #TODO: r==0
    denum = I/m*l +l
    theta_doubledot = num/denum
    return theta_doubledot