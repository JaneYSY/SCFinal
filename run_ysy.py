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

    """ Title: Python Course: Metaclasses - Creating Singletons using Metaclasses
    Author: Bernd Klein
    URL: https://www.python-course.eu/python3_metaclasses.php
    We decide to put the Singleton into each targeted class. """


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


class Bed:
    """
    Number of bed.
    Bed and IsoRoom are separated is because IsoRoom is Singleton for metaclass.
    """

    def __init__(self, bed_number):
        self.bed_number = bed_number
        self.occupied = False


class IsoRoom:

    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.occupied_beds = 0
        self.available_beds = Parameters.iso_room_capacity
        self.need_beds = 0
        # A list of bed to assign individual bed's condition.
        self.beds_list = []
        for i in range(0, Parameters.iso_room_capacity):
            self.beds_list.append(Bed(i))

    def expand_cap(self, quantity=1):
        last_num = self.beds_list[-1].bed_number
        for i in range(0, quantity):
            new_num = last_num + i + 1
            self.beds_list.append(Bed(new_num))

    def assign_bed(self):
        for bed in self.beds_list:
            if bed.occupied is False:
                self.available_beds -= 1
                bed.occupied = True
                return bed

    def vacate_bed(self, bed):
        bed.occupied = False
        self.available_beds += 1
        return bed


class Point:
    """
    This is to describe invididual as points.
    Points move with velocity.
    Points move from and to location which are spots (x, y) on the plot. 
    """

    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y

    def move(self, vec_x, vec_y):
        self.x += vec_x
        self.y += vec_y

    def move_to(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y


class Person(Point):
    """
    Person inherits from Point class. It describes each person's condition [individual condition].
    """

    def __init__(self, loc_x, loc_y):
        super(Person, self).__init__(loc_x, loc_y)
        self.status = Condition.healthy
        self.infected_time = 0
        self.confirmed_time = 0
        self.dead_time = 0
        self.need_iso = False
        self.relocation = None
        self.bed_assigned = None


class Parameters:
    """
    Parameters to be called in refreshing everyday's change. [Overall condition]
    """
    game_over = False
    total_population = 1000  # total population on the cruise
    current_day = 1

    # Size of cruise, for plotting
    cruise_width = 1000
    cruise_hight = 1000
    cruise_centerx = 500
    cruise_centery = 500

    # Number of people who are infected (brought the disease on board)
    patients_zero = 5

    fatal_rate = 0.08  # rate of death for infected patients
    trans_prob = 0.8  # if you are in contact with an infected person, the chance you'll get sick

    death_period = 15  # days take to die
    death_period_var = 15  # variance of days to die

    incubation_period = 7  # virus incubation period

    iso_latency = 2  # response latency - delay of a sick person getting isolation
    iso_room_capacity = 100

    safe_distance = 2  # safe distance to prevent spreading

    flow_intention = 3  # motivation for an individual to move on the cruise

    # normal_sigma = 1
    # normal_t_sigma = 50


class Condition:
    """
    Condition of each person.
    """

    healthy = 0
    susceptible = 1
    latency = 2  # incubation period
    sick = 3
    isolated = 4  # isolated people, location frozen
    death = 5  # dead people, location frozen, cannot transmit


class Track:
    """
    Track person's movement.
    """

    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y
        self.static = False


class LiveWindow(QtCore.QThread):
    """
    Refresh GUI window. 

    """

    def __init__(self):
        super(LiveWindow, self).__init__()

    def run(self):
        while Parameters.game_over is False:
            QtCore.QThread.msleep(100)
            Parameters.current_day += 0.1
            print(Parameters.current_day)


class Pool:
    """
    Pool of people and their conditions. Assigned in list.
    """

    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.all = []  # List of all people
        self.incubation = []  # List of people in incubation period
        for i in range(0, Parameters.total_population):
            loc_x = random.uniform(0, Parameters.cruise_width)
            loc_y = random.uniform(0, Parameters.cruise_hight)
            self.all.append(Person(loc_x, loc_y))

    def count_condition(self, condition_code=None):
        if condition_code == None:
            return len(self.all)
        count = 0
        for person in self.all:
            if person.status == condition_code:
                count += 1
        return count


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
