#!/usr/bin/pypy3

read_sample = 0
filename = ["input.txt", "sample.txt"][read_sample]
groups = open("rocks.txt").read().split('\n\n')
steam = open(filename).read().strip()

rocks = []

for group in groups:
    lines = group.strip().split('\n')
    rock = []
    for j, layer in enumerate(reversed(lines)):
        for i, shape in enumerate(layer):
            if shape == '#':
                rock.append((j, i))
    rocks.append(rock)

assert len(rocks) == 5
structure = set()
steam_id = 0
# hope no tetris inserts happen?

right = [0]*len(rocks)
for i, rock in enumerate(rocks):
    for _, l in rock:
        right[i] = max(right[i], l)

def init(rock_id, pos: tuple):
    rock = rocks[rock_id].copy()
    h, l = pos
    for i, (y, x) in enumerate(rock):
        rock[i] = (h+y, l+x)
    return rock

def translate_x(rock, t):
    for i, (y, x) in enumerate(rock):
        rock[i] = (y, x+t)

def translate_y(rock, t):
    for i, (y, x) in enumerate(rock):
        rock[i] = (y+t, x)

def is_hit(rock, pos, rock_id):
    h, l = pos
    
    # check left and right
    if l < 0 or right[rock_id] + l > 6:
        return True

    # check down
    if h < 0:
        return True

    # check other rocks
    for particle in rock:
        if particle in structure:
            return True
    return False

def extend_structure(rock):
    for particle in rock:
        structure.add(particle)

def calc_max_height():
    m = 0
    for (y, _) in structure:
        m = max(m, y + 1)
    return m

mh = 0

def maxh(rock):
    global mh
    for (y, _) in rock:
        mh = max(mh, y + 1)

hh = [0] * (len(steam) * 10)

for i in range(len(steam)*10):
    if i % len(steam) == 0:
        print(mh)

    hh[i] = mh
    # get initial position
    h = mh + 3
    l = 2

    rock_id = i % 5
    rock = init(rock_id, (h, l))

    while True:
        if steam[steam_id] == '<':
            direction = -1
        else:
            direction = 1

        steam_id += 1
        if steam_id == len(steam): steam_id = 0

        old_rock = rock.copy()
        translate_x(rock, direction)

        if is_hit(rock, (h, l + direction), rock_id):
            rock = old_rock
            # print("try", "left" if direction == -1 else "right")
        else:
            # print("left" if direction == -1 else "right")
            l += direction

        old_rock = rock.copy()
        translate_y(rock, -1)

        if is_hit(rock, (h - 1, l), rock_id):
            rock = old_rock
            extend_structure(rock)
            maxh(rock)
            break
        else:
            h -= 1

    # print("-----------------------")
    # print(i, max_height(), structure)


# with open("trick.txt", "w") as f:
#     for y in reversed(range(len(hh))):
#         for x in range(7):
#             pos = (y, x)
#             f.write(".#"[pos in structure])
#         f.write("\n")



print("-----------------------")

print(hh[2022])
print(len(hh))
print("-----------------------")
cycle = 2728
minn = 6000
for i in range(minn, minn+cycle):
    for j in range(i, minn+cycle):
        if hh[j] - hh[i] == cycle:
            print(i,j)
cycle_items = 1725
iterations, offset = divmod(1000000000000-minn, cycle_items)
# print(hh[5800+offset] + iterations*2728)

print(iterations, offset)
print(hh[minn+offset] + iterations * cycle)
# 1000000001482 is too low





