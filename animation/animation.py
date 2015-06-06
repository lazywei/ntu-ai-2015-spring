from Tkinter import *
import numpy as np
import time


class Drawer:
    def __init__(self, arrays):
        arrays = np.array(arrays)
        weight = arrays[0].shape[1]
        height = arrays[0].shape[0]

        self.master = Tk()

        self.w = Canvas(self.master, width=height*30, height=weight*30)
        self.w.pack()
        self.maps = arrays
        self.points = index2point(weight, height)
        self.cars = []

    def graph(self):
        map_ = self.maps[0]
        weight = map_.shape[1]
        height = map_.shape[0]
        for w in range(0, weight):
            for h in range(0, height):
                self.graphunit(map_[h][w], self.points[h][w])
        self.master.after(0, self.animation())
        self.master.mainloop()

    def graphunit(self, id, points):
        if id == -2:
            color = "red"
        else:
            colors = ["blue", "green", "yellow", "pink", "orange",
                      "purple", "black", "gray"]
            color = colors[id]

        if id == 0 or id == 1:
            tk_id = self.w.create_rectangle(points[0], points[1], points[2], points[3],
                                            fill=color, outline="white")
            self.cars.append(Car(id, tk_id, self.car_router(id)))

        elif id == -2:
            self.w.create_rectangle(points[0], points[1], points[2], points[3],
                                    fill=color, outline="white")

    def car_router(self, id):
        router = []
        for map_ in self.maps:
            x, y = np.nonzero(id == map_)
            router.append([x[0], y[0]])
        return router

    def animation(self):
        for index in range(1, len(self.maps)):
            for i in range(0, 51):
                for car in self.cars:
                    time.sleep(0.025)
                    points = car.router[index]
                    p_points = car.router[index-1]
                    x_offset = points[0] - p_points[0]
                    y_offset = points[1] - p_points[1]
                    if x_offset == 0 and y_offset != 0:
                        self.w.move(car.tk_id, 0, 0.6*y_offset)
                    elif x_offset != 0 and y_offset == 0:
                        self.w.move(car.tk_id, 0.6*x_offset, 0)
                    self.w.update()


class Car:
    def __init__(self, id, tk_id, router):
        self.id = id
        self.tk_id = tk_id
        self.router = router


def index2point(x, y):
    matrix = []
    for index_y in range(0, y):
        row = []
        for index_x in range(0, x):
            point_x = index_x*30
            point_y = index_y*30
            point = (point_y, point_x, point_y+30, point_x+30)
            row.append(point)
        matrix.append(row)
    return np.array(matrix)

if __name__ == "__main__":
    # test
    array = [[-2, -2, -2, -2, -2, -2, -2],
             [-2, -1, -1, -1, -1, -1, -2],
             [-2, 1, -1, -1, -1, -1, -2],
             [-2, -1, -1, -1, -1, -1, -2],
             [-2, -1, -1, -1, -1, 0, -2],
             [-2, -2, -2, -2, -2, -2, -2]]
    array_2 = [[-2, -2, -2, -2, -2, -2, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, 1, -1, -1, -1, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, -1, -1, 0, -1, -2],
               [-2, -2, -2, -2, -2, -2, -2]]
    array_3 = [[-2, -2, -2, -2, -2, -2, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, 1, -1, -1, -1, -2],
               [-2, -1, -1, 0, -1, -1, -2],
               [-2, -2, -2, -2, -2, -2, -2]]
    array_4 = [[-2, -2, -2, -2, -2, -2, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, -1, 0, -1, -1, -2],
               [-2, -1, 1, -1, -1, -1, -2],
               [-2, -2, -2, -2, -2, -2, -2]]
    array_5 = [[-2, -2, -2, -2, -2, -2, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, -1, -1, -1, -1, -2],
               [-2, -1, 0, -1, -1, -1, -2],
               [-2, -1, -1, 1, -1, -1, -2],
               [-2, -2, -2, -2, -2, -2, -2]]
    arrays = np.array([array, array_2, array_3, array_4, array_5, array_4, array_3, array_2, array])
    weight = arrays[0].shape[1]
    height = arrays[0].shape[0]
    dr_ = Drawer(arrays)
    dr_.graph()
