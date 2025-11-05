from flask import current_app as app
from flask import render_template, request, redirect
from backend.models import db, Customer, Admin, Professional
from flask_login import login_user, login_required,current_user
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register" , methods=["GET" , "POST"] )
def register():
    if request.method=="GET" : 
        return render_template("customer/register.html")
    elif request.method=="POST" :
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        phone = request.form.get("phone")
        if not name or not email or not password or not address or not phone :
            return "All fields are required" , 400
        cust = db.session.query(Customer).filter_by(email=email).first()
        if cust:
            return "Email already registered" , 400
        else:
            new_cust = Customer(name=name , email=email , password=password , address=address , phone=phone)
            db.session.add(new_cust)
            db.session.commit()
            return redirect("/login")

@app.route("/login", methods=["GET" , "POST"] )
def login():
    if request.method=="GET" :
        return render_template("login.html")
    elif request.method=="POST" :
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(Customer).filter_by(email=email , password=password).first() or\
                db.session.query(Admin).filter_by(email=email , password=password).first() or \
                db.session.query(Professional).filter_by(email=email , password=password).first()
        if isinstance(user ,Customer):
            login_user(user)
            return redirect("/customer/dashboard")
        elif isinstance(user ,Admin):
            login_user(user)
            return redirect("/admin/dashboard")
        elif isinstance(user ,Professional):
            login_user(user)
            return redirect("/professional/dashboard")
        else:
            return "Invalid credentials" , 401

@app.route("/customer/dashboard")
@login_required
def customer_dashboard():
    if isinstance(current_user , Customer):
        if request.method=="GET" :
            return f"welcome {current_user.name} to customer dashboard"
    else:
        return "Unauthorized" , 403
        


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if isinstance(current_user , Admin):
        if request.method=="GET" :
            return render_template("admin/dashboard.html")
    else:
        return "Unauthorized" , 403
    


@app.route("/professional/dashboard")
@login_required
def professional_dashboard():
    if isinstance(current_user , Professional):
        if request.method=="GET" :

            
            return f"welcome {current_user.name} to Professional dashboard"
    else:
        return "Unauthorized" , 403 
        


@app.route("/createservice")
@login_required
def create_service():
    if isinstance(current_user , Admin):
        if request.method=="GET" :
            return render_template("admin/create_service.html")
    else:
        return "Unauthorized" , 403