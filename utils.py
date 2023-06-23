import tkinter as tk
import heapq


class PriorityQueue:
    def __init__(self):
        self.data = list() 
    
    def empty(self):
        return len(self.data) == 0
    
    def push(self, item, priority):
        heapq.heappush(self.data, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.data)[1]


def draw_maze(maze, top, width, height):
    C = tk.Canvas(top, bg="white", height=height, width=width)
    dx = width / len(maze[0])
    dy = height / len(maze)
    coords = [0, 0, dx, dy]
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                C.create_rectangle(coords, fill='black')
            elif maze[i][j] == 'D':
                C.create_rectangle(coords, fill='orange')
            elif maze[i][j] == 'E':
                C.create_rectangle(coords, fill='green')
            else:
                C.create_rectangle(coords, fill='white')
            coords[0] += dx
            coords[2] += dx
        coords[0] = 0
        coords[2] = dx
        coords[1] += dy
        coords[3] += dy
    return C, dx, dy


def connect_points(canvas, dx, dy, point1, point2):
    canvas.create_line([point1[1]*dx + dx/2, point1[0]*dy+dy/2,
                        point2[1]*dx + dx/2, point2[0]*dy+dy/2],
                        width=2, fill='red')


def draw_plan(canvas, dx, dy, plan):
    point1 = plan[0]
    for point2 in plan[1:]:
        connect_points(canvas, dx, dy, point1, point2)
        point1 = point2


def visualize(maze, plan, width=700, height=700):
    top = tk.Tk()
    canvas, dx, dy = draw_maze(maze, top, width=width, height=height)
    draw_plan(canvas, dx, dy, plan)
    canvas.pack()
    top.mainloop()
