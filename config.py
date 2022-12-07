import pathlib
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)


basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.app_context().push()


# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'db.sqlite3'}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# engine = create_engine("postgresql://postgres:102030@localhost/fragment")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:102030@localhost/fragment"


db = SQLAlchemy(app)
ma = Marshmallow(app)
