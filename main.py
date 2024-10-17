import time
import numpy as np
import random
import pandas as pd
from PIL import Image, ImageDraw
from tqdm import tqdm

def start_point(M: int, N: int) -> tuple:
    start = ()
    if random.choice([True, False]):
        if random.choice([True, False]):
            start = (M - 1, random.choice([i for i in range(1, N - 1)]))
        else:
            start = (0, random.choice([i for i in range(1, N - 1)]))

    else:
        if random.choice([True, False]):
            start = (random.choice([i for i in range(0, M)]), 0)
        else:
            start = (random.choice([i for i in range(0, M)]), N - 1)

    return start
def create_labyrinth(M: int, N: int, count_door: int) -> np.ndarray:

    labyrinth = np.zeros((M*2-1, N*2-1))
    for i in range(M*2-1):
        for j in range(N*2-1):
            if ((i % 2 == 0) and (j % 2 == 0)):
                labyrinth[i][j] = 1

    rm = np.zeros((M, N))
    start = start_point(M, N)
    x, y = start
    rm[x][y] = 1
    list_transition = [start]
    x, y, tx, ty = choice_transition(x, y, rm, "create")
    for _ in range(1, M*N):

        while not (x >= 0 and y >= 0):
            x, y = list_transition[-1]
            list_transition.pop()
            x, y, tx, ty = choice_transition(x, y, rm, "create")
        rm[x][y] = 1
        list_transition.append((x, y))
        labyrinth[tx][ty] = 1

        x, y, tx, ty = choice_transition(x, y, rm, "create")

    while count_door != 0:
        x = random.randint(1, M*2-3)
        y = random.randint(1, N*2-3)
        if (labyrinth[x-1][y] == 1 and labyrinth[x+1][y] == 1):
            if (labyrinth[x][y-1] == 0 and  labyrinth[x][y+1]==0):
                labyrinth[x][y] = 1
                count_door -= 1
                continue
        elif (labyrinth[x][y - 1] == 1 and labyrinth[x][y + 1] == 1):
            if (labyrinth[x-1][y] == 0 and labyrinth[x+1][y] == 0):
                labyrinth[x][y] = 1
                count_door -= 1

    return labyrinth

def choice_transition(x: int, y: int, rm: np.ndarray, mode: str, finish = (-1, 1)) -> tuple:
    choice_list = []

    if mode == "create":
        if x > 0:
            if not rm[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if not rm[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not rm[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if not rm[x][y + 1]:
                choice_list.append((x, y + 1))

    if mode == "DFS" or mode == "AStar" or mode == "BFS":
        if x > 0:
            if rm[x - 1][y] == 1 or rm[x - 1][y] == 3:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if rm[x + 1][y] == 1 or rm[x + 1][y] == 3:
                choice_list.append((x + 1, y))
        if y > 0:
            if rm[x][y - 1] == 1 or rm[x][y-1] == 3:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if rm[x][y + 1] == 1 or rm[x][y+1] == 3:
                choice_list.append((x, y + 1))

    if choice_list:
        great_choice = []
        x_finish, y_finish = finish
        if mode == "AStar":
            for i in range(len(choice_list)):
                dx, dy = choice_list[i]
                dist = np.sqrt((dx-x_finish)**2+(dy-y_finish)**2)
                great_choice.append([(dx, dy), dist])
            great_choice.sort(key=lambda x: x[1])
            nx, ny = great_choice[0][0]

        elif mode == "BFS":
            return (x, y, choice_list)

        else:
            nx, ny = random.choice(choice_list)

        if x == nx:
            if ny > y:
                tx, ty = x * 2, ny * 2 - 1
            else:
                tx, ty = x * 2, ny * 2 + 1
        else:
            if nx > x:
                tx, ty = nx * 2 - 1, y * 2
            else:
                tx, ty = nx * 2 + 1, y * 2
        return (nx, ny, tx, ty)

    else:
        if mode == "BFS":
            return (-1, -1, [-1, -1])
        return (-1, -1, -1, -1)

def draw_lab(labyrinth: np.ndarray, path: str) -> None:
    labyrinth = np.pad(labyrinth, pad_width=1, constant_values=0)

    cell_size = 15
    width = labyrinth.shape[1] * cell_size
    height = labyrinth.shape[0] * cell_size

    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    for i in range(labyrinth.shape[0]):
        for j in range(labyrinth.shape[1]):
            if labyrinth[i][j] == 0: #BLOCK
                draw.rectangle([j * cell_size, i * cell_size,
                                (j + 1) * cell_size, (i + 1) * cell_size],
                               fill='black')
            elif labyrinth[i][j] == 2: #START
                draw.rectangle([j * cell_size, i * cell_size,
                                (j + 1) * cell_size, (i + 1) * cell_size],
                               fill='blue')
            elif labyrinth[i][j] == 3: #FINISH
                draw.rectangle([j * cell_size, i * cell_size,
                                (j + 1) * cell_size, (i + 1) * cell_size],
                               fill='red')
            elif labyrinth[i][j] == 4: #SEARCH
                draw.rectangle([j * cell_size, i * cell_size,
                                (j + 1) * cell_size, (i + 1) * cell_size],
                               fill='green')
            elif labyrinth[i][j] == 5: #WAY
                draw.rectangle([j * cell_size, i * cell_size,
                                (j + 1) * cell_size, (i + 1) * cell_size],
                               fill='yellow')
    image.save(f"{path}")

def start_finish(labyrinth: np.ndarray) -> tuple:
    while True:
        xs, ys, xf, yf = random.randint(1, labyrinth.shape[0]-1), random.randint(1, labyrinth.shape[1]-1),\
            random.randint(1, labyrinth.shape[0]-1), random.randint(1, labyrinth.shape[1]-1)
        if labyrinth[xs][ys] == 1 and labyrinth[xf][yf] == 1:
            return (xs, ys, xf, yf)


def DFS4Lab(labyrinth: np.ndarray, start: tuple, finish: tuple, mode: str) -> tuple:
    labyrinth = labyrinth.copy()
    count = 0
    x_start, y_start = start
    x_finish, y_finish = finish
    labyrinth[x_start][y_start] = 2
    labyrinth[x_finish][y_finish] = 3

    start_time = time.time()
    way = [(x_start, y_start)]
    x, y = way[-1]
    x, y, _, __ = choice_transition(x, y, labyrinth, mode, finish)
    while True:
        count += 1
        while not (x >= 0 and y >= 0):
            way.pop()
            x, y = way[-1]
            x, y, _, __ = choice_transition(x, y, labyrinth, mode, finish)

        way.append((x, y))
        if labyrinth[x][y] == 3:
            break
        labyrinth[x][y] = 4
        x, y, _, __ = choice_transition(x, y, labyrinth, mode, finish)
        #draw_lab(labyrinth, f"C:/Users/timof/Desktop/Progs/Labirint/{mode}/{count}.png")
    end_time = time.time()
    #for point in way[1:len(way)-1]:
        #x, y = point[0], point[1]
        #labyrinth[x][y] = 5
    #draw_lab(labyrinth, f"C:/Users/timof/Desktop/Progs/Labirint/{mode}/{count}.png")

    return (end_time-start_time, len(way))

def BFS4Lab(labyrinth: np.ndarray, start: tuple, finish: tuple, mode="BFS") -> tuple:
    labyrinth = labyrinth.copy()
    queue = [start]
    parent = {}
    count = 0
    x_start, y_start = start
    x_finish, y_finish = finish
    labyrinth[x_start][y_start] = 2
    labyrinth[x_finish][y_finish] = 3


    start_time = time.time()
    while queue:
        curr = queue.pop(0)
        x, y = curr
        if curr == finish:
            break
        x, y, choice = choice_transition(x, y, labyrinth, mode, finish)
        if x >= 0 and y >= 0:
            for nx, ny in choice:
                queue.append((nx, ny))
                if labyrinth[nx][ny] != 3:
                    labyrinth[nx][ny] = 4
                parent[(nx, ny)] = (x, y)

                #draw_lab(labyrinth, f"C:/Users/timof/Desktop/Progs/Labirint/{mode}/{count}.png")
                count += 1

    path = []
    curr = finish
    while curr in parent:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    end_time = time.time()
    #for point in path[:len(path)-1]:
        #x, y = point[0], point[1]
        #labyrinth[x][y] = 5
    #draw_lab(labyrinth, f"C:/Users/timof/Desktop/Progs/Labirint/{mode}/{count}.png")
    return (end_time-start_time, len(path)+1)


DFS_time = []
AStar_time = []
BFS_time = []

DFS_len = []
AStar_len = []
BFS_len = []

for i in tqdm(range(1000)):
    lab = create_labyrinth(5, 5, 5)
    xs, ys, xf, yf = start_finish(lab)

    times, length = DFS4Lab(lab, (xs, ys), (xf, yf), mode="DFS")
    DFS_time.append(times)
    DFS_len.append(length)

    times, length = DFS4Lab(lab, (xs, ys), (xf, yf), mode="AStar")
    AStar_len.append(length)
    AStar_time.append(times)

    times, length = BFS4Lab(lab, (xs, ys), (xf, yf))
    BFS_time.append(times)
    BFS_len.append(length)

data = pd.DataFrame({"DFS_time":DFS_time,
                     "DFS_len":DFS_len,
                     "BFS_time": BFS_time,
                     "BFS_len": BFS_len,
                     "AStar_time":AStar_time,
                     "AStar_len":AStar_len
                     })

data.to_csv("9x9_5.csv")

