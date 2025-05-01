from app import db
from datetime import datetime, timezone

class Internacao(db.Model):
    __tablename__ = 'internacoes'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_internacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    data_alta = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='internado')
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    paciente = db.relationship('Paciente', backref=db.backref('internacoes', lazy=True))

    def __repr__(self):
        return f'<Internacao {self.id}>'