import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import math
import numpy as np
import random
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)


class Singleton(type):
    '''
    Class object to prepare Singeleton for classes which has one instance.
    Metaclass is used for Singleton.
    '''

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Point:
    '''
    Class object to trace the location of points,
    which represents individuals on the cruise floor map.
    '''

    def __init__(self, loc_x, loc_y):
        """
        **Argu**
            loc_x: *int*
                Location on the x-axis of plot.
            loc_y: *int*
                Location on the y-axis of plot.
        """

        self.x = loc_x
        self.y = loc_y

    def move(self, vector):
        ''' This is to get moving direction of a point.'''

        self.x += vector.x
        self.y += vector.y

    def move_to(self, point):
        ''' Moving destination of a point.'''

        self.x = point.x
        self.y = point.y

    def get_vector(self, point):
        ''' To get the moving path direction in vector.'''
        return Vector(point.x - self.x, point.y - self.y)

    def get_distance(self, point):
        ''' Moving distance.'''

        return self.get_vector(point).get_len()


class Vector:
    ''' Class object to define the operators for vectors calculation.'''

    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def get_len(self):
        ''' To get the length of a vector.

        **return**
            math.sqrt(pow(self.x, 2) + pow(self.y, 2)): *float*
                Length of vector.
        '''
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))


class Bed:
    '''Class object to describe the bed numbers and usage.'''

    def __init__(self, bed_number):
        self.bed_number = bed_number
        self.occupied = False


class IsoRoom(metaclass=Singleton):
    '''
    Class object to describe the isolation room availbility. Add bed numbers.
    Assign patient to beds and vacate.
    Singleton type since only one overall Isolation room (regard all rooms as a unit).
    '''

    def __init__(self):
        self.occupied_beds = 0
        self.available_beds = Para.iso_room_capacity
        self.need_beds = 0
        self.beds_list = []
        for i in range(0, Para.iso_room_capacity):
            self.beds_list.append(Bed(i))

    def expand_cap(self, quantity=1):
        """
        This is to increase the isolation room numbers when there are more patients than available rooms.
        **Parameters**
            quantity: *int, optional*
                Initial value of available beds.
        """

        self.available_beds += quantity
        if len(self.beds_list) == 0:
            last_num = -1
        else:
            last_num = self.beds_list[-1].bed_number
        for i in range(0, quantity):
            new_num = last_num + i + 1
            self.beds_list.append(Bed(new_num))

    def assign_bed(self):
        """
        It changes the bed status to occupied (True) and return the new available bed numbers.
        **return**
            bed: <class '__main__.Bed'>
                Bed number and bed occupation condition.
        """
        for bed in self.beds_list:
            if bed.occupied is False:
                self.available_beds -= 1
                bed.occupied = True
                return bed

    def vacate_bed(self, bed):
        """
        It changes the bed status to empty (False) and return the new available bed numbers.
        **return**
            bed: *<class '__main__.Bed'>*
                Bed number and bed occupation condition.
        """
        bed.occupied = False
        self.available_beds += 1
        return bed


class Person(Point):
    """
    Person inherits from Point class. It describes each person's condition[individual condition].
    """

    def __init__(self, loc_x, loc_y):
        super(Person, self).__init__(loc_x, loc_y)
        self.status = Condition.healthy
        self.infected_time = 0
        self.inc_period = None
        self.confirmed_time = 0
        self.dead_time = 0
        self.recovery_time = 0
        self.need_iso = False
        self.relocation = None
        self.bed_assigned = None
        self.bed_waitlisted = False

    def gen_travel_dist(self):
        '''
        Get travel distance based on random assignment.
        **return**
            dist: *float*
                Float value of travel distance generated randomly based on mean and variation. 
        '''

        dist = np.random.normal(Para.travel_mean, math.sqrt(Para.travel_var))
        if dist > 0:
            return dist
        else:
            return 0

    def gen_unit_dir(self):
        '''
        Get the unit vector of travel direction.
        Unit vector = vector / length
        **return**
            unit_dir: *<class '__main__.Bed'>*
                x and y of unit vector.
        '''
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        dir = Vector(x, y)  # get random direction to move to
        unit_dir = dir / dir.get_len()
        return unit_dir

    # @OPTIONAL
    # def check_infection(self):
    #     '''
    #     Check if a person is infected.
    #     **return**
    #         status: *int*
    #             Condition code from class Condition.
    #     '''
    #     return self.status > Condition.susceptible

    def mark_infection(self):
        '''
        Change a person's condition to infected. 
        Assign it into infective list in class Pool.
        Record the day of getting infected.
        '''
        self.status = Condition.incubation
        Pool().infective.append(self)
        self.infected_time = Para.current_day

    def isolate(self):
        self.status = Condition.isolated

    def travel(self):
        '''
        Travel behavior of an individual at different conditions.
        '''

        dist = self.gen_travel_dist()  # randomly generated travel distance

        # Isolated and dead people do not travel. Dist is zero.
        if self.status == Condition.isolated or self.status == Condition.dead or dist == 0:
            return

        # If the person can travel, calculates the traveling.
        if self.relocation is None or self.relocation.arrived:
            unit_dir = self.gen_unit_dir()
            target_x = self.x + unit_dir.x * dist
            target_y = self.y + unit_dir.y * dist

            # Ensure the travel is in the range.
            if target_x < 10:
                target_x = 10
            if target_x > 10 + Para.cruise_width:
                target_x = 10 + Para.cruise_width
            if target_y < 10:
                target_y = 10
            if target_y > 10 + Para.cruise_height:
                target_y = 10 + Para.cruise_height
            self.relocation = Movement(target_x, target_y)

        if self.get_distance(self.relocation) < Para.move_speed / 10:
            self.move_to(self.relocation)
            self.relocation.arrived = True
            return

        target_dir = self.get_vector(self.relocation)
        step_dir = target_dir / target_dir.get_len()  # step direction in unit vector
        step_vec = Para.move_speed / 10 * step_dir
        self.move(step_vec)

    def refresh(self):
        '''
        This function is to deal with people in different conditions and refresh the numbers of people
        at each condition.

        '''
        # No need to refresh for dead people.
        if self.status == Condition.dead:
            return

        # Deal with sick person.
        if self.status == Condition.sick:
            if self.dead_time == 0:
                rand = np.random.uniform(0, 1)
                # If the person will die (fall in the fatal rate)
                if rand > Para.fatal_rate:
                    # Calculate the recovery time for the person who does not die.
                    self.dead_time = -1
                    recover_time = max(0, np.random.normal(
                        Para.recover_period, math.sqrt(Para.recover_period_var)))
                    self.recovery_time = self.infected_time + recover_time
                else:
                    # Calculate the time left for the person who will die.
                    life_left = max(0, np.random.normal(
                        Para.death_period, math.sqrt(Para.death_period_var)))
                    self.dead_time = self.confirmed_time + life_left

            # Isolate sick person if latency period has passed.
            if Para.current_day - self.confirmed_time >= Para.iso_latency:
                bed = IsoRoom().assign_bed()
                if bed is None:
                    if self.bed_waitlisted is False:
                        self.bed_waitlisted = True
                        IsoRoom().need_beds += 1
                else:
                    self.bed_assigned = bed
                    Pool().infective.remove(self)
                    self.status = Condition.isolated
                    if self.bed_waitlisted and IsoRoom().need_beds > 0:
                        IsoRoom().need_beds -= 1

        # Deal with dying person, either sick or isolated.
        if self.dead_time > 0:
            if Para.current_day >= self.dead_time:
                # vacate bed from deceased person
                if self.bed_assigned is not None:
                    IsoRoom().vacate_bed(self.bed_assigned)
                if self.bed_waitlisted and IsoRoom().need_beds > 0:
                    IsoRoom().need_beds -= 1
                # Deceased individual cannot be infected anymore
                if self.status == Condition.sick:
                    Pool().infective.remove(self)
                self.status = Condition.dead

        # Deal with recovering person
        if self.dead_time == -1 and Para.current_day >= self.recovery_time:
            if self.bed_assigned is not None:
                IsoRoom().vacate_bed(self.bed_assigned)
                self.bed_assigned = None
            if self.bed_waitlisted and IsoRoom().need_beds > 0:
                self.bed_waitlisted = False
                IsoRoom().need_beds -= 1
                Pool().infective.remove(self)
            self.status = Condition.healthy


        # Deal with incubation period person
        if self.status == Condition.incubation:
            # Random incubation period
            if self.inc_period is None:
                self.inc_period = max(0, np.random.normal(
                    Para.inc_period, math.sqrt(Para.inc_period_var)))
            # Change condition into sick after incubation period
            if Para.current_day > self.infected_time + self.inc_period:
                self.status = Condition.sick
                self.confirmed_time = Para.current_day
        # Incubation/ sick people still travel before being isolated.
        self.travel()

        # Deal with healthy or suseptible person.
        if self.status == Condition.healthy:
            infective_people = Pool().infective.copy()
            for person in infective_people:
                if self.dead_time != -1:
                    rand = np.random.uniform(0, 1)
                    # Individual get infected when fall into the trans possibility
                    # and does not follow social distancing.
                    if rand < Para.trans_prob and self.get_distance(person) < Para.safe_distance:
                        self.mark_infection()
                        break


class Pool(metaclass=Singleton):
    """
    Class object to make pools of people and their conditions. 
    People at different conditions are assigned into lists.
    """

    def __init__(self):
        self.all = []  # List of all people
        self.infective = []  # List of people in incubation period
        for i in range(0, Para.total_population):
            loc_x = np.random.uniform(10, Para.cruise_width + 10)
            loc_y = np.random.uniform(10, Para.cruise_height + 10)
            self.all.append(Person(loc_x, loc_y))

    def count_status(self, condition_code=None):
        """
        This is to count people in a particular condition.
        **parameter**
            condition_code: *int * starts with None Type
                See class Condition. Condition code of people.
        **output**
            len(self.all): *int*
                When no condition code is assigned, return the list of all
                population.
            count: *int*
                Number of people in a particular condition.

        """
        if condition_code is None:
            return len(self.all)
        count = 0
        for person in self.all:
            if person.status == condition_code:
                count += 1
        return count


class Para:
    '''
    Parameters are based on SIR virus transmission model:
    https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model
    SIR Statistics of COVID-19 source:
    https://www.cdc.gov/coronavirus/2019-ncov/hcp/clinical-guidance-management-patients.html

    '''
    game_over = False

    # total population on the cruise
    total_population = 1000

    current_day = 1

    # size of cruise, for plotting
    cruise_width = 1000
    cruise_height = 1000
    cruise_centerx = 500
    cruise_centery = 500

    # size of each person, for plotting
    dot_size = 10

    # Number of people who are infected (brought the disease on board)
    patients_zero = 25

    fatal_rate = 0.07
    trans_prob = 0.8

    death_period = 20  # days take to die after infected
    death_period_var = 20

    inc_period = 5  # virus incubation period
    inc_period_var = 5

    recover_period = 40
    recover_period_var = 40

    # response latency - delay of a sick person getting isolation
    iso_latency = 5

    iso_room_capacity = 0

    safe_distance = 10  # safe distance to prevent spreading of virus

    travel_mean = 50  # average travel distance of all people
    travel_var = 50  # variance of the travel distance of all people

    move_speed = 20  # moving distance of each person per day


class Condition:
    '''
    Object class to simplify conditions into codes from 0 to 5.
    '''

    healthy = 0
    susceptible = 1
    incubation = 2  # incubation period people
    sick = 3
    isolated = 4  # isolated people, location frozen
    dead = 5  # dead people, location frozen, cannot transmit


class Movement(Point):
    '''    
    Class object to define if the person arrives the next stop.
    '''

    def __init__(self, loc_x, loc_y):
        super(Movement, self).__init__(loc_x, loc_y)
        self.arrived = False


class LiveWindow(QtCore.QThread):
    '''
    Class object to refresh GUI window.
    '''

    def __init__(self, plot):
        super(LiveWindow, self).__init__()
        self.plot = plot

    # If the game is not over, Live Window keeps running.
    def run(self):
        while Para.game_over is False:
            QtCore.QThread.msleep(100)
            self.plot.update()
            Para.current_day += 0.1


class Plot(QtWidgets.QWidget):
    '''
    Class object to plot the people at different conditions in the cruise floor map on GUI.
    '''

    def __init__(self, ui):
        super(Plot, self).__init__(ui.centralwidget)
        self.ui = ui
        self.setGeometry(QtCore.QRect(
            0, 0, Para.cruise_width + 20, Para.cruise_height + 20))

    def paintEvent(self, event):
        '''
        Paint the plot everytime when it is refreshed.
        **Parameter**
            event: *<class 'PyQt5.QtGui.QPaintEvent'>*

        '''

        painter = QtGui.QPainter()
        painter.begin(self)
        if Para.game_over:
            return

        # start to draw the plot of all persons
        all_persons = Pool().all
        if all_persons is None:
            return

        healthy_count = 0  # Number of healty people
        incubation_count = 0  # Number of people in incubation period
        sick_count = 0  # Number of people who are sick
        isolated_count = 0  # Number of people in isolation
        dead_count = 0  # Number of deceased
        recover_count = 0  # Number of people who recovered

        for person in all_persons:
            if person.status == Condition.healthy:
                healthy_count += 1
                if person.dead_time == -1:
                    painter.setPen(QtGui.QColor(0, 170, 0))
                    recover_count += 1  # Recovered people
                else:
                    painter.setPen(QtGui.QColor(0, 255, 0))  # Healthy people
            elif person.status == Condition.incubation:
                painter.setPen(QtGui.QColor(255, 0, 255))
                incubation_count += 1  # Incubation period people
            elif person.status == Condition.sick:
                painter.setPen(QtGui.QColor(255, 0, 0))
                sick_count += 1  # Symptomatic/sick people
            elif person.status == Condition.isolated:
                painter.setPen(QtGui.QColor(0, 170, 255))
                isolated_count += 1  # Isolated patients
            elif person.status == Condition.dead:
                painter.setPen(QtGui.QColor(0, 0, 0))
                dead_count += 1  # Deceased people

            # Refresh the number of each condition
            person.refresh()

            # Setting size of dot on plot
            size_hf = Para.dot_size // 2
            dot = QtCore.QRect(person.x - size_hf, person.y -
                               size_hf, 2 * size_hf, 2 * size_hf)
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            brush.setColor(painter.pen().color())
            painter.setBrush(brush)
            painter.drawRect(dot)

        int_day = math.floor(Para.current_day)  # time (day)

        # Update numbers to GUI
        self.ui.label_18time.setText(
            f'<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">{int_day}</span></p></body></html>')
        self.ui.label_10Totalpopulation.setText(f'{Para.total_population}')
        self.ui.label_11healthy.setText(
            f'<html><head/><body><p><span style=\" color:#00ff00;\">{healthy_count}</span></p></body></html>')
        self.ui.label_11healthy_2.setText(
            f'<html><head/><body><p><span style=\" color:#00aa00;\">{recover_count}</span></p></body></html>')
        self.ui.label_13symtomatic.setText(
            f'<html><head/><body><p><span style=\" color:#ff00ff;\">{incubation_count}</span></p></body></html>')
        self.ui.label_12incubation.setText(
            f'<html><head/><body><p><span style=\" color:#ff0000;\">{sick_count}</span></p></body></html>')
        self.ui.label_15isolated.setText(
            f'<html><head/><body><p><span style=\" color:#00aaff;\">{isolated_count}</span></p></body></html>')
        self.ui.label_16remaning.setText(
            f'<html><head/><body><p><span style=\" color:#00aaff;\">{IsoRoom().available_beds}</span></p></body></html>')
        self.ui.label_14nonsymtomatic.setText(
            f'<html><head/><body><p><span style=\" color:#00aaff;\">{IsoRoom().need_beds}</span></p></body></html>')
        self.ui.label_17dead.setText(
            f'<html><head/><body><p><span style=\" color:#000000;\">{dead_count}</span></p></body></html>')
        self.ui.label_17.setText(f'{Para.iso_room_capacity}')
        self.ui.label_16.setText(f'{Para.trans_prob}')
        self.ui.label_18.setText(f'{Para.travel_mean}')
        self.ui.label_19.setText(f'{Para.inc_period}')
        self.ui.label_20.setText(f'{Para.iso_latency}')
        self.ui.label_21.setText(f'{Para.safe_distance}')

        if incubation_count == 0 and sick_count == 0 and isolated_count == 0:
            Para.game_over = True
            QtWidgets.QMessageBox.information(
                self.ui.centralwidget, 'Message', 'The virus outbreak is now ended.', QtWidgets.QMessageBox.Ok)
        painter.end()


class MyRequestHandler(SRH):
    '''
    Class object to receive requests from client and update related values.
    '''

    def handle(self):
        '''Read request from client.'''
        data = str(self.rfile.readline(), 'utf-8')
        # Receive commands from client socket.
        index = data.find(':')
        command = data[:index]
        # Send values related to command
        value = data[index + 1:]
        value = int(value)

        # Update parameters (in Para class) based on command received.
        if command == 'add_iso_beds':
            Para.iso_room_capacity += value
            IsoRoom().expand_cap(value)
        elif command == 'set_travel_mean':
            Para.travel_mean = value
        elif command == 'set_trans_prob':
            Para.trans_prob = value / 100
        elif command == 'close':
            Para.app.quit()

        self.wfile.write(b'ok\r\n')


class Receiver(QtCore.QThread):
    '''
    Create and run a TCP server.
        Reference:
        https://www.pythonstudio.us/pyqt-programming/creating-a-tcp-server.html
    '''

    tcp_server = None

    def __init__(self):
        super(Receiver, self).__init__()
        self.host = ''
        self.port = 6589
        self.addr = (self.host, self.port)
        Receiver.tcp_server = TCP(self.addr, MyRequestHandler)

    def run(self):
        Receiver.tcp_server.serve_forever()


def init_game():
    '''
    To start the game with random patient zeros and mark them as infected ones.
    '''
    Pool()
    IsoRoom()
    patient_zeros = random.sample(Pool().all, Para.patients_zero)
    for person in patient_zeros:
        person.mark_infection()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Para.app = app
    main = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_COVID19Simulation()
    ui.setupUi(main)

    init_game()
    plot = Plot(ui)
    live = LiveWindow(plot)
    live.start()

    receiver = Receiver()
    receiver.start()
    main.show()

    sys.exit(app.exec_())
