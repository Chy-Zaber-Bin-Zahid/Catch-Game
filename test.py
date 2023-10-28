from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 600
move = 0
fall = 0
point = 0
speed = .1
game = "continue"
randomValue = random.randint(0, 440)
basketOver = False
play = "resume"

colorFour = [[1.0,0.0,0.0],[0.0,0.0,1.0],[0.0,1.0,0.0],[1.0,1.0,0.0]]
diamondColor = random.choice(colorFour)
r = diamondColor[0]
g = diamondColor[1]
b = diamondColor[2]

diamondCornerZero = 0
diamondCornerFifteen = 15
diamondCornerThirty = 30



class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and # x_min_1 < x_max_2
                self.x + self.w > other.x  and # x_max_1 > m_min_2
                self.y < other.y + other.h and # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2
    


box1 = AABB(190, 10, 122, 31)
box2 = AABB(15+randomValue, 510, 33, 40)
box3 = AABB(10, 549, 38, 31)
box4 = AABB(240, 545, 34, 35)
box5 = AABB(450, 545, 31, 35)

box_speed = 7
collision = False

def draw_box(box):
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(box.x, box.y)
    glVertex2f(box.x + box.w, box.y)

    glVertex2f(box.x + box.w, box.y)
    glVertex2f(box.x + box.w, box.y + box.h)

    glVertex2f(box.x + box.w, box.y + box.h)
    glVertex2f(box.x, box.y + box.h)

    glVertex2f(box.x, box.y + box.h)
    glVertex2f(box.x, box.y)
    glEnd()

def check_collision():
    global box1, box2, collision

    if box1.collides_with(box2):
        collision = True
    else:
        collision = False

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


def show_screen():
    global move,fall,diamondCornerZero,diamondCornerFifteen,diamondCornerThirty,randomValue,r,g,b, basketOver, play
    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #diamond
    glColor3f(r, g, b)
    drawLine(diamondCornerZero+randomValue,530+fall,diamondCornerFifteen+randomValue,550+fall)
    drawLine(diamondCornerFifteen+randomValue,550+fall,diamondCornerThirty+randomValue,530+fall)
    drawLine(diamondCornerZero+randomValue,532+fall,diamondCornerFifteen+randomValue,510+fall)
    drawLine(diamondCornerFifteen+randomValue,510+fall,diamondCornerThirty+randomValue,529+fall)

    #basket
    if basketOver == False: 
      glColor3f(1, 1, 1)
    else:
      glColor3f(1.0, 0.0, 0.0)
    drawLine(210+move,10,290+move,10)
    drawLine(190+move,40,310+move,40)
    drawLine(270+move,10,290+move,40)
    drawLine(169+move,40,190+move,10)

    #playAgain
    glColor3f(0.529, 0.808, 0.922)
    drawLine(10,565,45,565)
    drawLine(0,564,10,580)
    drawLine(0,565,10,550)

    if play == "resume":
      #pause
      glColor3f(1.0, 0.647, 0.0)
      drawLine(247,545,247,580)
      drawLine(257,545,257,580)
    else:
      #play
      glColor3f(1.0, 0.647, 0.0)
      drawLine(240,545,240,580)
      drawLine(239,525,270,545)
      drawLine(240,594,270,579)

    #close
    glColor3f(1,0.0, 0.0)
    drawLine(420,545,450,580)
    drawLine(420,580,450,545)

    draw_box(box1)
    draw_box(box2)
    draw_box(box3)
    draw_box(box4)
    draw_box(box5)

    glutSwapBuffers()


def keyboard_special_keys(key, _, __):
    global move, box
    if key == GLUT_KEY_LEFT:
        if move != -190:
            box1.x -= box_speed
            move-=7
    elif key == GLUT_KEY_RIGHT:
        if move != 190:
            box1.x += box_speed
            move+=7
        

    glutPostRedisplay()

def animation():
    global fall,randomValue,diamondColor,r,g,b,colorFour,box1, collision,diamondCornerThirty, point,game,speed, basketOver
    check_collision()

    if game == "continue":
        if speed <= .3:
          fall-=speed
          box2.y-=speed
        else:
          fall-=.2
          box2.y-=.2
        if collision:
            fall = 0
            randomValue = random.randint(0, 440)
            box2.y = 510
            box2.x = randomValue+15
            previous = diamondColor
            colorFour.remove(previous)
            diamondColor = random.choice(colorFour)
            colorFour.append(previous)
            r = diamondColor[0]
            g = diamondColor[1]
            b = diamondColor[2]
            collision = False
            speed+=.05
            point+=1
            print(f"You Scored {point}")
        elif fall < -551:
            print(f"Game Over your score {point}!")
            game="finished"
            basketOver = True



    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL AABB Collision")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

# glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
# glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
