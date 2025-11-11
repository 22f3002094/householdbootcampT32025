from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    def get_id(self):
        return self.email

class ServiceCategory(db.Model , UserMixin):
    __tablename__ = 'service_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    professionals  = db.relationship("Professional", backref="service_category" , cascade="all, delete-orphan" )
    bookings = db.relationship("Booking" , backref="service_category" , cascade="all, delete-orphan")

class Professional(db.Model,UserMixin):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    servicecategoryid = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer,nullable=True)
    recived_bookings = db.relationship("Booking", backref="professional" ,cascade="all, delete-orphan" )
    availabilities = db.relationship("ProfessionalAvailability", backref="professional" , cascade="all, delete-orphan" )
    def get_id(self):
        return self.email

class Customer(db.Model ,UserMixin):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    status=db.Column(db.String)
    sent_bookings = db.relationship("Booking", backref="customer")
    def get_id(self):
        return self.email

    
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professionalid = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    servicecategoryid = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    slot_id = db.Column(db.Integer, db.ForeignKey('professional_availability.id'), nullable=True)

class ProfessionalAvailability(db.Model):
    __tablename__ = 'professional_availability'
    id = db.Column(db.Integer, primary_key=True)
    professionalid = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, nullable=False)