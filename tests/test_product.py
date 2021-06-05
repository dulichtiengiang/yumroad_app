import re
import pytest
from flask import url_for
from yumroad.extensions import db
from yumroad.models import Product


@pytest.fixture
def sample_book():
    book = Product(name="Book of Dev", description="Learning for Dev")
    db.session.add(book)
    db.session.commit()
    return book

def test_product_creation(client, init_database):
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

def test_new_page(client, init_database): #TEST VAO TRANG CREATE.HTML
    response = client.get(url_for('products.create')) #Lay toan bo du lieu response trong trang create.html
    assert response.status_code == 200
    assert b'Name' in response.data # ??? Ton tai b Name trong trang khong
    assert b'Create' in response.data # ??? Ton tai button 'Create' trong trang khong

def test_product_valid_creation(client, init_database): #TEST TAO SAN PHAM TRONG CREATE.HTML
    response = client.get(url_for('products.create'),#Lay toan bo response trong create.html truyen ve Client
                            data=dict(name='test name product', description='test valid'), #nhap Name va description
                            follow_redirects=True) #Cho phep return redirect(url_for(products.details))
    assert response.status_code == 200 # ??? 
    assert b'test name product' in response.data # ???
    assert b'test valid' in response.data # ???

def test_product_invalid_creation(client, init_database):
    response = client.get(url_for('products.create'),#Lay toan bo response trong create.html truyen ve Client
                            data=dict(name='a', description='test invalid'), #nhap Name va description
                            follow_redirects=True) #Cho phep return redirect(url_for(products.details))
    assert response.status_code == 200 # ??? 
    assert b'Field must be between 3 and 60 characters long' in response.data # ???
    assert b'is not valid' in response.data # ???
    assert b'is-invalid' in response.data # ???

def test_product_edit_page(client, init_database):
    response = client.get(url_for('products.edit', product_id=sample_book.id))
    assert response.state_code == 200
    assert b'Finish Product' in response.data
    assert sample_book.name in response.data
    assert sample_book.description in response.data

def test_product_edit_page_submission(client, init_database):
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
