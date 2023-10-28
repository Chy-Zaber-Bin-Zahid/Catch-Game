from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 600
move = 0

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    # def collides_with(self, other):
    #     return (self.x < other.x + other.w and # x_min_1 < x_max_2
    #             self.x + self.w > other.x  and # x_max_1 > m_min_2
    #             self.y < other.y + other.h and # y_min_1 < y_max_2
    #             self.y + self.h > other.y)     # y_max_1 > y_min_2


def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def midpoint(x1,y1,x2,y2,zone):
    dx = x2-x1
    dy = y2-y1
    d = (2*dy) - dx
    dE = 2*dy
    dNE = 2*(dy-dx)
    xInitial = x1
    yInitial = y2
    while (xInitial<x2):
        if d<=0:
            d=d+dE
            xInitial+=1
        else:
            d=d+dNE
            xInitial+=1
            yInitial+=1
        cx,cy = convertOriginal(xInitial,yInitial,zone)
        glVertex2f(cx,cy)



def findZone(x1,y1,x2,y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    # if dx>dy:
    #     #zone 0,3,4,7
    #     if dx >= 0 and dy >= 0:
    #         return 0
    #     elif dx <= 0 and dy >= 0:
    #         return 3
    #     elif dx >= 0 and dy <= 0:
    #         return 7
    #     else:
    #         return 4
    # else:
    #     #zone 1,2,5,6
    #     if dx >= 0 and dy >= 0:
    #         return 1
    #     elif dx <= 0 and dy >= 0:
    #         return 2
    #     elif dx >= 0 and dy <= 0:
    #         return 6
    #     else:
    #         return 5
    if dx >= dy:
        if x1 <= x2:
            if y1 <= y2:
                return 0
            else:
                return 7
        else:
            if y1 <= y2:
                return 3
            else:
                return 4
    else:
        if x1 <= x2:
            if y1 <= y2:
                return 1
            else:
                return 6
        else:
            if y1 <= y2:
                return 2
            else:
                return 5
        

def convertZone(x,y,zone):
    if zone == 0:
        return x,y
    elif zone == 1:
        x,y = y,x
        return x,y
    elif zone == 2:
        x,y = y,-x
        return x,y
    elif zone == 3:
        x,y = -x,y
        return x,y
    elif zone == 4:
        x,y = -x,-y
        return x,y
    elif zone == 5:
        x,y = -y,-x
        return x,y
    elif zone == 6:
        x,y = -y,x
        return x,y
    else:
        x,y = x,-y
        return x,y

def convertOriginal(x,y,zone):
    if zone == 0:
        return x,y
    elif zone == 1:
        x,y = y,x
        return x,y
    elif zone == 2:
        x,y = -y,x
        return x,y
    elif zone == 3:
        x,y = -x,y
        return x,y
    elif zone == 4:
        x,y = -x,-y
        return x,y
    elif zone == 5:
        x,y = -y,-x
        return x,y
    elif zone == 6:
        x,y = y,-x
        return x,y
    else:
        x,y = x,-y
        return x,y

def drawLine(x1,y1,x2,y2):
    if x1>x2:
        x1,x2,y1,y2 =x2,x1,y2,y1 
    zone = findZone(x1,y1,x2,y2)
    x1,y1 = convertZone(x1,y1,zone) 
    x2,y2 = convertZone(x2,y2,zone) 
    glBegin(GL_POINTS)
    midpoint(x1,y1,x2,y2,zone)
    glEnd()

0
def show_screen():
    global move
    # this function should contain the logic for drawing objects
    # DO NOT do game logic here (e.g. object movement, collision detection, sink detection etc.)

    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # drawLine(20,10,100,10)
    # drawLine(0,40,120,40)
    # drawLine(80,10,100,40)
    # drawLine(-21,40,0,10)

    drawLine(210+move,10,290+move,10)
    drawLine(190+move,40,310+move,40)
    drawLine(270+move,10,290+move,40)
    drawLine(169+move,40,190+move,10)


    # draw stuffs here
    # draw_box(box1)
    # draw_box(box2)

    # do not forget to call glutSwapBuffers() at the end of the function
    glutSwapBuffers()


def keyboard_special_keys(key, _, __):
    global move
    if key == GLUT_KEY_LEFT:
        if move != -190:
            move-=5
    elif key == GLUT_KEY_RIGHT:
        if move != 190:
            move+=5

    glutPostRedisplay()

# def animation():




#     glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL AABB Collision")

glutDisplayFunc(show_screen)
# glutIdleFunc(animation)

# glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
# glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
