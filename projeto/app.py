from flask import flask
from flark_sqlalchemy import SQLAlchemy
import os 

app = flask(__name__)

app.config ["SQLAlCHEMY_DATABASE_UR"] = "sqlite:///bibliteca.db"
app.config ["SQLAlCHEMY_TRACK_MODIFICATIONS"] = False

DB = SQLAlchemy(app)
from models import *
from controllers import *

if __name__== "__main__":
    with app.app_context():
     db.creat_all()

    app.run(debug=True)





