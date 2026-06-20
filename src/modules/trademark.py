from flask import Blueprint, render_template
from models import db, Marca  

# Create the Blueprint for the branding module
trademark_blueprint = Blueprint('trademark', __name__)

@trademark_blueprint.route('/marcas', methods=['GET'])
def query_trademarks():
    # Query all brands using the fields in models.py
    trademarks = Marca.query.all()
    return render_template('trademark.html', trademarks=trademarks)