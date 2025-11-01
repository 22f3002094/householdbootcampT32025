from flask import current_app as app



@app.route("/")
def home():
    return "hello world"



@app.route("/login")
def login():
    return "welcome to login page"