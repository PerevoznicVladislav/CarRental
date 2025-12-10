from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import DatabaseConnector, db
from db_models import User, Cars, Rentals


class DatabaseFacade:
    def __init__(self):
        self.connector = DatabaseConnector()

    def fetch_all_cars(self):
        try:
            cars_query = select(Cars).filter()
            cars = db.session.execute(cars_query).scalars().all()
            return cars
        except SQLAlchemyError as e:
            print("Error fetching cars:", e)
            return []

    def fetch_car_by_id(self, car_id):
        try:
            car = db.session.query(Cars).get(car_id)
            return car
        except SQLAlchemyError as e:
            print("Error fetching car by ID:", e)
            return None

    def fetch_all_available_cars(self):
        try:
            cars_query = select(Cars).filter(Cars.state == 'available')
            cars = db.session.execute(cars_query).scalars().all()
            return cars
        except SQLAlchemyError as e:
            print("Error fetching available cars:", e)
            return []

    def fetch_all_users(self):
        try:
            return db.session.query(User).all()
        except SQLAlchemyError as e:
            print("Error fetching users:", e)
            return []

    def add_user(self, username, email, password, full_name):
        try:
            user = User(username=username, email=email, password=password, full_name=full_name)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            print("Error adding user:", e)
            return None

    def fetch_user_rented_cars(self, user_id):
        try:
            rented_cars = db.session.query(Rentals).filter_by(user_id=user_id).all()
            return rented_cars
        except SQLAlchemyError as e:
            print("Error fetching rented cars for user:", e)
            return []

    def fetch_all_rented_cars(self):
        rented_cars = db.session.query(Rentals).all()
        return rented_cars

    def delete_car(self, car_id):
        car = db.session.query(Cars).get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()

    def delete_rental(self, rental_id):
        rental = db.session.query(Rentals).get(rental_id)
        if rental:
            car_id = rental.car_id

            # Update the status of the car to 'available'
            car = db.session.query(Cars).get(car_id)
            if car:
                car.state = 'available'
                db.session.commit()
            else:
                print(f"Car {car_id} not found")

            # Delete the rental after updating the car state
            db.session.delete(rental)
            db.session.commit()

    def delete_user_by_id(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def fetch_rental_by_id(self, rental_id):
        rental = db.session.query(Rentals).get(rental_id)
        return rental

    def delete_car_by_id(self, car_id):
        try:
            car = db.session.query(Cars).get(car_id)
            if car:
                db.session.delete(car)
                db.session.commit()
        except SQLAlchemyError as e:
            print("Error deleting car by ID:", e)

    def fetch_user_by_id(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            return user
        except SQLAlchemyError as e:
            print("Error fetching user by ID:", e)
            return None


