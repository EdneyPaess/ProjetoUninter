from app import db
from datetime import datetime, timezone

class Profissional(db.Model):
    __tablename__ = 'profissionais'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    consultas = db.relationship('Consulta', backref='profissional', lazy=True)

    def __repr__(self):
        return f'<Profissional {self.nome}>'