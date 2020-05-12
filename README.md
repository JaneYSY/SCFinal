# COVID-19 Simulation

Software Carpentry Final Project
Team: Zhezhi Chen, Shengyu Yao

## Background
We are all stuck at home now due to the horrible COVID-19. 
Cruise ships, due to the nature of being a close, isolated environment with highly concentrated populations of different backgrounds
and active social interaction, become one of the highest places of confirmed cases per capita.

This project demonstrates how COVID-19 (or any contagious disease) spreads in a closed environment, such as a cruise. 
1000 people are placed in the environment. 25 randomly-selected patient zeros are placed at different locations on the floor plan, which is an x-y plot.

We simulate how the disease spreads by showing it on GUI. Factors in disease-transmitting, such as transmission probability, traveling distance, and isolation space, are crucial to prevent further infection and to reduce death. In this simulation, users can "take actions," such as changing more rooms to isolation rooms, restricting moving, and wearing masks, and improve the factors on the Game Control Panel and see if they can control the disease. 

## What does the code do?
The run_main.py file
* Simulates all the movements and stores health conditions of individuals
* Simulates transmission of disease and calculating the using and the need of isolation beds
* Plotting and refreshing the cruise floor map to  demonstrate people at each condition with the changing of time by using different colors
* Receiving, separating, and updating inputs from clients onto the COVID19 Simulation window

The run_controlpanel.py file
* Establishes the Server for client sockets to communicate with
* Send client commands to the server from the Game Control Panel window in order to update the adjustable factors

## How to run?
Download code from GitHub.

Install PyQt5 before running:
```python
pip install PyQt5
```
Run both run_main.py and run_controlpanel.py files by entering
```python
python run_main.py
```
or
```python
python run_controlpanel.py
````
We suggest users to run one of the commands above and build another one in text editor due to the restriction of Anaconda. So both windows can be opened, and the communication can be established. 

Both COVID19 Simulation and Game Control Panel are opened by running the two files above. The Simulation window starts to run simulation spontaneously once opened. Adjust the numbers in boxes and click Update buttons on Game Control Panel window. New numbers will be updated to the Simulation window, and the disease transmission will start to change based on input.

If users want to exit the game when the outbreak has not reached an end, click Exit to close the Simulation window and then close the Control Panel manually.

When the outbreak reaches an end, a message will be sent to signal the game is over.

Note: The Control Panel ADDES new beds to the isolation space instead of changing the bed number directly. Please do good math before adding beds.
