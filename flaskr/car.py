from http import client
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pyparsing import col
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
    id = request.args.get('id')

    cars = get_cars(id)

    if request.method == 'POST':
        model = request.form['model']
        color = request.form.get('color')
        client_id = request.form['client_id']
        error = None

        if len(cars) >= 3:
            error = 'Registered car numbers not allowed.'

        if not model:
            error = 'Model is required.'
        
        if not color:
            error = 'Color is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO car (model,color,client_id) VALUES (?,?,?)', (model,color,client_id))
            db.commit()
            return redirect(url_for('car.index'))

    return render_template('car/create.html', id=id, data=[{'name':'yellow'}, {'name':'blue'}, {'name':'Grey'}])


def get_cars(id):
    car = get_db().execute('SELECT * FROM car c WHERE client_id = ?', (id,)).fetchall()

    if car is None:
        abort(404, f"Car id {id} doesn't exist.")

    return car


@bp.route('/<int:id>/updateCar', methods=('GET', 'POST'))
@login_required
def update(id):
    cars = get_cars(id)
    
    if request.method == 'POST':
        client_id = request.form['client_id']
        id = request.form['id']
        model = request.form['model']
        color = request.form['color']
        error = None

        if not model:
            error = 'Model is required.'
        
        if not color:
            error = 'Color is required.'

        if not client_id:
            error = 'Client_id is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE car SET client_id = ?, model = ?, color = ? WHERE id = ?', (client_id, model, color, id))
            db.commit()
            return redirect(url_for('car.index'))

 
    return render_template('car/update.html', cars=cars)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_cars(id)
    db = get_db()
    db.execute('DELETE FROM car WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('car.index'))
