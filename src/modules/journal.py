import io, os
from datetime import datetime
from flask import Blueprint, render_template, request, make_response, current_app
from models import db, LibroDiario
from xhtml2pdf import pisa
from sqlalchemy.orm import joinedload

journal_blueprint = Blueprint('journal', __name__)

@journal_blueprint.route('/libro_diario')
def query_journal_entries():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', '', type=str).strip()
    end_date = request.args.get('end_date', '', type=str).strip()
    
    per_page = 11

    # Consulta base ordenada por fecha y número de asentamiento
    query = LibroDiario.query.order_by(LibroDiario.Fecha.asc(), LibroDiario.NumeroDeAsentamiento.asc())

    # Aplicar filtros de fecha si están presentes
    if start_date:
        query = query.filter(LibroDiario.Fecha >= start_date)
    if end_date:
        query = query.filter(LibroDiario.Fecha <= end_date)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'journal.html', 
        pagination=pagination, 
        start_date=start_date, 
        end_date=end_date
    )

@journal_blueprint.route('/journal/report')
def generate_journal_report():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query_asientos = LibroDiario.query.order_by(
        LibroDiario.Fecha.asc(), 
        LibroDiario.NumeroDeAsentamiento.asc(), 
        LibroDiario.IdLibroDiario.asc()
    )
    
    if start_date:
        query_asientos = query_asientos.filter(LibroDiario.Fecha >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query_asientos = query_asientos.filter(LibroDiario.Fecha <= datetime.strptime(end_date, '%Y-%m-%d').date())

    asientos = query_asientos.all()

    # Suma global de columnas Debe y Haber para la comprobación
    total_debe = sum(float(a.Debe or 0) for a in asientos)
    total_haber = sum(float(a.Haber or 0) for a in asientos)

    ruta_static = os.path.join(current_app.root_path, 'static')
    
    html_renderizado = render_template(
        'pdf_journal.html', 
        asientos=asientos, 
        start_date=start_date,
        end_date=end_date,
        total_debe=total_debe,
        total_haber=total_haber,
        base_dir=ruta_static
    )
    
    output_memoria = io.BytesIO()
    pisa_status = pisa.CreatePDF(src=html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF del Libro Diario", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_libro_diario.pdf'
    
    return response