code_pos = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
decode_pos = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


def num_pos(posit):
    return code_pos[posit[0]] + (int(posit[1]) - 1) * 8


def stan_pos(posit):
    return decode_pos[posit % 8] + str((posit // 8) + 1)


line = input().split()

start_pos, finish_pos, state = num_pos(line[0]), num_pos(line[1]), tuple(int(i) for i in line[2:])


def go_forward(state_c):
    return state_c[4], state_c[2], state_c[0], state_c[3], state_c[1], state_c[5]


def go_back(state_c):
    return state_c[2], state_c[4], state_c[1], state_c[3], state_c[0], state_c[5]


def go_right(state_c):
    return state_c[0], state_c[1], state_c[5], state_c[2], state_c[3], state_c[4]


def go_left(state_c):
    return state_c[0], state_c[1], state_c[3], state_c[4], state_c[5], state_c[2]


s_dist = [0]

state_cub = {(start_pos, state): state[4]}

state_by_dis = {0: [(start_pos, state, [start_pos])]}

while True:
    min_dis = min(s_dist)

    s_dist.remove(min_dis)

    pos, state, path = state_by_dis[min_dis].pop()
    if pos == finish_pos:
        break

    var_moving = []

    if pos + 8 <= 63:
        var_moving.append((pos + 8, go_forward(state)))
    if pos - 8 >= 0:
        var_moving.append((pos - 8, go_back(state)))
    if pos % 8 != 7:
        var_moving.append((pos + 1, go_right(state)))
    if pos % 8 != 0:
        var_moving.append((pos - 1, go_left(state)))

    for i, j in var_moving:
        if (i, j) not in state_cub:

            new_dist = state_cub[pos, state] + j[4]
            state_cub[i, j] = new_dist
            s_dist.append(new_dist)
            if new_dist not in state_by_dis:
                state_by_dis[new_dist] = []
            state_by_dis[new_dist].append((i, j, path + [i]))

print(state_cub[pos, state], " ".join(stan_pos(i) for i in path))
