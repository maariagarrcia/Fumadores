from multiprocessing import Process, Lock
import random

class ProviderModel(Process):
    def __init__(self):
        super(ProviderModel, self).__init__()

    def run(self):
        pass

class SmokerModel(Process):
    def __init__(self):
        super(SmokerModel, self).__init__()

    def run(self):
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