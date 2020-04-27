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

    f = open(file)
    line = f.readline()

    while line:
        while line.startswith('first confirmed case'):
            line = line.split()
            firstcase_day = line[1]
            line = f.readline()

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
    return (firstcase_day, mask_day, quarantine_day, isolation_day)


class People():
    # define the behavior of people

    ppl = 2000  # total no. of people in cruise
    crew = 650  # total no. of crews
    broad_rate = 0.8  # possibility for you to get the virus from being in contact with a person w/out protection
    # latency between a person get infected and shows sympton
    virus_latency = random.randint(3, 14)

    def __init__(self, aaa):
        self.aaa = aaa

    def patient_0(self):
        '''
        generate a random age of the patient 0 and tell the player.

        '''
        age = random.randint(0, 85)

        role_list = ['passenger', 'crew']
        role = random.choice(role_list)

        print("The patient 0's age is:", age, role)

        while True:
            msg = input(
                "Please confirm the patient age, enter 'NEXT' to continue the game:")

            if msg == "NEXT":
                return
            else:
                input("Wrong input, please enter 'NEXT' to continue the game:")

        return(age, role)


    def infection(self, age, role):
        
        if role == 'passenger':
            # social interaction rate indicates how many percent of people on the cruise you are in close contact with
            if age < 18:
                social_interaction = 0.2
            elif 18 <= age < 35:
                social_interaction = 0.3
            elif 35 <= age < 65:
                social_interaction = 0.2
            else:
                social_interaction = 0.1

        else:
            social_interaction = 0.5

        


if __name__ == "__main__":

    sth = readfile('Easy.bff')
    print(sth)
