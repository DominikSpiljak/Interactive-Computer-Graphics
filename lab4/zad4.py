import argparse
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width = 500
height = 500

angle = 0.0
refreshMills = 15

points = []
polygons = []
window : GLint

def myReshape(width, height):
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.0)
    glColor3f(0.0, 0.0, 0.0)

def center_and_scale_model():
    x = [point[0].value for point in points]
    y = [point[1].value for point in points]
    z = [point[2].value for point in points]
    maxx = max(x)
    minx = min(x)
    maxy = max(y)
    miny = min(y)
    maxz = max(z)
    minz = min(z)
    div = max([maxx - minx, maxy - miny, maxz - minz])
    for point in points:
        point[0] = GLfloat(((point[0].value - (minx + maxx)/2)) * (2/div))
        point[1] = GLfloat(((point[1].value - (miny + maxy)/2)) * (2/div))
        point[2] = GLfloat(((point[2].value - (minz + maxz)/2)) * (2/div))

def myDisplay():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(angle, 0.0, 1.0, 0.0)
    for polygon in polygons:

        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(points[polygon[0]][0], points[polygon[0]][1], points[polygon[0]][2])
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(points[polygon[1]][0], points[polygon[1]][1], points[polygon[1]][2])
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(points[polygon[2]][0], points[polygon[2]][1], points[polygon[2]][2])
        glEnd()
    angle += 0.2
    glutSwapBuffers()


def parse_args():
    parser = argparse.ArgumentParser(description='Draws 3d model from object file')
    parser.add_argument('object_file', help='path to object file')
    parser.add_argument('point', help='point to check if inside object')
    args = parser.parse_args()
    return args


def read_file(object_file):
    global points, polygons
    with open(object_file, 'r') as inp:
        for line in inp:
            if line.startswith('v'):
                line = line.strip().split(' ')
                points.append([GLfloat(float(line[1])), GLfloat(float(line[2])), GLfloat(float(line[3]))])
            elif line.startswith('f'):
                line = line.strip().split(' ')
                polygons.append([int(line[1]) - 1, int(line[2]) - 1, int(line[3]) - 1])

def check_point(point):
    point = list(eval(point))
    x = point[0]
    y = point[1]
    z = point[2]
    for polygon in polygons:
        x1 = points[polygon[0]][0].value
        x2 = points[polygon[1]][0].value
        x3 = points[polygon[2]][0].value
        y1 = points[polygon[0]][1].value
        y2 = points[polygon[1]][1].value
        y3 = points[polygon[2]][1].value
        z1 = points[polygon[0]][2].value
        z2 = points[polygon[1]][2].value
        z3 = points[polygon[2]][2].value
        A = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        B = -1 * (x2 - x1) * (z3 - z1) + (z2 - z1) * (x3 - x1)
        C = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        D = -1 * x1 * A - y1 * B - z1 * C

        VR = A*x + B*y + C*z + D
        if VR > 0:
            print('Tocka nije unutar objekta!')
            return
    print('Tocka je unutar objekta')

def timer(value):
   glutPostRedisplay()
   glutTimerFunc(refreshMills, timer, 0)

def main():
    global window
    args = parse_args()
    read_file(args.object_file)
    center_and_scale_model()

    if args.point is not None:
        check_point(args.point)

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)

    glutCreateWindow("Glut OpenGL 3d object")
    glutReshapeFunc(myReshape)
    glutDisplayFunc(myDisplay)

    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__=="__main__":
    main()
