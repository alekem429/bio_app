from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from services.db_context import *
from routes import routes
app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['CORS_HEADERS'] = 'Content-Type'

# db = SQLAlchemy()

app.app_context().push()

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(routes.main)

if __name__ == "__main__":
    app.run(debug=True)
