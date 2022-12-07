from config import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(250))
    price = db.Column(db.BigInteger)
    date = db.Column(db.Integer)
    time_created = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow)
    time_updated = db.Column(db.DateTime(
        timezone=True), onupdate=datetime.utcnow)
    # date_created = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Auction {}>'.format(self.domain)
    __table_args__ = (UniqueConstraint('domain', 'date',
                                       name='domainDateUniqueConstraint'),)
