import pyglet as pgl
import numpy as np
from math import sqrt

# Create Window
window = pgl.window.Window(1280, 720, "COVID-19 SIM")

# Bind key data
key = pgl.window.key

# Loac map
map = pgl.image.load("res/map.gif")

# Camera
cam_pos = [0, 0]
cam_input = [0, 0]

# Edit Mode, allows for saving and node creation
edit = False

# Currently selected node
closest_node = -1
selected_node = -1

# Node & Edge data
node_list = []
edge_list = []

def clean_edges():
    for ei in range(0, len(edge_list)-1):
        for si in range(0, len(edge_list)-1):
            if ei == si: continue
            if edge_list[ei][0] == edge_list[si][0] and edge_list[ei][1] == edge_list[si][1]: del edge_list[si]
            if edge_list[ei][0] == edge_list[si][1] and edge_list[ei][1] == edge_list[si][0]: del edge_list[si]

# Load nodes and edges from file
datafile = open("res/datafile.txt", "r")
lines = datafile.readlines()

# Determines if we're storing edges or points
points = True
for l in lines:
    if(l == "EDGES\n"): # This signifys that edges will follow
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

# Update is called 30 times a second
def update(dt):
    # Update camera position
    cam_pos[0] += cam_input[0]*5
    cam_pos[1] += cam_input[1]*5

@window.event
def on_draw():
    window.clear()

    #render here
    map.blit(cam_pos[0], cam_pos[1])
    
    #draw edges
    nodeedge = pgl.shapes.Line(0, 0, 0, 0, 4, color=(0,0,255))
    if edit:
        for edge in edge_list:
            # Get node data
            p1 = node_list[edge[0]]
            p2 = node_list[edge[1]]

            # set the lines points
            nodeedge.x = p1[0] + cam_pos[0]
            nodeedge.y = p1[1] + cam_pos[1]
            nodeedge.x2 = p2[0] + cam_pos[0]
            nodeedge.y2 = p2[1] + cam_pos[1]
            
            nodeedge.draw()
    else:
        for edge in edge_list:
            subnode = -1
            if edge[0] == closest_node:
                subnode = edge[1]
            elif edge[1] == closest_node: 
                subnode = edge[0]
            else:
                continue
            
            for e in edge_list:
                if (e[0] != subnode and e[1] != subnode) or e[0] == closest_node or e[1] == closest_node: continue
                nodeedge.color = (255, 100, 100)
                # Get node data
                p1 = node_list[e[0]]
                p2 = node_list[e[1]]

                # set the lines points
                nodeedge.x = p1[0] + cam_pos[0]
                nodeedge.y = p1[1] + cam_pos[1]
                nodeedge.x2 = p2[0] + cam_pos[0]
                nodeedge.y2 = p2[1] + cam_pos[1]
                
                nodeedge.draw()
                
            
            nodeedge.color = (0, 0, 255)
            # Get node data
            p1 = node_list[edge[0]]
            p2 = node_list[edge[1]]

            # set the lines points
            nodeedge.x = p1[0] + cam_pos[0]
            nodeedge.y = p1[1] + cam_pos[1]
            nodeedge.x2 = p2[0] + cam_pos[0]
            nodeedge.y2 = p2[1] + cam_pos[1]
            
            nodeedge.draw()

    # draw nodes
    nodecircle = pgl.shapes.Circle(100, 100, 8, color=(0, 0, 0))
    for pos in node_list:
        # Draw the outline circle
        nodecircle.radius = 8
        nodecircle.color = (0, 0, 0)
        nodecircle.x = pos[0] + cam_pos[0]
        nodecircle.y = pos[1] + cam_pos[1]
        nodecircle.draw()
        
        # Draw inner circle
        nodecircle.radius = 5
        nodecircle.color = (255,255,255)
        nodecircle.draw()
    
    # Draw the selection cursor
    if selected_node != -1:
        nodecircle.x = node_list[selected_node][0] + cam_pos[0]
        nodecircle.y = node_list[selected_node][1] + cam_pos[1]
        nodecircle.color = (255, 0, 0)
        nodecircle.draw()



@window.event
def on_key_press(symbol, modifiers):
    # Movement
    if symbol == key.W:
        cam_input[1] = -1
    if symbol == key.S:
        cam_input[1] = 1
    if symbol == key.A:
        cam_input[0] = 1
    if symbol == key.D:
        cam_input[0] = -1
    
    # Edit mode
    if symbol == key.E:
        global edit 
        edit = not edit

    if not edit:
        return
    
    # Save to file
    if symbol == key.F:
        clean_edges()
        datafile = open("res/datafile.txt", "w")
        lines = []
        # Save nodes
        for n in node_list:
            lines.append(str(n[0]) + " " + str(n[1]) + "\n")

        # Save Edges
        lines.append("EDGES\n")
        for e in edge_list:
            lines.append(str(e[0]) + " " + str(e[1]) + "\n")
        
        datafile.writelines(lines)
        datafile.close()

@window.event
def on_mouse_motion(x, y, dx, dy):
    global closest_node
    best_dist = 10000
    for n in range(0, len(node_list)):
        current_dist = sqrt((node_list[n][0] - (x - cam_pos[0]))**2 + (node_list[n][1] - (y - cam_pos[1]))**2)
        if current_dist < best_dist:
            closest_node = n
            best_dist = current_dist


@window.event
def on_mouse_press(x, y, button, modifiers):
    if not edit:
        return

    if button == pgl.window.mouse.LEFT:
        # Create Node
        node_list.append([x - cam_pos[0], y - cam_pos[1]])
    else:
        global selected_node
        if closest_node == selected_node: # if node is the same as selected
            return
        if selected_node == -1: # if there is no selected node
            # Select node
            selected_node = closest_node
        else: # If twe different nodes have been selected
            # Create edge
            edge_list.append([selected_node, closest_node])
            selected_node = -1



@window.event
def on_key_release(symbol, modifiers):
    #key up
    if symbol == key.W or symbol == key.S:
        cam_input[1] = 0
    if symbol == key.A or symbol == key.D:
        cam_input[0] = 0

pgl.clock.schedule_interval(update, 1/30) # 30 fps clock
pgl.app.run()
