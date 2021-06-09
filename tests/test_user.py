from werkzeug.wrappers import response
from yumroad.blueprints.products import create
import yumroad
from flask import url_for
import pytest

from yumroad.models import User
from yumroad.extensions import db

TEST_EMAIL = 'test@valid.com'
TEST_PASSWORD = 'testvalid'

VALID_REGISTER_PARAMS = {
    'email': TEST_EMAIL,
    'password': TEST_PASSWORD,
    'confirm_password': TEST_PASSWORD
}

NEW_REGISTER_PARAMS = {
    'email' : 'newtest@valid.com',
    'password' : 'newtest',
    'confirm_password' : 'newtest'
}

def create_user(email=TEST_EMAIL, password=TEST_PASSWORD):
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return user

#Test user duoc tao chua
def test_create__user(client, init_database):
    assert User.query.count() == 0
    user = create_user()
    assert User.query.count() == 1
    assert user.password is not TEST_PASSWORD

#Test vao Signup
def test_register__get(client, init_database):
    response = client.get(url_for('user.register'))
    assert response.status_code == 200
    assert 'Email Address:' in str(response.data)
    assert 'Password:' in str(response.data)
    assert 'Confirm Password:' in str(response.data)

def test_register__already_logged_in(client, init_database, authenticated_request):
    response = client.post(url_for('user.register'), data=NEW_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'__flash__You are already logged in' in response.data

def test_login__already_logged_in(client, init_database, authenticated_request):
    response = client.post(url_for('user.login'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'__flash__You are already logged in' in response.data

def test_register__valid(client, init_database):
    response = client.post('/register', data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'__Registered successfully' in response.data
    assert TEST_EMAIL in str(response.data)
    assert b'Yumroad' in response.data

def test_register__invalid__with_email(client, init_database):
    invalid_data = VALID_REGISTER_PARAMS.copy()
    invalid_data['email'] = 'abc' #Thay doi email
    response = client.post('/register', data=invalid_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email' in response.data

def test_register__invalid__with_existing_email(client, init_database):
    user = create_user() #! Tao 1 acc 
    response = client.post(url_for('user.register'), data=dict(email=TEST_EMAIL, password=TEST_PASSWORD, confirm_password=TEST_PASSWORD), follow_redirects=True)
    assert response.status_code == 200
    assert b'__form_validate__That email already has an account' in response.data
    assert b'__flash__Registered successfully' not in response.data
    assert b'__flash__You are already logged in' not in response.data

def test_register__already_logged_in(client, init_database, authenticated_request):
    response = client.post(url_for('user.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'__flash__You are already logged in' in response.data

def test_login__get(client, init_database):
    response = client.get(url_for('user.login'))
    assert b'Email:' in response.data
    assert b'Password:' in response.data
    assert b'Login' in response.data

#! Login valid
def test_login__valid(client, init_database):
    user = create_user()
    response = client.post(url_for('user.login'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'__flash__Logged in successfully' in response.data
    assert b'__flash__You are already logged in' not in response.data
    assert url_for('user.logout') in str(response.data)
    assert b'Sign Out' in response.data

#! Login invalid #! Khong tim thay  email
def test_login__invalid__with_noexisting_email(client, init_database):
    response = client.post(url_for('user.login'), data=dict(email=TEST_EMAIL, password=TEST_PASSWORD), follow_redirects=True)
    assert b'__form_validate__Invalid email or password' in response.data
    assert b'__flash__Logged in successfully' not in response.data

#! Wrong pass
def test_login__bad_password(client, init_database):
    create_user()
    response = client.post(url_for('user.login'), data=dict(email=TEST_EMAIL, password='badpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_logout(client, init_database, authenticated_request):
    response = client.get(url_for('user.logout'), follow_redirects=True)
    response.status_code == 200
    assert b'Sign Out' not in response.data
    assert b'Login' in response.data