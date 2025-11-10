from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

class Objeto3D:
        
    def __init__(self):
        self.vertices = []
        self.faces    = []
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)
        pass

    def LoadFile(self, file: str):
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()  # remove espaços e quebras de linha
                    if not line or line.startswith('#'):
                        continue  # ignora comentários e linhas vazias

                    parts = line.split()
                    if parts[0] == 'v':  # vértice
                        try:
                            x, y, z = map(float, parts[1:4])
                            self.vertices.append(Ponto(x, y, z))
                        except ValueError:
                            continue

                    elif parts[0] == 'f':  # face
                        face = []
                        for p in parts[1:]:
                            if p == '':
                                continue
                            # pega só o índice do vértice antes da primeira barra
                            v_idx = p.split('/')[0]
                            if v_idx:
                                face.append(int(v_idx) - 1)
                        if len(face) >= 3:  # ignora faces degeneradas
                            self.faces.append(face)


    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(.1, .1, .8)
        glPointSize(8)

        glBegin(GL_POINTS)
        for v in self.vertices:
            glVertex(v.x, v.y, v.z)
        glEnd()
        
        glPopMatrix()
        pass

    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass


