from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 800

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

# Global variables
box1 = AABB(200, 150, 100, 100)
box2 = AABB(350, 250, 50, 50)
box_speed = 5
collision = False

def draw_box(box):
    global collision
    is_colliding = collision
    
    if is_colliding:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(0.0, 1.0, 0.0)

    # glBegin(GL_LINES)
    # glVertex2f(box.x, box.y)
    # glVertex2f(box.x + box.w, box.y)

    # glVertex2f(box.x + box.w, box.y)
    # glVertex2f(box.x + box.w, box.y + box.h)

    # glVertex2f(box.x + box.w, box.y + box.h)
    # glVertex2f(box.x, box.y + box.h)

    # glVertex2f(box.x, box.y + box.h)
    # glVertex2f(box.x, box.y)
    # glEnd()

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def check_collision():
    global box1, box2, collision

    if box1.collides_with(box2):
        collision = True
    else:
        collision = False

def show_screen():
    # this function should contain the logic for drawing objects
    # DO NOT do game logic here (e.g. object movement, collision detection, sink detection etc.)

    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw stuffs here
    draw_box(box1)
    draw_box(box2)

    # do not forget to call glutSwapBuffers() at the end of the function
    glutSwapBuffers()

def keyboard_ordinary_keys(key, _, __):
    # check against alphanumeric keys here (e.g. A..Z, 0..9, spacebar, punctuations)
    # must cast characters to binary when comparing (e.g. key == b'q')

    glutPostRedisplay()

def keyboard_special_keys(key, _, __):
    # check against special keys here (e.g. F1..F11, arrow keys, etc.)
    # use GLUT_KEY_* constants while comparing (e.g. GLUT_KEY_F1, GLUT_KEY_LEFT, etc.)
    global box1

    if key == GLUT_KEY_UP:
        box1.y += box_speed
    elif key == GLUT_KEY_DOWN:
        box1.y -= box_speed
    elif key == GLUT_KEY_LEFT:
        box1.x -= box_speed
    elif key == GLUT_KEY_RIGHT:
        if box1.x != 450:
            box1.x += box_speed
        print(box1.x)

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    # check for mouse clicks here (left, middle and right click)
    # use GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON constants while comparing
    # use GLUT_DOWN and GLUT_UP constants while comparing for button state
    # You should either listen to GLUT_DOWN or GLUT_UP, so filter that out

    # convert coordinates, (flip the y-axis first)
    mx, my = x, WINDOW_HEIGHT - y

    # do your click detection here using button, state, mx, my


    glutPostRedisplay()

def animation():
    # write codes here that's going to run every frame
    # for example, updating coordinates of objects that move spotaneously
    # or collision detection, or sink detection, etc.
    # Note: DO NOT write drawing codes here

    check_collision()


    # don't forget to call glutPostRedisplay()
    # otherwise your animation will be stuck
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL AABB Collision")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
