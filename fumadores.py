from multiprocessing import Process, Semaphore
from enum import Enum
import  random
from time import sleep


class ProviderModel(Process):
    def __init__(self, production_semaphore: Semaphore, ingredient_semaphores: list[Semaphore]):
        super(ProviderModel, self).__init__()

        self.ingredient_semaphores: list[Semaphore] = ingredient_semaphores
        self.production_semaphore: Semaphore = production_semaphore

    def produce_ingredients(self, ingredient_semaphores: list[Semaphore]):
        # Desbloquear cuatro ingredientes
        rest_of_ingredients: list[Semaphore] = ingredient_semaphores.copy()
        for i in range(0, 5):
            # Ojo hay que evitar repetir
            ingredient_idx = random.randint(0, len(rest_of_ingredients)-1)
            rest_of_ingredients[ingredient_idx].release()
            rest_of_ingredients.pop(ingredient_idx)

    def run(self):
        while True:
            # Esperar tiempo ilimitado a que se desbloquee el semaforo de producion
            # Al desbloquearse producir 4 ingredientes
            self.production_semaphore.acquire(block=True)
            self.produce_ingredients(self.ingredient_semaphores)


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
    def __init__(self, ingredient_type: IngredientTypes,
                 production_semaphore: Semaphore, ingredient_semaphores: list[Semaphore]):

        super(SmokerModel, self).__init__()
        self.production_semaphore = production_semaphore
        self.my_ingredient_type: IngredientTypes = ingredient_type
        self.ingredient_semaphores = ingredient_semaphores
        self.name = self.my_ingredient_type.name
        self.status: SmokerStatus = SmokerStatus.RUNNING

    def run(self):
        while True:
            # Intentar adquirir el semaforo de cada uno de lo ingredientes.
            # Si uno de los semaforos se NO consigue bloquear se hay que
            # liberar todos los adquiridios para prevenir el deadlock
            # (hay otras estrategias pero esta es valida ...).
            ingredients_acquired = [False] * len(IngredientTypes)
            ingredients_acquired[self.my_ingredient_type.value] = True

            # Bucle de bloqueo de ingredientes
            for ingredient_type in IngredientTypes:
                if ingredient_type != self.my_ingredient_type:
                    ingredients_acquired[ingredient_type.value] = \
                        self.ingredient_semaphores[ingredient_type.value].acquire(
                        block=True, timeout=random.random()*3)

                # Caso de no conseguir el bloqueo salimos del bucle de bloqueo
                if not ingredients_acquired[ingredient_type.value]:
                    self.status = SmokerStatus(ingredient_type.value)
                    break  # ====== Salir del bucle de bloqueo de ingredientes ======>

            # Comprobar si todos los semaforos se han adquirido
            if all(ingredients_acquired):
                # Fumar
                self.status = SmokerStatus.SMOKING
                sleep(random.random() * 2)

                # Desbloquear el productor
                self.production_semaphore.release()

            else:
                # Desbloquear los semáforos de productos
                for ingredient_type_value, ingredient_acquired in enumerate(ingredients_acquired):
                    if ingredient_type != self.my_ingredient_type:
                        if ingredient_acquired:
                            self.ingredient_semaphores[ingredient_type_value].release(
                            )

            self.status = SmokerStatus.RUNNING


class Controller():
    def __init__(self):
        self.ingredient_semaphores: list[Semaphore] = \
            self.create_ingredient_semaphores()

        self.production_semaphore: Semaphore = Semaphore(1)

        self.smokers: list[SmokerModel] = self.create_smokers(
            self.production_semaphore, self.ingredient_semaphores)

        self.provider: ProviderModel = ProviderModel(
            self.production_semaphore, self.ingredient_semaphores)

    def create_smokers(self, production_semaphore: Semaphore, ingredient_semaphores: list[Semaphore]) -> list():
        smokers: list[SmokerStatus] = []

        for ingredient_type in IngredientTypes:
            smokers.append(SmokerModel(ingredient_type,
                           production_semaphore, ingredient_semaphores))

        return smokers

    def create_ingredient_semaphores(self) -> list():
        ingredients = []

        for ingredient_type in IngredientTypes:
            ingredients.append(Semaphore(0))

        return ingredients

    def start_smokers(self, smokers: list):
        for smoker in smokers:
            smoker.start()

    def start(self):
        print("Controller starting...")

        self.start_smokers(self.smokers)
        self.provider.start()


def smoker_callback():
    pass


def provider_callback():
    pass


def main():
    print("Starting simulation (main) ...")

    controller = Controller()
    controller.start()

    print("Done simulation (main) ...")


if __name__ == '__main__':
    main()
