from models import Auction
from config import db
from config import app

app.app_context().push()

db.drop_all()
db.create_all()
