from multiprocessing import Process, Lock
from enum import Enum
import random
from time import sleep
from colorama import Fore

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
    CREATED = 5

    SMOKING = 10

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
        self.status:SmokerStatus = SmokerStatus.CREATED

    def run(self):
        while True:
            #  conseguir los ingredientes
            for ingredient in Ingredient:
                if ingredient != self.my_ingredient:
                    pass

            # si se consiguen todos los ingredientes ---> fumar
            sleep(random.random()*2) # tiempo de simulacion

class Controller():
    def __init__(self):
        self.smokers:list = self.create_smokers()

    def create_smokers(self):       
        smokers=[]
        for ingredient in Ingredient:
            smokers.append(SmokerModel(ingredient))
        return smokers

    def start_smokers(self, smokers:list):
        for smoker in smokers:
            smoker.start()

    def start(self):
        self.start_smokers(self.smokers)

def smoker_callback():
    pass

def provider_callback():
    pass


def main():
    controller = Controller()
    controller.start()

if __name__ == '__main__':
    main()