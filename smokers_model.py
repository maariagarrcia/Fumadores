from multiprocessing import Process, Semaphore
from enum import Enum
from random import random
from time import sleep

from ingredient_types import *


class SmokerStatus(Enum):
    WAITING_FOR_PAPER = 0
    WAITING_FOR_TOBACCO = 1
    WAITING_FOR_MATCHES = 2
    WAITING_FOR_GREEN = 3
    WAITING_FOR_FILTER = 4
    RUNNING = 5
    CREATED = 6
    SMOKING = 10


class SmokerModel(Process):
    def __init__(self, ingredient_type: IngredientTypes,
                 production_semaphore: Semaphore, ingredient_semaphores: list[Semaphore],
                 callback):

        super(SmokerModel, self).__init__()

        self.production_semaphore: Semaphore = production_semaphore
        self.my_ingredient_type: IngredientTypes = ingredient_type
        self.ingredient_semaphores: list[Semaphore] = ingredient_semaphores
        self.name: str = self.my_ingredient_type.name
        self.callback = callback
        self.__count: int = 0

        self.set_status(SmokerStatus.CREATED)

    def __str__(self) -> str:
        return "Smoker " + self.name + " · " + self.status.name + "  Smoking times: " + str(self.__count)

    def __release_ingredients(self, ingredient_semaphores: list[Semaphore]) -> None:
        # Desbloquear los semáforos de productos
        for s in ingredient_semaphores:
            s.release()

    def run(self):
        self.set_status(SmokerStatus.RUNNING)

        while True:
            # Intentar adquirir el semaforo de cada uno de lo ingredientes.
            # Si uno de los semaforos NO consigue bloquear se hay que
            # liberar todos los adquiridios para prevenir el deadlock.
            #
            # OJO: Error típico.
            # Cuidado con hacer release() de semaforos no adquiridos ya
            # que incremente el contador sin dar error -> es como producir
            # ingredientes pero solo el productor deber producir ingredientes.
            #    ===> SOLO HACER RELEASE DE SEMAFOROS ADQUIRIDOS <===
            #

            # Aquí guardo los semáforos adquiridos
            ingredients_acquired = []

            # Bucle de bloqueo de ingredientes
            for ingredient_type in IngredientTypes:

                # El ingrediente que el fumador posee NO se ha de bloquear
                if ingredient_type != self.my_ingredient_type:

                    if self.ingredient_semaphores[ingredient_type.value].acquire(
                            block=True, timeout=random()):
                        # Bloqueo conseguido
                        ingredients_acquired.append(
                            self.ingredient_semaphores[ingredient_type.value])
                        self.set_status(SmokerStatus(ingredient_type.value))
                    else:
                        # Bloqueo NO conseguido
                        break  # ====== Salir del bucle de bloqueo de ingredientes ======>

            # Comprobar si todos los semaforos se han adquirido
            if len(ingredients_acquired) == 4:
                # Fumar
                self.__count += 1
                self.set_status(SmokerStatus.SMOKING)
                sleep(random())

                # Desbloquear el productor
                self.production_semaphore.release()

            else:
                # Liberar semáforos
                self.__release_ingredients(ingredients_acquired)

            self.set_status(SmokerStatus.RUNNING)

    def set_status(self, new_status: SmokerStatus):
        self.status: SmokerStatus = new_status
        self.callback(self)

