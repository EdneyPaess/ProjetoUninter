from app import db
from datetime import datetime, timezone

class Prescricao(db.Model):
    __tablename__ = 'prescricoes'

    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    medicamentos = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    consulta = db.relationship('Consulta', backref=db.backref('prescricao', uselist=False))

    def __repr__(self):
        return f'<Prescricao {self.id}>'