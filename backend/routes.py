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
            profs = db.session.query(Professional).all()
            custs = db.session.query(Customer).all()
            return render_template("admin/dashboard.html" , allcats= allcats , profs=profs , custs=custs)
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
    if request.method =="GET" and request.args.get("action") == "edit":
        all_cats = db.session.query(ServiceCategory).all()
        id  = request.args.get("id")
        prof = db.session.query(Professional).filter_by(id = id).first()

        return render_template("/professional/add.html" , all_cats = all_cats , prof=prof)
    elif request.method=="POST" and request.args.get("action") =="create":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        category_id = request.form.get("servicecat")
        experience = request.form.get("exp")
        print(name)
        print(email)
        print(password)
        print(phone)
        print(category_id)
        print(experience)
        if not name or not email or not password or not phone or not category_id or not experience :
            return "All fields are required" , 400
        prof = db.session.query(Professional).filter_by(email=email).first()
        if prof:
            return "Email already registered" , 409
        else:
            new_prof = Professional(name=name , email=email , password=password , phone=phone ,status="Active" , servicecategoryid=category_id , experience = experience )
            db.session.add(new_prof)
            db.session.commit()
            return redirect("/admin/dashboard")
    elif request.method=="POST" and request.args.get("action") =="edit":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        category_id = request.form.get("servicecat")
        experience = request.form.get("exp")
        id = request.args.get("id")
        prof = db.session.query(Professional).filter(Professional.email==email , Professional.id != id).first()
        if prof:
            return "Email already registered" , 409
        else:
            prof = db.session.query(Professional).filter_by(id = id).first()
            if name:
                prof.name = name
            if email : 
                prof.email = email
            if password :
                prof.password = password
            if experience:
                prof.experience = experience
            if phone:
                prof.phone = phone
            if category_id:
                prof.servicecategoryid = category_id

            db.session.commit()
            return redirect("/admin/dashboard") 
    elif request.method=="POST" and request.args.get("action") =="delete":
        id = request.args.get("id")
        prof = db.session.query(Professional).filter_by(id=id).first()
        db.session.delete(prof)
        db.session.commit()
        return redirect("/admin/dashboard")
    elif request.method=="POST" and request.args.get("action") =="flag":
        id = request.args.get("id")
        prof = db.session.query(Professional).filter_by(id=id).first()
        prof.status="Flagged"
        db.session.commit()
        return redirect("/admin/dashboard")
    elif request.method=="POST" and request.args.get("action") =="unflag":
        id = request.args.get("id")
        prof = db.session.query(Professional).filter_by(id=id).first()
        prof.status="Active"
        db.session.commit()
        return redirect("/admin/dashboard")
    

@app.route("/managecustomer" , methods=["GET" ,"POST"])  
def managecustomer():
    if request.method=="POST" and request.args.get("action") =="flag":
        id = request.args.get("id")
        cust = db.session.query(Customer).filter_by(id=id).first()
        cust.status="Flagged"
        db.session.commit()
        return redirect("/admin/dashboard")
    elif request.method=="POST" and request.args.get("action") =="unflag":
        id = request.args.get("id")
        cust = db.session.query(Customer).filter_by(id=id).first()
        cust.status="Active"
        db.session.commit()
        return redirect("/admin/dashboard")



