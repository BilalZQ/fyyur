from .imports import *
from forms import VenueForm
from serializers import venue_serializer
from utils import serialized_venue_for_list


@app.route('/venues')
def venues():
    """
    Return list of all venues grouped by city.

    :return:
    """
    data_set = {}
    for venue in Venue.query.all():
        key = f'{venue.city}-{venue.state}-'
        data_set.update({key: {
            'city': venue.city,
            'state': venue.state,
            'venues': [serialized_venue_for_list(venue)]
        }}) if not data_set.get(key) else data_set[key]['venues'].append(
            serialized_venue_for_list(venue))
    return render_template(
      'pages/venues.html', areas=[data for data in data_set.values()])


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Return list of venues based on search term.
    """
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    response = {
        "count": venues.count(),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.get_upcoming_shows),
        } for venue in venues]
    }
    return render_template(
      'pages/search_venues.html', results=response,
      search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Return venues based on provided venue_id.

    :params venue_id:
    :return:
    """
    venue = Venue.query.get(venue_id)
    return render_template(
      'pages/show_venue.html', venue=venue_serializer(venue, False))

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
    Create venue form.

    :return:
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Create venue entry on form submission.

    :return:
    """
    form = VenueForm()
    err = False
    try:
        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            address=form.address.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            website_link=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue {venue.name} was successfully listed!')
    except Exception:
        err = True
        db.session.rollback()
        flash('An error occurred. Venue ' +
              form.name.data + ' could not be listed.')

    return render_template('pages/home.html') if err else redirect(
      url_for('venues'))


@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    """"
    Delete venue based on provided venue_id.

    :return:
    """
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue {venue.name} was successfully deleted!')
    except Exception as err:
        db.session.rollback()
        flash('An error occurred while trying to delete venue.')
    finally:
        db.session.close()

    return redirect(url_for('venues'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Edit venue form for given venue id.

    :return:
    """
    venue = Venue.query.get(venue_id)
    serialized_data = venue_serializer(venue, False)
    form = VenueForm(obj=venue)
    return render_template(
      'forms/edit_venue.html', form=form, venue=serialized_data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    Update venue data for given venue id.

    :return:
    """
    form = VenueForm()
    try:
        venue = Venue.query.get(venue_id)
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.address = form.address.data
        venue.genres = form.genres.data
        venue.image_link = form.image_link.data
        venue.website_link = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f'The Artist {form.name.data} successfully updated!')
    except Exception:
        db.session.rollback()
        flash(f'The Artist {form.name.data} failed to update!')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))
