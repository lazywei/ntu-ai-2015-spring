from Tkinter import *
import pickle
import numpy as np
import time
import redis


blockWidth = 30
offset_size = 2

class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def flushall(self):
        self.__db.flushall()

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, items):
        items = map(lambda item: pickle.dumps(item), items)
        self.__db.rpush(self.key, *items)

    def get(self, block=True, timeout=None):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return pickle.loads(item)


class Drawer:
    def __init__(self, r):
        map_ = np.array(r.get())
        weight = map_.shape[1]
        height = map_.shape[0]
        self.start = map_
        self.maps = r

        # tinker
        self.master = Tk()
        self.w = Canvas(self.master,
                        width=height*blockWidth,
                        height=weight*blockWidth)
        self.w.pack()
        self.points = index2point(weight, height)
        self.cars = []
        self.graph()

    def graph(self):
        map_ = self.start
        weight = map_.shape[1]
        height = map_.shape[0]
        for w in range(0, weight):
            for h in range(0, height):
                self.graphunit(map_[h][w], self.points[h][w], map_)

        self.master.after(0, self.animation())

    def graphunit(self, id, points, map_):
        if id == -2:
            color = "red"
        else:
            colors = ["blue", "green", "yellow", "pink", "orange",
                      "purple", "black", "gray"]
            color = colors[id % len(colors)]

        if id >= 0:
            tk_id = self.w.create_rectangle(points[0], points[1], points[2], points[3],
                                            fill=color, outline="white")
            self.cars.append(Car(id, tk_id, self.car_state(id, map_)))

        elif id == -2:
            self.w.create_rectangle(points[0], points[1], points[2], points[3],
                                    fill=color, outline="white")

    def car_state(self, id, map_):
        x, y = np.nonzero(id == map_)
        return [x[0], y[0]]

    def animation(self):
        while not self.maps.empty():
            map_ = self.maps.get()
            for i in range(0, int(round(blockWidth/offset_size))):
                for car in self.cars:
                    points = self.car_state(car.id, map_)
                    if points != car.state:
                        x_offset = points[0] - car.state[0]
                        y_offset = points[1] - car.state[1]
                        if x_offset == 0 and y_offset != 0:
                            self.w.move(car.tk_id, 0, offset_size*y_offset)
                        elif x_offset != 0 and y_offset == 0:
                            self.w.move(car.tk_id, offset_size*x_offset, 0)
                        self.w.update()
            print ('Finish 1 map')
            for car in self.cars:
                car.state = self.car_state(car.id, map_)
        while self.maps.empty():
            time.sleep(10)
            #   if self.maps.empty():
            #       # If there is no new map after 60 second, the animation will stop
            #       self.master.mainloop()
            #       exit()
            self.animation()

class Car:
    def __init__(self, id, tk_id, state):
        self.id = id
        self.tk_id = tk_id
        self.state = state


def index2point(x, y):
    matrix = []
    for index_y in range(0, y):
        row = []
        for index_x in range(0, x):
            point_x = index_x*blockWidth
            point_y = index_y*blockWidth
            point = (point_y, point_x, point_y+blockWidth, point_x+blockWidth)
            row.append(point)
        matrix.append(row)
    return np.array(matrix)

if __name__ == "__main__":
    r = RedisQueue('key')
    while True:
        if r.qsize() >= 2:
            print ('start!')
            Drawer(r)
