from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from ton_api import get_all_auctions

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.app_context().push()


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(250))
    date = db.Column(db.Integer)
    date_created = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Auction {}>'.format(self.domain)
    __table_args__ = (UniqueConstraint('domain', 'date',
                                       name='domainDateUniqueConstraint'),)


auctions = Auction.query.all()

for auction in auctions:
    print(auction.date_created)

tonapi_auctions = get_all_auctions()

for item in tonapi_auctions:
    auction = Auction(domain=item['domain'], date=int(item['date']))
    db.session.add(auction)
db.session.commit()


# @app.route('/')
# def nader():
#     return "Hi"
