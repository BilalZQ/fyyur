from .imports import *
from forms import ShowForm
from serializers import show_serializer


@app.route('/shows')
def shows():
    """
    Return list of all shows.

    :return:
    """
    return render_template(
      'pages/shows.html', shows=show_serializer(Show.query.all()))


@app.route('/shows/create')
def create_shows():
    """
    Render create show form.

    :return:
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Create show submission from form data.

    :return:
    """
    form = ShowForm()
    err = False
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception:
        err = True
        db.session.rollback()
        flash('An error occurred while trying to list show.')
    finally:
        db.session.close()

    return render_template(
      'pages/home.html') if err else redirect(url_for('shows'))
