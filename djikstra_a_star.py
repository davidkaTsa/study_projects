import random
import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt
tS = time.perf_counter()

vertex = ["Москва","Барселона", "Лилль","Ереван","Осло","Берлин", "Прага"]
vertexWithDist = {"Москва": {"Барселона":3010, "Лилль":2344, "Ереван": 1803, "Осло":1643, "Берлин":1608, "Прага": 1667, "Москва": 0},
          "Барселона": {"Москва":3010, "Лилль":1030, "Ереван":3532, "Осло":2142, "Берлин":1500, "Прага":1353, "Барселона": 0},
          "Лилль": {"Москва":2344, "Барселона":1030, "Ереван":3386, "Осло":1139, "Берлин":744, "Прага":807, "Лилль": 0},
          "Ереван": {"Москва":1803, "Барселона":3532, "Лилль":3386, "Осло":3197, "Берлин":2722, "Прага":2581, "Ереван": 0},
          "Осло": {"Москва":1643, "Барселона":2142, "Лилль":1139, "Ереван":3197, "Берлин":837, "Прага":1116, "Осло": 0},
          "Берлин": {"Москва":1608, "Барселона":1500, "Лилль":744, "Ереван":2722, "Осло":837, "Прага":279, "Берлин": 0},
          "Прага": {"Москва":1667, "Барселона":1353, "Лилль":807, "Ереван":2581, "Осло":1116, "Берлин":279, "Прага": 0}}

graph = {i: {} for i in vertex}
mileage = 7000
for vertStart in vertex:
    num_nb = random.randint(2, 3)
    name_nb = random.sample(list(vertexWithDist.keys()), num_nb)
    current_nb = graph[vertStart]
    for vertEnd in name_nb:
        if vertEnd not in current_nb.keys() and vertEnd != vertStart:
            dist = vertexWithDist[vertStart][vertEnd]
            graph[vertStart][vertEnd] = dist
            graph[vertEnd][vertStart] = dist

# graph = {'Москва': {'Осло': 1643, 'Барселона': 3010, 'Ереван': 1803, 'Прага': 1667}, 'Барселона': {'Москва': 3010, 'Лилль': 1030}, 'Лилль': {'Осло': 1139, 'Барселона': 1030, 'Берлин': 744, 'Ереван': 3386}, 'Ереван': {'Москва': 1803, 'Лилль': 3386}, 'Осло': {'Москва': 1643, 'Лилль': 1139, 'Берлин': 837}, 'Берлин': {'Лилль': 744, 'Осло': 837}, 'Прага': {'Москва': 1667}}

distToAllVerts = {i: {} for i in vertex}


def djikstra(graph, start):
    global draw_edge_color, draw_color, draw_labels
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if (current_vertex, neighbor) in draw_edge_color.keys():
                draw_edge_color[(current_vertex,neighbor)] = "orange"
            else:
                draw_edge_color[(neighbor, current_vertex)] = "orange"
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                draw_labels[neighbor] = f"{neighbor}: {distance}"


        plt.clf()
        draw_color[current_vertex] = "orange"
        nx.draw_networkx(nt, pos, node_size=draw_node_size, labels = draw_labels, node_color = draw_color.values(), font_size=7,
                         edge_color = draw_edge_color.values())
        nx.draw_networkx_edge_labels(nt, pos, edge_labels=draw_edge_num, font_size=8)
        plt.pause(2)

        for n in graph[current_vertex].keys():
            if (current_vertex, n) in draw_edge_color.keys():
                draw_edge_color[(current_vertex, n)] = "black"
            else:
                draw_edge_color[(n, current_vertex)] = "black"
        draw_color[current_vertex] = "green"
    return distances


def a_star_search(graph, start, goal):
    global draw_edge_color, draw_color, draw_labels

    queue = [(0, start)]
    cost_so_far = {}
    cost_so_far[start] = 0

    while queue:
        current = heapq.heappop(queue)[1]

        if current == goal:
            break

        for next in graph[current]:
            if (current, next) in draw_edge_color.keys():
                draw_edge_color[(current,next)] = "orange"
            else:
                draw_edge_color[(next, current)] = "orange"

            new_cost = cost_so_far[current] + graph[current][next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + vertexWithDist[next][goal]
                heapq.heappush(queue, (priority, next))
                draw_labels[next] = f"{next}: {new_cost}"

        plt.clf()
        draw_color[current] = "orange"
        draw_color[goal] = "blue"
        nx.draw_networkx(nt, pos, node_size=draw_node_size, labels = draw_labels, node_color = draw_color.values(), font_size=7,
                         edge_color = draw_edge_color.values())
        nx.draw_networkx_edge_labels(nt, pos, edge_labels=draw_edge_num, font_size=8)
        plt.pause(2)

        for n in graph[current].keys():
            if (current, n) in draw_edge_color.keys():
                draw_edge_color[(current, n)] = "black"
            else:
                draw_edge_color[(n, current)] = "black"
        draw_color[current] = "green"

    return cost_so_far[goal]

def a_star_forall(graph, start):
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    vertexs = list(graph.keys())
    vertexs.remove(start)
    for vertex in vertexs:
        for vertT in graph:
            draw_labels[vertT] = f"{vertT}: inf"
            draw_color[vertT] = "red"
        draw_labels[vert] = f"{vert}: 0 "
        shortdist = a_star_search(graph, start, vertex)
        distances[vertex] = shortdist

    return distances



minDistToCity = {vertex: -1 for vertex in graph}
draw_labels = {}
draw_color = {}

draw_edge_num = {}
draw_node_size = [1700]*7
nt = nx.Graph()
for vert in vertex:
    nt.add_node(vert)
for vert in vertex:
    for n_vert in graph[vert].items():
        draw_edge_num[(vert, n_vert[0])] = n_vert[1]
        nt.add_edge(vert, n_vert[0])
pos = nx.circular_layout(nt)
plt.figure(figsize=(10, 10))
draw_edge_color = {edge: f"black" for edge in nt.edges}



for vert in vertex:
    for vertT in graph:
        draw_labels[vertT] = f"{vertT}: inf"
        draw_color[vertT] = "red"
    draw_labels[vert] = f"{vert}: 0 "
    dist = djikstra(graph, vert)
    #dist = a_star_forall(graph, vert)
    sumdist = 0
    cVert = 0
    dist = sorted(dist.values())
    dist.reverse()
    for d in dist:
        sumdist += d
        if sumdist < mileage:
            cVert += 1
        else:
            minDistToCity[vert] = cVert
            break

tE = time.perf_counter()