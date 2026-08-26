from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, make_response
from models import db, EntregaVenta 
from datetime import datetime
from xhtml2pdf import pisa
import os
import io

# Initialize blueprint for delivery management
delivery_blueprint = Blueprint('delivery', __name__)

# Route to list and filter sales deliveries with pagination
@delivery_blueprint.route('/entregas', methods=['GET'])
def query_deliveries():
    # Get pagination and search query parameters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()

    query = EntregaVenta.query

    # Filter by delivery status if search query is provided
    if search_query:
        query = query.filter(
            (EntregaVenta.Estatus.ilike(f'%{search_query}%'))
        )

    # Paginate results ordered by most recent
    pagination = query.order_by(EntregaVenta.IdEntregaVenta.desc()).paginate(
        page=page, per_page=11, error_out=False
    )

    return render_template('delivery.html', pagination=pagination, search_query=search_query)


# Route to update a delivery's date and status
@delivery_blueprint.route('/entregas/update/<int:id>', methods=['POST'])
def update_delivery(id):
    entrega = EntregaVenta.query.get_or_404(id)

    # Get submitted form data
    fecha_str = request.form.get('FechaEntrega')
    estatus = request.form.get('Estatus')

    # Validate required fields
    if not fecha_str or not estatus:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('delivery.query_deliveries'))

    try:
        # Update delivery date and status
        entrega.FechaEntrega = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        entrega.Estatus = estatus.strip()
        
        db.session.commit()
        flash('Entrega actualizada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la entrega: {str(e)}', 'danger')

    return redirect(url_for('delivery.query_deliveries'))


# Route to generate a PDF report of deliveries
@delivery_blueprint.route('/report', methods=['GET'])
def generate_report():
    search_query = request.args.get('search', '', type=str).strip()

    query = EntregaVenta.query

    # Filter by sale ID or status if search query exists
    if search_query:
        query = query.filter(
            (EntregaVenta.IdVenta.cast(db.String).ilike(f'%{search_query}%')) |
            (EntregaVenta.Estatus.ilike(f'%{search_query}%'))
        )

    # Fetch all matching deliveries (or all deliveries if search_query is empty)
    deliveries = query.order_by(EntregaVenta.IdEntregaVenta.desc()).all()

    # Render HTML template for the PDF
    ruta_static = os.path.join(current_app.root_path, 'static')
    html_renderizado = render_template('pdf_delivery.html', deliveries=deliveries, base_dir=ruta_static)

    # Convert HTML to PDF stream
    output_memoria = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)

    if pisa_status.err:
        return "Error al generar el PDF de entregas", 500

    output_memoria.seek(0)

    # Return PDF response inline for preview
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_entregas.pdf'

    return response