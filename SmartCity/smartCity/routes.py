# ---------------------------------------------------------
#
# Page for the milano contest by Iasmina Martinovici, Alex Tanase and Gruescu Daniel
# Designer : Iasmina Martinovici
# FrontEnd developer : Alex Tanase
# BackEnd developer : Gruescu Daniel
#
# ---------------------------------------------------------


#Imports
import os
from flask import render_template, url_for, flash, redirect, request, jsonify
from smartCity import app, db, bcrypt
from smartCity.forms import RegistrationForm, LoginForm, AccountForm, PostForm, thirdPartyForm
from smartCity.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required, mixins
from smartCity.textDetection import getTextFromImage
from smartCity.barcodeDetection import readBarcode
app.config["IMAGE_UPLOADS"] = "smartCity/static/img/uploads"

#The routes for the home page
@app.route("/")
@app.route("/home")
def home():
    if not(current_user.is_anonymous):
        return render_template('home.html', posts=posts, level = current_user.level)
    else:
        return render_template('home.html', posts=posts, level = 'not user')


#The route for the about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')



#The route for the register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,experience=0, level=0, email=form.email.data, password=hashed_password, cart="Empty", ItemsInCart = 0)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



#The route for the login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#The logout function
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#The route to modify an account
@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.username.data != '':
            editUser = User.query.filter_by(username=current_user.username).first()
            editUser.username = form.username.data
            db.session.commit()
        if form.email.data != '':
            editUser = User.query.filter_by(email=current_user.email).first()
            editUser.email = form.email.data
            db.session.commit()
        if form.password.data != '':
            editUser = User.query.filter_by(password=current_user.password).first()
            editUser.password = hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
    return render_template('account.html', title='Account', form = form)

#The route for the option page
@app.route('/actions')
@login_required
def actions():
    return render_template('actions.html')

#The route for the image recognition
@app.route('/image', methods=['GET', 'POST'])
def image():
    imageData = ''
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            imageData = getTextFromImage(app.config['IMAGE_UPLOADS'] + '/' + image.filename)
            print(imageData)
            for item in ecoItems:
                if item in imageData:
                    score += 1

            if score > 0:

                print(imageData.index('\n'))
                return render_template('imageUpload.html', text = "Ai apa")

            else:
                return render_template('imageUpload.html', text = 'Nu ai apa')
    return render_template('imageUpload.html', text = imageData)

#The route for the barcode recognition
@app.route('/transportImage', methods=['GET', 'POST'])
def transport():
    imageData = ''
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            imageData = readBarcode(app.config['IMAGE_UPLOADS'] + '/' + image.filename)
            return render_template('transportFinder.html', text = imageData)
    return render_template('transportFinder.html', text = imageData)


@app.route('/thirdPartyPanel', methods=['GET', 'POST'])
def thirdParty():
    form = thirdPartyForm();
    if form.validate_on_submit:
        if request.method == 'POST':
            editUser = User.query.filter_by(username=form.username.data).first()
            if editUser is not None:
                editUser.giveExp(form.expGiven.data)
            else:
                print("User not found")

    return render_template('post.html',form=form) #Need to add page
