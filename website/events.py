from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User, Booking
from .forms import EventForm, CommentForm
from .forms import BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime
#additional import:
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix='/events')


@destbp.route('/my_bookings', methods=['GET'])
@login_required  # This will ensure that only authenticated users can access this page.
def my_bookings():
    # Fetch bookings from the database for the current user.
    # Assuming 'Booking' has a 'user_id' field that references the 'User' table's 'id' field.
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=user_bookings)

#I tried using a seperate route for ticket booking and kept breaking if someone else can try 

@destbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = CommentForm()
    booking_form = BookingForm()

    if booking_form.validate_on_submit():
        if not current_user.is_authenticated:  # Check if user is logged in
            # If the user is not authenticated, redirect them to the login page with a message
            flash('You need to be logged in to make a booking.', 'info')
            return redirect(url_for('auth.login'))  

        # Prices based on ticket type just for example in db
        ticket_prices = {
            'standard': 10.0,
            'vip': 20.0,
            'vip+': 30.0,
        }

        # Get the price for the selected ticket type
        price_per_ticket = ticket_prices.get(booking_form.ticket_type.data, 0)

        # Create a new Booking instance
        new_booking = Booking(
            name=current_user.name,  # Logged-in user's name
            number_of_tickets=booking_form.number_of_tickets.data,
            price_per_ticket=price_per_ticket,
            user_id = current_user.id,
            event_id=event.id  # This assumes event.id is valid and not None
        )

        # Add and commit the new booking to the database
        db.session.add(new_booking)
        db.session.commit()

        # Flash a success message
        flash('Booking successful!')
        
        
  

    # Render the same view for GET requests and failed POST validations
    return render_template('events/show.html', event=event, form=form, booking_form=booking_form)




@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
      
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
                  image=db_file_path, date=form.date.data, location=form.location.data, artist=form.artist.data,
                  start_time=form.start_time.data, end_time=form.end_time.data, genre=form.genre.data,
                  attendees=form.attendees.data, tickets=', '.join(form.tickets.data), status=form.status.data, owner_id=current_user.id)
    
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new music event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)





@destbp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get(id)
    #If the user is not the creator of the event, they are unable to edit it
    if event.owner_id != current_user.id:
        flash('You are not permitted to update the details of this event', 'failure')
        return redirect(url_for('event.show', id=id))
    
    form = EventForm(obj=event)

    #Updates the event databse
    if form.validate_on_submit():
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path
        event.name = form.name.data
        event.genre = form.genre.data
        event.description = form.description.data
        event.artist = form.artist.data
        event.date = datetime.combine(form.date.data, datetime.min.time()) if form.date.data else None
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        event.attendees = form.attendees.data
        event.tickets = ', '.join(form.tickets.data)
        event.status = form.status.data
        
        # Debugging output
        print("Form Status:", form.status.data)
        print("Event Status (before commit):", event.status)
        
        db.session.commit()
        flash('Event details have been updated', 'success')
        return redirect(url_for('event.show', id=id))

    return render_template('events/update.html', form=form, event=event)


      
    

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id): #Creates commments and saves them to the databse
    form = CommentForm()
    booking_form = BookingForm()
    
    form.timestamp.data = datetime.utcnow()
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('event.show', id=id, booking_form = booking_form))

        comment = Comment(text=form.text.data, event=event, user=user, timestamp=form.timestamp.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
        
    return redirect(url_for('event.show', id=id))

