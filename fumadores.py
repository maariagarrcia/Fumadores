from multiprocessing import Process, Lock
import random
from enum import Enum

class ProviderModel(Process):
    def __init__(self):
        super(ProviderModel, self).__init__()

    def run(self):
        pass

class SmokerStatus(Enum):
    WAITING_FOR_PAPER = 0
    WAITING_FOR_TOBACCO = 1
    WAITING_FOR_MATCHES = 2
    WAITING_FOR_GREEN= 3
    WAITING_FOR_FILTER = 4
    SMOKING = 5

class Ingredient(Enum):
    PAPER = 0
    TOBACCO = 1
    MATCHES = 2
    GREEN = 3
    FILTER = 4

class SmokerModel(Process):
    def __init__(self, ingredient:Ingredient):
        super(SmokerModel, self).__init__()

        self.my_ingredient:Ingredient = ingredient

    def run(self):
        while True:
            #  conseguir los ingredientes

            # si se consiguen todos los ingredientes
            pass

class Controller():
    def __init__(self):
        pass

    def start(self):
        pass

def smoker_callback():
    pass

def provider_callback():
    pass


def main():
    controller = Controller()
    controller.start()

if __name__ == '__main__':
    main()