from . import db


class Company(db.Model):
    """
    Model class backed by the accompanying database table
    """
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    nr_cnpj = db.Column(db.BigInteger, unique=False, nullable=True)
    nm_fantasia = db.Column(db.String(255), unique=False, nullable=True, index=True)
    sg_uf = db.Column(db.String(255), unique=False, nullable=False)
    in_cpf_cnpj = db.Column(db.Integer, unique=False, nullable=False)
    nr_cpf_cnpj_socio = db.Column(db.BigInteger, unique=False, nullable=True)
    cd_qualificacao_socio = db.Column(db.Integer, unique=False, nullable=False)
    ds_qualificacao_socio = db.Column(db.String(255), unique=False, nullable=False)
    nm_socio = db.Column(db.String(255), unique=False, nullable=False, index=True)
