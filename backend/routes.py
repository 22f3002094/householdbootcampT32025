from flask import current_app as app
from flask import render_template, request, redirect
from backend.models import db, Customer, Admin, Professional, ServiceCategory , Booking
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
            allcats  = db.session.query(ServiceCategory).all()
            return render_template("admin/dashboard.html" , allcats= allcats)
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
        


@app.route("/manageservice" , methods=["GET" , "POST"] )
@login_required
def manageservice():
    if isinstance(current_user , Admin):
        if request.method=="GET" and request.args.get("action") =="create":
            return render_template("admin/create_service.html")
        elif request.method=="GET" and request.args.get("action") =="edit":
            id = request.args.get("id")
            serobj = db.session.query(ServiceCategory).filter_by(id=id).first()
            return render_template("admin/create_service.html" , serobj  = serobj)
        elif request.method =="POST" and request.args.get("action")=="edit":
            sn = request.form.get("servname")
            sd= request.form.get("servdesc")
            id = request.args.get("id")
            ser = db.session.query(ServiceCategory).filter_by(id = id).first()
            if sn:
                ser.name = sn
            if sd:
                ser.description = sd
            db.session.commit()

            return  redirect("/admin/dashboard")
        
        elif request.method=="POST" and request.args.get("action") =="delete":
            id = request.args.get("id")
            ser = db.session.query(ServiceCategory).filter_by(id = id).first()
            if ser: 
                db.session.delete(ser)
                db.session.commit()
                return  redirect("/admin/dashboard")
            else:
                return "category doesn't exist" 
        elif request.method=="POST" and request.args.get("action") =="create":
            sn = request.form.get("servname")
            sd= request.form.get("servdesc")
            servobj = db.session.query(ServiceCategory).filter_by(name = sn).first()
            if servobj:
                return "Category already exist"
            else : 
                newserv = ServiceCategory(name = sn , description = sd)
                db.session.add(newserv)
                db.session.commit()
                return redirect("/admin/dashboard")
    else:
        return "Unauthorized" , 403
    

@app.route("/manageprofessional" , methods=["GET" ,"POST"]) 
def mangeprofessional():
    if request.method=="GET" and request.args.get("action") =="create":
        all_cats = db.session.query(ServiceCategory).all()
        return render_template("/professional/add.html",all_cats= all_cats)
    elif request.method=="POST" and request.args.get("action") =="create":
        name = request.form.get("cust_name")
        email = request.form.get("cust_email")
        password = request.form.get("cust_password")
        phone = request.form.get("cust_phone")
        category_id = request.form.get("cust_category")
        experience = request.form.get("cust_experience")
        if not name or not email or not password or not phone or not category_id or not experience :
            return "All fields are required" , 400
        prof = db.session.query(Professional).filter_by(email=email).first()
        if prof:
            return "Email already registered" , 409
        else:
            new_prof = Professional(name=name , email=email , password=password , phone=phone , servicecategoryid=category_id )
            db.session.add(new_prof)
            db.session.commit()