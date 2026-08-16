from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for
from models import db, Producto, Marca
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
import io, os
from xhtml2pdf import pisa

# Create the blueprint for the product module
product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/productos', methods=['GET'])
def query_products():
    # Get pagination and search parameters from URL
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('product', '').strip()
    
    # Eager load brand relationship and order ascending by IdProducto
    query = Producto.query.options(joinedload(Producto.marca)).order_by(Producto.IdProducto.asc())
    
    # Apply search filters by product name
    if search_query:
        query = query.filter(Producto.NombreProducto.ilike(f'%{search_query}%'))
            
    # Execute pagination (10 items per page)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    # Fetch all brands ordered alphabetically for the modal dropdown
    all_brands = Marca.query.order_by(Marca.Marca.asc()).all()
    
    # Render view template with data context
    return render_template('product.html', pagination=pagination, search_query=search_query, brands=all_brands)

@product_blueprint.route('/productos/registrar', methods=['POST'])
def register_product():
    try:
        # Get form inputs from active modal context
        Codigo = request.form.get('Codigo').strip()
        NombreProducto = request.form.get('NombreProducto').strip()
        Descripcion = request.form.get('Descripcion').strip()
        IdMarca = request.form.get('IdMarca').strip()
        PrecioDeContado = request.form.get('PrecioDeContado').strip()
        PrecioCredito = request.form.get('PrecioCredito').strip()
        PorcenajeDeContado = request.form.get('PorcenajeDeContado').strip()
        PorcentajeCredito =  request.form.get('PorcentajeCredito').strip()
            
        # Prevent database primary key conflicts
        existing_product = Producto.query.filter_by(Codigo=int(Codigo)).first()
        if existing_product:
            flash('El código de producto ya se encuentra registrado.', 'danger')
            return redirect(url_for('product.query_products'))
            
        # Create new entity instance mapping inputs
        NewProduct = Producto(
            Codigo=(Codigo),
            NombreProducto=NombreProducto,
            Descripcion=Descripcion,
            IdMarca=(IdMarca),
            PrecioDeContado=(PrecioDeContado),
            PrecioCredito=(PrecioCredito),
            PorcenajeDeContado=(PorcenajeDeContado),
            PorcentajeCredito=(PorcentajeCredito),
        )
        
        # Persist entry inside database session context
        db.session.add(NewProduct)
        db.session.commit()
        flash('Producto Registrado con éxito.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar el producto: {str(e)}', 'danger')
        
    # Standard clean redirect to dynamic data list
    return redirect(url_for('product.query_products'))

@product_blueprint.route('/productos/modificar/<int:IdProducto>', methods=['POST'])
def update_product(IdProducto):
    try:
        # Search for the existing product in the database
        ExistingProduct = Producto.query.get_or_404(IdProducto)
        
        # Extract the data from the edit form
        Codigo = request.form.get('Codigo').strip()
        NombreProducto = request.form.get('NombreProducto').strip()
        Descripcion = request.form.get('Descripcion').strip()
        IdMarca = request.form.get('IdMarca').strip()
        PrecioDeContado = request.form.get('PrecioDeContado').strip()
        PrecioCredito = request.form.get('PrecioCredito').strip()
        PorcenajeDeContado = request.form.get('PorcenajeDeContado').strip()
        PorcentajeCredito = request.form.get('PorcentajeCredito').strip()

        # Validate code duplicates (only if the code has changed)
        if int(Codigo) != ExistingProduct.Codigo:
            duplicate_check = Producto.query.filter_by(Codigo=int(Codigo)).first()
            if duplicate_check:
                flash('El nuevo código de producto ya está registrado por otro artículo.', 'danger')
                return redirect(url_for('product.query_products'))

        #  Update the attributes of the mapped object.
        ExistingProduct.Codigo = Codigo
        ExistingProduct.NombreProducto = NombreProducto
        ExistingProduct.Descripcion = Descripcion
        ExistingProduct.IdMarca = IdMarca
        ExistingProduct.PrecioDeContado = PrecioDeContado
        ExistingProduct.PrecioCredito = PrecioCredito
        ExistingProduct.PorcenajeDeContado = PorcenajeDeContado
        ExistingProduct.PorcentajeCredito = PorcentajeCredito

        # Guardar los cambios en PostgreSQL
        db.session.commit()
        flash('Producto Modificado con éxito.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al modificar el producto: {str(e)}', 'error')

    return redirect(url_for('product.query_products'))

@product_blueprint.route('/productos/eliminar/<int:IdProducto>', methods=['POST'])
def delete_product(IdProducto):
    try:
        producto = Producto.query.get_or_404(IdProducto)
        db.session.delete(producto)
        db.session.commit()
        flash('Producto Eleminado exitosamente', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar este producto porque está asociado ya sea a una compra o venta o inventario', 'danger')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al intentar eliminar el producto', 'danger')

    return redirect(url_for('product.query_products'))

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