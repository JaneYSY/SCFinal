class Parameters:
    complete = False
    cruise_width = 1100
    cruise_height = 800
    cruise_centerx = 550
    cruise_centery = 400
    initial_infected = 5
    trans_prob = 0.8
    incubation_period = 140
    # Time to move a patient to the isolation room
    receive_time = 10
    iso_room_size = 100
    iso_room_with = 0
    safe_distance = 2
    # Average flow intention of people (dependent of public alert) [-3,3]
    flow_intention = 3
    population = 5000
    fatal_rate = 0.02
    death_time = 30
    # Variance of the death time.
    death_time_var = 30
    current_time = 1
