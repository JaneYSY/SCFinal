import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import math
import numpy as np


# class Singleton(type):
#     """
#     For some classes, only ONE instance is allowed. Singleton is to define here using metaclass,
#     and metaclass to define the behavior of a class and its instance.
#     """

#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(
#                 Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

#     """ Title: Python Course: Metaclasses - Creating Singletons using Metaclasses
#     Author: Bernd Klein
#     URL: https://www.python-course.eu/python3_metaclasses.php
#     """


'''
class Cruise:
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance
    def __init__(self, cruise_centerx, cruise_centery):
        self.centerx = cruise_centerx
        self.centery = cruise_centery
'''


class Point:
    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y

    def move(self, vec_x, vec_y):
        self.x += vec_x
        self.y += vec_y

    def move_to(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y


class Bed:
    def __init__(self, bed_number):
        self.bed_number = bed_number


class IsoRoom:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.occupied_beds = 0
        self.free_beds = Parameters.iso_room_capacity
        self.need_beds = 0
        self.beds_list = []


class Person(Point):
    def __init__(self, loc_x, loc_y, cruise):
        super(Person, self).__init__(loc_x, loc_y)
        self.cruise = cruise
        self.sigma = Parameters.normal_sigma
        self.t_sigma = Parameters.t_sigma
        self.status = Condition.healthy
        self.infected_time = 0
        self.confirmed_time = 0
        self.dead_time = 0
        self.need_iso = False
        self.relocation = None
        self.assigned_bed = None


class Parameters:
    game_over = False
    # total population on the cruise
    total_population = 1000

    current_day = 1

    # size of cruise, for plotting
    cruise_width = 1000
    cruise_length = 1000
    cruise_centerx = 500
    cruise_centery = 500

    # Number of people who are infected (brought the disease on board)
    patients_zero = 5

    # rate of death for infected patients
    fatal_rate = 0.08
    trans_prob = 0.8

    # days take to die
    death_period = 15

    # variance of days to die
    death_period_var = 15

    # virus incubation period
    incubation_period = 7

    # response latency - delay of a sick person getting isolation
    iso_latency = 2

    iso_room_capacity = 100
    iso_room_size = 0

    # safe distance of virus
    safe_distance = 2

    flow_intention = 3

    # normal_sigma = 1
    # normal_t_sigma = 50


class Condition:
    healthy = 0
    susceptible = 1
    latency = 2
    sick = 3
    isolated = 4  # isolated people, location frozen
    death = 5  # dead people, location frozen, cannot transmit


class Track:
    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y
        self.static = False


class LiveWindow(QtCore.QThread):
    def __init__(self):
        super(LiveWindow, self).__init__()

    def run(self):
        while Parameters.game_over is False:
            QtCore.QThread.msleep(100)
            Parameters.current_day += 0.1


class Pool:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.all = []
        self.incubation = []


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Parameters.app = app
    main = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_MainWindow()
    ui.setupUi(main)
    live = LiveWindow()
    live.start()
    main.show()

    sys.exit(app.exec_())
