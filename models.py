from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as _sql
import datetime as _dt
import passlib.hash as _hash


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    last_name = _sql.Column(_sql.String)


    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
