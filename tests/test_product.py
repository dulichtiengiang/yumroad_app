import pytest
from flask import url_for
from yumroad.extensions import db
from yumroad.models import Product

TEST_NAME = "test_name"
TEST_DESC = "test_desc"

@pytest.fixture
def sample_book():
    book = Product(name="Book of Dev", description="Learning for Dev")
    db.session.add(book)
    db.session.commit()
    return book

def test_product_creation(client, init_database, authenticated_request):
    assert Product.query.count() == 0
    book = Product(name="Book of Dev", description="Learning for Dev")
    db.session.add(book)
    db.session.commit()
    assert Product.query.count() == 1
    assert Product.query.first().name == book.name

def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name="   a", description="invalid book")

def test_index_page(client, init_database, sample_book):
    # client.get('/product') #blueprint('/product')
    response = client.get(url_for('products.index'))
    assert response.status_code == 200
    assert 'Yumroad' in str(response.data)
    assert sample_book.name in str(response.data)

    expected_link = url_for('products.details', product_id=sample_book.id)
    assert expected_link in str(response.data)

def test_detail_page(client, init_database, sample_book):
    # client.get('/product/1')
    response = client.get(url_for('products.details', product_id=sample_book.id))
    assert response.status_code == 200
    assert 'Yumroad' in str(response.data) 
    assert 'Purchase coming soon' in str(response.data) 

def test_not_found_page(client, init_database):
    # client.get('/product/1')
    response = client.get(url_for('products.details', product_id=1))
    assert response.status_code == 404
    assert url_for('products.index') in str(response.data)

def test__new_product(client, init_database, authenticated_request):
    response = client.get(url_for('products.create'))
    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

#Test Login fail
def test__new_product__unauth(client, init_database): 
    response = client.get(url_for('products.create'))
    assert response.status_code == 302 #Khong co tai khoan dang nhap, nó sẽ redirect response.status_code = 302
    assert response.location == url_for('user.login', _external=True) #Chuyển hướng redirects 

def test__create_product__valid(client, init_database, authenticated_request): #TEST TAO SAN PHAM TRONG CREATE.HTML
    response = client.post(url_for('products.create'),
                            data={'name': 'test_name', 'description':'test_desc'}, #nhap Name va description
                            follow_redirects=True) #Cho phep return redirect(url_for(products.details))
    assert response.status_code == 200 #
    assert b'Create Product' in response.data #
    assert b'test_name' in response.data #
    assert b'test_desc' in response.data #


def test__create_product__invalid(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),#Lay toan bo response trong create.html truyen ve Client
                            data=dict(name='ab', description='is not valid'), #nhap Name va description
                            follow_redirects=True) #Cho phep return redirect(url_for(products.details))
    assert response.status_code == 200 # ??? 
    assert b'Field must be between 3 and 60 characters long' in response.data #
    assert b'is not valid' in response.data # description
    assert b'is-invalid' in response.data # class="is-invalid" in This response

#Test just get URL
def test__edit_product(client, init_database, sample_book, authenticated_request):
    response = client.get(url_for('products.edit', product_id=sample_book.id))
    assert response.status_code == 200
    assert b'Finish Product' in response.data
    assert sample_book.name in str(response.data)
    assert sample_book.description in str(response.data)

def test__edit_product__submission__valid(client, init_database, sample_book, authenticated_request):
    old_name = sample_book.name
    old_description = sample_book.description
    response = client.post(url_for('products.edit', product_id=sample_book.id),
                                    data=dict(name='test-changed', description='is persisted'),
                                    follow_redirects=True)
    assert response.status_code == 200
    assert 'tett-changed' in response.data
    assert 'is persisted' in response.data
    assert old_name not in response.data
    assert old_description not in response.data
    assert b'Finish Product' not in response.data

def test_product__edit_page__invalid_submission(client, init_database):
    old_name = sample_book.name
    old_description = sample_book.description
    response = client.post(url_for('vi0', product_id=sample_book.id),
                                    data=dict(name='test-changed', description='is persisted'),
                                    follow_redirects=True)
    assert response.status_code == 200
    assert 'vi0' in response.data
    assert 'Field must be between 3 and 60 characters long' in response.data
    assert Product.query.get(sample_book.id).name == old_name
    assert old_description not in str(response.data)
    assert old_name in str(response.data)
    assert b'Finish Product' in response.data
