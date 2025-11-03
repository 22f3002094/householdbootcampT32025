from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class ServiceCategory(db.Model):
    __tablename__ = 'service_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    decription = db.Column(db.String, nullable=True)
    professionals  = db.relationship("Professional", backref="service_category")

class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    servicecategoryid = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    recived_bookings = db.relationship("Booking", backref="professional")

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    sent_bookings = db.relationship("Booking", backref="customer")

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professionalid = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    servicecategoryid = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')

