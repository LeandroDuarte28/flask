from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def principal():
    nome = "Leandro"
    idade = 44
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

#http://127.0.0.1:5000/