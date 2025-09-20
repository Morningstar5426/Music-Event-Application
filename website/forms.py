from wtforms import TextAreaField, SubmitField, HiddenField, DateField
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed, DataRequired



ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}
#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    contact_no = IntegerField("Phone Number", validators=[InputRequired()])
    address = TextAreaField(u'Mailing Address', validators = [InputRequired()])
    
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")
    
# Form for creating an event within the database   
class EventForm(FlaskForm):
  name = StringField('Event Title', validators=[InputRequired()])
  image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  genre = SelectField('Genre', choices=[
    ('Rock', 'Rock'),
    ('Pop', 'Pop'),
    ('Hip-Hop', 'Hip Hop'),
    ('Country', 'Country'),
    ('Jazz', 'Jazz'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical')], validators=[DataRequired()])
  artist = TextAreaField('Artist/Group', validators=[InputRequired()])
  description = TextAreaField('Description', validators=[InputRequired()])
  date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
  start_time = TextAreaField('Start Time', validators=[InputRequired()])
  end_time = TextAreaField('End Time', validators=[InputRequired()])
  location = TextAreaField('Location', validators=[InputRequired()])
  attendees = TextAreaField('Number of Attendees', validators=[InputRequired()])
  tickets = SelectMultipleField('Ticket Types', choices=[('Standard', 'Standard'), ('VIP', 'VIP'), ('VIP+', 'VIP+')], validators=[DataRequired()])
                              
  status = SelectField('Event Status', choices=[('Open', 'Open'), ('Inactive', 'Inactive'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
  submit = SubmitField("Create")
  
      
#Form for booking an event
class BookingForm(FlaskForm):
    ticket_type = SelectField('Ticket Type', choices=[('standard', 'Standard'), ('vip', 'VIP'), ('vip+', 'VIP+')])
    number_of_tickets = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1)])
    event_image = HiddenField()
    event_name = HiddenField()
    submit = SubmitField('Book Now')
 
#Form for commenting on an event   
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  timestamp = HiddenField()
  submit = SubmitField('Submit')