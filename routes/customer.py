from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.category import Category
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from app import db

customer_bp = Blueprint('customer', __name__)

# PUBLIC ROUTES
@customer_bp.route('/category-list')
def category_list():
    return jsonify([
        {'id': c.id, 'name': c.name}
        for c in Category.query.all()
    ])


@customer_bp.route('/product-list')
def product_list():
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'category_id': p.category_id
        }
        for p in Product.query.all()
    ])


@customer_bp.route('/product-by-category/<int:cid>')
def product_by_category(cid):
    products = Product.query.filter_by(category_id=cid).all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price
        }
        for p in products
    ])


# ADD TO CART
@customer_bp.route('/add-to-cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.json

    product = Product.query.get_or_404(data['product_id'])

    # create cart order if not exists
    order = Order.query.filter_by(user_id=user_id, status='cart').first()

    if not order:
        order = Order(user_id=user_id, total=0, status='cart')
        db.session.add(order)
        db.session.commit()

    item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=data['quantity']
    )
    order.total += product.price * data['quantity']

    db.session.add(item)
    db.session.commit()

    return jsonify(msg="Added to cart", order_id=order.id)


# CHECKOUT
@customer_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()

    order = Order.query.filter_by(user_id=user_id, status='cart').first()

    if not order:
        return jsonify(msg="Cart is empty"), 400

    order.status = 'paid'
    db.session.commit()

    return jsonify(
        msg="Checkout successful",
        order_id=order.id,
        total=order.total
    )


# TRACK ORDER
@customer_bp.route('/tracking-order')
@jwt_required()
def tracking_order():
    user_id = get_jwt_identity()

    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            'order_id': o.id,
            'total': o.total,
            'status': o.status
        }
        for o in orders
    ])


# RESET PASSWORD
@customer_bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    user_id = get_jwt_identity()
    data = request.json

    # Check if old_password and new_password are provided
    if 'old_password' not in data or 'new_password' not in data:
        return jsonify(msg="old_password and new_password are required"), 400

    user = User.query.get_or_404(user_id)

    # Verify old password
    if not user.check_password(data['old_password']):
        return jsonify(msg="Old password is incorrect"), 401

    # Set new password
    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify(msg="Password updated successfully")
