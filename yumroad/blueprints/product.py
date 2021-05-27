from flask import Blueprint, render_template, abort

from yumroad.models import Product

product = Blueprint('product', __name__)

@product.route('/')
def index():
    # all_products = Product.query.all()
    # return all_products
    return ('This is Index Page')

@product.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('/products/details.html', product=product)

@product.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404