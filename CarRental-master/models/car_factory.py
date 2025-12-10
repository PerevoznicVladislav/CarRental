# models/factories.py
from abc import abstractmethod, ABC

from db_models import Cars


class Factory(ABC):
    @abstractmethod
    def create(self, name, model, year, color, price, gearbox, engine, image_url):
        pass


class CarFactory(Factory):
    def create(self, name, model, year, color, price, gearbox, engine, image_url):
        if not all([name, model, year, color, price, gearbox, engine, image_url]):
            raise ValueError("Incomplete car information. Make sure all attributes are set.")
        new_car = Cars(
            name=name,
            model=model,
            year=year,
            color=color,
            price=price,
            gearbox=gearbox,
            engine=engine,
            image_url=image_url
        )
        # Create and return a new Cars object
        return new_car


