from multiprocessing import Semaphore
from colorama import Fore, Back

from smokers_model import SmokerModel, SmokerStatus
from provider_model import ProviderModel
from ingredient_types import IngredientTypes


class Controller():
    def __init__(self):
        self.ingredient_semaphores: list[Semaphore] = \
            self.__create_ingredient_semaphores()

        self.production_semaphore: Semaphore = Semaphore(1)

        self.smokers: list[SmokerModel] = self.__create_smokers()

        self.provider: ProviderModel = ProviderModel(
            self.production_semaphore, self.ingredient_semaphores, provider_callback)

    def __create_smokers(self) -> list():
        smokers: list[SmokerModel] = []

        for ingredient_type in IngredientTypes:
            smokers.append(
                SmokerModel(
                    ingredient_type,
                    self.production_semaphore,
                    self.ingredient_semaphores,
                    smoker_callback))

        return smokers

    def __create_ingredient_semaphores(self) -> list():
        ingredients = []

        for ingredient_type in IngredientTypes:
            # Los ingredientes se crean "vacios"
            # por lo que no podrán ser adquiridos
            # por los consumidores
            ingredients.append(Semaphore(0))

        return ingredients

    def __start_smokers(self):
        print("*** Starting smokers ***")
        for smoker in self.smokers:
            smoker.start()

    def start(self):
        print(Fore.YELLOW + "*** Controller starting ***")

        self.__start_smokers()

        print(Fore.YELLOW + "*** Starting provider ***")
        self.provider.start()


def smoker_callback(smoker: SmokerModel):
    if smoker.status == SmokerStatus.SMOKING:
        print(Fore.LIGHTGREEN_EX, end="")
    elif (smoker.status == SmokerStatus.RUNNING) or (smoker.status == SmokerStatus.CREATED):
        print(Fore.WHITE, end="")
    else:
        print(Fore.LIGHTRED_EX, end="")

    print("-", smoker, Fore.RESET)


def provider_callback(ingredient_type: IngredientTypes):
    print(Fore.BLUE + "+ Produced: " + ingredient_type.name)


def main():
    print(Fore.YELLOW + "*** Starting simulation ***")

    controller = Controller()
    controller.start()

    print(Fore.YELLOW + "*** Done simulation ***")


if __name__ == '__main__':
    main()

