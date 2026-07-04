from flask import Blueprint, render_template, redirect, url_for, request
from models import db, Marca  

# Create the Blueprint for the branding module
trademark_blueprint = Blueprint('trademark', __name__)

@trademark_blueprint.route('/marcas')
def query_trademarks():
    # Get URL parameters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str).strip()
    
    per_page = 11  # Rows per page

    # Query and sort from the Marca model
    query = Marca.query.order_by(Marca.IdMarca.asc())

    # Apply search filter if query exists
    if search_query:
        query = query.filter(Marca.Marca.ilike(f"%{search_query}%"))

    # Execute pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Render template with data
    return render_template('trademark.html', pagination=pagination, search_query=search_query)

@trademark_blueprint.route('/register_trademark', methods=['POST'])
def register_trademark():
    # Get value from form input
    trademark_name = request.form.get('Marca')
    
    # Clean and save to database if valid
    if trademark_name:
        trademark_name = trademark_name.strip()
        
        new_trademark = Marca(Marca=trademark_name)
        db.session.add(new_trademark)
        db.session.commit()
            
    # Redirect back to trademarks list
    return redirect(url_for('trademark.query_trademarks'))

@trademark_blueprint.route('/update_trademark/<int:IdMarca>', methods=['POST'])
def update_trademark(IdMarca):
    # Buscamos en Postgres usando el ID exacto
    trademark = Marca.query.get_or_404(IdMarca)
    trademark_name = request.form.get('Marca')
    
    if trademark_name:
        trademark.Marca = trademark_name.strip()
        db.session.commit()
        
    return redirect(url_for('trademark.query_trademarks'))