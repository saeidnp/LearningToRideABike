#!/usr/bin/python3

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import  *
import sys
import time

import constants as consts
from bicycle_model import *


window = 0     # number of the glut window
simTime = 0
simRun = True
ground_height = -10
resize_image = 1

axis_to_rotate = 0
lookat = [1,1,3,  0,0,0,  0,1,0]
lookat_idx = 0

class Obj:
    color=[1,0.9,0.9]    ## draw color
    #color=[7/256,0,217/256]
    size = [.1, .3, 0.8]     ## dimensions
    size_handlebar = [0.5, 0.05, 0.05]

    theta=np.array([0, 0, 0])          ## 3D orientation
    steering_angle = 0
    posn=np.array([0.0,0.0,0.0])     ## 3D position (keep z=0 for 2D)

    def setDynamicAttrs(self, posn, theta, steering_angle):
        self.posn = posn
        self.theta = theta
        self.steering_angle = steering_angle

    def draw(self):                     ### steps to draw an obj
        glPushMatrix()                  ## save copy of coord frame
        handlebar_x = self.posn[0]
        handlebar_y = self.posn[1]
        handlebar_z = self.posn[2]
        glTranslatef(handlebar_x, \
                    handlebar_y, \
                    handlebar_z)      ## move (puts the handlebar on the center of the bike)
        glRotatef(self.theta[0],  1,0,0)                 ## rotate
        glRotatef(self.theta[1],  0,1,0)                 ## rotate
        glRotatef(self.theta[2],  0,0,1)                 ## rotate
        glTranslatef(0, \
                    self.size[1]/2 + self.size_handlebar[1]/2, \
                    - (self.size[2]/2 - self.size_handlebar[2]/2))      ## move (puts the handlebar from center of the bike to its corner)
        glRotatef(self.steering_angle, 0,1,0)                           ## Rotate handlebar according to steering angle
        glScale(self.size_handlebar[0], self.size_handlebar[1], self.size_handlebar[2])           ## set size
        glColor3f(self.color[0], self.color[1], self.color[2])      ## set colour
        DrawCube()                                                  ## draw a scaled cube
        glPopMatrix()                                               ## restore old coord frame

        glPushMatrix()                                      ## save copy of coord frame
        glTranslatef(self.posn[0], self.posn[1], self.posn[2])      ## move
        glRotatef(self.theta[0],  1,0,0)                 ## rotate
        glRotatef(self.theta[1],  0,1,0)                 ## rotate
        glRotatef(self.theta[2],  0,0,1)                 ## rotate
        glScale(self.size[0], self.size[1], self.size[2])           ## set size
        glColor3f(self.color[0], self.color[1], self.color[2])      ## set colour
        DrawCube()                                                  ## draw a scaled cube
        glPopMatrix()                                               ## restore old coord frame

def start(idleFunc):
    global window
    global obj
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)     # display mode
    glutInitWindowSize(640, 480)                                  # window size
    glutInitWindowPosition(0, 0)                                  # window coords for mouse start at top-left
    window = glutCreateWindow("Bicycle")
    glutDisplayFunc(DrawWorld)       # register the function to draw the world
    # glutFullScreen()               # full screen
    glutIdleFunc(idleFunc)           # when doing nothing, redraw the scene
    glutReshapeFunc(ReSizeGLScene)   # register the function to call when window is resized
    glutKeyboardFunc(keyPressed)     # register the function to call when keyboard is pressed
    InitGL(640, 480)                 # initialize window

    obj = Obj()

    #resetSim()

    glutMainLoop()                   # start event processing loop

def resetSim():
    global simTime, simRun
    global obj

    printf("Simulation reset\n")
    simRun = True
    simTime = 0

def SimWorld(model):
    global simRun, simTime
    global obj

    simTime += consts.dt

    #### draw the updated state
    if (simRun==False):             ## is simulation stopped?
        return
    obj.setDynamicAttrs(np.array([model.posn[1], 0, -model.posn[0]]),\
                        -np.array([0, model.heading_angle, model.lean_angle]),\
                        -model.steering_angle)

    DrawWorld()
    #printf("simTime=%.2f\n",simTime)
    #printf("(%f, %f)\n", model.posn[0], model.posn[1])

def keyPressed(key,x,y):
    global simRun
    global obj
    global lookat, lookat_idx
    global axis_to_rotate

    ch = key.decode("utf-8")
    if ch == ' ':                #### toggle the simulation
        if (simRun == True):
             simRun = False
        else:
             simRun = True
    elif ch == chr(27):          #### ESC key
        sys.exit()
    elif ch == 'q':              #### quit
        sys.exit()
    elif ch == 'r':              #### reset simulation
        resetSim()
    elif ch == 'x':
        axis_to_rotate = 0
    elif ch == 'y':
        axis_to_rotate = 1
    elif ch == 'z':
        axis_to_rotate = 2
    elif ord(ch) >= ord('1') and ch <= '9':
        axis_to_rotate = -1
        lookat_idx = ord(ch) - ord('1')
    elif ch == 'w':
        if axis_to_rotate == -1:
            lookat[lookat_idx] += 1
        else:
            obj.theta[axis_to_rotate] += 2
    elif ch == 's':
        if axis_to_rotate == -1:
            lookat[lookat_idx] -= 1
        else:
            obj.theta[axis_to_rotate] -= 2

#####################################################
#### DrawWorld():  draw the world
#####################################################
def DrawWorld():
    global obj
    global lookat

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
    glLoadIdentity();
    #gluLookAt(lookat[0],lookat[1],lookat[2],  lookat[3],lookat[4],lookat[5],  lookat[6],lookat[7],lookat[8])
    gluLookAt(obj.posn[0]+1,1,obj.posn[2]+3,  obj.posn[0],obj.posn[1],obj.posn[2],  0,1,0)

    DrawOrigin()
    obj.draw()

    DrawGround()

    glutSwapBuffers()                      # swap the buffers to display what was just drawn

def InitGL(Width,Height):				# We call this right after our OpenGL window is created.
    glClearColor(1.0, 1.0, 0.9, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);    glEnable( GL_LINE_SMOOTH );
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

#####################################################
#### ReSizeGLScene():    called when window is resized
#####################################################
def ReSizeGLScene(Width,Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
	    Height = 1
    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)    ## 45 deg horizontal field of view, aspect ratio, near, far
    glMatrixMode(GL_MODELVIEW)

#####################################################
#### DrawOrigin():  draws RGB lines for XYZ origin of coordinate system
#####################################################
def DrawOrigin():
    glLineWidth(3.0);

    glColor3f(1,0.5,0.5)   ## light red x-axis
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glEnd()

    glColor3f(0.5,1,0.5)   ## light green y-axis
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glEnd()

    glColor3f(0.5,0.5,1)   ## light blue z-axis
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

#####################################################
#### DrawGround():  draws the ground
#####################################################
def DrawGround():
    global ground_height, obj

    ground_height = -obj.size[1]

    ground_vertices = []
    d = 40
    mx = 100.0
    mn = -10.0
    for i in range(d):
        ground_vertices.append(((-mx + 2.0*mx/d*i, ground_height, 300),
                                (-mx + 2.0*mx/d*(i+1),ground_height,300),
                                (mn - 2.0*mn/d*i,ground_height,-300),
                                (mn - 2.0*mn/d*(i+1),ground_height,-300),
                                ))

    colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 1),
    )

    glBegin(GL_QUADS)

    #for i in range(len(ground_vertices)):
    #    glColor3fv(colors[i])
    #    glVertex3fv(ground_vertices[i])

    #for vertex in ground_vertices:
    #    glColor3fv((0,0.1,0.1))
    #    glVertex3fv(vertex)

    for i in range(len(ground_vertices)):
        for vertex in ground_vertices[i]:
            glColor3fv((i%2, i%2, i%2))
            glVertex3fv(vertex)


    glEnd()

#####################################################
#### DrawCube():  draws a cube that spans from (-1,-1,-1) to (1,1,1)
#####################################################
def DrawCube():
	glScalef(0.5,0.5,0.5);                  # dimensions below are for a 2x2x2 cube, so scale it down by a half first
	glBegin(GL_QUADS);			# Start Drawing The Cube

	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Top)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Top)
	glVertex3f(-1.0, 1.0, 1.0);		# Bottom Left Of The Quad (Top)
	glVertex3f( 1.0, 1.0, 1.0);		# Bottom Right Of The Quad (Top)

	glVertex3f( 1.0,-1.0, 1.0);		# Top Right Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0, 1.0);		# Top Left Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Bottom)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Bottom)

	glVertex3f( 1.0, 1.0, 1.0);		# Top Right Of The Quad (Front)
	glVertex3f(-1.0, 1.0, 1.0);		# Top Left Of The Quad (Front)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Front)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Front)

	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Back)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Back)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Right Of The Quad (Back)
	glVertex3f( 1.0, 1.0,-1.0);		# Top Left Of The Quad (Back)

	glVertex3f(-1.0, 1.0, 1.0);		# Top Right Of The Quad (Left)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Left)

	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Right)
	glVertex3f( 1.0, 1.0, 1.0);		# Top Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Right)
	glEnd();				# Done Drawing The Quad

            ### Draw the wireframe edges
	glColor3f(0.0, 0.0, 0.0);
	glLineWidth(1.0);

	glBegin(GL_LINE_LOOP);
	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Top)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Top)
	glVertex3f(-1.0, 1.0, 1.0);		# Bottom Left Of The Quad (Top)
	glVertex3f( 1.0, 1.0, 1.0);		# Bottom Right Of The Quad (Top)
	glEnd();				# Done Drawing The Quad

	glBegin(GL_LINE_LOOP);
	glVertex3f( 1.0,-1.0, 1.0);		# Top Right Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0, 1.0);		# Top Left Of The Quad (Bottom)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Bottom)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Bottom)
	glEnd();				# Done Drawing The Quad

	glBegin(GL_LINE_LOOP);
	glVertex3f( 1.0, 1.0, 1.0);		# Top Right Of The Quad (Front)
	glVertex3f(-1.0, 1.0, 1.0);		# Top Left Of The Quad (Front)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Front)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Front)
	glEnd();				# Done Drawing The Quad

	glBegin(GL_LINE_LOOP);
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Back)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Back)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Right Of The Quad (Back)
	glVertex3f( 1.0, 1.0,-1.0);		# Top Left Of The Quad (Back)
	glEnd();				# Done Drawing The Quad

	glBegin(GL_LINE_LOOP);
	glVertex3f(-1.0, 1.0, 1.0);		# Top Right Of The Quad (Left)
	glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Left)
	glVertex3f(-1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Left)
	glEnd();				# Done Drawing The Quad

	glBegin(GL_LINE_LOOP);
	glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Right)
	glVertex3f( 1.0, 1.0, 1.0);		# Top Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Right)
	glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Right)
	glEnd();				# Done Drawing The Quad

####################################################
# printf()
####################################################
def printf(format, *args):
    sys.stdout.write(format % args)