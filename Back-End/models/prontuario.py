from app import db
from datetime import datetime, timezone

class Prontuario(db.Model):
    __tablename__ = 'prontuarios'

    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    anotacoes = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    consulta = db.relationship('Consulta', backref=db.backref('prontuario', uselist=False))

    def __repr__(self):
        return f'<Prontuario {self.id}>'