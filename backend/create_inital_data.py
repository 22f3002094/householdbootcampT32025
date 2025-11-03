from .models import db, Admin,Customer ,ServiceCategory, Professional
from flask import current_app as app

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
            ServiceCategory(name="Plumbing", decription="All plumbing related services"),
            ServiceCategory(name="Electrical", decription="All electrical related services"),
            ServiceCategory(name="Cleaning", decription="All cleaning related services"),
            ServiceCategory(name="Carpentry", decription="All carpentry related services"),
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