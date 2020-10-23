import pyglet as pgl
from scipy.spatial import Voronoi
import numpy as np

np.random.seed(2)

window = pgl.window.Window(1280, 720, "COVID-19 SIM")
key = pgl.window.key

cam_pos = [0, 0]
cam_input = [0, 0]

nodes = []
for i in range(0, 4):
    nodes.append([np.random.randint(1270)+10, np.random.randint(710)+10])

voronoi = Voronoi(nodes, incremental=True)

def update(dt):
    cam_pos[0] += cam_input[0]*5
    cam_pos[1] += cam_input[1]*5

@window.event
def on_draw():
    window.clear()
    #render here
    
    #draw edges
    nodeedge = pgl.shapes.Line(0, 0, 0, 0, 1, color=(0,0,255))
    for edge in voronoi.ridge_vertices:
        if edge[0] == -1 or edge[1] == -1: continue
        p1 = voronoi.vertices[edge[0]]
        p2 = voronoi.vertices[edge[1]]
        nodeedge.x = p1[0] + cam_pos[0]
        nodeedge.y = p1[1] + cam_pos[1]
        nodeedge.x2 = p2[0] + cam_pos[0]
        nodeedge.y2 = p2[1] + cam_pos[1]
        nodeedge.draw();

    # draw nodes
    nodecircle = pgl.shapes.Circle(100, 100, 5, color=(255, 255, 255))
    for pos in voronoi.vertices:
        nodecircle.x = pos[0] + cam_pos[0]
        nodecircle.y = pos[1] + cam_pos[1]
        # nodecircle.color = (255, 255 - (nodes[i][2]*2), 255 - (nodes[i][2]*2))
        nodecircle.draw()
    

@window.event
def on_key_press(symbol, modifiers):
    #key down
    if symbol == key.W:
        cam_input[1] = -1
    if symbol == key.S:
        cam_input[1] = 1
    if symbol == key.A:
        cam_input[0] = 1
    if symbol == key.D:
        cam_input[0] = -1

@window.event
def on_mouse_press(x, y, button, modifiers):
    voronoi.add_points([[x, y]])

@window.event
def on_key_release(symbol, modifiers):
    #key up
    if symbol == key.W or symbol == key.S:
        cam_input[1] = 0
    if symbol == key.A or symbol == key.D:
        cam_input[0] = 0

pgl.clock.schedule_interval(update, 1/30)
pgl.app.run()