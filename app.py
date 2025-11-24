from bottle import route, run, template, request, redirect, static_file, TEMPLATE_PATH
from database import session, Medico, Agendamento
from datetime import datetime
import hashlib
import os


TEMPLATE_PATH.insert(0, './view')


# ===========================================
#  ARQUIVOS ESTÁTICOS
# ===========================================
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


# ===========================================
#  PÁGINA INICIAL
# ===========================================
@route('/')
def home():
    return template('view/agend.html')


# ===========================================
#  ÁREA DO MÉDICO
# ===========================================
@route('/medico')
def medico():
    return template('view/logmedico.html')


@route('/login_medico', method='POST')
def login_medico_post():
    crm = request.forms.get('crm')
    senha = request.forms.get('senha')

    medico = session.query(Medico).filter_by(crm=crm).first()
    
    if not medico:
        return "<h2>CRM não encontrado!</h2><a href='/medico'>Voltar</a>"
    
    salt_hex = medico.salt
    senha_hash_salva = medico.senha
    
    salt_bt = bytes.fromhex(salt_hex)
    
    hash_digitado = hashlib.sha256(salt_bt + senha.encode()).hexdigest()
    
    if hash_digitado == senha_hash_salva:
        return f"<h2>Bem-vindo, Dr(a). {medico.nome}!</h2><br><a href='/medico'>Voltar</a>"
    else:
        return "<h2>Senha incorreta!</h2><a href='/medico'>Voltar</a>"


# ---------- CADASTRO DO MÉDICO ----------
@route('/cadastro_medico')
def cadastro_medico():
    return template('view/cadastromedico.html')


@route('/salvar_medico', method='POST')
def salvar_medico():
    nome = request.forms.get('nome')
    idade = int(request.forms.get('idade'))
    genero = request.forms.get('genero')
    crm = request.forms.get('crm')
    especialidade = request.forms.get('especialidade')
    senha = request.forms.get('senha')
    
    salt = os.urandom(16)
    salt_hex = salt.hex()
    
    senha_hash = hashlib.sha256(salt+ senha.encode()).hexdigest()

    novo = Medico(
        nome=nome,
        idade=idade,
        genero=genero,
        crm=crm,
        especialidade=especialidade,
        senha=senha_hash,
        salt = salt_hex
    )

    session.add(novo)
    session.commit()

    return f"""
        <h2>Médico cadastrado com sucesso!</h2>
        <p>{nome} — {especialidade}</p>
        <a href='/medico'>Voltar</a>
    """


# ===========================================
#  ÁREA DO PACIENTE
# ===========================================
@route('/paciente')
def paciente():
    return template('view/logpaciente.html')


@route('/enviar', method='POST')
def enviar_paciente():
    nome = request.forms.get('nome')
    telefone = request.forms.get('telefone')
    email = request.forms.get('email')
    return template('view/agendamento1.html', nome=nome, telefone=telefone, email=email)


# ===========================================
#  AGENDAMENTO 
# ===========================================
@route('/agendamento')
def agendamento():

    especialidades = (
        session.query(Medico.especialidade)
        .distinct()
        .order_by(Medico.especialidade)
        .all()
    )
    especialidades = [e[0] for e in especialidades]

    return template('view/agendamento1.html', especialidades=especialidades)


@route('/agendamento_etapa1', method='POST')
def agendamento_etapa1_post():
    idade = request.forms.get('idade')
    convenio = request.forms.get('convenio')
    especialidade = request.forms.get('especialidade')

    nome = request.forms.get('nome')
    telefone = request.forms.get('telefone')
    email = request.forms.get('email')

    return template(
        'view/agendamento2.html',
        idade=idade,
        convenio=convenio,
        especialidade=especialidade,
        nome=nome,
        telefone=telefone,
        email=email
    )


# ===========================================
#  AGENDAMENTO 
# ===========================================
@route('/agendamento_data')
def agendamento_data():
    return template('view/agendamento2.html')


@route('/confirmar_agendamento', method='POST')
def confirmar_agendamento():

    nome = request.forms.get('nome')    
    idade = int(request.forms.get('idade'))
    convenio = request.forms.get('convenio')
    especialidade = request.forms.get('especialidade')
    data = request.forms.get('data')
    hora = request.forms.get('hora')

    data_conv = datetime.strptime(data, "%Y-%m-%d").date()
    hora_conv = datetime.strptime(hora, "%H:%M").time()

    novo = Agendamento(
        nome=nome,   
        idade=idade,
        convenio=convenio,
        especialidade=especialidade,
        data=data_conv,
        hora=hora_conv
    )

    session.add(novo)
    session.commit()

    return f"""
        <h2>Consulta Agendada!</h2>
        <p><b>Nome:</b> {nome}</p>
        <p><b>Idade:</b> {idade}</p> 
        <p><b>Convênio:</b> {convenio}</p> 
        <p><b>Especialidade:</b> {especialidade}</p> 
        <p><b>Data:</b> {data}</p> 
        <p><b>Hora:</b> {hora}</p> 
        <br> <a href='/paciente'>Voltar</a>
    """


run(host='localhost', port=8080, debug=True, reloader=True)
