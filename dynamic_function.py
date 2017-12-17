from math import *
import constants as const

def dynamicFunction(r, model): #TODO: fix the inputs
    v = model.velocity
    g = const.g
    l = model.get_l()
    I = model.I
    m = model.mass
    v_2_r = 0
    theta = radians(model.lean_angle)

    if(r != -1):
        v_2_r = v**2/r

    #num = -v**2/r * cos(theta) + l*sin(theta)*cos(theta)* v**2/r**2 + g*sin(theta) #TODO: r==0
    num = -v_2_r * cos(theta) + l*sin(theta)*cos(theta)* v_2_r/r + g*sin(theta)
    denum = I/m*l + l
    theta_doubledot = num/denum
    return theta_doubledot