import math
import random


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class IsoRoom(metaclass = Singleton):
    # _instances = {}
    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instances:
    #         cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    #     return cls._instances[cls]

    def __init__(self):
        self.occupied_beds = 0
        self.free_beds = Parameters.iso_room_capacity
        self.need_beds = 0
        self.beds_list = []

class Individual():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moving(self, x, y):
        self.x += step_x
        self.y += step_y

    def person(self, x, y):

        # variance of movement
        self.sigma = moving_sigma

        # status: healthy,
        self.status = healthy

        # the day# a person is infected
        self.infected_time = 0

        # the day# a person is dead
        self.death_time = 0

        # the day# a person is sick
        self.sick_time = self.infected_time + latency

        # if a person is isolated
        self.isolated = False

        # if a person reaches his next stop
        self.arrival = False


'''
# Constants

    # healthy, including recovered
    healthy = 0

    #infected, including incubation, symptomatic and non-symptomatic
    infected = 1

    # days between individual is infected and shows symptoms
    latency = 2

    # sick people
    symptomatic = 3
    non-symptomatic = 4

    # isolated people, movement frozen
    isolated = 5

    # dead people, location frozen, cannot transmit
    death = 6
'''
