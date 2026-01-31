from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models import User
from models.category import Category
from models.product import Product
from models.order import Order
from helper.auth_middleware import admin_required

admin_bp = Blueprint('admin', __name__)

# CATEGORY ROUTES
@admin_bp.route('/category', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify(msg="Category created")


@admin_bp.route('/category', methods=['GET'])
@jwt_required()
@admin_required
def list_category():
    categories = Category.query.all()
    return jsonify([
        {"id": c.id, "name": c.name}
        for c in categories
    ])


@admin_bp.route('/category/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def category_by_id(id):
    category = Category.query.get_or_404(id)
    return jsonify({
        "id": category.id,
        "name": category.name
    })


@admin_bp.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json
    category.name = data['name']
    db.session.commit()
    return jsonify(msg="Category updated")


@admin_bp.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(msg="Category deleted")


# PRODUCT ROUTES
@admin_bp.route('/product', methods=['POST'])
@jwt_required()
@admin_required
def create_product():
    data = request.json
    product = Product(
        name=data['name'],
        price=data['price'],
        category_id=data['category_id']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(msg="Product created")


@admin_bp.route('/product', methods=['GET'])
@jwt_required()
@admin_required
def list_product():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_id": p.category_id
        }
        for p in products
    ])


@admin_bp.route('/product/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def product_by_id(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "category_id": product.category_id
    })


@admin_bp.route('/product/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data['name']
    product.price = data['price']
    product.category_id = data['category_id']
    db.session.commit()
    return jsonify(msg="Product updated")


@admin_bp.route('/product/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(msg="Product deleted")


# USER MANAGEMENT
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ])


@admin_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']  # e.g., 'admin' or 'customer'
    db.session.commit()

    return jsonify(msg=f"User {id} updated successfully")


@admin_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(msg=f"User {id} deleted successfully")


# ORDER MANAGEMENT
@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
@admin_required
def list_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "order_id": o.id,
            "user_id": o.user_id,
            "total": o.total,
            "status": o.status
        }
        for o in orders
    ])


# SALES REPORT
@admin_bp.route('/report/sale', methods=['GET'])
@jwt_required()
@admin_required
def sale_report():
    orders = Order.query.all()
    total_orders = len(orders)
    total_revenue = sum(o.total for o in orders)

    return jsonify({
        "total_orders": total_orders,
        "total_revenue": total_revenue
    })
