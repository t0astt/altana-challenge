from . import db
from typing import Optional


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

    def __init__(self,
                 nr_cnpj: int,
                 nm_fantasia: str,
                 sg_uf: str,
                 in_cpf_cnpj: int,
                 nr_cpf_cnpj_socio: Optional[int],
                 cd_qualificacao_socio: int,
                 ds_qualificacao_socio: str,
                 nm_socio: str):
        self.nr_cnpj = nr_cnpj
        self.nm_fantasia = nm_fantasia
        self.sg_uf = sg_uf
        self.in_cpf_cnpj = in_cpf_cnpj
        self.nr_cpf_cnpj_socio = nr_cpf_cnpj_socio
        self.cd_qualificacao_socio = cd_qualificacao_socio
        self.ds_qualificacao_socio = ds_qualificacao_socio
        self.nm_socio = nm_socio

    def to_json(self) -> dict:
        """
        Returns a serializable dictionary representation of the class
        """
        return {
            "nr_cnpj": self.nr_cnpj,
            "nm_fantasia": self.nm_fantasia,
            "sg_uf": self.sg_uf,
            "in_cpf_cnpj": self.in_cpf_cnpj,
            "nr_cpf_cnpj_socio": self.nr_cpf_cnpj_socio,
            "cd_qualificacao_socio": self.cd_qualificacao_socio,
            "ds_qualificacao_socio": self.ds_qualificacao_socio,
            "nm_socio": self.nm_socio
        }

