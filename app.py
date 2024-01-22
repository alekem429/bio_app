from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from bioapp.routes import main
from bioapp.services.db_context import db


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

app.app_context().push()
# db = SQLAlchemy(app)

app.register_blueprint(main)

app.run(debug=True)