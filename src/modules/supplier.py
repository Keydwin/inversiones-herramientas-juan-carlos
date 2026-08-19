import io, os
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, current_app
from models import db, Proveedor
from sqlalchemy.exc import IntegrityError
from xhtml2pdf import pisa

# Create the Blueprint for the supplier module
supplier_blueprint = Blueprint('supplier', __name__)

@supplier_blueprint.route('/proveedores')
def query_suppliers():
    # Get URL parameters for pagination and search
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('supplier', '', type=str).strip()
    
    per_page = 11  # Rows per page

    # Query and sort from the Proveedor model
    query = Proveedor.query.order_by(Proveedor.IdProveedor.asc())

    # Apply search filter if query exists
    if search_query:
        query = query.filter(Proveedor.NombreProveedor.ilike(f"%{search_query}%"))

    # Execute pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Render template with data
    return render_template('supplier.html', pagination=pagination, search_query=search_query)

@supplier_blueprint.route('/proveedores/register_supplier', methods=['POST'])
def register_supplier():
    # Get values from form input
    supplier_name = request.form.get('NombreProveedor', '').strip()
        
    # Verify that no supplier with the same name already exists
    existe = Proveedor.query.filter(Proveedor.NombreProveedor.ilike(supplier_name)).first()
    if existe:
        flash("Este proveedor ya se encuentra registrado", "danger")
        return redirect(url_for('supplier.query_suppliers'))

    # Save to database if valid
    if supplier_name:
        try:
            new_supplier = Proveedor(
                NombreProveedor=supplier_name
            )
            db.session.add(new_supplier)
            db.session.commit()
            flash('Proveedor registrado con éxito.', 'success')
        except Exception:
            db.session.rollback()
            flash('Error al intentar registrar el proveedor.', 'danger')
            
    return redirect(url_for('supplier.query_suppliers'))

@supplier_blueprint.route('/proveedores/update_supplier/<int:IdProveedor>', methods=['POST'])
def update_supplier(IdProveedor):
    # Search supplier in database or return 404
    supplier = Proveedor.query.get_or_404(IdProveedor)
    supplier_name = request.form.get('NombreProveedor', '').strip()
    
    if supplier_name:
        try:
            supplier.NombreProveedor = supplier_name
            db.session.commit()
            flash('Proveedor modificado con éxito.', 'success')
        except Exception:
            db.session.rollback()
            flash('Error al intentar modificar el proveedor.', 'danger')
        
    return redirect(url_for('supplier.query_suppliers'))

@supplier_blueprint.route('/proveedores/delete_supplier/<int:IdProveedor>', methods=['POST'])
def delete_supplier(IdProveedor):
    try:
        # Consult supplier model
        supplier = Proveedor.query.get_or_404(IdProveedor)
        db.session.delete(supplier)
        db.session.commit()
        flash('Proveedor eliminado exitosamente.', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar el proveedor porque tiene compras o registros asociados.', 'danger')
        
    except Exception:
        db.session.rollback()
        flash('Error al intentar eliminar el proveedor.', 'danger')
    
    return redirect(url_for('supplier.query_suppliers'))

@supplier_blueprint.route('/proveedores/supplier_report')
def generate_supplier_report():
    # Get data from database ordered by name
    suppliers = Proveedor.query.order_by(Proveedor.NombreProveedor.asc()).all()
    
    # Absolute path to static folder
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    # Render HTML template with data and static path
    html_renderizado = render_template('pdf_supplier.html', suppliers=suppliers, base_dir=ruta_static)
    
    # Create an in-memory byte buffer
    output_memoria = io.BytesIO()
    
    # Convert HTML to PDF and store it in memory
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_proveedores.pdf'
    
    return response