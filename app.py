from flask import Flask, render_template, request, flash, url_for, redirect
import urllib.request, json, ipdb;
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'

db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch

#rota
@app.route('/', methods=["GET","POST"])
def principal():

    if request.method == "POST":
        if request.form.get("fruta"):
            frutas.append(request.form.get("fruta"))
    #reinderizando dentro do html
    return render_template('index.html', frutas=frutas)

@app.route('/sobre', methods=["GET", "POST"])
def sobre():
    if request.method == "POST":
        if request.form.get("aluno") and request.form.get("nota"):
            registros.append({"aluno": request.form.get("aluno"), "nota": request.form.get("nota")})

    return render_template('sobre.html', registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):

    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=3bffa017bbed5d9bec50ad634274e64f"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=3bffa017bbed5d9bec50ad634274e64f"
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=3bffa017bbed5d9bec50ad634274e64f"
    elif propriedade == 'drama':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=3bffa017bbed5d9bec50ad634274e64f"
    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=3bffa017bbed5d9bec50ad634274e64f"
        
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    #return jsondata['results']
    #return jsondata
    return render_template("filmes.html", filmes=jsondata['results'])

@app.route('/cursos')
def lista_cursos():
    #retorna o conteudo da tabela cursos mapeado no SQLAlquemy, reinderizando na pagina cursos.html
    return render_template("cursos.html", cursos=cursos.query.all())

@app.route('/cria_curso', methods=["GET", "POST"])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == "POST":
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do formulário","error")
        else:
            curso = cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    #ipdb.set_trace()
    return render_template("novo_curso.html")

@app.route('/<int:id>/atualiza_curso', methods=["GET", "POST"])
def atualiza_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    return render_template("atualiza_curso.html", curso=curso)

# seta como ambiente de desenvolvimento
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
