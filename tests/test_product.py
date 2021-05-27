import pytest

from yumroad.extensions import db
from yumroad.models import Product

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

