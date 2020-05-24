#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# Done
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy=True, uselist=False)

    def short(self):
        info ={'id': self.id,
               'name': self.name
               }
        return info

    def details(self):
        info = {'id': self.id,
                'name': self.name,
                'genres': self.genres,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'website': self.website,
                'facebook_link': self.facebook_link,
                }
        return info
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # Done 

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True, uselist=False)

    def short(self):
        info ={'id': self.id, 
               'name': self.name
               }
        return info

    def details(self):
        info ={'id': self.id,
               'name': self.name,
               'genres': self.genres,
               'city': self.city,
               'state': self.state,
               'phone': self.phone,
               'website': self.website,
               'facebook_link': self.facebook_link,
               }
        return info
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # Done
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#D Done 

class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
                          'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def detail(self):
        info = {'venue_id': self.venue_id,
                'venue_name': self.Venue.name,
                'artist_id': self.artist_id,
                'artist_name': self.Artist.name,
                'start_time': self.start_time
                }
        return info
        # TODO: implement any missing fields, as a database migration using Flask-Migrate
        # Done
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # Done
    all_venues = Venue.query.all()

    data = []
    for venue in all_venues:
        data.append({"city": venue.city,
                     "state": venue.state,
                     "venues": [{
                         "id": venue.id,
                         "name": venue.name,
                         "num_upcoming_shows": 0
                     }]
                     })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # Done
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    data = db.session.query(Venue).filter(
        Venue.name.ilike(f'%{search_term}%')).all()
    venueList = list(map(Venue.short, data))
    response = {
        "count": len(venueList),
        "data": venueList
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO:  replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    show_time = Show.query.get(venue_id).start_time
    data_dict = {
        "id": venue.id,
        "name": venue.name,
        "genres": [venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": "https://www.example.com",
        "facebook_link": venue.facebook_link,
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [{
            "start_time": show_time
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }

    data = list(filter(lambda d: d['id'] == venue_id, [data_dict]))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # Done 
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        genres = request.form.get('genres')
        facebook_link = request.form.get('facebook_link')
        venue = Venue(name=name, city=city, state=state, address=address,
                    phone=phone, genres=genres, facebook_link=facebook_link)
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        db.session.close()
        flash('Something went wrong!')

    # TODO: on unsuccessful db insert, flash an error instead.
    # Done
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # Done
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # Done 
    artists = Artist.query.all()

    data = []
    for artist in artists:
        data.append({"id": artist.id,
                     "name": artist.name
                     })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string
    # Done
    # search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and
    search_term = request.form.get('search_term', '')
    data = db.session.query(Artist).filter(
        Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # Done 
    artist = Artist.query.get(artist_id)
    show = Show.query.get(artist_id).start_time
    data_dict = {
        "id": artist_id,
        "name": artist.name,
        "genres": [artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link,
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "seeking_venue": True,
        "past_shows": [{
            "start_time": show
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data = list(filter(lambda d: d['id'] == artist_id, [data_dict]))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    
    details = Artist.details(artist)
    form.name.data = details["name"]
    form.genres.data = details["genres"]
    form.city.data = details["city"]
    form.state.data = details["state"]
    form.phone.data = details["phone"]
    form.website.data = details["website"]
    form.facebook_link.data = details["facebook_link"]
    form.seeking_venue.data = details["seeking_venue"]
    form.seeking_description.data = details["seeking_description"]
    form.image_link.data = details["image_link"]
    flash('artist details has been updated')
    # TODO: populate form with fields from artist with ID <artist_id>
    # Done
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # Done 
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.get('genres')
        artist.facebook_link = request.form.get('facebook_link')
        db.session.commit()
        return redirect(url_for('show_artist', artist_id=artist_id))
    except:
        db.session.rollback()
        db.session.close()
        return render_template('errors/404.html'), 404


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    details = Venue.detail(venue_query)
    form.name.data = details["name"]
    form.genres.data = details["genres"]
    form.address.data = details["address"]
    form.city.data = details["city"]
    form.state.data = details["state"]
    form.phone.data = details["phone"]
    form.website.data = details["website"]
    form.facebook_link.data = details["facebook_link"]
    form.seeking_talent.data = details["seeking_talent"]
    form.seeking_description.data = details["seeking_description"]
    form.image_link.data = details["image_link"]
    # TODO: populate form with values from venue with ID <venue_id>
    # Done 
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # Done 
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.genres = request.form.get('genres')
        venue.facebook_link = request.form.get('facebook_link')
        db.session.commit()
        return redirect(url_for('show_venue', venue_id=venue_id))
    except:
        db.session.rollback()
        db.session.close()
        return render_template('errors/404.html'), 404


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # Done 
    # TODO: modify data to be the data object returned from db insertion
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        genres = request.form.get('genres')
        facebook_link = request.form.get('facebook_link')
        artist = Artist(name=name, city=city, state=state, phone=phone,
                        genres=genres, facebook_link=facebook_link)
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        db.session.close()
        flash('Something went wrong')
    # TODO: on unsuccessful db insert, flash an error instead.
    # Done
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    show_query = Show.query.options(db.joinedload(
        Show.Venue), db.joinedload(Show.Artist)).all()
    data = list(map(Show.detail, show_query))
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    # Done
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')

        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        db.session.close()
        flash('something went wrong')
    # TODO: on unsuccessful db insert, flash an error instead.
    # Done
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
