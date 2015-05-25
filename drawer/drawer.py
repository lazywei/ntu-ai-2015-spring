# -*- coding: utf-8 -*-
from termcolor import colored
import os
import time


class Drawer:
    def __init__(self, _array):
        self._array = _array
        time.sleep(0.5)
        os.system('clear')

    def to_map(self):
        _map = []
        for raw in self._array:
            raw = map(lambda pix: self.color(pix), raw)
            _map.append(''.join(raw))
        self._map = '\n'.join(_map)
        print self._map

    def color(self, pix):
        if pix == 1:
            return colored(" ▩", "green")
        elif pix == 0:
            return colored("  ", "blue")
        elif pix > 0:
            return colored(" {0}".format(pix), "yellow")
        else:
            return colored(" #".format(pix), "red")
