from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Marca, Producto  

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
    trademark_name = request.form.get('Marca').strip()
        
    # Verify that no trademark with the same name exists.
    existe = Marca.query.filter_by(Marca=trademark_name).first()
    if existe:
        flash("Esta marca ya se encuentra registrada.", "danger")
        return redirect(url_for('trademark.query_trademarks'))

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
    # We search in Postgres using the exact ID.
    trademark = Marca.query.get_or_404(IdMarca)
    trademark_name = request.form.get('Marca')
    
    if trademark_name:
        trademark.Marca = trademark_name.strip()
        db.session.commit()
        
    return redirect(url_for('trademark.query_trademarks'))


@trademark_blueprint.route('/delete_trademark/<int:IdMarca>', methods=['POST'])
def delete_trademark(IdMarca):
    # We are looking for the existing trademark.
    trademark = Marca.query.get_or_404(IdMarca)
    
    # We check the 'producto' table for dependencies.
    linked_product = Producto.query.filter_by(IdMarca=IdMarca).count()
    
    if linked_product:
        # If we find at least one product, we stop the deletion.
        flash("No se puede eliminar la marca porque tiene productos asociados.", "danger")
        return redirect(url_for('trademark.query_trademarks'))
    
    #  If there are no linked products, we proceed to securely delete them
    try:
        db.session.delete(trademark)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error interno al intentar eliminar la marca.", "danger")
    
    return redirect(url_for('trademark.query_trademarks'))