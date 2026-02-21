import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

dist_left = ctrl.Antecedent(np.arange(0, 11, 0.1), "dist_left")
dist_right = ctrl.Antecedent(np.arange(0, 11, 0.1), "dist_right")
dist_forward = ctrl.Antecedent(np.arange(0, 11, 0.1), "dist_forward")
ang_goal = ctrl.Antecedent(np.arange(-180, 181, 0.1), "ang_goal")

angle = ctrl.Consequent(np.arange(-180, 181, 0.1), "angle")
speed = ctrl.Consequent(np.arange(0, 5.1, 0.1), "speed")

dist_left["nearly"] = fuzz.trimf(dist_left.universe, [0.0,0.0,2.0])
dist_left["average"] = fuzz.trimf(dist_left.universe, [0.0,2.0,6.0])
dist_left["far"] = fuzz.trimf(dist_left.universe, [6.0,10.0,10.0])

dist_right["nearly"] = fuzz.trimf(dist_right.universe, [0.0,0.0,2.0])
dist_right["average"] = fuzz.trimf(dist_right.universe, [0.0,2.0,6.0])
dist_right["far"] = fuzz.trimf(dist_right.universe, [6.0,10.0,10.0])

dist_forward["nearly"] = fuzz.trimf(dist_forward.universe, [0.0,0.0,2.0])
dist_forward["average"] = fuzz.trimf(dist_forward.universe, [0.0,2.0,6.0])
dist_forward["far"] = fuzz.trimf(dist_forward.universe, [6.0,10.0,10.0])

ang_goal["right"] = fuzz.trimf(ang_goal.universe, [-180.0,-180.0,-50.0])
ang_goal["forward"] = fuzz.trimf(ang_goal.universe, [-50.0,0.0,50.0])
ang_goal["left"] = fuzz.trimf(ang_goal.universe, [50.0,180.0,180.0])


angle["right_fast"] = fuzz.trimf(angle.universe, [-180.0,-120.0,-60.0])
angle["right_slow"] = fuzz.trimf(angle.universe, [-60.0,-45.0,-20.0])
angle["forward"] = fuzz.trimf(angle.universe, [-20.0,0.0,20.0])
angle["left_slow"] = fuzz.trimf(angle.universe, [20.0,45.0,60.0])
angle["left_fast"] = fuzz.trimf(angle.universe, [60.0,120.0,180.0])


speed["low"] = fuzz.trimf(speed.universe, [0,0,1])
speed["average"] = fuzz.trimf(speed.universe, [0,2,5])
speed["high"] = fuzz.trimf(speed.universe, [3,3,5])



rule1 = ctrl.Rule(dist_left["nearly"] & ang_goal["left"], angle["forward"])
rule2 = ctrl.Rule(dist_left["nearly"] & ang_goal["forward"], angle["forward"])
rule3 = ctrl.Rule(dist_left["nearly"] & ang_goal["right"], angle["right_slow"])
rule4 = ctrl.Rule(dist_left["average"] & ang_goal["left"], angle["left_slow"])
rule5 = ctrl.Rule(dist_left["average"] & ang_goal["forward"], angle["forward"])
rule6 = ctrl.Rule(dist_left["average"] & ang_goal["right"], angle["right_slow"])
rule7 = ctrl.Rule(dist_left["far"] & ang_goal["left"], angle["left_slow"])
rule8 = ctrl.Rule(dist_left["far"] & ang_goal["forward"], angle["forward"])
rule9 = ctrl.Rule(dist_left["far"] & ang_goal["right"], angle["right_slow"])

rule10 = ctrl.Rule(dist_left["nearly"] & ang_goal["left"], speed["low"])
rule11 = ctrl.Rule(dist_left["nearly"] & ang_goal["forward"], speed["low"])
rule12 = ctrl.Rule(dist_left["nearly"] & ang_goal["right"], speed["low"])
rule13 = ctrl.Rule(dist_left["average"] & ang_goal["left"], speed["average"])
rule14 = ctrl.Rule(dist_left["average"] & ang_goal["forward"], speed["average"])
rule15 = ctrl.Rule(dist_left["average"] & ang_goal["right"], speed["average"])
rule16 = ctrl.Rule(dist_left["far"] & ang_goal["left"], speed["average"])
rule17 = ctrl.Rule(dist_left["far"] & ang_goal["forward"], speed["high"])
rule18 = ctrl.Rule(dist_left["far"] & ang_goal["right"], speed["high"])


rule19 = ctrl.Rule(dist_right["nearly"] & ang_goal["left"], angle["left_slow"])
rule20 = ctrl.Rule(dist_right["nearly"] & ang_goal["forward"], angle["forward"])
rule21 = ctrl.Rule(dist_right["nearly"] & ang_goal["right"], angle["forward"])
rule22 = ctrl.Rule(dist_right["average"] & ang_goal["left"], angle["left_slow"])
rule23 = ctrl.Rule(dist_right["average"] & ang_goal["forward"], angle["forward"])
rule24 = ctrl.Rule(dist_right["average"] & ang_goal["right"], angle["right_slow"])
rule25 = ctrl.Rule(dist_right["far"] & ang_goal["left"], angle["left_slow"])
rule26 = ctrl.Rule(dist_right["far"] & ang_goal["forward"], angle["forward"])
rule27 = ctrl.Rule(dist_right["far"] & ang_goal["right"], angle["right_slow"])

rule28 = ctrl.Rule(dist_right["nearly"] & ang_goal["left"], speed["low"])
rule29 = ctrl.Rule(dist_right["nearly"] & ang_goal["forward"], speed["low"])
rule30 = ctrl.Rule(dist_right["nearly"] & ang_goal["right"], speed["low"])
rule31 = ctrl.Rule(dist_right["average"] & ang_goal["left"], speed["average"])
rule32 = ctrl.Rule(dist_right["average"] & ang_goal["forward"], speed["average"])
rule33 = ctrl.Rule(dist_right["average"] & ang_goal["right"], speed["average"])
rule34 = ctrl.Rule(dist_right["far"] & ang_goal["left"], speed["high"])
rule35 = ctrl.Rule(dist_right["far"] & ang_goal["forward"], speed["high"])
rule36 = ctrl.Rule(dist_right["far"] & ang_goal["right"], speed["average"])

rule37 = ctrl.Rule(dist_forward["nearly"] & ang_goal["left"], angle["left_fast"])
rule38 = ctrl.Rule(dist_forward["nearly"] & ang_goal["forward"], angle["right_fast"])
rule39 = ctrl.Rule(dist_forward["nearly"] & ang_goal["right"], angle["right_fast"])
rule40 = ctrl.Rule(dist_forward["average"] & ang_goal["left"], angle["left_slow"])
rule41 = ctrl.Rule(dist_forward["average"] & ang_goal["forward"], angle["forward"])
rule42 = ctrl.Rule(dist_forward["average"] & ang_goal["right"], angle["right_slow"])
rule43 = ctrl.Rule(dist_forward["far"] & ang_goal["left"], angle["left_slow"])
rule44 = ctrl.Rule(dist_forward["far"] & ang_goal["forward"], angle["forward"])
rule45 = ctrl.Rule(dist_forward["far"] & ang_goal["right"], angle["right_slow"])

rule46 = ctrl.Rule(dist_forward["nearly"] & ang_goal["left"], speed["low"])
rule47 = ctrl.Rule(dist_forward["nearly"] & ang_goal["forward"], speed["high"])
rule48 = ctrl.Rule(dist_forward["nearly"] & ang_goal["right"], speed["low"])
rule49 = ctrl.Rule(dist_forward["average"] & ang_goal["left"], speed["average"])
rule50 = ctrl.Rule(dist_forward["average"] & ang_goal["forward"], speed["low"])
rule51 = ctrl.Rule(dist_forward["average"] & ang_goal["right"], speed["average"])
rule52 = ctrl.Rule(dist_forward["far"] & ang_goal["left"], speed["high"])
rule53 = ctrl.Rule(dist_forward["far"] & ang_goal["forward"], speed["average"])
rule54 = ctrl.Rule(dist_forward["far"] & ang_goal["right"], speed["high"])

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18,
         rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36,
         rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54]


robot_ctrl = ctrl.ControlSystem(rules)
robot_fuzzy = ctrl.ControlSystemSimulation(robot_ctrl)


class Robot:
    def __init__(self, x, y, speed, angle, dt):
        self.position = [x, y]
        self.speed = speed
        self.angle = angle
        self.dt = dt

    def move(self):
        dx = self.speed * self.dt * np.cos(self.angle)
        dy = self.speed * self.dt * np.sin(self.angle)

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        if (0 <= new_x <= 10) and (0 <= new_y <= 10):
            self.position = [new_x, new_y]
        else:
            self.angle = self.angle + np.pi



    def sence_obstacles(self, obstacles):
        left_obs = []
        forward_obs = []
        right_obs = []
        up_obs = []
        forward_and_right = []
        shortest_vector_left = []
        shortest_vector_forward = []
        shortest_vector_right = []

        up_vector = [np.cos(self.angle + np.pi/2) * 1, np.sin(self.angle + np.pi/2) * 1]
        left_vector = [np.cos(self.angle + np.pi/12) * 1, np.sin(self.angle + np.pi/12) * 1]
        forward_vector = [np.cos(self.angle - np.pi/12) * 1, np.sin(self.angle - np.pi/12) * 1]

        for obstacle in obstacles:
            obs_vector = [obstacle.position[0] - self.position[0], obstacle.position[1] - self.position[1]]
            vec_mul = np.cross(up_vector, obs_vector)
            if vec_mul <=0: up_obs.append(obs_vector)

        for obs_vector in up_obs:
            vec_mul = np.cross(left_vector, obs_vector)
            if vec_mul >=0:
                left_obs.append(obs_vector)
                shortest_vector_left.append(np.linalg.norm(obs_vector, ord=2))
            else:
                forward_and_right.append(obs_vector)

        for obs_vector in forward_and_right:
            vec_mul = np.cross(forward_vector, obs_vector)
            if vec_mul >=0:
                forward_obs.append(obs_vector)
                shortest_vector_forward.append(np.linalg.norm(obs_vector, ord=2))
            else:
                right_obs.append(obs_vector)
                shortest_vector_right.append(np.linalg.norm(obs_vector, ord=2))

        return round(min(shortest_vector_left), 1) if len(shortest_vector_left) != 0 else 10.0, round(min(shortest_vector_forward), 1) if len(shortest_vector_forward) != 0 else 10.0, round(min(shortest_vector_right), 1) if len(shortest_vector_right) != 0 else 10.0


    def sence_goal(self, goal):
        # goal_angle = np.arccos(goal[0]/np.linalg.norm(goal, ord=2))
        #
        # if goal[1] < 0:
        #     if goal[0] > 0:
        #         goal_angle += 3 * np.pi
        #     elif goal[0] < 0:
        #         goal_angle += np.pi/2
        #     else:
        #         goal_angle += np.pi
        # print(goal_angle, self.angle)
        # return round((goal_angle - self.angle), 1)
        angle_vector = [np.cos(self.angle) * 1, np.sin(self.angle) * 1]
        goal_vector = [goal[0] - self.position[0], goal[1] - self.position[1]]

        vec_mul = np.cross(angle_vector, goal_vector)
        goal_angle = np.arccos(np.dot(angle_vector, goal_vector) / np.linalg.norm(angle_vector) / np.linalg.norm(goal_vector))
        goal_angle = goal_angle if vec_mul >= 0 else -goal_angle

        return goal_angle




class Create_Obstacles:
    def __init__(self, x, y, angle = None, speed= None, dt= None):
        self.position = [x, y]
        self.angle = angle
        self.speed = speed
        self.dt = dt

    def move(self):
        dx = self.speed * self.dt * np.cos(self.angle)
        dy = self.speed * self.dt * np.sin(self.angle)

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy


        if (0 <= new_x <= 10) and (0 <= new_y <= 10):
            self.position = [new_x, new_y]
        else:
            self.angle = self.angle + np.pi





robot = Robot(2,3, 1, -np.pi/3, 0.03)

goal = [2,9]

static_obs = [Create_Obstacles(3,4), Create_Obstacles(2,6), Create_Obstacles(5,9),Create_Obstacles(5,5), Create_Obstacles(3,7)]
dynamic_obs = [Create_Obstacles(1,3, np.pi/2, 3, 0.03), Create_Obstacles(1,8, np.pi/5, 1.5, 0.03), Create_Obstacles(7,3, np.pi/8, 2, 0.03),
               Create_Obstacles(2,4, np.pi/5, 3, 0.03), Create_Obstacles(4,8, -np.pi/5, 1.5, 0.03), Create_Obstacles(3,3, -np.pi/8, 2, 0.03),
               Create_Obstacles(2,5, -np.pi/2, 3, 0.03), Create_Obstacles(4,8, -np.pi/12, 1.5, 0.03), Create_Obstacles(3,7, -np.pi/1, 2, 0.03)]

all_obstacles = []
all_obstacles.extend(static_obs)
all_obstacles.extend(dynamic_obs)

x_obs = []
y_obs = []
for i in all_obstacles:
    x_obs.append(i.position[0])
    y_obs.append(i.position[1])


fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

points = [ax.plot(robot.position[0], robot.position[1], 'o', color="blue", markersize=10)[0], ax.plot(goal[0], goal[1], "o", color="green", markersize=10), ax.plot(x_obs, y_obs, 's', color="red", markersize=10)[0]]
plt.ion()
plt.show()

while np.linalg.norm([robot.position[0] - goal[0], robot.position[1] - goal[1]], ord=2) > 0.1:

    shortest_obs = robot.sence_obstacles(all_obstacles)
    angle_goal = robot.sence_goal(goal)

    # normalize_angle = (angle_goal % 2*np.pi)
    #
    # if normalize_angle > np.pi:
    #     normalize_angle -= 2*np.pi
    # elif normalize_angle < -np.pi:
    #     normalize_angle += 2*np.pi

    robot_fuzzy.input["dist_left"] = shortest_obs[0]
    robot_fuzzy.input["dist_forward"] = shortest_obs[1]
    robot_fuzzy.input["dist_right"] = shortest_obs[2]
    robot_fuzzy.input["ang_goal"] = angle_goal * 180/np.pi

    robot_fuzzy.compute()
    for output in robot_fuzzy.output:
        if output == "speed":
            robot.speed = robot_fuzzy.output["speed"]
        else:
            robot.angle += robot_fuzzy.output["angle"]*np.pi/180
            # robot.angle = robot.angle % 2*np.pi

    robot.move()

    for obstacle in dynamic_obs:
        obstacle.move()

    x_obs = []
    y_obs = []
    for i in all_obstacles:
        x_obs.append(i.position[0])
        y_obs.append(i.position[1])

    points[0].set_data([robot.position[0]], [robot.position[1]])
    points[2].set_data(x_obs, y_obs)
    plt.draw()
    plt.gcf().canvas.flush_events()

