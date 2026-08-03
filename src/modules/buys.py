from flask import Blueprint, render_template, request, make_response, current_app, flash, redirect, url_for
from models import db, Compra, Proveedor
from sqlalchemy.orm import joinedload
from datetime import datetime
import io, os
from xhtml2pdf import pisa

buy_blueprint = Blueprint('buy', __name__)

@buy_blueprint.route('/compras', methods=['GET'])
def query_purchases():
    # 1. Get pagination parameters and dates from the URL.
    page = request.args.get('page', 1, type=int)
    start_date_str = request.args.get('start_date', '').strip() 
    end_date_str = request.args.get('end_date', '').strip()    
    
    # 2.  relations
    query = Compra.query.options(joinedload(Compra.proveedor),joinedload(Compra.productocompra))
    
    # 3. Apply date filters if they exist in the URL.
    if start_date_str:
        try:

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Compra.Fecha >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Compra.Fecha <= end_date)
        except ValueError:
            pass
            
    # 4. Perform pagination, sorting by the most recent purchases.
    pagination = query.order_by(Compra.Fecha.desc()).paginate(page=page, per_page=11, error_out=False)
    
    # 6. Renderizar la plantilla devolviendo las fechas para mantener los inputs llenos en el HTML
    return render_template('buy.html', pagination=pagination, start_date=start_date_str, end_date=end_date_str)