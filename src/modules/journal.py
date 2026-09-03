import io, os
from datetime import datetime
from flask import Blueprint, render_template, request, make_response, current_app
from models import db, LibroDiario
from xhtml2pdf import pisa
from sqlalchemy.orm import joinedload

# Create Blueprint for journal routes
journal_blueprint = Blueprint('journal', __name__)

@journal_blueprint.route('/libro_diario')
def query_journal_entries():
    # Get pagination and date filter parameters
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', '', type=str).strip()
    end_date = request.args.get('end_date', '', type=str).strip()
    
    per_page = 11

    # Base query ordered by date and entry number
    query = LibroDiario.query.order_by(LibroDiario.Fecha.asc(), LibroDiario.NumeroDeAsentamiento.asc())

    # Apply date filters if present
    if start_date:
        query = query.filter(LibroDiario.Fecha >= start_date)
    if end_date:
        query = query.filter(LibroDiario.Fecha <= end_date)

    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'journal.html', 
        pagination=pagination, 
        start_date=start_date, 
        end_date=end_date
    )

@journal_blueprint.route('/journal/report')
def generate_journal_report():
    # Get date filter parameters
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    # Base query ordered by date, entry number, and ID
    query_asientos = LibroDiario.query.order_by(
        LibroDiario.Fecha.asc(), 
        LibroDiario.NumeroDeAsentamiento.asc(), 
        LibroDiario.IdLibroDiario.asc()
    )
    
    # Parse dates and filter if valid; ignore filter if invalid
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query_asientos = query_asientos.filter(LibroDiario.Fecha >= start_date_obj)
        except ValueError:
            pass

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query_asientos = query_asientos.filter(LibroDiario.Fecha <= end_date_obj)
        except ValueError:
            pass

    # Fetch all filtered entries
    asientos = query_asientos.all()

    # Calculate total Debit and Credit sums
    total_debe = sum(float(a.Debe or 0) for a in asientos)
    total_haber = sum(float(a.Haber or 0) for a in asientos)

    # Get static folder path for PDF assets
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    # Render HTML template for PDF
    html_renderizado = render_template(
        'pdf_journal.html', 
        asientos=asientos, 
        start_date=start_date,
        end_date=end_date,
        total_debe=total_debe,
        total_haber=total_haber,
        base_dir=ruta_static
    )
    
    # Generate PDF in memory
    output_memoria = io.BytesIO()
    pisa_status = pisa.CreatePDF(src=html_renderizado, dest=output_memoria)
    
    # Check for PDF generation errors
    if pisa_status.err:
        return "Error al generar el PDF del Libro Diario", 500
        
    output_memoria.seek(0)
    
    # Return PDF response for inline viewing
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_libro_diario.pdf'
    
    return response