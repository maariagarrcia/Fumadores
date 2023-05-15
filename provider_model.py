from multiprocessing import Process, Semaphore
from random import randint
from colorama import Fore

from ingredient_types import IngredientTypes


class ProviderModel(Process):
    def __init__(self, production_semaphore: Semaphore, ingredient_semaphores: list[Semaphore], callback):
        super(ProviderModel, self).__init__()

        self.ingredient_semaphores: list[Semaphore] = ingredient_semaphores
        self.production_semaphore: Semaphore = production_semaphore
        self.produced_ingredients: list[str] = [None] * 4
        self.callback = callback

    def __str__(self) -> str:
        str: str = Fore.BLUE + "+ PRODUCED INGREDIENTS\n"
        for ingredient in IngredientTypes:
            str += "  " + ingredient.name + " · " + \
                self.ingredient_semaphores[ingredient.value].__str__() + "\n"

        return str

    def produce_new_ingredients(self):
        # Aleatoriamente decidimos cual tiene que quedar bloqueado (contador = 0)
        ingredient_idx_to_let_blocked = randint(0, 4)

        # Hay que liberar cuatro ingredientes de cinco (contador = 1)
        for idx, ingredient in enumerate(self.ingredient_semaphores):
            if idx != ingredient_idx_to_let_blocked:
                # Salvo el ingrediente excluido libreramos el resto
                ingredient.release()
                self.callback(IngredientTypes(idx))

    def run(self):
        while True:

            # Esperar tiempo ilimitado a que se desbloquee el semaforo de producion.
            # (lo desbloquea un fumador cuando consigue fumar)
            self.production_semaphore.acquire(block=True)

            self.produce_new_ingredients()

    def set_status(self):
        # self.callback(self)
        pass

