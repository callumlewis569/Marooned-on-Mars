#Upgrades Files used to define the upgrade pathways
from achievements import *

cost_drillbits = [
    "10",
    "20",
    "10",
    "20",
    "30",
    "10",
    "20",
    "30"
]
cost_batteries = [
    "10",
    "10",
    "10"
]
cost_oxygentanks = [
    "10",
    "10",
    "10"
]

class Upgrades():

    def __init__(self):
        pass

    def upgrade_drillbit():
        temp_up_1 = 0
        for i in achievement_drillbits:
            if (not achievement_drillbits[i]):
                if (temp_up_1 < 2):
                    cost = cost_drillbits[i] + " Rustalon"
                    return (cost, temp_up_1, int (cost_drillbits[i]))
                elif (temp_up_1 < 5):
                    cost = cost_drillbits[i] + " Hexacron"
                    return (cost, temp_up_1, int (cost_drillbits[i]))
                else:
                    cost = cost_drillbits[i] + " Xerocite"
                    return (cost, temp_up_1, int (cost_drillbits[i]))
            else:
                temp_up_1 += 1

    def upgrade_batteries():
        temp_up_2 = 0
        for i in achievement_batteries:
            if (not achievement_batteries[i]):
                if (temp_up_2 == 0):
                    cost = cost_batteries[i] + " Rustalon" + " and " + cost_batteries[i] + " Combustite"
                    return (cost, temp_up_2, int (cost_batteries[i]))
                elif (temp_up_2 == 1):
                    cost = cost_batteries[i] + " Hexacron" + " and " + cost_batteries[i] + " Ionflux"
                    return (cost, temp_up_2, int (cost_batteries[i]))
                else:
                    cost = cost_batteries[i] + " Xerocite" + " and " + cost_batteries[i] + " Void Ether"
                    return (cost, temp_up_2, int (cost_batteries[i]))
            else:
                temp_up_2 += 1

    def upgrade_oxygentanks():
        temp_up_3 = 0
        for i in achievement_oxygentanks:
            if (not achievement_oxygentanks[i]):
                if (temp_up_3 == 0):
                    cost = cost_oxygentanks[i] + " Rustalon" + " and " + cost_oxygentanks[i] + " Nytrazene"
                    return (cost, temp_up_3, int (cost_oxygentanks[i]))
                elif (temp_up_3 == 1):
                    cost = cost_oxygentanks[i] + " Hexacron" + " and " + cost_oxygentanks[i] + " Tatonium"
                    return (cost, temp_up_3, int (cost_oxygentanks[i]))
                else:
                    cost = cost_oxygentanks[i] + " Xerocite" + " and " + cost_oxygentanks[i] + " Aetherium-94"
                    return (cost, temp_up_3, int (cost_oxygentanks[i]))
            else:
                temp_up_3 += 1
            



