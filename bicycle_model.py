#!/usr/bin/python3

import numpy as np
from math import *
import sys

window = 0     # number of the glut window
simTime = 0
simRun = True
RAD_TO_DEG = 180.0/pi
DEG_TO_RAD = pi/180.0
resize_image = 1
ground_height = -10

class BicycleModel:
    ### Static attributes
    size = [.1, .3, 0.8]            #meters
    mass = 60                       #kg
    color=[1,0.9,0.9]               # draw color
    #color=[7/256,0,217/256]
    d = 1.0                         #m
    I = 10/3*mass * d**2                         #angular mass (kg.m^2)


    visualizer = None

    ### Dynamic attributes
    lean_angle = 0.0                #degrees
    steering_angle = 0.0            #degrees
    heading_angle = 0.0             #degrees
    velocity = 5.0                  #m/s
    lean_angle_dot = 0.0            #deg/s
    posn = np.array([0.0, 0.0])     #m

    def get_l(self):
        return self.size[1]

    def __init__(self, size=[.1, .3, 0.8], color=[1,0.9,0.9], mass=60):
        self.size = size
        self.color = color
        self.mass = mass

    def reset(self):
        self.lean_angle = 0.0
        self.steering_angle = 0.0
        self.heading_angle = 0.0
        self.lean_angle_dot = 0.0
        self.posn = np.array([0.0, 0.0])

    def print(self):
        printf("lean anlge = %f \tsteering angle = %f \theading angle = %f\n", self.lean_angle, self.steering_angle, self.heading_angle)
        printf("velocity = %f \tlean angle dot = %f \tposn = (%f,%f)\n", self.velocity, self.lean_angle_dot, self.posn[0], self.posn[1])


    def update(self, delta_t):
        self.posn += delta_t/100
        self.heading_angle = 20
        self.lean_angle+= delta_t/100

def printf(format, *args):
    sys.stdout.write(format % args)