import math
import random

import matplotlib.pyplot as plt
from graph.DiGraph import DiGraph

"""
in this class we draw the graph we receive from a Json file using matplotlib
"""


# Function draw receives a graph a draw it


def draw(di: DiGraph):
    nodes = di.get_all_v()  # all the nodes in the graph
    id_nums = []
    randPosX = {}
    randPosY = {}
    # id_nums holds all the id numbers of the nodes in the graph
    # used to draw the numbers of each node
    for _id in nodes:
        id_nums.append(str(_id))

    x = []  # the x values of the position of every node
    y = []  # the y values of the position of every node

    # for scaling
    max_x = math.inf * (-1)
    min_x = math.inf
    max_y = math.inf * (-1)
    min_y = math.inf

    # going through all the nodes id values in the graph
    for node in nodes.values():
        list_pos = node.get__pos()  # this node's position (in tuple format)
        posX = float(list_pos[0])  # the value at place 0 is x
        posY = float(list_pos[1])  # the value at place 1 is y

        # scaling
        if max_x < posX:
            max_x = posX
        if max_y < posY:
            max_y = posY
        if min_x > posX:
            min_x = posX
        if min_y > posY:
            min_y = posY
    if max_x == min_x:
        max_x = 1
        min_x = 0
    if max_y == min_y:
        max_y = 1
        min_y = 0
    scalelog = 1 / (max_x - min_x)  # scaling the x
    scalelat = 1 / (max_y - min_y)  # scaling the y

    for j in nodes.values():

        list_pos = j.get__pos()
        # x axis value list.
        if float(list_pos[0]) == -1:
            randX = random.uniform(min_x, max_x)
            randPosX[j.get__id()] = randX
            x.append(randX)
        else:
            x.append((float(list_pos[0]) - min_x) * scalelog)
        # y axis value list.
        if float(list_pos[1]) == -1:
            randY = random.uniform(min_y, max_y)
            randPosY[j.get__id()] = randY
            y.append(randY)
        else:
            y.append((float(list_pos[1]) - min_y) * scalelat)

    # Draw points based on above x, y axis values.
    plt.scatter([0, 1], [0, 1], c='white', marker='o', s=10, zorder=3)
    plt.scatter(x, y, c='red', marker='o', s=10, zorder=3)

    # Loop for annotation of all points
    for i in range(len(x)):
        plt.annotate(id_nums[i], (x[i], y[i] + 0.02))

    counter = 0
    x_s = []  # x values of source node
    y_s = []  # y values of source node
    x_d = []  # x values of dest node
    y_d = []  # y values of dest node

    # plot line between points
    for node in nodes.values():
        outE = di.all_out_edges_of_node(node.get__id())  # the edges that goes out of this node
        for dest_id in outE.keys():
            # the x and y of src node
            pos_src = node.get__pos()
            # x axis value list.
            if float(pos_src[0]) == -1:
                x_s.append(randPosX[node.get__id()])
            else:
                x_s.append((float(pos_src[0]) - min_x) * scalelog)
            # y axis value list.
            if float(pos_src[1]) == -1:
                y_s.append(randPosY[node.get__id()])
            else:
                y_s.append((float(pos_src[1]) - min_y) * scalelat)

            # the x and y of dest node
            destN = di.get_node(dest_id)
            pos_dest = di.get_node(dest_id).get__pos()
            # x axis value list.
            if float(pos_dest[0]) == -1:
                x_d.append(randPosX[destN.get__id()])
            else:
                x_d.append((float(pos_dest[0]) - min_x) * scalelog)
            # y axis value list.
            if float(pos_dest[1]) == -1:
                y_d.append(randPosY[destN.get__id()])
            else:
                y_d.append((float(pos_dest[1]) - min_y) * scalelat)

            # add arrow to plot
            dx = x_d[counter] - x_s[counter]  # distance between x values of dest node and src node
            dy = y_d[counter] - y_s[counter]  # distance between y values of dest node and src node
            plt.arrow(x_s[counter], y_s[counter], dx, dy, head_width=0.02, width=.004, length_includes_head=True,
                      facecolor='black')
            counter += 1

    plt.show()
