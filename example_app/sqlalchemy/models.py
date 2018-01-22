import sqlalchemy as sqa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_name = "aalam_py_ang_testapp"


class Owners(Base):
    __tablename__ = "owners"
    __table_args__ = {'schema': db_name}

    id = sqa.Column(sqa.Integer, primary_key=True)
    email = sqa.Column(sqa.VARCHAR(32), nullable=False, unique=True)

    def __init__(self, email):
        self.email = email


class Items(Base):
    __tablename__ = "items"
    __table_args__ = {'schema': db_name}

    name = sqa.Column(sqa.VARCHAR(16), primary_key=True)
    type_ = sqa.Column(sqa.VARCHAR(16))
    owner = sqa.Column(sqa.Integer, sqa.ForeignKey(Owners.id))

    def __init__(self, name, type_, owner):
        self.name = name
        self.owner = owner
        self.type_ = type_
