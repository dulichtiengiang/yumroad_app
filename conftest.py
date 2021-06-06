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

#! Tao mot tai khoan test
@pytest.fixture
def authenticated_request(client):
    new_user = User.create("test@test.com", "testpass")
    db.session.add(new_user)
    db.session.commit()

    response = client.post(url_for('user.login'),
                            data={'email':"test@test.com",
                                    'password':"testpass"},
                            follow_redirects=True
    )
    yield client

