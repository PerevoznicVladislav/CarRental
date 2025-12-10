# models/car.py
import copy


class Car:
    def __init__(self):
        self.name = None
        self.model = None
        self.year = None
        self.color = None
        self.price = None
        self.gearbox = None
        self.engine = None
        self.image_url = None

    def clone(self):
        return copy.deepcopy(self)

    # def description(self):
    #    return f"{self.name} {self.model} {self.year} ({self.color})"
