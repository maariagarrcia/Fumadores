from multiprocessing import Process, Semaphore
from enum import Enum
import random
from time import sleep
from colorama import Fore

class ProviderModel(Process):
    def __init__(self,ingredient_semaphores:list):
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

class IngredientTypes(Enum):
    PAPER = 0
    TOBACCO = 1
    MATCHES = 2
    GREEN = 3
    FILTER = 4

class SmokerModel(Process):
    def __init__(self, Ingredient_type:IngredientTypes, ingredient_semaphores:list):
        super(SmokerModel, self).__init__()

        self.my_ingredient_type:IngredientTypes = IngredientTypes
        self.status:SmokerStatus = SmokerStatus.CREATED
        self.ingredient_semaphores:list = ingredient_semaphores

    def run(self):
        # comprobar que ingredientes tengo
        ingredients_acquired = [False] * len(IngredientTypes)
        ingredients_acquired[self.my_ingredient_type] = True
        while True:
            #  conseguir los IngredientTypeses
            for ingredient_type in IngredientTypes:
                if ingredient_type != self.my_ingredient_type:
                    ingredients_acquired[ingredient_type]=self.ingredient_semaphores[ingredient_type].acquire(blocking=True, timeout=random.random())

            # si se consiguen todos los IngredientTypeses ---> fumar
            if all(ingredients_acquired):
                self.status= SmokerStatus.SMOKING
                sleep(random.random()*2) # tiempo de simulacion

            for ingredient_type, ingredient_acquired in enumerate(ingredients_acquired):
                if ingredient_acquired:
                    self.ingredient_semaphores[ingredient_type].release()


class Controller():
    def __init__(self):
        self.smokers:list = self.create_smokers()
        self.ingredient_semaphores:list = self.create_smokers(self.ingredient_semaphores)
        self.provider:ProviderModel = ProviderModel(self.ingredient_semaphores)
    def create_smokers(self,ingredient_semaphores:list):       
        smokers=[]
        for ingredient_type in IngredientTypes:
            smokers.append(SmokerModel(ingredient_type))
        return smokers

    def create_ingredients_semaphores(self):       
        ingredients=[]
        for ingredient_type in IngredientTypes:
            ingredients.append(Semaphore(0))
        return ingredients


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