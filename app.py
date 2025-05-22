import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from send_mail import send_mail
from config import DevelopmentConfig, ProductionConfig  # Import your configs

app = Flask(__name__)

# Use environment variable to select config
ENV = os.environ.get('FLASK_ENV')

if ENV == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# ✅ Initialize SQLAlchemy
db = SQLAlchemy(app)

# ✅ Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define your model
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.String(100), unique=True)        
    customer = db.Column(db.String(200))
    driver = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, ride_id, customer, driver, rating, comments):
        self.ride_id = ride_id
        self.customer = customer
        self.driver = driver
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    print("DB in use:", app.config['SQLALCHEMY_DATABASE_URI'])  # 👈 ADD THIS
    if request.method == 'POST':
        ride_id = request.form['ride_id']        
        customer = request.form['customer']
        driver = request.form['driver']
        rating = request.form['rating']
        comments = request.form['comments']

        if customer == '' or driver == '':
            return render_template('index.html', message='Please enter required fields')

        existing_feedback = Feedback.query.filter_by(customer=customer, ride_id=ride_id).first()
        if not existing_feedback:
            data = Feedback(ride_id, customer, driver, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(ride_id, customer, driver, rating, comments)
            return render_template('success.html')

        return render_template('index.html', message='You have already submitted feedback with the same ride ID')

if __name__ == '__main__':
    app.run()
