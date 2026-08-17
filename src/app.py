from flask import Flask
from models import db
# We imported the blueprint from the .py files
from modules.trademark import trademark_blueprint
from modules.product import product_blueprint
from modules.buys import buy_blueprint
from modules.statistics import stats_blueprint

app = Flask(__name__)

app.secret_key = 'ClaveSuperArrechisimaeñeñe'

# Configuring the PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/SISGE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# We initialize the database
db.init_app(app)

# We registered the blueprint in the central application
app.register_blueprint(trademark_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(buy_blueprint)
app.register_blueprint(stats_blueprint)

# PostgreSQL tables are created if they are not already created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)