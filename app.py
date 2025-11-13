from bottle import Bottle, run, static_file, request, template

app = Bottle()


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/')
@app.route('/inicio')
def inicio():
    return template('view/agend.html')


@app.route('/paciente')
def paciente():
    return template('view/log.html')


@app.route('/medico')
def medico():
    return "<h2>Área do Médico</h2>"


@app.post('/enviar')
def enviar():
    nome = request.forms.get('nome')
    numero = request.forms.get('numero')
    return template('view/log.html', nome=nome, numero=numero)


if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True)