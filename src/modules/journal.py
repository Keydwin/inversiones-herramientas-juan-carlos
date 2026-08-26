import io, os
from datetime import datetime
from flask import Blueprint, render_template, request, make_response, current_app
from models import db, LibroDiario
from xhtml2pdf import pisa

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