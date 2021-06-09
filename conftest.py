from flask.helpers import url_for
import pytest

from yumroad import create_app
from yumroad.extensions import db
from yumroad.models import *

@pytest.fixture
def app():
    return create_app('test')

@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()

#! Tao mot tai khoan va dang nhap -> follow_redirects=True
@pytest.fixture
def authenticated_request(client):
    new_user = User.create('test@valid.com', 'testvalid')
    db.session.add(new_user)
    db.session.commit()
    response = client.post(url_for('user.login'), data=dict(email='test@valid.com', password='testvalid'), follow_redirects=True)
    yield client