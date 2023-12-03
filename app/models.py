import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Books(db.Model):
    __tablename__ = 'books'
    ISBN = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    author = db.Column(db.String(100))
    min_age = db.Column(db.Integer)
    rating = db.Column(db.Float)
    review_number = db.Column(db.Integer)
    available = db.Column(db.Boolean)
    link = db.Column(db.String(200))
