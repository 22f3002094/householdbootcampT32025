from .models import db, Admin,Customer ,ServiceCategory, Professional, ProfessionalAvailability, Booking
from flask import current_app as app
from datetime import date,time

with app.app_context():
    db.create_all()


    if db.session.query(Admin).count() == 0:
        admin = Admin(email = "admin@gmail.com" , password = "pass")
        db.session.add(admin)
        db.session.commit()
    if db.session.query(Customer).count() == 0:
        customer = Customer(name="Himanshu", email="h@gmail.com" , password = "pass" , phone = "9999999999" , address = "IITM chennai")
        db.session.add(customer)
        db.session.commit()
    
    if db.session.query(ServiceCategory).count() == 0:
        categories = [
            ServiceCategory(name="Plumbing", description="All plumbing related services"),
            ServiceCategory(name="Electrical", description="All electrical related services"),
            ServiceCategory(name="Cleaning", description="All cleaning related services"),
            ServiceCategory(name="Carpentry", description="All carpentry related services"),
        ]
        db.session.add_all(categories)
        db.session.commit()
    if db.session.query(Professional).count() == 0:
        professionals = [
            Professional(name="P1", servicecategoryid=1, email="p1@gmail.com", password="pass", phone="8888888888", experience=5),
            Professional(name="P2", servicecategoryid=1, email="p2@gmail.com" , password="pass", phone="7777777777", experience=3),
            Professional(name="P3", servicecategoryid=2, email="p3@gmail.com", password="pass", phone="8888888888", experience=5),
            Professional(name="P4", servicecategoryid=4, email="p4@gmail.com" , password="pass", phone="7777777777", experience=3),
        ]
        db.session.add_all(professionals)
        db.session.commit()
    if db.session.query(ProfessionalAvailability).count() == 0:
        availabilities = [
            ProfessionalAvailability(professionalid=1, available_date=date(2025,11,12), start_time=time(9,0), end_time=time(10,0) , status="available"),
            ProfessionalAvailability(professionalid=1, available_date=date(2025,11,13), start_time=time(10,0), end_time=time(11,0) , status="booked"),
        ]
        db.session.add_all(availabilities)
        db.session.commit()
    if db.session.query(Booking).count() == 0:
        bookings = [
            Booking(customerid=1, professionalid=1, servicecategoryid=1, booking_date=date(2025,11,13), start_time=time(10,0), end_time=time(11,0), status="booked", slot_id=2),
        ]
        db.session.add_all(bookings)
        db.session.commit()