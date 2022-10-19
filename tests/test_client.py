import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Customer list' in response.data
    assert b'Carford' in response.data


@pytest.mark.parametrize('path', (
    '/createClient',
    '/1/update',
    '/1/view?name=Teste',
    'createCar?id=1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/createClient').status_code == 200
    client.post('/createClient', data={'name': 'Teste'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM client').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'name':'testechange'})

    with app.app_context():
        db = get_db()
        client = db.execute('SELECT * FROM client WHERE id = 1').fetchone()
        assert client['name'] == 'testechange'

@pytest.mark.parametrize("path", ("/create", "/1/update"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'name':''})

    print('aqui response',response)
    assert b'Name is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM client WHERE id = 1').fetchone()
        assert post is None
