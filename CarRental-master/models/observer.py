from abc import abstractmethod


class Observer:
    @abstractmethod
    def update(self, data):
        pass
    @abstractmethod
    def format_notification(self, data):
        pass


class Subject:
    def __init__(self):
        self._observers = []
        self.notifications = []

    def register(self, observer):
        self._observers.append(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data=None):
        for observer in self._observers:
            observer.update(data)
            self.notifications.append(observer.format_notification(data))


class UserObserver(Observer):
    def update(self, data):
        # Logic to notify regular users about new cars added
        print(f"New car added: {data['car_model']}")

    def format_notification(self, data):
        return f"New car added: {data['car_model']}"


class AdminObserver:
    def update(self, data):
        # Logic to notify admins about car rentals
        print(f"Car rented: {data['car_model']} by user {data['user_id']}")

    def format_notification(self, data):
        return f"Car rented: {data['car_model']} by user {data['user_id']}"
