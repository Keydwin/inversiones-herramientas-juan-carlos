import io, os
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, current_app, jsonify
from models import db, Cliente, Persona, Parroquia, Estado, Municipio
from sqlalchemy import cast, String
from sqlalchemy.exc import IntegrityError
from xhtml2pdf import pisa

client_blueprint = Blueprint('client', __name__)

@client_blueprint.route('/clientes')
def query_clients():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('client', '', type=str).strip()
    
    per_page = 11
    query = Cliente.query.join(Cliente.persona).order_by(Cliente.IdCliente.asc())

    if search_query:
        query = query.filter(
            (Persona.Nombre.ilike(f"%{search_query}%")) | 
            (Persona.Apellido.ilike(f"%{search_query}%")) |
            (cast(Persona.Cedula, String).ilike(f"%{search_query}%"))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    estados = Estado.query.order_by(Estado.Estado.asc()).all()

    return render_template(
        'client.html', 
        pagination=pagination, 
        search_query=search_query,
        estados=estados
    )

# --- ENDPOINTS AJAX UBICACIÓN ---

@client_blueprint.route('/get_municipios/<int:id_estado>')
def get_municipios(id_estado):
    municipios = Municipio.query.filter_by(IdEstado=id_estado).order_by(Municipio.Municipio.asc()).all()
    return jsonify([{'IdMunicipio': m.IdMunicipio, 'Municipio': m.Municipio} for m in municipios])

@client_blueprint.route('/get_parroquias/<int:id_municipio>')
def get_parroquias(id_municipio):
    parroquias = Parroquia.query.filter_by(IdMunicipio=id_municipio).order_by(Parroquia.Parroquia.asc()).all()
    return jsonify([{'IdParroquia': p.IdParroquia, 'Parroquia': p.Parroquia} for p in parroquias])

@client_blueprint.route('/get_ubicacion_parroquia/<int:id_parroquia>')
def get_ubicacion_parroquia(id_parroquia):
    parroquia = Parroquia.query.get_or_404(id_parroquia)
    return jsonify({
        'IdEstado': parroquia.municipio.IdEstado,
        'IdMunicipio': parroquia.IdMunicipio
    })

# --- OPERACIONES CRUD Y REPORTES ---

@client_blueprint.route('/clientes/register_client', methods=['POST'])
def register_client():
    try:
        cedula = int(request.form.get('Cedula', 0))
        nombre = request.form.get('Nombre', '').strip()
        apellido = request.form.get('Apellido', '').strip()
        telefono = int(request.form.get('Telefono', 0))
        id_parroquia = request.form.get('IdParroquia')
        direccion = request.form.get('Direccion', '').strip()

        persona = Persona.query.filter_by(Cedula=cedula).first()

        if not persona:
            persona = Persona(
                Cedula=cedula,
                Nombre=nombre,
                Apellido=apellido,
                Telefono=telefono
            )
            db.session.add(persona)
            db.session.flush()
        else:
            existe_cliente = Cliente.query.filter_by(IdPersona=persona.IdPersona).first()
            if existe_cliente:
                flash("La cédula ingresada ya pertenece a un cliente registrado", "danger")
                return redirect(url_for('client.query_clients'))

        if persona and id_parroquia and direccion:
            new_client = Cliente(
                IdPersona=persona.IdPersona,
                IdParroquia=id_parroquia,
                Direccion=direccion
            )
            db.session.add(new_client)
            db.session.commit()
            flash('Cliente registrado con éxito.', 'success')

    except Exception:
        db.session.rollback()
        flash('Error al intentar registrar el cliente', 'danger')

    return redirect(url_for('client.query_clients'))

@client_blueprint.route('/clientes/update_client/<int:IdCliente>', methods=['POST'])
def update_client(IdCliente):
    try:
        client = Cliente.query.get_or_404(IdCliente)
        
        client.persona.Cedula = int(request.form.get('Cedula', 0))
        client.persona.Nombre = request.form.get('Nombre', '').strip()
        client.persona.Apellido = request.form.get('Apellido', '').strip()
        client.persona.Telefono = int(request.form.get('Telefono', 0))
        
        client.IdParroquia = request.form.get('IdParroquia')
        client.Direccion = request.form.get('Direccion', '').strip()

        db.session.commit()
        flash('Cliente modificado con éxito.', 'success')

    except Exception:
        db.session.rollback()
        flash('Error al intentar modificar el cliente', 'danger')

    return redirect(url_for('client.query_clients'))

@client_blueprint.route('/clientes/delete_client/<int:IdCliente>', methods=['POST'])
def delete_client(IdCliente):
    try:
        client = Cliente.query.get_or_404(IdCliente)
        db.session.delete(client)
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
        
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar el cliente porque tiene ventas u operaciones asociadas', 'danger')
        
    except Exception:
        db.session.rollback()
        flash('Error al intentar eliminar el cliente', 'danger')
    
    return redirect(url_for('client.query_clients'))

@client_blueprint.route('/clientes/client_report')
def generate_client_report():
    clients = Cliente.query.join(Cliente.persona).order_by(Persona.Nombre.asc()).all()
    ruta_static = os.path.join(current_app.root_path, 'static')
    
    html_renderizado = render_template('pdf_client.html', clients=clients, base_dir=ruta_static)
    output_memoria = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(html_renderizado, dest=output_memoria)
    
    if pisa_status.err:
        return "Error al generar el PDF", 500
        
    output_memoria.seek(0)
    
    response = make_response(output_memoria.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_clientes.pdf'
    
    return response