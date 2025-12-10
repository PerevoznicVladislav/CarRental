import os
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor for parallel processing
from datetime import datetime
from flask import Flask, render_template, send_from_directory, redirect, request, url_for, flash, session
from werkzeug.utils import secure_filename
from db import db, DatabaseConnector
from db_models import Cars, User, Rentals
from models.DatabaseFacade import DatabaseFacade
from models.RentalStrategy import StandardPricingStrategy, MonthlyPricingStrategy
from models.Reposotory import UserRepository
from models.car_factory import CarFactory
from models.rental_builder import RentalsBuilder
from models.car_decorator import *
from models.observer import Subject, AdminObserver, UserObserver

# Import statements

# Initialize the Flask app
app = Flask(__name__)

# Define constants
UPLOAD_FOLDER = 'photos'

# Configure the Flask app
app.config['SECRET_KEY'] = 'do later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql@localhost/carrentaldb'
app.config['UPLOADED_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
db.init_app(app)

# Initialize the DatabaseFacade instance
db_facade = DatabaseFacade()

# Register the admin observer

subject = Subject()
subject.register(AdminObserver())
subject.register(UserObserver())

# Initialize the ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

car_factory = CarFactory()

db_connector = DatabaseConnector.get_instance()
db = db_connector.db

@app.route('/')
def main():
    # Fetch all cars using DatabaseFacade
    cars = db_facade.fetch_all_available_cars()
    user_logged_in = 'user_id' in session
    return render_template('home.html', cars=cars, user_logged_in=user_logged_in)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']

        new_user = db_facade.add_user(username, email, password, full_name)

        flash("User registered successfully", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use db.session.query() instead of User.query
        login_user = db.session.query(User).filter_by(username=username, password=password).first()

        if login_user is not None:
            login_user.last_login = datetime.now()  # Update last login time
            db.session.commit()

            # Set user_id in session upon successful login
            session['user_id'] = login_user.id_user

            return redirect(url_for('account'))
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route('/delete-user/<int:id_user>', methods=['GET', 'POST'])
def delete_user(id_user):
    if request.method == 'POST':
        # Check if the user is logged in and is an admin
        if 'user_id' not in session:
            flash("You need to log in to perform this action", "error")
            return redirect(url_for('login'))

        # Call the delete_user method from UserRepository
        if UserRepository.delete_user(id_user):
            flash("User deleted successfully", "success")
        else:
            flash("User not found", "error")

        return redirect(url_for('home'))

    # If the request method is not POST, return a method not allowed error
    return "Method not allowed", 405


@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = db_facade.fetch_user_by_id(user_id)
    user_logged_in = True
    username = user.username
    notifications = subject.notifications

    if user.is_admin:
        all_users = db_facade.fetch_all_users()
        all_rented_cars = db_facade.fetch_all_rented_cars()
        cars = db_facade.fetch_all_cars()

        return render_template('account.html', rented_cars=all_rented_cars, is_admin=user.is_admin,
                               user_logged_in=user_logged_in,
                               all_users=all_users, username=username, cars=cars, notifications=notifications)
    else:
        return render_template('account.html', is_admin=user.is_admin,
                               user_logged_in=user_logged_in, username=username, notifications=notifications)


@app.route('/rented-cars')
def rented_cars():
    if 'user_id' not in session:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = db.session.query(User).get(user_id)
    user_logged_in = True

    if user.is_admin:
        # Fetch all rented cars if user is an admin
        rented_cars = db_facade.fetch_all_rented_cars()
    else:
        # Fetch cars rented by the current user
        rented_cars = db_facade.fetch_user_rented_cars(user_id)

    return render_template('rented_cars.html', rented_cars=rented_cars, user_logged_in=user_logged_in,
                           is_admin=user.is_admin)


@app.route('/delete-rental/<int:rental_id>', methods=['POST'])
def delete_rental(rental_id):
    if request.method == 'POST':
        # Check if the user is logged in or has admin privileges (if applicable)
        if 'user_id' not in session:
            flash("You need to log in to perform this action", "error")
            return redirect(url_for('login'))

        # Fetch the rental by its ID
        rental = db_facade.fetch_rental_by_id(rental_id)

        # Check if the rental exists
        if not rental:
            flash("Rental not found", "error")
            return redirect(url_for('rented_cars'))

        # Delete the rental from the database
        db_facade.delete_rental(rental_id)

        flash("Rental deleted successfully", "success")
        return redirect(url_for('rented_cars'))
    # If the request method is not POST, return a method not allowed error
    return "Method not allowed", 405


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/cars')
def car_list():
    user_logged_in = 'user_id' in session
    user_is_admin = False
    if user_logged_in:
        # Fetch user details from session or database, assuming User model has an attribute is_admin
        user_id = session['user_id']
        user = db_facade.fetch_user_by_id(user_id)
        user_is_admin = user.is_admin if user else False

    # Fetch all cars using DatabaseFacade
    cars = db_facade.fetch_all_available_cars()

    return render_template('car list.html', cars=cars, user_logged_in=user_logged_in, user_is_admin=user_is_admin)


@app.route('/delete-car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    if request.method == 'POST':
        # Check if the user is logged in and is an admin
        if 'user_id' not in session:
            flash("You need to log in to perform this action", "error")
            return redirect(url_for('login'))

        user_id = session['user_id']
        user = db.session.query(User).get(user_id)

        if not user.is_admin:
            flash("You do not have permission to perform this action", "error")
            return redirect(url_for('car_list'))

        # Delete the car from the database
        db_facade.delete_car_by_id(car_id)

        flash("Car deleted successfully", "success")
        return redirect(url_for('car_list'))

    # If the request method is not POST, return a method not allowed error
    return "Method not allowed", 405


@app.route('/add_car')
def add_car():
    user_logged_in = 'user_id' in session
    return render_template('add_car.html', user_logged_in=user_logged_in)


@app.route('/car-details/<int:car_id>')
def car_details(car_id):
    user_logged_in = 'user_id' in session
    car = db_facade.fetch_car_by_id(car_id)
    if car:
        return render_template('car_details.html', car=car, user_logged_in=user_logged_in)
    else:
        return render_template('404.html'), 404


@app.route('/photos/<path:filename>')
def serve_image(filename):
    return send_from_directory('photos', filename)

@app.route('/submit-new-car', methods=['POST'])
def submit_new_car():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        model = request.form.get('model')
        year = request.form.get('year')
        color = request.form.get('color')
        price = request.form.get('price')
        gearbox = request.form.get('gearbox')
        engine = request.form.get('engine')

        # Handle the file upload
        if 'image_url' in request.files:
            photo = request.files['image_url']
            if photo.filename != '':
                filename = secure_filename(photo.filename)
                photo_path = os.path.join('photos', filename)
                photo.save(photo_path)
                image_url = f"photos/{filename}"
            else:
                image_url = None
        else:
            image_url = None

        # Create the car using the factory pattern
        new_car = car_factory.create(name, model, year, color, price, gearbox, engine, image_url)

        # Add the new car to the database
        db.session.add(new_car)
        db.session.commit()

        # subject.notify_observers({"car_model": model})

        # Redirect to the main page or any other appropriate page
        return redirect('/')

    return "Method not allowed", 405

@app.route("/rent/<int:car_id>", methods=['GET', 'POST'])
def rent_car(car_id):
    if 'user_id' not in session:
        flash("You need to log in to rent a car", "error")
        return redirect(url_for('login'))

    # Get the user ID from the session
    user_id = session['user_id']

    user = db.session.get(User, user_id)
    user_fullname = user.full_name

    # Get the car object from the database
    car = db.session.get(Cars, car_id)

    # Check if the car exists
    if not car:
        flash("Car not found", "error")
        return redirect(url_for('main'))

    if request.method == 'POST':
        # Extract form data
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        selected_decorators = request.form.getlist('decorators')  # Assuming decorators are selected as checkboxes

        # Retrieve car model and name from the database
        car_model = car.model
        car_name = car.name
        price_per_day = car.price

        rental_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

        # Determine pricing strategy based on the number of days rented
        if rental_days > 30:
            pricing_strategy = MonthlyPricingStrategy()
        else:
            pricing_strategy = StandardPricingStrategy()

        # Calculate total price using selected pricing strategy
        total_price = pricing_strategy.calculate_rental(rental_days, price_per_day)

        # Apply decorator costs
        decorated_car = car  # Initialize decorated car with the base car
        for decorator_name in selected_decorators:
            if decorator_name == 'ChildSeat':
                decorated_car = ChildSeat(decorated_car)
            elif decorator_name == 'GPS':
                decorated_car = GPS(decorated_car)
            elif decorator_name == 'RoofBag':
                decorated_car = RoofBag(decorated_car)

        # total_price += decorated_car.price()
        # Create a RentalsBuilder instance and set its properties

        builder = RentalsBuilder()
        rental = builder.set_user_id(user_id) \
                        .set_car_id(car_id) \
                        .set_car_model(car_model) \
                        .set_car_name(car_name) \
                        .add_decorations(selected_decorators) \
                        .set_start_date(start_date) \
                        .set_end_date(end_date) \
                        .set_price_per_day(price_per_day) \
                        .set_rental_days(rental_days) \
                        .total_price(total_price) \
                        .build()

        # Save the rental object to the database
        db.session.add(rental)
        car.state = 'rented'
        db.session.commit()

        subject.notify_observers({"car_model": car_model, "user_id": user_id})

        flash("Car rented successfully", "success")
        return redirect(url_for('main'))

    return render_template('rent_car.html', car=car)





if __name__ == '__main__':
    app.run(debug=True)
