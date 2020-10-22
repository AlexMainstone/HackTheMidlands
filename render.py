import pyglet as pgl
from scipy.spatial import Voronoi
import numpy as np

np.random.seed(2)

window = pgl.window.Window(1280, 720, "COVID-19 SIM")

nodes = []
for i in range(0, 100):
    nodes.append([np.random.randint(1280), np.random.randint(720)])

voronoi = Voronoi(nodes)

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
        nodeedge.x = p1[0]
        nodeedge.y = p1[1]
        nodeedge.x2 = p2[0]
        nodeedge.y2 = p2[1]
        nodeedge.draw();

    # draw nodes
    nodecircle = pgl.shapes.Circle(100, 100, 5, color=(255, 255, 255))
    for pos in voronoi.vertices:
        nodecircle.x = pos[0]
        nodecircle.y = pos[1]
        # nodecircle.color = (255, 255 - (nodes[i][2]*2), 255 - (nodes[i][2]*2))
        nodecircle.draw()

pgl.app.run()