Software Carpentry Final Project

Group member: Zhezhi Chen, Shengyu Yao

Background:
Currently, everyone in this class is stuck at home due to COVID-19. Johns Hopkins has done a great job of monitoring and predicting the development of this global pandemic. 
Cruise ships, due to the nature of being a close, isolated environment with highly concentrated populations of widespread backgrounds and active social interaction, become one of the highest places of confirmed cases per capita. Additionally, many of us played the game Plague Inc. years ago and never took it seriously. Unfortunately, it has become a real-world tragedy today. Inspired by this game and the unique environment of cruise ships, we designed a prediction of how COVID-19 transmits on a cruise.

Project Description:
In this game, we will create a floor plan of the cruise with connecting rooms and have 2,500 passengers inside. Some of them will be randomly selected for the first infection (Patient 0). Then the spread of the disease will be mathematically modeled and simulated (according to the Susceptible-Infectious-Recovered model for which we will do some literature research), looking at how different actions the player takes, for instance, social distancing, quarantine, or face coverage, would affect the spread of the disease. The player¡¯s final performance will be scored by the outbreak duration as well as the number of total deaths and infected cases. However, once all people onboard are infected, the game is over immediately and 0 as the score will be received.

Possible Input/Output (TBD):
Input: 
¡ñ Patient 0¡¯s background (such as age)
¡ñ The time of confirmation of COVID-19 (Day X)
¡ñ The time of each preventive action is taken (Day X)
¡ñ The number of a particular day (Day X)
Output: 
¡ñ Condition (numbers of cases of infection, death, and recovered) by the input day number
¡ñ All passengers are infected, report the game is over

References:
SingleTon(https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python)
 
