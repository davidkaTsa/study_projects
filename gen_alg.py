import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.markers import MarkerStyle
import time


def fitness(x, y):
    return - (x**2 + y - 11)**2 - (x + y**2 - 7)**2

def population(size):
    return np.random.uniform(-5, 5, (size, 2))

def tournament_selection(population, n, k):
    winner = []
    for _ in range(n):
        tourn_part = population[np.random.choice(population.shape[0], k, replace=False)]
        best_fit = (abs(fitness(*tourn_part[0])), tourn_part[0])
        for partic in tourn_part[1:]:
            fit = abs(fitness(*partic))
            if fit < best_fit[0]:
                best_fit = (fit, partic)
        winner.append(best_fit[1])

    return np.array(winner)

def roulette_wheel_selection(population, n):
    winner = []

    fitnesses = [1/abs(fitness(*individ)) for individ in population]
    total_fitness = sum(fitnesses)

    selection_probs = [(f/total_fitness) for f in fitnesses]
    for _ in range(n):
        r = random.random()
        sum_prob = 0
        for i, prob in enumerate(selection_probs):
            sum_prob += prob
            if sum_prob > r:
                winner.append(population[i])
                break

    return np.array(winner)


def intermediate_recombination(population, n):
    children = []

    for _ in range(n):
        if random.random() <= 1:
            parents = population[np.random.choice(population.shape[0], 2, replace=False)]
            alpha = random.randint(2, 8) * 0.1
            child = np.array([alpha*parents[0][0] + (1-alpha)*parents[1][0], alpha*parents[0][1] + (1-alpha)*parents[1][1]])
            children.append(child)
        else:
            children.append(population[np.random.choice(population.shape[0], 1, replace=False)][0])

    return np.array(children)

def blx_a(population, n):
    children = []
    alpha = 0.5
    for _ in range(n):
        if random.random() <= 1:
            child = []
            parents = population[np.random.choice(population.shape[0], 2, replace=False)]
            for i in range(2):
                delta = parents[0][i] - parents[1][i]
                left_b = min(parents[0][i], parents[1][i]) - alpha*delta
                right_b = max(parents[0][i], parents[1][i]) + alpha*delta

                u = random.uniform(left_b, right_b)
                child.append(u)
            children.append(np.array(child))
        else:
            children.append(population[np.random.choice(population.shape[0], 1, replace=False)][0])
    return np.array(children)

def mutation(population, prob_mut):
    mutation_population = []

    for i in range(len(population)):
        individ = []
        if random.random() < prob_mut:
            for j in range(2):
                m = np.random.normal(0, 0.5)
                individ.append(population[i][j] + m)
            mutation_population.append(np.array(individ))
        else:
            mutation_population.append(population[i])
    return np.array(mutation_population)


population_size = 50
current_population = population(population_size)

epoch = 100
prob_mut = [0.2 - ((0.2 - 0.01)/epoch)*i for i in range(epoch)]
n = 0
k = 0
fitness_populations = []
start = time.time()
aa = False
tt = 0
r = 0
all_pop = []
all_val = []
while r != 10:
    fitness_populations = []
    current_population = population(population_size)
    n = 0
    while n != epoch:
        selection = tournament_selection(current_population, int(len(current_population)*0.3), 3)
        next_population = blx_a(selection, int(len(current_population)*0.95))
        next_population_mutation = mutation(next_population, prob_mut[n])

        fit_prev_population = {abs(fitness(*individ)): individ for individ in current_population}
        best_prev_population = []

        for i in sorted(fit_prev_population)[:int(len(current_population)*0.05)]:
            best_prev_population.append(fit_prev_population[i])

        new_population = np.concatenate([next_population_mutation, np.array(best_prev_population)])

        current_population = new_population

        fitness_current_population = [abs(fitness(*individ)) for individ in current_population]
        fitness_populations.append((sum(fitness_current_population)/len(fitness_current_population), min(fitness_current_population)))

        if not aa and fitness_populations[-1][0] <= 0.01:
            end = time.time()
            tt = end - start
            aa = True

        if len(fitness_populations) > 1 and (fitness_populations[-1][0] - fitness_populations[-2][0] < 0.01):
            k += 1
            if k == 20:
                break
        else:
            k = 0

        n += 1
    all_pop.extend(current_population)
    r+=1


def plot_results(best_fitness, avg_fitness):
    plt.plot(best_fitness[:,0], best_fitness[:,1], label = "Max Fitness")
    plt.plot(avg_fitness[:,0], avg_fitness[:,1] ,label = "Avg Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()

best_fitness = np.array([(i + 1, fitness_populations[i][1]) for i in range(len(fitness_populations))])
avg_fitness = np.array([(i + 1, fitness_populations[i][0]) for i in range(len(fitness_populations))])
print(tt, fitness_populations[-1][0])
plot_results(best_fitness, avg_fitness)
plt.show()

x, y = np.meshgrid(np.linspace(-5, 5, 200), np.linspace(-5, 5, 200))
z = fitness(x, y)

plt.contour(x, y, z, 100)
plt.colorbar()
all_pop = np.array(all_pop)
plt.scatter(all_pop[:,0], all_pop[:, 1], s=1, color="red")
plt.show()