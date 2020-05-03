import random
import numpy as np
from scipy.integrate import odeint


class people():
    # define the behavior of people

    n = 2500  # total no. of people in cruise

    def __init__(self, aaa):
        self.aaa = aaa  # 先挂着，到时候改

    def patient_0(self):
        '''
        generate a random age of the patient 0 and tell the player.

        '''
        i_0 = random.randint(1, 10)

        print(i_0, "patient(s) on board are infected by COVID-19.")

        while True:
            msg = input(
                "Please confirm the number of patient 0(s), enter 'NEXT' to continue the game:")

            while msg != "NEXT":
                msg = input(
                    "Wrong input, please enter 'NEXT' to continue the game:")
                if msg != "NEXT":
                    msg = input(
                        "Wrong input, please enter 'NEXT' to continue the game:")

            return i_0

    def person_state(self, statecode):
        '''
        This is to check if the person is healthy, sick, recover, or dead and adjust the population number
        0 is healthy, 1 is sick, 2 is recovered, 3 is death.
        # 我也不知道有没有用 放着看看吧


        '''
        healthy_number = ppl

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

    def __init__(self,):
        self.aaa = aaa  # 先挂着，到时候改

    def deriv(self, t, n, infection_rate = 4, recovery_per_day, incubation_period, days_to_die, death_rate):
        '''
        Number of suspecious, exposed, infected, death, and recovery per time unit dX / dt
        The model and corresponding code referred to https://github.com/hf2000510/infectious_disease_modelling/blob/master/part_two.ipynb 
        and articles https://towardsdatascience.com/infectious-disease-modelling-part-i-understanding-sir-28d60e29fdfc
        and https://towardsdatascience.com/infectious-disease-modelling-beyond-the-basic-sir-model-216369c584c4

        **parameter**
            t: *int*
                time = day #
            n: *int*
                total people on board at the beginning, 2500.
            infection_rate: *float*
                beta. # of ppl ONE infected person infects daily = 4
            recovery_per_day:*float*
                gamma γ. proportion of infected recovering per day (γ = 1/d,
                d - number of days an infected person CAN spread the disease)
            incubation_period:*float*
                delta. Incubation period. Period before infectious, carrier cannot spread the disease
            days_to_die:*int*
                rho. Days take to die.
            death_rate:*float*
                alpha. Possibility to die.

        **output**

        '''
        death_rate = 0.12  # 20% death rate
        days_to_die = 1/14  # 9 days from infection until death
        S0, E0, I0, R0, D0 = N-1, 1, 0, 0, 0  # initial conditions: one exposed
        # 写到这里啊 记得！！！！！！！！！！！！



        
        def infection_rate_opt(self, t):
            '''
            This is do change the infection rate based on action taken.
            '''

            if t < min(day_of_handswash, day_of_masks, day_of_quarantine):
                return infection_rate
            else:
                if t > day_of_handswash:
                    infection_rate *= 0.95
                if t > day_of_masks:
                    infection_rate *= 0.6
                if t > day_of_quarantine:
                    infection_rate *= 0.3
                return infection_rate

        d = 


        dSdt = -infection_rate_opt(t) * S * I / n
        dEdt = infection_rate_opt(t) * S * I / n - incubation_period * E
        dIdt = incubation_period * E - (1 - death_rate) * recovery_per_day * I - death_rate * days_to_die * I
        dRdt = (1 - death_rate) * recovery_per_day * I
        dDdt = death_rate * days_to_die * I

        return dSdt, dEdt, dIdt, dRdt, dDdt





    def develop_without_preventation(self, a, b, c):
        '''
        To predict the development of covid 19 without preventation before people start to take action

        '''

        broad_rate = 2.5  # possibility for you to get the virus from being in contact with a person w/out protection
        action_latency = random.randint(3, 5)
        # latency between a person get infected and shows sympton
        disease_latency = random.randint(3, 14)

        t_0 = 1  # day 1, day of boarding
        r_0 = 0.35  # growth rate without preventation

        firstcase_day = random.randint(1, 14)
        t = firstcase_day + action_latency  # day when initial action is taken

        N_without_preventation = 0_numbers * exp(r_0 * (t - t_0))
        if N_without_preventation > 2500:
            return False
        return True

        if

    def dev_with_preventation(self, a, b, c):


def report():
    # To get the numbers of healthy, sick, recovered, and dead conditions in a certain day

    # 日情况
    def daily_report():

    def total_report():  # 总情况


if __name__ == "__main__":

    sth = readfile('Easy.bff')
    print(sth)
