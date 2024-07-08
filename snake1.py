import time
import os

def wingup():
    print("X    X")
    print(" X  X")
    print("  O")
    time.sleep(0.9)
    os.system('cls')


def wingdown():
    print("  O")
    print(" X  X")
    print("X    X")
    time.sleep(0.9)
    os.system('cls')


while (True):
    wingup()
    wingdown()

