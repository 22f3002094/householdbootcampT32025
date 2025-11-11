from flask import current_app as app
from flask import render_template, request, redirect
from backend.models import db, Customer, Admin, Professional, ServiceCategory , Booking , ProfessionalAvailability
from flask_login import login_user, login_required,current_user
from datetime import datetime, timedelta
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




@app.route("/customer/dashboard" , methods=["GET" , "POST"] )
@login_required
def customer_bookings():
    if isinstance(current_user , Customer):
        if request.method=="GET" :
            # bookings = db.session.query(Booking).filter_by(customerid=current_user.id).all()
            all_cats = db.session.query(ServiceCategory).all()
            return render_template("customer/dashboard.html" , allcats=all_cats)
    else:
        return "Unauthorized" , 403
    
@app.route("/service/<id>")
@login_required
def view_service(id):
    if isinstance(current_user , Customer):
        if request.method=="GET" :
            service = db.session.query(ServiceCategory).filter_by(id=id).first()
            professionals = db.session.query(Professional).filter_by(servicecategoryid=service.id , status="Active").all()
            return render_template("customer/service.html" , service=service , professionals=professionals)
    else:
        return "Unauthorized" , 403
    


@app.route("/professional/dashboard")
@login_required
def professional_dashboard():
    if isinstance(current_user , Professional):
        if request.method=="GET" :

            
            return render_template("professional/dashboard.html")
    else:
        return "Unauthorized" , 403 
    

@app.route("/admin/search" , methods=["GET" , "POST"] )
def admin_search():
    if request.method=="GET":
        return render_template("admin/search.html")
    elif request.method=="POST":
        query_type = request.form.get("query_type")
        query_term = request.form.get("query_term")   
        if query_type =="service":
            services = db.session.query(ServiceCategory).filter(ServiceCategory.name.ilike(f"%{query_term}%")).all()
            return render_template("/admin/search.html" , services = services , query_type=query_type )
        elif query_type =="professional":
            professionals = db.session.query(Professional).filter(Professional.name.ilike(f"%{query_term}%")).all()
            return render_template("/admin/search.html" , professionals=professionals , query_type=query_type )
        elif query_type =="customer":
            customers = db.session.query(Customer).filter(Customer.name.ilike(f"%{query_term}%")).all()
            return render_template("/admin/search.html" , customers=customers , query_type=query_type )

def get_next_seven_days():
    today = datetime.now().date()
    dates = []
    for i in range(7):
        day = today + timedelta(days=i)
        dates.append(day)
    return dates

def get_fixed_slots():
    slots = [
        ("09:00", "10:00"),
        ("10:00", "11:00"),
        ("11:00", "12:00"),
        ("13:00", "14:00"),
        ("14:00", "15:00"),
        ("15:00", "16:00"),
    ]
    f_slots = []
    for start,end in slots:
        f_slots.append( (datetime.strptime(start , "%H:%M").time() , datetime.strptime(end , "%H:%M").time() ) )
    return f_slots



@app.route("/professional/provideavailability" , methods=["GET" , "POST"] )
@login_required 
def provide_availability(): 
    if isinstance(current_user , Professional):
        if request.method=="GET":
            dates = get_next_seven_days()
            slots = get_fixed_slots()
            all_slots = []
            existing_availabilities = db.session.query(ProfessionalAvailability).filter(ProfessionalAvailability.professionalid==current_user.id , ProfessionalAvailability.available_date>=datetime.today().date()).all()
            print(dates)
            for day in dates:
                days_slots = []
                for start,end in slots:

                    if any(es.available_date==day and es.start_time==start and es.end_time == end and es.status=='booked' for es in existing_availabilities ):
                        days_slots.append({'start_time':start,'end_time':end,'status':'booked'})
                    elif any(es.available_date==day and es.start_time==start and es.end_time == end and es.status=='available' for es in existing_availabilities ):
                        days_slots.append({'start_time':start,'end_time':end,'status':'available'})    
                    else:
                        days_slots.append({'start_time':start,'end_time':end,'status':'not selected'})
                all_slots.append( {"date": day , "slots": days_slots} )
            print(all_slots)
            return render_template("professional/availability.html" , all_slots=all_slots)
        elif request.method=="POST":
            slots_data = request.form.getlist("slots")
            db.session.query(ProfessionalAvailability).filter(ProfessionalAvailability.professionalid==current_user.id , ProfessionalAvailability.available_date>=datetime.today().date() , ProfessionalAvailability.status=="available").delete()
            for slot in slots_data:
                selected_date = datetime.strptime(slot.split("_")[0], "%Y-%m-%d").date()
                start_time = datetime.strptime(slot.split("_")[1], "%H:%M:%S").time()
                end_time = datetime.strptime(slot.split("_")[2], "%H:%M:%S").time()
                new_availability = ProfessionalAvailability(
                    professionalid=current_user.id,
                    available_date=selected_date,
                    start_time=start_time,
                    end_time=end_time,
                    status="available"
                )
                db.session.add(new_availability)
                db.session.commit()
            return redirect("/professional/dashboard")