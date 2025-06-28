import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos, pi
import random

your_name = "Zhen Rhaizen"

class BurgerGL(OpenGLFrame):
    def initgl(self):
        glutInit()
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION,  (5, 5, 10, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT,   (0.2, 0.2, 0.2, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE,   (0.7, 0.7, 0.7, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR,  (1, 1, 1, 1))
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1))
        glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 50)

        self.angle = 0
        self.auto_rotate = True
        self.pos_x = 0
        self.pos_y = 0
        self.dx = 0.05
        self.dy = 0.04
        self.bounce_boundary = 2.5

        self.text_color = (1, 1, 1)

        self.rot_x = 0
        self.rot_y = 0

        self.bind_all("<space>", self.toggle_rotation)

        self.text_list = glGenLists(1)
        glNewList(self.text_list, GL_COMPILE)
        glPushMatrix()
        glScalef(0.004, 0.004, 0.004)  # Adjust size of name
        for ch in your_name:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
        glPopMatrix()
        glEndList()

        width, height = self.winfo_width(), self.winfo_height()
        self.reshape(width, height)

        self.after(16, self.redraw)

    def reshape(self, width, height):
        if height == 0: height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / float(height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def toggle_rotation(self, event=None):
        self.auto_rotate = not self.auto_rotate
        self.dx = 0.05 if self.auto_rotate else 0
        self.dy = 0.04 if self.auto_rotate else 0

    def draw_gradient_bg(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glBegin(GL_QUADS)
        glColor3f(0.2, 0.3, 0.5)
        glVertex2f(0, 1)
        glVertex2f(1, 1)
        glColor3f(0.05, 0.05, 0.15)
        glVertex2f(1, 0)
        glVertex2f(0, 0)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def draw_hemisphere(self, radius, slices, stacks, top=True, color=(1, 1, 0)):
        glColor3fv(color)
        for i in range(stacks):
            theta1 = (pi / 2) * (i / stacks)
            theta2 = (pi / 2) * ((i + 1) / stacks)
            if not top:
                theta1 = pi - theta1
                theta2 = pi - theta2
            for j in range(slices):
                phi1 = 2 * pi * (j / slices)
                phi2 = 2 * pi * ((j + 1) / slices)
                def norm(x, y, z):
                    l = (x*x + y*y + z*z)**0.5
                    return (x/l, y/l, z/l) if l else (0, 0, 0)
                x1 = radius * cos(phi1) * sin(theta1)
                y1 = radius * sin(phi1) * sin(theta1)
                z1 = radius * cos(theta1)
                nx1, ny1, nz1 = norm(x1, y1, z1)

                x2 = radius * cos(phi1) * sin(theta2)
                y2 = radius * sin(phi1) * sin(theta2)
                z2 = radius * cos(theta2)
                nx2, ny2, nz2 = norm(x2, y2, z2)

                x3 = radius * cos(phi2) * sin(theta2)
                y3 = radius * sin(phi2) * sin(theta2)
                z3 = radius * cos(theta2)
                nx3, ny3, nz3 = norm(x3, y3, z3)

                x4 = radius * cos(phi2) * sin(theta1)
                y4 = radius * sin(phi2) * sin(theta1)
                z4 = radius * cos(theta1)
                nx4, ny4, nz4 = norm(x4, y4, z4)

                glBegin(GL_TRIANGLES)
                glNormal3f(nx1, ny1, nz1); glVertex3f(x1, y1, z1)
                glNormal3f(nx2, ny2, nz2); glVertex3f(x2, y2, z2)
                glNormal3f(nx3, ny3, nz3); glVertex3f(x3, y3, z3)
                glNormal3f(nx1, ny1, nz1); glVertex3f(x1, y1, z1)
                glNormal3f(nx3, ny3, nz3); glVertex3f(x3, y3, z3)
                glNormal3f(nx4, ny4, nz4); glVertex3f(x4, y4, z4)
                glEnd()

    def draw_cylinder(self, radius, height, slices, color):
        glColor3fv(color)
        step = 2 * pi / slices
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(slices + 1):
            angle = i * step
            x = radius * cos(angle)
            y = radius * sin(angle)
            nx, ny = x / radius, y / radius
            glNormal3f(nx, ny, 0)
            glVertex3f(x, y, height / 2)
            glVertex3f(x, y, -height / 2)
        glEnd()
        # Top cap
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 0, 1)
        glVertex3f(0, 0, height / 2)
        for i in range(slices + 1):
            angle = i * step
            x = radius * cos(angle)
            y = radius * sin(angle)
            glVertex3f(x, y, height / 2)
        glEnd()
        # Bottom cap
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 0, -1)
        glVertex3f(0, 0, -height / 2)
        for i in range(slices + 1):
            angle = -i * step
            x = radius * cos(angle)
            y = radius * sin(angle)
            glVertex3f(x, y, -height / 2)
        glEnd()

    def draw_burger(self):
        glPushMatrix()
        glTranslatef(self.pos_x, self.pos_y, 0)

        # Bottom bun
        glPushMatrix()
        glTranslatef(0, 0, -0.4)
        glScalef(1, 1, 0.5)
        self.draw_hemisphere(1.8, 20, 10, top=False, color=(0.93, 0.7, 0.3))
        glPopMatrix()

        # Patty
        glPushMatrix()
        glTranslatef(0, 0, -0.05)
        self.draw_cylinder(1.5, 0.4, 20, (0.4, 0.15, 0.1))
        glPopMatrix()

        # Top bun
        glPushMatrix()
        glTranslatef(0, 0, 0.34)
        glScalef(1, 1, 0.8)
        self.draw_hemisphere(1.8, 20, 10, top=True, color=(0.93, 0.7, 0.3))
        glPopMatrix()

        # Name in center
        glPushMatrix()
        glTranslatef(0, 0, 0.8)
        glColor3fv(self.text_color)
        glCallList(self.text_list)
        glPopMatrix()

        glPopMatrix()

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_gradient_bg()

        glLoadIdentity()
        gluLookAt(7, 0, 3, 0, 0, 0, 0, 0, 1)

        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        if self.auto_rotate:
            self.angle += 0.5
        glRotatef(self.angle, 0, 0, 1)

        self.move_burger()
        self.draw_burger()

        self.tkSwapBuffers()
        self.after(16, self.redraw)

    def move_burger(self):
        self.pos_x += self.dx
        self.pos_y += self.dy
        if abs(self.pos_x) > self.bounce_boundary:
            self.dx *= -1
            self.randomize_text_color()
        if abs(self.pos_y) > self.bounce_boundary:
            self.dy *= -1
            self.randomize_text_color()

    def randomize_text_color(self):
        self.text_color = (random.random(), random.random(), random.random())

def main():
    root = tk.Tk()
    root.title("3D Bouncing Burger - Zhen Rhaizen")
    root.geometry("800x700+300+50")
    root.resizable(False, False)
    frame = BurgerGL(root, width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=tk.YES)
    frame.focus_set()
    root.mainloop()

if __name__ == "__main__":
    main()