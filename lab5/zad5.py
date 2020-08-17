import argparse
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width = 500
height = 500
viewpoint = []
H = 0
scale = 2

points = []
polygons = []
window: GLint

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
        point[0] = GLfloat(((point[0].value - (minx + maxx)/2)) * (scale/div))
        point[1] = GLfloat(((point[1].value - (miny + maxy)/2)) * (scale/div))
        point[2] = GLfloat(((point[2].value - (minz + maxz)/2)) * (scale/div))


def multiply_array_of_matrices(matrices):
    result = matrices[0]
    for i in range(1, len(matrices)):
        X = result
        Y = matrices[i]
        result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
    return result


def get_transformation_matrix():
    global points
    global H
    model_center = [0 - viewpoint[0], 0 - viewpoint[1], 0 - viewpoint[2]]
    t1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [model_center[0], model_center[1], model_center[2], 1]]
    sinalpha = model_center[1] / (math.sqrt(model_center[0] ** 2 + model_center[1] ** 2))
    cosalpha = model_center[0] / (math.sqrt(model_center[0] ** 2 + model_center[1] ** 2))   
    model_center = [math.sqrt(model_center[0] ** 2 + model_center[1] ** 2), 0, model_center[2]]
    t2 = [[cosalpha, -sinalpha, 0, 0], [sinalpha, cosalpha, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    sinbeta = model_center[0] / (math.sqrt(model_center[0] ** 2 + model_center[2] ** 2))
    cosbeta = model_center[2] / (math.sqrt(model_center[0] ** 2 + model_center[2] ** 2))
    model_center = [0, 0, math.sqrt(model_center[0] ** 2 + model_center[2] ** 2)]
    t3 = [[cosbeta, 0, sinbeta, 0], [0, 1, 0, 0], [-sinbeta, 0, cosbeta, 0], [0, 0, 0, 1]]
    H = model_center[2]
    t4 = [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    t5 = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    return multiply_array_of_matrices([t1, t2, t3, t4, t5])


def myReshape(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.0)
    glColor3f(0.0, 0.0, 0.0)


def myDisplay():
    center_and_scale_model()
    transform_matrix = get_transformation_matrix()
    transformed_points = []
    #Transforming points
    for i in range(len(points)):
        transformed_point = [part.value for part in points[i]]
        transformed_point.append(1.0)
        transformed_point = multiply_array_of_matrices([[transformed_point], transform_matrix])[0]
        draw_point = [transformed_point[0]/transformed_point[2] * H, transformed_point[1]/transformed_point[2] * H]
        draw_point = [GLfloat(part) for part in draw_point]
        transformed_points.append(draw_point)
    
    #Drawing points
    for polygon in polygons:
        glBegin(GL_LINE_LOOP)
        glVertex2f(transformed_points[polygon[0]][0], transformed_points[polygon[0]][1])
        glVertex2f(transformed_points[polygon[1]][0], transformed_points[polygon[1]][1])
        glVertex2f(transformed_points[polygon[2]][0], transformed_points[polygon[2]][1])
        glEnd()
    glFlush()


def parse_args():
    parser = argparse.ArgumentParser(description='Draws 3d model from object file')
    parser.add_argument('object_file', help='path to object file')
    parser.add_argument('viewpoint', help='viewpoint (x, y, z)')
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
        if VR >= 0:
            return False
    return True


def myKeyboard(theKey, mouseX, mouseY):
    global viewpoint, scale
    theKey = theKey.decode().lower()
    if theKey == 'w':
        viewpoint[1] += .1
    elif theKey == 's':
        viewpoint[1] -= .1
    elif theKey == 'd':
        viewpoint[0] += .1
    elif theKey == 'a':
        viewpoint[0] -= .1
    elif theKey == 'g':
        viewpoint[2] += .1
    elif theKey == 'f':
        viewpoint[2] -= .1
    elif theKey == '+':
        scale += .1
    elif theKey == '-':
        if scale > .1:
            scale -= .1
    else:
        return
    print('New viewpoint is:')
    print(viewpoint)
    myReshape(width, height)
    myDisplay()


def main():
    global window, viewpoint
    args = parse_args()
    read_file(args.object_file)

    viewpoint = list(eval(args.viewpoint))
    while check_point(viewpoint):
        print('Viewpoint is inside model, choose another one')
        viewpoint = list(eval(input('Viewpoint (x, y, z): ')))

    print("Observation point is calculated as the center of the model (0, 0, 0 since model will be centered)")

    print('Use "a" to decrease viewpoint x value and "d" to increase x value')
    print('Use "s" to decrease viewpoint y value and "w" to increase y value')
    print('Use "f" to decrease viewpoint z value and "g" to increase z value')
    print('Use "-" to zoom out and "+" to zoom in')

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)

    glutCreateWindow("Glut OpenGL 3d object")
    glutReshapeFunc(myReshape)
    glutKeyboardFunc(myKeyboard)
    glutDisplayFunc(myDisplay)
    glutMainLoop()


if __name__ == "__main__":
    main()
