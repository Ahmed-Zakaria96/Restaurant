from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default="Customer")
    role = db.relationship('Role', backref=db.backref('role', lazy='dynamic'))

    def __repr__(self):
        return f"{self.username}"
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"{self.name}"

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.title}"
    

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('owner', lazy='dynamic'))
    title = db.Column(db.String(50))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    series = db.relationship('Series', backref=db.backref('series', lazy='dynamic'))

    def __repr__(self):
        return f"{self.title}"
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant', lazy='dynamic'))

    def __repr__(self):
        return f"{self.restaurant}"

class MenuItem(db.Model):
    __tablename__ = "menuitem"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    menu = db.relationship('Menu', backref=db.backref('menuitem', lazy='dynamic'))

    def __repr__(self):
        return f"{self.name}: {self.price}$"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy='dynamic'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deliver_status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.id}"
    
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'status': self.deliver_status
        }

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'), nullable=False)
    item = db.relationship('MenuItem', backref=db.backref('item', lazy='dynamic'))
    amount = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('order', lazy='dynamic'))




