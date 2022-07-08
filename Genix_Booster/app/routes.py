import os
from app import app,db
from datetime import timedelta
from flask import render_template, request, flash,url_for,redirect,session,make_response,send_from_directory
from app.models import User,Product,Watch,Group
from app.stock_function import is_valid_email, check_login
import hashlib
from werkzeug.utils import secure_filename
from config import Config



@app.route('/whatsapp_group_list')
def indexes():
    group= Group.query.all()
    return render_template('grouplist.html',groups=group)

@app.route('/whatsapp_phone_list')
def userindexes():
    watch= Watch.query.all()
    return render_template('phonelist.html',watchs=watch)

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')




@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password']
        print("Submitted email is", email)
        print("Submitted password is", password)
        if email == "":
            flash("Invalid Email")
        elif password == "":
            flash("Invalid Password")
        if email == '' or password == '':
            return render_template("login.html")
        else:
            # hash submitted password
            password_hash = hashlib.sha256(password.encode())
            hashed = password_hash.hexdigest()
            user = User.query.filter(User.email== email)
            user = User.query.filter((User.email == email)&(User.password==hashed)).first()
            if user is None:
                flash("Invalid Email or Password")
                return redirect(url_for("login_page"))
            # set sessions
            session['email']= email
            session['name']= user.name
            session['hashed'] = hashed
            #set cookies
            resp = redirect(url_for("list_numbers"))
            resp.set_cookie('UserEmail',email,max_age=timedelta(hours=24))
            resp.set_cookie('Hashed',hashed,max_age=timedelta(hours=24))
            resp.set_cookie('name',user.name,max_age=timedelta(hours=24))
            return resp

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['number']
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print("Submitted email is", email)
        print('Submitted name is', name)
        print("submitted phone number is", phone)
        print('submitted gender is', gender)
        print("Submitted password is", password)
        validated = False
        if email == '' or name == '' or password == '' or confirm_password == "":
            flash("All fields are required")
        elif len(password) < 6:
            flash("Password is too short!")
        elif password != confirm_password:
            flash("Password does not match")
        elif len(name) < 3:
            flash("Please enter a valid Name!")
        elif not is_valid_email(email):
            flash('Email is invalid')
        elif len(phone) != 11:
            flash("Invalid Phone Number")
        else:
            validated = True
        if not validated:
            return render_template("signup.html")
        else:
            print("Form submitted")

        # hash submitted password
        password_hash = hashlib.sha256(password.encode())
        hashed = password_hash.hexdigest()
        user = User(name=name, phone=phone,
                    gender=gender, password=hashed, email=email)
        db.session.add(user)
        db.session.commit()
        session['email']= email
        session['name']= user.name
        session['hashed'] = hashed
        return redirect(url_for('list_numbers'))


@app.route("/delete/<wid>")
def delete_product(wid):
    user = check_login
    if not user:
        return redirect(url_for('login_page'))
    watch = Watch.query.filter(Watch.id == wid).first()
    if watch is None:
        flash('Number not found!!')
        return redirect(url_for('list_numbers'))

    db.session.delete(watch)
    db.session.commit()
    flash('Number deleted successfully!')
    return redirect(url_for('list_numbers'))


@app.route("/logout")
def logout():
    #remove sessions
    session['email']= None
    session['name']= None
    session['hashed'] = None
    # remove cookies
    resp = redirect(url_for("login_page"))
    resp.set_cookie('UserEmail','',expires=0)
    resp.set_cookie('Hashed','',expires=0)
    resp.set_cookie('name','',expires=0)
    return resp

@app.route("/deletegroup/<gid>")
def delete_group(gid):
    user = check_login
    if not user:
        return redirect(url_for('login_page'))
    group = Group.query.filter(Group.id == gid).first()
    if group is None:
        flash('Group not found!!')
        return redirect(url_for('list_groups'))

    db.session.delete(group)
    db.session.commit()
    flash('Group deleted successfully!')
    return redirect(url_for('list_groups'))

@app.route("/phonelist", methods=['POST', 'GET'])
def list_numbers():
    check_login()
    user = check_login()
    watch= Watch.query.all()
    return render_template('adminphonelist.html',watchs=watch, user=user)
@app.route("/home",  methods=['POST', 'GET'])
def create_numbers():
    if request.method =="GET":
        return render_template('index.html')
    else:
        title = request.form["name"]
        phone = request.form["phone"]

        validated = False
        if title == '' or phone == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("index.html")
        watch = Watch(name=title ,phone=phone)
        db.session.add(watch)
        db.session.commit()
        return redirect(url_for("userindexes"))

@app.route("/grouplist", methods=['POST', 'GET'])
def list_groups():
    check_login()
    user = check_login()
    group= Group.query.all()
    return render_template('admingrouplist.html',groups=group, user=user)
@app.route("/home2",  methods=['POST', 'GET'])
def create_groups():
    if request.method =="GET":
        return render_template('index.html')
    else:
        title = request.form["name"]
        group = request.form["group"]
        description = request.form["description"]

        validated = False
        if title == '' or group == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("index.html")
        group =Group(name=title ,group=group,description=description)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for("indexes"))

@app.route("/home",  methods=['POST', 'GET'])
def report():
    if request.method =="GET":
        return render_template('index.html')
    else:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        validated = False
        if name == '' or email == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("index.html")
        report = Report(name=name ,email=email,subject=subject,message=message)
        db.session.add(report)
        db.session.commit()
        return redirect(url_for("userindexes"))

@app.route("/home",  methods=['POST', 'GET'])
def contact():
    if request.method =="GET":
        return render_template('index.html')
    else:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        validated = False
        if name == '' or email == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("index.html")
        contact = Contact(name=name ,email=email,subject=subject,message=message)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for("userindexes"))
@app.route("/home",  methods=['POST', 'GET'])
def advert():
    if request.method =="GET":
        return render_template('index.html')
    else:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        validated = False
        if name == '' or email == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("index.html")
        advert = Advert(name=name ,email=email,subject=subject,message=message)
        db.session.add(advert)
        db.session.commit()
        return redirect(url_for("userindexes"))





