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
    gluPerspective(45, 1, 0.1, 5000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 900, 50, 0, 0, 0, 0, 1, 0)
    
    
    #CAMERA -----------------------------------------------------------
    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml



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
    
    
def init_lighting():
    glEnable(GL_LIGHTING)          # ativa o sistema de luz
    glEnable(GL_LIGHT0)            # ativa a luz 0 (default)
    glEnable(GL_COLOR_MATERIAL)    # permite que glColor() afete o material
    glShadeModel(GL_SMOOTH)        # suaviza a iluminação entre vértices

    # luz ambiente global (ilumina tudo levemente)
    ambient_light = [0.3, 0.3, 0.3, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)

    # parâmetros da luz 0
    light_position = [10.0, 10.0, 10.0, 1.0]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)



# ==========================
#  FUNÇÕES DE DESENHO
# ==========================
   
def desenha_obj1():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(15, 0, 10, 0, 0, 0, 0, 1, 0)

    obj1.Desenha()
    glutSwapBuffers()

def desenha_obj2():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(15, 0, 10, 0, 0, 0, 0, 1, 0)

    obj2.Desenha()
    glutSwapBuffers()

def desenha_morph():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(15, 0, 10, 0, 0, 0, 0, 1, 0)

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
#def teclado_morph(key, x, y):
#    global morph_active, morph_direction
#    if key == b' ':
#        morph_active = True
#        morph_direction *= -1
def teclado(key, x, y):
    obj1.rotation = (1, 1, 0, obj1.rotation[3] + 2)    
    glutPostRedisplay()
    pass
# def teclado(key, x, y):
#     global morph_active, morph_direction
#     if key == b' ':
#         morph_active = True
#         morph_direction *= -1
#         print("SPACE pressed -> morph_active:", morph_active, "direction:", morph_direction)
#         glutPostRedisplay()

# --------------------------------------------------------
# FUNÇÃO DE INICIALIZAÇÃO
# --------------------------------------------------------
def init_objs():
    global obj1, obj2, morph_vertices, morph_faces
    obj1 = Objeto3D()
    obj2 = Objeto3D()
    obj1.LoadFile("Objetos/bursto1.obj")
    obj2.LoadFile("Objetos/Banana1.obj")
    
    # Alinha número de vértices
    min_v = min(len(obj1.vertices), len(obj2.vertices))
    morph_vertices = [
    np.array(obj1.vertices[i]) if i < len(obj1.vertices) else np.zeros(3)
    for i in range(min_v)
    ]


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
    glutKeyboardFunc(teclado)
    glutIdleFunc(update_morph)

    init_objs()
    print("OBJ1 -> vértices: ", len(obj1.vertices), "faces: ", len(obj1.faces))
    print("OBJ2 -> vértices: ", len(obj2.vertices), "faces: ", len(obj2.faces))
    print("Morph_vertices: ",len(morph_vertices), "Morph_faces: ",len(morph_faces))
    glutMainLoop()
    

if __name__ == "__main__":
    main()