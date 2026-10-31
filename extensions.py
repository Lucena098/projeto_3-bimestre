from flask import Flask
from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "book2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



