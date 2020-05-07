import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import random
import math


class Cruise:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, cruise_centerx, cruise_centery):
        self.centerx = cruise_centerx
        self.centery = cruise_centery


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


class Track:
    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y
        self.static = False


class Parameters:
    finish = False
    # total population on the cruise
    total_population = 2500

    current_time = 1  # by day

    # size of cruise, for plotting
    cruise_width = 500
    cruise_length = 2000
    cruise_centerx = 250
    cruise_centery = 1000

    # Number of people who are infected (brought the disease on board)
    patients_zero = 5

    # rate of death for infected patients
    fatal_rate = 0.08
    trans_prob = 0.8

    # days take to die
    death_period = 15

    # variance of days to die
    death_period_var = 15

    # virus latency period
    latency_period = 7

    # response latency - delay of a sick person getting isolation
    iso_latency = 2

    iso_room_capacity = 100
    iso_room_size = 0

    # safe distance of virus
    safe_distance = 2

    flow_intention = 3

    normal_sigma = 1
    normal_t_sigma = 50


class Condition:
    healthy = 0
    susceptible = 1
    latency = 2
    sick = 3
    isolated = 4  # isolated people, location frozen
    death = 5  # dead people, location frozen, cannot transmit



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Params.
    MainWindow = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
