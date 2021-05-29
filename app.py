from flask import Flask
from flask import session, url_for, abort, jsonify
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_admin import Admin
from flask_user import roles_required
from flask_user import login_required


import sqlite3

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import requests
import datetime

from models import db, Restaurant, User, Series, Order, OrderItems, Menu, MenuItem, Role

from forms import RegistrationForm

from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

# custom admin dashboard access that require admin or restaurant to view or redirect to login

class CustomAdminIndexView(AdminIndexView):
    column_hide_backrefs = False
    def is_accessible(self):
        if 'username' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            if user.role.name == "Admin":
                return True
            elif user.role.name == "Restaurant":
                self.can_create = False
                self.can_edit = False
                self.can_delete = False
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# app setting
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bzxskshktslqpk:c1c6837f0e7dd63078be2faf1119149b46fd37833cd40d53d888c476cf8cfacb@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dat44p1thlebt5'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
admin = Admin(app, template_mode='bootstrap3', index_view=CustomAdminIndexView())

# custom admin model view to control user interaction with dashboard
class SuperView(ModelView):
    can_export = True
    def is_accessible(self):
        if 'username' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            if user.role.name == "Admin":
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return True
            elif user.role.name == "Restaurant":
                self.can_create = False
                self.can_edit = False
                self.can_delete = False
                return True
            return False

# register models to admin and categorieze them
admin.add_view(SuperView(User, db.session, category="Users"))
admin.add_view(SuperView(Role, db.session, category="Users"))

admin.add_view(SuperView(Series, db.session, category="Restaurants"))
admin.add_view(SuperView(Restaurant, db.session, category="Restaurants"))
admin.add_view(ModelView(Menu, db.session, category="Restaurants"))
admin.add_view(ModelView(MenuItem, db.session, category="Restaurants"))
admin.add_view(ModelView(Order, db.session, category="Restaurants"))
admin.add_view(SuperView(OrderItems, db.session, category="Restaurants"))

db.init_app(app)
import click
from flask.cli import with_appcontext

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    
# index route
@app.route("/", methods=["GET"])
def index():
    restaurants = Restaurant.query.all()
    return render_template("layout.html", restaurants=restaurants)

# order route
@app.route('/order', methods=['GET'])
def order():
    restaurants = Restaurant.query.all()
    return render_template('order.html', restaurants=restaurants)

# submit order by api
@app.route('/submit_order', methods=["GET", "POST"])
def submit_order():
    data = request.json
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first().id
    order = Order(user_id=user)
    db.session.add(order)
    db.session.commit()
    for i in data:
        menuitem = MenuItem.query.filter_by(name=i).first().id
        order_item = OrderItems(item_id=menuitem, order_id=order.id)
        db.session.add(order_item)
        db.session.commit()

    return jsonify(order.id)

# get all restaurants api
@app.route("/restaurants", methods=["GET"])
def restaurants():
    restaurants = [r.serialize() for r in Restaurant.query.all()]
    return jsonify(restaurants)

# get restaurant menu api
@app.route("/restaurants/<int:restaurant_id>", methods=["GET"])
def restaurant_detail(restaurant_id):
    menu = Menu.query.filter_by(restaurant_id=restaurant_id).first()
    menuitems = [m.serialize() for m in MenuItem.query.filter_by(menu_id=menu.id)]
    return jsonify(menuitems)

# register using html template
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm(request.form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        name = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        role = request.form.get('user_type')
        role_id = Role.query.filter_by(name=role).first().id

        # check if user name already taken
        user_check = User.query.filter_by(username=name).first()

        if user_check is not None:
            flash("Username already taken")
            return render_template("register.html", form=form)

        # if not taken register (insert into data base)
        else:
            user = User(username=name, password=password, roles_id=role_id)
            db.session.add(user)
            db.session.commit()
            # Remember which user has logged in
            session["user_id"] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))

    # if request method is get
    else:
        return render_template("register.html", form=form)

# login view for redirected users from admin
@app.route("/login", methods=["GET", "POST"])
def login():

    """Log user in"""
    
    # Forget any user_id
    session.clear()
    form = RegistrationForm(request.form)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        role = request.form.get('user_type')

        # Query database for username
        user_check = User.query.filter_by(username=request.form.get('username')).first()

        # Ensure username exists and password is correct
        if user_check is None or not check_password_hash(user_check.password, request.form.get("password")) or not user_check.role.name == role:
            flash('Incorrect Username, Password and/or Role.')
            return render_template("login.html", form=form, error=user_check.role.name)

        # Remember which user has logged in
        session["user_id"] = user_check.id
        session["username"] = user_check.username

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", form=form)

import json

# login for normal user with api
@app.route("/apilogin", methods=["POST"])
def apilogin():
    
    if request.method != "POST":
        return jsonify({"error": "POST request required."}, status=400)
    
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # Ensure username was submitted
    if not username:
        return jsonify(error = "username required.", status=400)

    # Ensure password was submitted
    elif not password:
        return jsonify(error = "password required.", status=400)

    role = 'Customer'

    # Query database for username
    user_check = User.query.filter_by(username=request.form.get('username')).first()

        # Ensure username exists and password is correct
    if user_check is None or not check_password_hash(user_check.password, request.form.get("password")) or not user_check.role.name == role:
        return jsonify(error = "Incorrect Username, Password and/or Role..", status=400)

    # Remember which user has logged in
    session["user_id"] = user_check.id
    session["username"] = user_check.username

    # Redirect user to home page
    return redirect(url_for('index'))


@app.route("/logout", methods=["GET"])
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

