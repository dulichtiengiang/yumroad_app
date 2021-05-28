from flask import Blueprint, render_template, abort

from yumroad.models import Product

products = Blueprint('products', __name__)

@products.route('/')
def index():
    # all_products = Product.query.all()
    # return all_products
    product_all = Product.query.all()
    return render_template('/products/index.html', product=product_all)

@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('/products/details.html', product=product)

@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404