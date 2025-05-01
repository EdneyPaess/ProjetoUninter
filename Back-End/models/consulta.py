from app import db
from datetime import datetime, timezone

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendada')
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))

    def __repr__(self):
        return f'<Consulta {self.id}>'