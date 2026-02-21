import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.markers import MarkerStyle


class Node:
    def __init__(self, pos, parent=None):
        self.parent = parent
        self.pos = pos
        self.children = []

    def addChild(self, child):
        self.children.append(child)



tree = []

map = [(i,j) for i in range(30) for j in range(30)]

start = (4, 7)

tree.append(Node(start))

goal = (80, 80)


map_for_obs = map.copy()
map_for_obs.remove(goal)
map_for_obs.remove(start)

obstacles = random.sample(map_for_obs, 8)

for obstacle in obstacles:
    map.remove(obstacle)

plt.figure(figsize=(8, 8))


while True:
    plt.scatter(start[0], start[1], color="yellow", s=100)
    plt.scatter(goal[0], goal[1], color="green", s=100)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color="red", marker=MarkerStyle(","), s=300)

    node = random.choice(map)

    usedNode = False

    for n in tree:
        if node == n.pos:
            usedNode = True
            break

    if usedNode:
        continue

    near_Node = (None, np.inf)
    for node_p in tree:
        d = np.linalg.norm((node[0] - node_p.pos[0], node[1] - node_p.pos[1]))
        if d < near_Node[1]:
            near_Node = (node_p, d)

    near_Node = near_Node[0]
    vector = (node[0] - near_Node.pos[0], node[1] - near_Node.pos[1])
    disc_vector = [(near_Node.pos[0] + vector[0]*i*0.1, near_Node.pos[1] + vector[1]*i*0.1) for i in range(0, 11, 1)]
    disc_in = False
    for obstacle in obstacles:
        for disc in disc_vector:
            if (obstacle[0] - 0.5 <= disc[0] <= obstacle[0] + 0.5) and (obstacle[1] - 0.5 <= disc[1] <= obstacle[1] + 0.5):
                disc_in = True
                break
        if disc_in:
            break

    if not disc_in:
        tree.append(Node(node, parent=near_Node))
        near_Node.addChild(tree[-1])

    for n in tree:
        for n_child in n.children:
            plt.plot((n.pos[0], n_child.pos[0]), (n.pos[1], n_child.pos[1]), marker=".", markersize=10, color="grey")

    plt.pause(0.00001)
    if tree[-1].pos == goal:
        current_node = tree[-1]
        while current_node.parent:
            plt.plot((current_node.pos[0], current_node.parent.pos[0]), (current_node.pos[1], current_node.parent.pos[1]), marker=".", markersize=10, color="blue")
            current_node = current_node.parent
        plt.pause(5)
        break
    plt.clf()


