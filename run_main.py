import UIWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import math
import numpy as np
import random
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Point:
    def __init__(self, loc_x, loc_y):
        self.x = loc_x
        self.y = loc_y

    def move(self, vector):
        self.x += vector.x
        self.y += vector.y

    def move_to(self, point):
        self.x = point.x
        self.y = point.y

    def get_vector(self, point):
        return Vector(point.x - self.x, point.y - self.y)

    def get_distance(self, point):
        return self.get_vector(point).get_len()


class Vector:
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
        return self*other

    def get_len(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))


class Bed:
    def __init__(self, bed_number):
        self.bed_number = bed_number
        self.occupied = False


class IsoRoom(metaclass=Singleton):
    def __init__(self):
        self.occupied_beds = 0
        self.available_beds = Para.iso_room_capacity
        self.need_beds = 0
        self.beds_list = []
        for i in range(0, Para.iso_room_capacity):
            self.beds_list.append(Bed(i))

    def expand_cap(self, quantity=1):
        self.available_beds += quantity
        if len(self.beds_list) == 0:
            last_num = -1
        else:
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


class Person(Point):
    """
    Person inherits from Point class. It describes each person's condition [individual condition].
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
        dist = np.random.normal(Para.travel_mean, math.sqrt(Para.travel_var))
        if dist > 0:
            return dist
        else:
            return 0

    def gen_unit_dir(self):
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        dir = Vector(x, y)
        unit_dir = dir / dir.get_len()
        return unit_dir

    def check_infection(self):
        return self.status > Condition.susceptible

    def mark_infection(self):
        self.status = Condition.incubation
        Pool().infective.append(self)
        self.infected_time = Para.current_day

    def isolate(self):
        self.status = Condition.isolated

    def travel(self):
        dist = self.gen_travel_dist()
        if self.status == Condition.isolated or self.status == Condition.dead or dist == 0:
            return
        if self.relocation is None or self.relocation.arrived:
            unit_dir = self.gen_unit_dir()
            target_x = self.x + unit_dir.x * dist
            target_y = self.y + unit_dir.y * dist
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
        step_dir = target_dir / target_dir.get_len()
        step_vec = Para.move_speed / 10 * step_dir
        self.move(step_vec)

    def refresh(self):
        if self.status == Condition.dead:
            return
        # Deal with sick person.
        if self.status == Condition.sick:
            if self.dead_time == 0:
                rand = np.random.uniform(0,1)
                if rand > Para.fatal_rate:
                    self.dead_time = -1  # will not die
                    recover_time = max(0, np.random.normal(Para.recover_period, math.sqrt(Para.recover_period_var)))
                    self.recovery_time = self.infected_time + recover_time
                else:
                    life_left = max(0, np.random.normal(Para.death_period, math.sqrt(Para.death_period_var)))
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
                if self.bed_assigned is not None:
                    IsoRoom().vacate_bed(self.bed_assigned)
                if self.bed_waitlisted and IsoRoom().need_beds > 0:
                    IsoRoom().need_beds -= 1
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
            self.status = Condition.healthy
        # Deal with incubation period person.
        if self.status == Condition.incubation:
            if self.inc_period is None:
                self.inc_period = max(0, np.random.normal(Para.inc_period, math.sqrt(Para.inc_period_var)))
            if Para.current_day > self.infected_time + self.inc_period:
                self.status = Condition.sick
                self.confirmed_time = Para.current_day
        self.travel()
        # Deal with healthy or suseptible person.
        if self.status == Condition.healthy:
            infective_people = Pool().infective.copy()
            for person in infective_people:
                if self.dead_time != -1:
                    rand = np.random.uniform(0,1)
                    if rand < Para.trans_prob and self.get_distance(person) < Para.safe_distance:
                        self.mark_infection()
                        break


class Pool(metaclass=Singleton):
    """
    Pool of people and their conditions. Assigned in list.
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
            condition_code: *int* starts with None Type
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
    healthy = 0
    susceptible = 1
    incubation = 2  # incubation period people
    sick = 3
    isolated = 4  # isolated people, location frozen
    dead = 5  # dead people, location frozen, cannot transmit


class Movement(Point):
    """
    Track person's movement path.
    """

    def __init__(self, loc_x, loc_y):
        super(Movement, self).__init__(loc_x, loc_y)
        self.arrived = False


class LiveWindow(QtCore.QThread):
    """
    Refresh GUI window.

    """

    def __init__(self, plot):
        super(LiveWindow, self).__init__()
        self.plot = plot

    def run(self):
        while Para.game_over is False:
            QtCore.QThread.msleep(100)
            self.plot.update()
            Para.current_day += 0.1


class Plot(QtWidgets.QWidget):
    def __init__(self, ui):
        super(Plot, self).__init__(ui.centralwidget)
        self.ui = ui
        self.setGeometry(QtCore.QRect(0, 0, Para.cruise_width + 20, Para.cruise_height + 20))

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        if Para.game_over:
            return
        # start to draw the plot of all persons
        all_persons = Pool().all
        if all_persons is None:
            return
        healthy_count = 0
        incubation_count = 0
        sick_count = 0
        isolated_count = 0
        dead_count = 0
        recover_count = 0
        for person in all_persons:
            if person.status == Condition.healthy:
                healthy_count += 1
                if person.dead_time == -1:
                    painter.setPen(QtGui.QColor(0, 170, 0))
                    recover_count += 1
                else:
                    painter.setPen(QtGui.QColor(0, 255, 0))
            elif person.status == Condition.incubation:
                painter.setPen(QtGui.QColor(255, 0, 255))
                incubation_count += 1
            elif person.status == Condition.sick:
                painter.setPen(QtGui.QColor(255, 0, 0))
                sick_count += 1
            elif person.status == Condition.isolated:
                painter.setPen(QtGui.QColor(0, 170, 255))
                isolated_count += 1
            elif person.status == Condition.dead:
                painter.setPen(QtGui.QColor(0, 0, 0))
                dead_count += 1
            person.refresh()
            size_hf = Para.dot_size // 2
            dot = QtCore.QRect(person.x - size_hf, person.y - size_hf, 2 * size_hf, 2 * size_hf)
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            brush.setColor(painter.pen().color())
            painter.setBrush(brush)
            painter.drawRect(dot)
        int_day = math.floor(Para.current_day)
        self.ui.label_18time.setText(f'<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">{int_day}</span></p></body></html>')
        self.ui.label_10Totalpopulation.setText(f'{Para.total_population}')
        self.ui.label_11healthy.setText(f'<html><head/><body><p><span style=\" color:#00ff00;\">{healthy_count}</span></p></body></html>')
        self.ui.label_11healthy_2.setText(f'<html><head/><body><p><span style=\" color:#00aa00;\">{recover_count}</span></p></body></html>')
        self.ui.label_13symtomatic.setText(f'<html><head/><body><p><span style=\" color:#ff00ff;\">{incubation_count}</span></p></body></html>')
        self.ui.label_12incubation.setText(f'<html><head/><body><p><span style=\" color:#ff0000;\">{sick_count}</span></p></body></html>')
        self.ui.label_15isolated.setText(f'<html><head/><body><p><span style=\" color:#00aaff;\">{isolated_count}</span></p></body></html>')
        self.ui.label_16remaning.setText(f'<html><head/><body><p><span style=\" color:#00aaff;\">{IsoRoom().available_beds}</span></p></body></html>')
        self.ui.label_14nonsymtomatic.setText(f'<html><head/><body><p><span style=\" color:#00aaff;\">{IsoRoom().need_beds}</span></p></body></html>')
        self.ui.label_17dead.setText(f'<html><head/><body><p><span style=\" color:#000000;\">{dead_count}</span></p></body></html>')
        self.ui.label_17.setText(f'{Para.iso_room_capacity}')
        self.ui.label_16.setText(f'{Para.trans_prob}')
        self.ui.label_18.setText(f'{Para.travel_mean}')
        self.ui.label_19.setText(f'{Para.inc_period}')
        self.ui.label_20.setText(f'{Para.iso_latency}')
        self.ui.label_21.setText(f'{Para.safe_distance}')

        if incubation_count == 0 and sick_count == 0 and isolated_count == 0:
            Para.game_over = True
            QtWidgets.QMessageBox.information(self.ui.centralwidget, 'Message', 'The virus outbreak is now ended.', QtWidgets.QMessageBox.Ok)
        painter.end()


class MyRequestHandler(SRH):
    def handle(self):
        # read request from client
        data = str(self.rfile.readline(),'utf-8')
        index = data.find(':')
        command = data[:index]
        value = data[index + 1:]
        value = int(value)

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
    tcp_server = None
    def __init__(self):
        super(Receiver,self).__init__()
        self.host = ''
        self.port = 6589
        self.addr = (self.host, self.port)
        Receiver.tcp_server = TCP(self.addr, MyRequestHandler)

    def run(self):
        Receiver.tcp_server.serve_forever()


def init_game():
    Pool()
    IsoRoom()
    patient_zeros = random.sample(Pool().all, Para.patients_zero)
    for person in patient_zeros:
        person.mark_infection()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Para.app = app
    main = QtWidgets.QMainWindow()
    ui = UIWindow.Ui_MainWindow()
    ui.setupUi(main)

    init_game()
    plot = Plot(ui)
    live = LiveWindow(plot)
    live.start()

    receiver = Receiver()
    receiver.start()
    main.show()

    sys.exit(app.exec_())
