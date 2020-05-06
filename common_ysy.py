import math
import random


class Singleton(type):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls.__instance


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
