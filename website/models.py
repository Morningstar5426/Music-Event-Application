from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column

#Database table structure for user accounts
class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    contact = db.Column(db.String(100), index=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user') #Creates a relationship with the comment table

    def __repr__(self):
        return f"Name: {self.name}"
    
#Initialises an account
def __init__(self, name, emailid, password_hash, contact, address):
        self.name = name
        self.emailid = emailid
        self.password_hash = password_hash
        self.contact = contact
        self.address = address
        
#Database table structure for creating and updating events      
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    genre = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200))
    artist = db.Column(db.String(80))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(400))
    location = db.Column(db.String(200))
    attendees = db.Column(db.String(10))
    tickets = db.Column(db.String(200))
    status = db.Column(db.String(40), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', foreign_keys=[owner_id])
    comments = db.relationship('Comment', backref='event')
    bookings = db.relationship('Booking', back_populates='event')
    

    def __repr__(self):
        return f"{self.name}"

#Database table structure for comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"
    
#Database structure for booking events
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    price_per_ticket = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event = db.relationship('Event')
    

    def __repr__(self):
        
        return f"<Booking {self.name}, Tickets: {self.number_of_tickets}, Price per Ticket: ${self.price_per_ticket}>"