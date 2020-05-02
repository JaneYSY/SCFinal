import random


def readfile(file):
    '''
    This is to read the input file.
    It defines the player's defined parameter they want to put into the game.

    **parameters**
        file:

    **output**
        day_of_first_case
        day_of_mask
        day_of_quarantine

    '''
    '''
    # THIS IS THE FILE PUT IN .BFF

    Mask wearing
    '''

    f = open(file)
    line = f.readline()

    while line:

        while line.startswith('mask wearing'):
            line = line.split()
            mask_day = line[1]
            line = f.readline()

        while line.startswith('quarantine starts'):
            line = line.split()
            quarantine_day = line[1]
            line = f.readline()

        while line.startswith('patients isolation starts'):
            line = line.split()
            isolation_day = line[1]
            line = f.readline()

        line = f.readline()

    f.close()
    return (mask_day, quarantine_day, isolation_day)


class People():
    # define the behavior of people

    ppl = 2500  # total no. of people in cruise

    def __init__(self, aaa):
        self.aaa = aaa  # 先挂着，到时候改

    def patient_0(self):
        '''
        generate a random age of the patient 0 and tell the player.

        '''
        0_numbers = random.randint(1, 10)

        print(0_numbers, "patient(s) on board are infected by COVID-19.")

        while True:
            msg = input(
                "Please confirm the number of patient 0(s), enter 'NEXT' to continue the game:")

            if msg == "NEXT":
                return
            else:
                input("Wrong input, please enter 'NEXT' to continue the game:")

        return 0_numbers

    def person_state(self, statecode):
        '''
        This is to check if the person is healthy, sick, recover, or dead and adjust the population number
        0 is healthy, 1 is sick, 2 is recovered, 3 is death.

        '''

        if self.statecode = 1:
            healthy_number -= 1
        elif self.statecode = 2:
            healthy_number += 1
            recovered_number += 1
            sick_number -= 1
        elif self.statecode = 3:
            healthy_number -= 1
            sick_number -= 1
            population -= 1
            death_number += 1

        return healthy_number, sick_number, death_number, recovered_number

    def check_total_number(healthy_number, sick_number, death_number):
        '''
        ppl == healthy_number + sick_number + death number
        population == healthy_number + sick number
        recovered_number should be smaller than 
        '''

        if healthy_number + sick_number + death_number == ppl:
            return True
            if healthy_number + sick number == population:
                return True
        return False
        # 此处加入自动避错code


class covid19():

    broad_rate = 2.5  # possibility for you to get the virus from being in contact with a person w/out protection
    action_latency = random.randint(3, 5)
    # latency between a person get infected and shows sympton
    disease_latency = random.randint(3, 14)

    def __init__(self, aaa):
        self.aaa = aaa  # 先挂着，到时候改

    def develop_without_preventation(self, a, b, c):

        t_0 = 1  # day 1, day of boarding
        r_0 = 0.35  # growth rate without preventation

        firstcase_day = random.randint(1, 14)
        t = firstcase_day + action_latency  # day when initial action is taken

        N_without_preventation = 0_numbers * exp(r_0 * (t - t_0))
        if N_without_preventation > 2500:
            return False
        return True

        if

class report():
    # To get the numbers of healthy, sick, recovered, and dead conditions in a certain day
    def __init__(self, day):
        self.day = day

    # 日情况

    # 总情况
    

if __name__ == "__main__":

    sth = readfile('Easy.bff')
    print(sth)
