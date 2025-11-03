from flask import current_app as app
from flask import render_template, request, redirect
from backend.models import db, Customer

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
        cust = db.session.query(Customer).filter_by(email=email , password=password).first()
        if cust:
            return redirect("/customer/dashboard?cust_id="+str(cust.id))
        else:
            return "Invalid credentials" , 401

@app.route("/customer/dashboard")
def customer_dashboard():
    if request.method=="GET" :
        id = request.args.get("cust_id")
        cust = db.session.query(Customer).filter_by(id=id).first()
        
        return f"welcome {cust.name} to customer dashboard"
    

