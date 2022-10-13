from http import client
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('car', __name__)


@bp.route('/')
def index():
    db = get_db()
    cars = db.execute(
        'SELECT * FROM car',
    ).fetchall()
    return render_template('index.html', cars=cars)

@bp.route('/createCar', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        model = request.form['model']
        color = request.form['color']
        client_id = request.form['client_id']
        error = None

        if not model:
            error = 'Model is required.'
        
        if not color:
            error = 'Color is required.'

        if not client_id:
            error = 'Clientid is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO car (model,color,client_id) VALUES (?,?,?)', (model,color,client_id))
            db.commit()
            return redirect(url_for('car.index'))

    return render_template('car/create.html')


def get_post(id):
    client = get_db().execute('SELECT * FROM client c WHERE id = ?', (id,)).fetchone()

    if client is None:
        abort(404, f"Client id {id} doesn't exist.")

    return client


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    clients = get_post(id)
    

    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE client SET name = ? WHERE id = ?', (name, id))
            db.commit()
            return redirect(url_for('client.index'))

    return render_template('client/update.html', clients=clients)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM client WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('client.index'))
