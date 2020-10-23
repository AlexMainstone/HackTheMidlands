import pyglet as pgl
import numpy as np
from math import sqrt

np.random.seed(2)

window = pgl.window.Window(1280, 720, "COVID-19 SIM")
key = pgl.window.key
map = pgl.image.load("res/map.gif")

cam_pos = [0, 0]
cam_input = [0, 0]

edit = False
selected_node = -1
node_list = []
edge_list = []

# Load nodes and edges from file
datafile = open("res/datafile.txt", "r")
Lines = datafile.readlines();
points = True
for l in Lines:
    if(l == "EDGES\n"):
        points = False
        continue

    data = []
    for w in l.split(" "):
        data.append(int(w))
    
    if points:
        node_list.append(data)
    else:
        edge_list.append(data)
datafile.close()

def update(dt):
    cam_pos[0] += cam_input[0]*5
    cam_pos[1] += cam_input[1]*5

@window.event
def on_draw():
    window.clear()

    #render here
    map.blit(cam_pos[0], cam_pos[1])
    
    #draw edges
    nodeedge = pgl.shapes.Line(0, 0, 0, 0, 4, color=(0,0,255))
    for edge in edge_list:
        p1 = node_list[edge[0]]
        p2 = node_list[edge[1]]
        nodeedge.x = p1[0] + cam_pos[0]
        nodeedge.y = p1[1] + cam_pos[1]
        nodeedge.x2 = p2[0] + cam_pos[0]
        nodeedge.y2 = p2[1] + cam_pos[1]
        nodeedge.draw();

    # draw nodes
    nodecircle = pgl.shapes.Circle(100, 100, 8, color=(0, 0, 0))
    for pos in node_list:
        nodecircle.radius = 8
        nodecircle.color = (0, 0, 0)
        nodecircle.x = pos[0] + cam_pos[0]
        nodecircle.y = pos[1] + cam_pos[1]
        nodecircle.draw()
        
        nodecircle.radius = 5
        nodecircle.color = (255,255,255)
        nodecircle.draw()
    
    if selected_node != -1:
        nodecircle.x = node_list[selected_node][0] + cam_pos[0]
        nodecircle.y = node_list[selected_node][1] + cam_pos[1]
        nodecircle.color = (255, 0, 0)
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
    
    if symbol == key.E:
        global edit 
        edit = True
    
    if not edit:
        return
    
    if symbol == key.F:
        datafile = open("res/datafile.txt", "w")
        lines = []
        for n in node_list:
            lines.append(str(n[0]) + " " + str(n[1]) + "\n")

        lines.append("EDGES\n")

        for e in edge_list:
            lines.append(str(e[0]) + " " + str(e[1]) + "\n")
        
        datafile.writelines(lines)
        datafile.close()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if not edit:
        return

    if button == pgl.window.mouse.LEFT:
        node_list.append([x - cam_pos[0], y - cam_pos[1]])
    else:
        best_node = 0
        best_dist = 10000
        for n in range(0, len(node_list)):
            current_dist = sqrt((node_list[n][0] - (x - cam_pos[0]))**2 + (node_list[n][1] - (y - cam_pos[1]))**2)
            if current_dist < best_dist:
                best_node = n
                best_dist = current_dist
        
        
        global selected_node
        if best_node == selected_node:
            return
        if selected_node == -1:
            selected_node = best_node
        else:
            edge_list.append([selected_node, best_node])
            selected_node = -1



@window.event
def on_key_release(symbol, modifiers):
    #key up
    if symbol == key.W or symbol == key.S:
        cam_input[1] = 0
    if symbol == key.A or symbol == key.D:
        cam_input[0] = 0

pgl.clock.schedule_interval(update, 1/30)
pgl.app.run()