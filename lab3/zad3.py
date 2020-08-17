from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width = height = 300
Ix: GLint
Lx = []
Ly = []
edges = []
window: GLint


def myReshape(w, h):
    global Ix, window, Lx, Ly, edges
    width = w
    height = h
    Ix = 0
    Lx = []
    Ly = []
    edges = []
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

def myDisplay():
    glFlush()

def myMouse(button, state, x, y):
    global Lx, Ly, Ix
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        print("Koordinate tocke {}: {} {} ".format(Ix, x, y))

        Lx.append(x)
        Ly.append(height - y)
        
        Ix += 1
        glVertex2i(x, height - y)
        glFlush()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        myReshape(width, height)
        glFlush()

def myPolygon():
    global Ix, Lx, Ly, edges
    print('Crtanje poligona...')
    if len(Lx) >= 3:
        Lx.append(Lx[0])
        Ly.append(Ly[0])
        edges = []
        for i in range(len(Lx) - 1):
            # Racunanje bridova
            edges.append([Ly[i] - Ly[i + 1],
                          Lx[i + 1] - Lx[i],
                          Lx[i] *  Ly[i + 1] - Lx[i + 1] * Ly[i]])

            # Crtanje bridova
            glBegin(GL_LINES)
            glVertex2i(Lx[i], Ly[i])
            glVertex2i(Lx[i + 1], Ly[i + 1])
            glEnd()
    else:
        print('Nedovoljan broj tocaka!')

def checkDot(x, y):
    y = height - y
    if len(edges) == 0:
        print('Prvo nacrtaj poligon!')
        return
    for edge in edges:
        if(x * edge[0] + y * edge[1] + edge[2] > 0):
            print('Tocka({}, {}) je izvan poligona!'.format(x, y))
            return
    print('Tocka({}, {}) je unutar poligona!'.format(x, y))

def paintPolygon():
    print("Bojanje poligona...")
    for y in range(min(Ly), max(Ly) + 1):
        L = min(Lx)
        D = max(Lx)
        for i, edge in enumerate(edges):
            if edge[0] == 0:
                continue
            else:
                x = (-edge[1] * y - edge[2])/edge[0]
                if Ly[i] < Ly[i + 1]:
                    if x > L:
                        L = x
                else:
                    if x < D:
                        D = x
        if L < D:
            glBegin(GL_LINES)
            glVertex2i(GLint(round(L)), GLint(y))
            glVertex2i(GLint(round(D)), GLint(y))
            glEnd()

def myKeyboard(theKey, mouseX, mouseY):
    theKey = theKey.decode()
    if theKey == 'r':
        glColor3f(1, 0, 0)
        glRecti(width - 15, height - 15, width, height)

    elif theKey == 'g':
        glColor3f(0, 1, 0)
        glRecti(width - 15, height - 15, width, height)

    elif theKey == 'b':
        glColor3f(0, 0, 1)
        glRecti(width - 15, height - 15, width, height)
    
    elif theKey == 'k':
        glColor3f(0, 0, 0)
        glRecti(width - 15, height - 15, width, height)
    
    elif theKey == 'd':
        myPolygon()

    elif theKey == 't':
        checkDot(mouseX, mouseY)

    elif theKey == 'p':
        paintPolygon()

    glFlush()


def main():
    global window
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutInit()

    window = glutCreateWindow("Glut OpenGL Poligon")
    glutReshapeFunc(myReshape)
    glutDisplayFunc(myDisplay)
    glutMouseFunc(myMouse)
    glutKeyboardFunc(myKeyboard)
    print("Lijevom tipkom misa zadaj tocke poligona")
    print("Tipke r, g, b, k mijenjaju boju.")
    print("Tipka d crta poligon na temelju zadanih tocaka")
    print("Tipka t provjerava je li tocka unutar poligona na temelju pozicije misa")
    print("Tipka p oboji poligon")
    glutMainLoop()

if __name__=="__main__":
    main()