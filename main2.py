import sys, random
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Objeto3D import Objeto3D


# Banana1:   f 320
# Bursto1:   f 2500
# Cachorro1: f 3400
# Carro1:    f 8000

# --------------------------------------------------------
# VARIÁVEIS GLOBAIS
# --------------------------------------------------------
obj1 = None
obj2 = None
morph_vertices = []
morph_faces = []

t = 0.0
morph_direction = 1  # 1 = obj1->obj2, -1 = obj2->obj1
morph_active = False

window_ids = {}

# ==========================
#  AJUSTES DE CÂMERA E LUZ
# ==========================

def ajusta_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 500, 0, 0, 0, 0, 1, 0)
    glScalef(0.1, 0.1, 0.1)


def setup_luz_camera():
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glClearColor(0.4, 0.4, 0.8, 1.0)

    # Luz suave
    light_position = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])


# ==========================
#  FUNÇÕES DE DESENHO
# ==========================

def desenha_obj1():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(0, 1, 1, 0)
    # desenha aqui o objeto 1
    obj1.Desenha()
    glutSwapBuffers()

def desenha_obj2():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(0, 1, 1, 0)
    # desenha aqui o objeto 2
    obj2.Desenha()
    glutSwapBuffers()

def desenha_morph():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(0, 1, 0, 0)
    glRotatef(0, 0, 1, 0)
    glColor3f(1, 1, 0)
    obj1.Desenha()
    glutSwapBuffers()
    
# --------------------------------------------------------
# ATUALIZAÇÃO DO MORPHING
# --------------------------------------------------------
def update_morph():
    global t, morph_active, morph_direction
    if morph_active:
        t += 0.01 * morph_direction
        t = max(0.0, min(1.0, t))
        recompute_morph_vertices(t)
        if t == 0.0 or t == 1.0:
            morph_active = False
        glutPostRedisplay()

# --------------------------------------------------------
# CÁLCULO DOS VÉRTICES INTERPOLADOS
# --------------------------------------------------------
def recompute_morph_vertices(t):
    global morph_vertices
    morph_vertices = []
    for v1, v2 in zip(obj1.vertices, obj2.vertices):
        # se for objeto do tipo Ponto, converte para np.array
        if hasattr(v1, 'x'):
            v1 = np.array([v1.x, v1.y, v1.z], dtype=float)
        else:
            v1 = np.array(v1, dtype=float)

        if hasattr(v2, 'x'):
            v2 = np.array([v2.x, v2.y, v2.z], dtype=float)
        else:
            v2 = np.array(v2, dtype=float)

        v = (1 - t) * v1 + t * v2
        morph_vertices.append(v)

# --------------------------------------------------------
# TECLADO (JANELA DE MORPH)
# --------------------------------------------------------
def teclado_morph(key, x, y):
    global morph_active, morph_direction
    if key == b' ':
        morph_active = True
        morph_direction *= -1

# --------------------------------------------------------
# FUNÇÃO DE INICIALIZAÇÃO
# --------------------------------------------------------
def init_objs():
    global obj1, obj2, morph_vertices, morph_faces
    obj1 = Objeto3D()
    obj2 = Objeto3D()
    obj1.LoadFile("Objetos/Cachorro1.obj")
    obj2.LoadFile("Objetos/Banana1.obj")

    # Alinha número de vértices
    min_v = min(len(obj1.vertices), len(obj2.vertices))
    obj1.vertices = obj1.vertices[:min_v]
    obj2.vertices = obj2.vertices[:min_v]

    # 🔧 Corrige as faces inválidas
    filter_faces(obj1)
    filter_faces(obj2)

    morph_vertices = [np.array(v) for v in obj1.vertices]
    morph_faces = obj1.faces[:min(len(obj1.faces), len(obj2.faces))]

    
    
def filter_faces(obj):
    max_index = len(obj.vertices) - 1
    valid_faces = []
    for face in obj.faces:
        if all(iv <= max_index for iv in face):
            valid_faces.append(face)
    obj.faces = valid_faces


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
def main():
    global window_ids

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    # Janela 1
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 50)
    window_ids['obj1'] = glutCreateWindow(b"Objeto 1")
    ajusta_camera()
    setup_luz_camera()
    glutDisplayFunc(desenha_obj1)

    # Janela 2
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(800, 50)
    window_ids['obj2'] = glutCreateWindow(b"Objeto 2")
    ajusta_camera()
    setup_luz_camera()
    glutDisplayFunc(desenha_obj2)

    # Janela 3 (morph)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(450, 250)
    window_ids['morph'] = glutCreateWindow(b"Morphing")
    ajusta_camera()
    setup_luz_camera()
    glutDisplayFunc(desenha_morph)
    glutKeyboardFunc(teclado_morph)
    glutIdleFunc(update_morph)

    init_objs()
    print("OBJ1 -> vértices: ", len(obj1.vertices), "faces: ", len(obj1.faces))
    print("OBJ2 -> vértices: ", len(obj2.vertices), "faces: ", len(obj2.faces))
    print("Morph_vertices: ",len(morph_vertices), "Morph_faces: ",len(morph_faces))
    glutMainLoop()
    

if __name__ == "__main__":
    main()
