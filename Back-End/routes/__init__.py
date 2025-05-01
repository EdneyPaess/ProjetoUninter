from datetime import datetime, timezone
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models.paciente import Paciente
from models.profissional import Profissional
from models.usuario import Usuario
from models.consulta import Consulta
from models.notificacao import Notificacao
from models.teleconsulta import Teleconsulta
from models.internacao import Internacao
from models.prescricao import Prescricao
from models.prontuario import Prontuario


# Endpoint para criar um novo paciente
@app.route("/pacientes", methods=["POST"])
@jwt_required()
def criar_paciente():
    data = request.get_json()

    # Validação básica (nome, cpf, data_nascimento são obrigatórios)
    if not data or not all(k in data for k in ("nome", "cpf", "data_nascimento")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    # Verifica se já existe paciente com o mesmo CPF
    paciente_existente = Paciente.query.filter_by(cpf=data["cpf"]).first()
    if paciente_existente:
        return jsonify({"error": "Paciente com este CPF já existe"}), 409

    try:
        # Criar novo paciente
        novo_paciente = Paciente(
            nome=data["nome"],
            cpf=data["cpf"],
            data_nascimento=datetime.strptime(data["data_nascimento"], "%d/%m/%Y"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            endereco=data.get("endereco"),
        )

        db.session.add(novo_paciente)
        db.session.commit()

        return jsonify({"message": "Paciente cadastrado com sucesso"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Endpoint para listar todos os pacientes
@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = []
    
    if not paciente:
        return jsonify({'error': 'Nenhum paciente encontrado'}), 404

    for paciente in pacientes:
        resultado.append(
            {
                "id": paciente.id,
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "data_nascimento": paciente.data_nascimento.strftime("%d/%m/%Y"),
                "email": paciente.email,
                "telefone": paciente.telefone,
                "endereco": paciente.endereco,
                "criado_em": paciente.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    return jsonify(resultado), 200
    


# Endpoint para agendar nova consulta
@app.route('/consultas', methods=['POST'])
@jwt_required()
def agendar_consulta():
    data = request.get_json()

    if not data or not all(k in data for k in ('paciente_id', 'profissional_id', 'especialidade', 'data_hora')):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400
    

    paciente = Paciente.query.get(data['paciente_id'])
    if not paciente:
        return jsonify({'error': 'Paciente não encontrado'}), 404

    profissional = Profissional.query.get(data['profissional_id'])
    if not profissional:
        return jsonify({'error': 'Profissional não encontrado'}), 404

    try:
        nova_consulta = Consulta(
            paciente_id=paciente.id,
            profissional_id=profissional.id,
            especialidade=data['especialidade'],
            data_hora=datetime.strptime(data['data_hora'], '%d/%m/%Y %H:%M:%S')
        )

        db.session.add(nova_consulta)
        db.session.commit()

        return jsonify({'message': 'Consulta agendada com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint para listar todas as consultas
@app.route('/consultas', methods=['GET'])
def listar_consultas():
    consultas = Consulta.query.all()
    resultado = []

    for consulta in consultas:
        resultado.append({
            'id': consulta.id,
            'paciente_id': consulta.paciente_id,
            'profissional_id': consulta.profissional_id,
            'profissional_nome': consulta.profissional.nome if consulta.profissional else None,
            'especialidade': consulta.especialidade,
            'data_hora': consulta.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
            'status': consulta.status,
            'criado_em': consulta.criado_em.strftime('%d/%m/%Y %H:%M:%S')
        })

    return jsonify(resultado), 200

# Endpoint para cancelar uma consulta
@app.route("/consultas/<int:id>", methods=["PUT"])
@jwt_required()
def cancelar_consulta(id):
    consulta = Consulta.query.get(id)

    if not consulta:
        return jsonify({"error": "Consulta não encontrada"}), 404

    if consulta.status == "cancelada":
        return jsonify({"error": "Consulta já foi cancelada"}), 400

    try:
        consulta.status = "cancelada"
        db.session.commit()

        return jsonify({"message": "Consulta cancelada com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Endpoint de Cadastro de usuario
@app.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()

    if not data or not all(k in data for k in ("nome", "email", "senha")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já cadastrado"}), 409

    try:
        novo_usuario = Usuario(
            nome=data["nome"],
            email=data["email"],
            senha=generate_password_hash(data["senha"]),
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Endpoint de login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "senha")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if not usuario or not check_password_hash(usuario.senha, data["senha"]):
        return jsonify({"error": "Email ou senha inválidos"}), 401

    # Geração do token JWT
    access_token = create_access_token(identity=str(usuario.id))

    return jsonify({"access_token": access_token}), 200


# Criar nova notificação para paciente
@app.route("/notificacoes", methods=["POST"])
@jwt_required()
def criar_notificacao():
    data = request.get_json()

    if not data or not all(k in data for k in ("paciente_id", "mensagem")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    paciente = Paciente.query.get(data["paciente_id"])
    if not paciente:
        return jsonify({"error": "Paciente não encontrado"}), 404

    try:
        nova_notificacao = Notificacao(
            paciente_id=data["paciente_id"], mensagem=data["mensagem"]
        )

        db.session.add(nova_notificacao)
        db.session.commit()

        return jsonify({"message": "Notificação criada com sucesso"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Listar notificações de um paciente
@app.route("/notificacoes/<int:paciente_id>", methods=["GET"])
@jwt_required()
def listar_notificacoes(paciente_id):
    notificacoes = Notificacao.query.filter_by(paciente_id=paciente_id).all()
    resultado = []
    
    if not notificacao:
        return jsonify({'error':'Nenhuma notificação encontrada'}), 404

    for notificacao in notificacoes:
        resultado.append(
            {
                "id": notificacao.id,
                "mensagem": notificacao.mensagem,
                "lida": notificacao.lida,
                "criado_em": notificacao.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    return jsonify(resultado), 200

# Endpoint para criar telemedicina
@app.route("/teleconsultas", methods=["POST"])
@jwt_required()
def criar_teleconsulta():
    data = request.get_json()

    if not data or "consulta_id" not in data:
        return jsonify({"error": "ID da consulta é obrigatório"}), 400

    consulta = Consulta.query.get(data["consulta_id"])
    if not consulta:
        return jsonify({"error": "Consulta não encontrada"}), 404

    if Teleconsulta.query.filter_by(consulta_id=consulta.id).first():
        return jsonify({"error": "Teleconsulta já criada para esta consulta"}), 409

    try:
        # Link fictício
        link = f"https://localhost/consulta/{consulta.id}"

        nova_teleconsulta = Teleconsulta(consulta_id=consulta.id, link=link)

        db.session.add(nova_teleconsulta)
        db.session.commit()

        return (
            jsonify({"message": "Teleconsulta criada com sucesso", "link": link}),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Listar teleconsultas de um paciente
@app.route('/teleconsultas/<int:paciente_id>', methods=['GET'])
@jwt_required()
def listar_teleconsultas(paciente_id):
    teleconsultas = Teleconsulta.query.join(Consulta).filter(Consulta.paciente_id == paciente_id).all()
    resultado = []
    
    if not teleconsulta:
        return jsonify({'error':'Nenhuma teleconsulta encontrada'}), 404

    for teleconsulta in teleconsultas:
        resultado.append({
            'id': teleconsulta.id,
            'consulta_id': teleconsulta.consulta.id,
            'profissional_id': teleconsulta.consulta.profissional_id,
            'profissional_nome': teleconsulta.consulta.profissional.nome if teleconsulta.consulta.profissional else None,
            'especialidade': teleconsulta.consulta.especialidade,
            'data_consulta': teleconsulta.consulta.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
            'link': teleconsulta.link,
            'status': teleconsulta.status,
            'criado_em': teleconsulta.criado_em.strftime('%d/%m/%Y %H:%M:%S')
        })

    return jsonify(resultado), 200


# Endpoint pra criar novo profissional
@app.route('/profissionais', methods=['POST'])
@jwt_required()
def criar_profissional():
    data = request.get_json()

    if not data or not all(k in data for k in ('nome', 'especialidade')):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400

    try:
        novo_profissional = Profissional(
            nome=data['nome'],
            especialidade=data['especialidade'],
            email=data.get('email'),
            telefone=data.get('telefone')
        )

        db.session.add(novo_profissional)
        db.session.commit()

        return jsonify({'message': 'Profissional cadastrado com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint para registrar internacao
@app.route('/internacoes', methods=['POST'])
@jwt_required()
def registrar_internacao():
    data = request.get_json()

    if not data or 'paciente_id' not in data:
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400

    paciente = Paciente.query.get(data['paciente_id'])
    if not paciente:
        return jsonify({'error': 'Paciente não encontrado'}), 404

    try:
        nova_internacao = Internacao(
            paciente_id=paciente.id
        )

        db.session.add(nova_internacao)
        db.session.commit()

        return jsonify({'message': 'Internação registrada com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Dar alta em internação
@app.route('/internacoes/<int:id>', methods=['PUT'])
@jwt_required()
def dar_alta_internacao(id):
    internacao = Internacao.query.get(id)

    if not internacao:
        return jsonify({'error': 'Internação não encontrada'}), 404

    if internacao.status == 'alta':
        return jsonify({'error': 'Paciente já teve alta'}), 400

    try:
        internacao.status = 'alta'
        internacao.data_alta = datetime.now(timezone.utc)

        db.session.commit()

        return jsonify({'message': 'Alta registrada com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Listar internações
@app.route('/internacoes', methods=['GET'])
@jwt_required()
def listar_internacoes():
    internacoes = Internacao.query.all()
    resultado = []

    for internacao in internacoes:
        resultado.append({
            'id': internacao.id,
            'paciente_id': internacao.paciente_id,
            'data_internacao': internacao.data_internacao.strftime('%d/%m/%Y %H:%M:%S'),
            'data_alta': internacao.data_alta.strftime('%d/%m/%Y %H:%M:%S') if internacao.data_alta else None,
            'status': internacao.status
        })

    return jsonify(resultado), 200

# Listar profissionais
@app.route('/profissionais', methods=['GET'])
@jwt_required()
def listar_profissionais():
    profissionais = Profissional.query.all()
    resultado = []

    if not profissionais:
        return jsonify({'error': 'Nenhum profissional encontrado'}), 404

    for prof in profissionais:
        resultado.append({
            'id': prof.id,
            'nome': prof.nome,
            'especialidade': prof.especialidade,
            'email': prof.email,
            'telefone': prof.telefone,
            'criado_em': prof.criado_em.strftime('%d/%m/%Y %H:%M:%S')
        })

    return jsonify(resultado), 200


# Criar novo prontuário
@app.route("/prontuarios", methods=["POST"])
@jwt_required()
def criar_prontuario():
    data = request.get_json()

    if not data or not all(k in data for k in ("consulta_id", "anotacoes")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    consulta = Consulta.query.get(data["consulta_id"])
    if not consulta:
        return jsonify({"error": "Consulta não encontrada"}), 404

    if Prontuario.query.filter_by(consulta_id=consulta.id).first():
        return jsonify({"error": "Prontuário já registrado para esta consulta"}), 409

    try:
        novo_prontuario = Prontuario(
            consulta_id=consulta.id, anotacoes=data["anotacoes"]
        )

        db.session.add(novo_prontuario)
        db.session.commit()

        return jsonify({"message": "Prontuário registrado com sucesso"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Criar nova prescrição
@app.route("/prescricoes", methods=["POST"])
@jwt_required()
def criar_prescricao():
    data = request.get_json()

    if not data or not all(k in data for k in ("consulta_id", "medicamentos")):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    consulta = Consulta.query.get(data["consulta_id"])
    if not consulta:
        return jsonify({"error": "Consulta não encontrada"}), 404

    if Prescricao.query.filter_by(consulta_id=consulta.id).first():
        return jsonify({"error": "Prescrição já registrada para esta consulta"}), 409

    try:
        nova_prescricao = Prescricao(
            consulta_id=consulta.id, medicamentos=data["medicamentos"]
        )

        db.session.add(nova_prescricao)
        db.session.commit()

        return jsonify({"message": "Prescrição registrada"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Endpoint para listar os prontuarios de um paciente
@app.route("/prontuarios/<int:paciente_id>", methods=["GET"])
@jwt_required()
def listar_prontuarios(paciente_id):
    # Buscar todas as consultas do paciente
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).all()
    resultado = []
    
    if not consulta.prontuario:
        return jsonify({'error':'Nenhum prontuario encontrado'}), 404

    for consulta in consultas:
        if consulta.prontuario:
            resultado.append(
                {
                    "consulta_id": consulta.id,
                    "anotacoes": consulta.prontuario.anotacoes,
                    "criado_em": consulta.prontuario.criado_em.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                }
            )

    return jsonify(resultado), 200


# Listar prescrições de um paciente
@app.route("/prescricoes/<int:paciente_id>", methods=["GET"])
@jwt_required()
def listar_prescricoes(paciente_id):
    # Buscar todas as consultas do paciente
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).all()
    resultado = []

    if not consulta.prescricao:
        return jsonify({"error": "Nenhuma prescrição encontrada"})

    for consulta in consultas:
        if consulta.prescricao:
            resultado.append(
                {
                    "consulta_id": consulta.id,
                    "medicamentos": consulta.prescricao.medicamentos,
                    "criado_em": consulta.prescricao.criado_em.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                }
            )

    return jsonify(resultado), 200
