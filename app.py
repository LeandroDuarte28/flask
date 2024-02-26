from flask import Flask, render_template
app = Flask(__name__)

#rota
@app.route('/')
def principal():
    nome = "Leandro"
    idade = 44
    #reinderizando dentro do html
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Acesso para o servidor
# http://127.0.0.1:5000/