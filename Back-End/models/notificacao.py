from app import db
from datetime import datetime, timezone

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    paciente = db.relationship('Paciente', backref=db.backref('notificacoes', lazy=True))

    def __repr__(self):
        return f'<Notificacao {self.id}>'
