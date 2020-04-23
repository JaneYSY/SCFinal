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


# class People():
    # define the behavior of people
    
    # total_ppl = 1000 # total no. of people in cruise
    # broad_rate = 0.8 # possibility for you to get the virus from being in contact with a person
    # virus_latency = random.randint(3, 14) # latency between a person get infected and shows sympton
    # first_infection_day = 
    # mask_day = 
    # quarantine_day = 
    # isolation_day =

    # def __init__(self,aaa):
    #   self.aaa = aaa

    # def patient0(age,)


if __name__ == "__main__":

    sth = readfile('Easy.bff')
    print(sth)
