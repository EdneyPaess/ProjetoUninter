from app import db
from datetime import datetime, timezone

class Teleconsulta(db.Model):
    __tablename__ = 'teleconsultas'

    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    consulta = db.relationship('Consulta', backref=db.backref('teleconsulta', uselist=False))

    def __repr__(self):
        return f'<Teleconsulta {self.id}>'