from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

colors = []

width = height = 900
eps: int
iterations: int
umin: float
umax: float
vmin: float
vmax: float
method: int
creal: float
cimag: float
window: GLint

def myReshape(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.0)	
    glFlush()

def myDisplay():
    global creal, cimag
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    colors = [[(i * 2)/iterations,0,0] for i in range(round(iterations/2))]
    colors.extend([[0,0,((i - round(iterations/2)) * 2)/iterations] for i in range(round(iterations/2), iterations + 1)])
    for x in range(width):
        for y in range(height):
            u_zero = (umax - umin)/width * x + umin
            v_zero = (vmax - vmin)/height * y + vmin
            r = 0
            k = -1
            if method == 0:
                creal = u_zero
                cimag = v_zero
                zreal = 0
                zimag = 0
            else:
                zreal = u_zero
                zimag = v_zero
            while r < eps and k < iterations:
                k = k + 1
                zrealnew = zreal ** 2 - zimag ** 2
                zimagnew = 2 * zreal * zimag
                zreal = zrealnew + creal
                zimag = zimagnew + cimag
                r = math.sqrt(zreal ** 2 + zimag ** 2)
            glBegin(GL_POINTS)
            glColor3f(colors[k][0], colors[k][1], colors[k][2])
            glVertex2f(x, y)
            glEnd()
            glFlush()

def main():
    global eps, iterations, umin, umax, vmin, vmax, method, creal, cimag
    print('Sets:\n0) Mandelbrot set\n1) Julia set')
    method = int(input('Set: '))
    while method not in [0, 1]:
        method = int(input('Invalid set, please choose a set from one of above (0 or 1): '))
    eps = int(input('Epsilon threshold: '))
    iterations = int(input('Max iterations: '))
    umin, umax = list(eval(input('(umin, umax): ')))
    vmin, vmax = list(eval(input('(vmin, vmax): ')))
    if method == 1:
        creal, cimag = list(eval(input('(creal, cimag): ')))
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow("OpenGL")
    glutReshapeFunc(myReshape)
    glutDisplayFunc(myDisplay)
    glutMainLoop()



if __name__ == "__main__":
    main()