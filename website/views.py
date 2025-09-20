from flask import Blueprint, render_template, request, url_for, redirect
from .models import Event, Booking
from . import db
from sqlalchemy import or_
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Predefined list of all possible genres
    all_genres = ['Rock', 'Pop', 'Hip-Hop', 'Country', 'Jazz', 'Blues', 'Classical']

    # Get genre query parameter, defaults to None if not provided
    genre_query = request.args.get('genre', None)
    search_query = request.args.get('search', '')

    if genre_query:
        # Filter events by the provided genre
        events = Event.query.filter_by(genre=genre_query).all()
    elif search_query:
        # If there is a search query, filter events based on the search term
        query = "%" + search_query + "%"
        events = db.session.query(Event).filter(
            or_(Event.name.like(query), Event.description.like(query))
        ).all()
    else:
        # Get all events if no genre or search query is provided
        events = Event.query.all()
    
    return render_template('index.html', events=events, genres=all_genres, search_query=search_query)


@main_bp.route('/search')
def search():
    # Redirect to the index with the search term as a query parameter
    return redirect(url_for('main.index', search=request.args.get('search', '')))

    
ROWS_PER_PAGE = 6

@main_bp.route('/my_bookings')
@login_required
def my_bookings():
    page = request.args.get('page', 1, type=int)
    # Modify the query to paginate the bookings.
    paginated_bookings = Booking.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=ROWS_PER_PAGE, error_out=False
    )
    return render_template('my_bookings.html', bookings=paginated_bookings, ROWS_PER_PAGE=ROWS_PER_PAGE)
