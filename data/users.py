import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String(30), unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(200), nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def __repr__(self):
        return ' '.join([f"<Colonist>", str(self.id), self.name, self.login])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
