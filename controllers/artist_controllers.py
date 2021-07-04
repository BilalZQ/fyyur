from .imports import *
from forms import ArtistForm

from serializers import artist_serializer

@app.route('/artists')
def artists():
    """"
    Return list of all artists.

    :return:
    """
    return render_template('pages/artists.html', artists=[
        {'id': obj.id, 'name': obj.name} for obj in Artist.query.all()]
    )


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Return list of all artists based on searched term.

    :return:
    """
    search_term = request.form.get('search_term', '')

    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
    response = {
        'count': artists.count(),
        'data': [{
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len(artist.get_upcoming_shows)
            } for artist in artists]
        }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  """
  Return artist based on provided artist_id.

  :param artist_id:
  :return:
  """
  return render_template('pages/show_artist.html', artist=artist_serializer(
      Artist.query.get(artist_id), False))


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Edit artist form for given artist id.

    :return:
    """
    artist = Artist.query.get(artist_id)
    serialized_artist = artist_serializer(artist, False)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=serialized_artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Update artist data for given artist id.

    :return artist_id:
    :return:
    """
    form = ArtistForm()

    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website_link = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data

        db.session.commit()
        flash('The Artist ' + request.form['name'] + ' successfully updated.')
    except Exception as err:
        print(err)
        db.session.rollback()
        flash('The Artist ' + request.form['name'] + ' failed to update.')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    Create artist form.

    :return:
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Create artist submission from form data.

    :return:
    """
    form = ArtistForm()
    err = False

    try:
        artist = Artist(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            image_link = form.image_link.data,
            genres = form.genres.data,
            facebook_link = form.facebook_link.data,
            website_link = form.website_link.data,
            seeking_venue = form.seeking_venue.data,
            seeking_description = form.seeking_description.data
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        err = True
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html') if err else redirect(url_for('artists'))

#  Delete
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
    """
    Delete artist for given artist id.

    :param artist_id:
    :return:
    """
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        flash(f'Artist {artist.name} was successfully deleted!')
    except:
        db.session.rollback()
        flash('An error occured while trying to delete artist!')
    finally:
        db.session.close()

    return redirect(url_for('artists'))
