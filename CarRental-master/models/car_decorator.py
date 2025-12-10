from abc import abstractmethod, ABC

from models import Car


class CarDecorator(Car, ABC):
    def __init__(self, car):
        self.car = car

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def price(self):
        pass


class ChildSeat(CarDecorator):
    def __init__(self, car):
        super().__init__(car)

    def description(self):
        return f"{super().description()}, Children Seat: Yes"

    def price(self):
        return self.car.price() + 20


class GPS(CarDecorator):
    def __init__(self, car):
        super().__init__(car)

    def description(self):
        return f"{super().description()}, GPS: Yes"

    def price(self):
        return self.car.price() + 20


class RoofBag(CarDecorator):
    def __init__(self, car):
        super().__init__(car)

    def description(self):
        return f"{super().description()}, Roof Bag: Yes"

    def price(self):
        return self.car.price() + 30
