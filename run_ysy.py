import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import random
import math





class Bed():
	def __init__(self,)


class Singleton(object):
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance


# Parameters
class Parameters():
	
	#total population on the cruise
	total_population = 2500

	current_time = 1 # by day

	# size of cruise, for plotting
	cruise_width = 500
	cruise_length = 2000
	cruise_centerx = 250
	cruise_centery = 1000

	# Number of people who are infected (brought the disease on board)
	patients_zero = random.randint(1, 10)

	# rate of death for infected patients
	fatal_rate = 0.12

	#days take to die
	death_period = 15

	#variance of days to die
	#以后看看要不要写

	# number of people a sick individual can infect
	reproduction_rate = 2

	#virus latency period
	latency_period = random.randint(2, 14)

	#response latency - delay of a sick person getting treatment, such as isolation
	response_latency = 2

	#safe distance of social distancing
	safe_distance = 2

	#moving factor - how much movement is allowed, [0, 5]
	moving_factors = 2


class Constant():
	healthy = 0
	susceptible = healthy + 1
	latency = susceptible + 1
	sick = latency + 1
	isolated = sick + 1 # isolated people, location frozen
	death = isolated + 1 # dead people, location frozen, cannot transmit


# 单件模式
class 









if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Params.
    MainWindow = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    
    sys.exit(app.exec_())

