from flask import Blueprint, render_template, request
from models import db, Producto
from sqlalchemy.orm import joinedload

# Create the blueprint for the product module
product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/productos')
def query_products():
    # Retrieve page and search query parameters from the URL
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('product', '', type=str).strip()
    
    items_per_page = 11

    # Base query: eagerly load the associated brand (marca) relationship
    query = Producto.query.options(joinedload(Producto.marca)).order_by(Producto.IdProducto.asc())

    # Apply search filter on the product name if provided
    if search_query:
        query = query.filter(Producto.NombreProducto.ilike(f"%{search_query}%"))

    # Execute pagination
    pagination = query.paginate(page=page, per_page=items_per_page, error_out=False)

    # Render template passing pagination details and the search query
    return render_template('product.html',pagination=pagination,search_query=search_query)