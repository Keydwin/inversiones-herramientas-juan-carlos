from flask import Blueprint, render_template, request, make_response, current_app
from models import db, Producto
from sqlalchemy.orm import joinedload
import io, os
from xhtml2pdf import pisa

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

@product_blueprint.route('/productos/product_report')
def generate_product_report():
    # Get data from PostgreSQL
    products = Producto.query.options(joinedload(Producto.marca)).order_by(Producto.Codigo.asc()).all()
    
    # Obsolute path to the static folder
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    # Render HTML template with data and static path
    html_renderizado = render_template('pdf_product.html', products=products, base_dir=ruta_static)
    
    # Create an in-memory byte buffer
    output_memoria = io.BytesIO()
    
    # Convert HTML to PDF and store it in memory
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    # Check for rendering errors
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    # Move pointer to the beginning of the buffer
    output_memoria.seek(0)
    
    # Send PDF file back to the browser as a download
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_productos.pdf'
    
    return response