from app.main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Asset(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ticker = db.Column(db.String())
    date = db.Column(db.DateTime())
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float())

    def __repr__(self):
        return self.ticker
