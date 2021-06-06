from werkzeug.wrappers import response
from yumroad.blueprints.products import create
import yumroad
from flask import url_for
import pytest

from yumroad.models import User
from yumroad.extensions import db

TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "passtestwrong"

VALID_REGISTER_PARAMS = {
    'email': TEST_EMAIL,
    'password': TEST_PASSWORD,
    'confirm_password': TEST_PASSWORD
}

def create_user(email=TEST_EMAIL, password=TEST_PASSWORD):
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return user

#Test user duoc tao chua
def test_user_creation(client, init_database):
    assert User.query.count() == 0
    user = create_user
    assert User.query.count() == 1
    assert user.password is not TEST_PASSWORD

#Test vao Signup
def test_get_register(client, init_database):
    response = client.get(url_for('user.register'))
    assert response.status_code == 200
    assert 'Email:' in str(response.data)
    assert 'Password:' in str(response.data)
    assert 'Confirm Password:' in str(response.data)

def test_register(client, init_database):
    response = client.post('/register',
                            data=VALID_REGISTER_PARAMS,
                            follow_redirects=True)
    print(response)
    assert response.status_code == 200
    assert b'Registered Successfully' in response.data
    assert TEST_EMAIL in response.data
    assert b'Yumroad' in response.data

def test_register_invalid(client, init_database):
    invalid_data = VALID_REGISTER_PARAMS.copy()
    invalid_data['email'] = 'abc'
    response = client.post('/register',
                            data=VALID_REGISTER_PARAMS,
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email' in response.data