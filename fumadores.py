from multiprocessing import Process, Semaphore
from enum import Enum
import random
from time import sleep
from colorama import Fore


class ProviderModel(Process):
    def __init__(self, ingredient_semaphores: list):
        super(ProviderModel, self).__init__()

        self.ingredient_semaphores: list = ingredient_semaphores
        self.production_semaphore: Semaphore = production_semaphore

    def produce_ingredient(self, ingredient_semaphores: list):
        # desblooquear 4 ingredientea de forma aleatoria
        rest_of_ingredients: list[Semaphore] = ingredient_semaphores.copy()

        for i in range(0, 5):
            ingredient_idx = random.randint(0, len(rest_of_ingredients)-1)
            rest_of_ingredients[ingredient_idx].release()
            ingredient_semaphores.pop(ingredient_idx)

    def run(self):
        while True:
            # esperar tiempo ilimitado a q  se desbloquee el semaforo de produccion
            # al desbloquearse producir 4 ingredientes
            self.production_semaphore.acquire(block=True)
            self.produce_ingredient(self.ingredient_semaphores)


class SmokerStatus(Enum):
    WAITING_FOR_PAPER = 0
    WAITING_FOR_TOBACCO = 1
    WAITING_FOR_MATCHES = 2
    WAITING_FOR_GREEN = 3
    WAITING_FOR_FILTER = 4
    RUNNING = 5

    SMOKING = 10


class IngredientTypes(Enum):
    PAPER = 0
    TOBACCO = 1
    MATCHES = 2
    GREEN = 3
    FILTER = 4


class SmokerModel(Process):
    def __init__(self, Ingredient_type: IngredientTypes, ingredient_semaphores: list):
        super(SmokerModel, self).__init__()

        self.my_ingredient_type: IngredientTypes = IngredientTypes
        self.status: SmokerStatus = SmokerStatus.RUNNING
        self.ingredient_semaphores: list = ingredient_semaphores

    def run(self):
        # intentar   adquirir  el semaforo de cada  uno de los ingredientes
        #  si uno  de los semaforos no se  adquiere hayq  liberar  todos
        # para prevenir el deadlock

        ingredients_acquired = [False] * len(IngredientTypes)
        ingredients_acquired[self.my_ingredient_type] = True

        while True:

            #  conseguir los IngredientTypeses
            for ingredient_type in IngredientTypes:
                if ingredient_type != self.my_ingredient_type:
                    ingredient_acquired[ingredient_type] = self.ingredient_semaphores[ingredient_type].acquire(
                        blocking=True, timeout=random.random())

                # caso de no conseguir el bloqueo salimos del bloque  de bloqueo
                if not ingredient_acquired[ingredient_type]:
                    self.status = SmokerStatus[ingredient_type]
                    break  # =====================>  salir del bloqueo

            # comprobar si todos los semaforos se adquirieron
            if all(ingredient_acquired):
                self.status = SmokerStatus.SMOKING
                sleep(random.random()*2)

            else:
                # desbloquear los semaforos
                for ingredient_type, ingredient_acquired in enumerate(ingredients_acquired):
                    if ingredient_acquired != self.my_ingredient_type:
                        if ingredient_acquired:
                            self.ingredient_semaphores[ingredient_type].release(
                            )

            self.status = SmokerStatus.RUNNING


class Controller():
    def __init__(self):
        self.smokers: list = self.create_smokers()
        self.production_semaphores: Semaphore = Semaphore(1)
        self.ingredient_semaphores: list = self.create_smokers(
            self.ingredient_semaphores)
        self.provider: ProviderModel = ProviderModel(
            self.ingredient_semaphores)

    def create_smokers(self, ingredient_semaphores: list):
        smokers = []
        for ingredient_type in IngredientTypes:
            smokers.append(SmokerModel(ingredient_type))
        return smokers

    def create_ingredients_semaphores(self):
        ingredients = []
        for ingredient_type in IngredientTypes:
            ingredients.append(Semaphore(0))
        return ingredients

    def start_smokers(self, smokers: list):
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
