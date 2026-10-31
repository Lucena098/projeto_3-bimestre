from flask import (
    render_template, request, redirect,
    url_for, flash
)
from extensions import app
from database import db
from models import Autor, Livro, Leitor, Emprestimo

@app.route("/")
def index():
    autores = Autor.query.all()
    livros = Livro.query.all()
    leitura = Leitor.query.all()
    emprestimos = Emprestimo.query.all()
    return render_template(
        "index.html",
        autores=autores,
        livros=livros,
        leitura=leitura,
        emprestimos=emprestimos
    )

# Cadastra o escritor do livro
@app.route("/autores", methods=["POST"])
def cadastrar_autor():
    nome = request.form["nome"].strip()
    if nome:
        autor = Autor(nome=nome)
        db.session.add(autor)
        db.session.commit()
        flash("Autor cadastrado!")
    return redirect(url_for("index"))

# cadastra o livro escritor
@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    titulo = request.form["titulo"].strip()
    ano = request.form.get("ano")
    autores_id = request.form.get("autores_id")
    if not titulo or not autores_id:
        flash("Por favor digite os dados dos livros.")
        return redirect(url_for("index"))
    autor = db.session.get(Autor, int(autores_id))
    if not autor:
        flash("O autor do livro não foi localizado.")
        return redirect(url_for("index"))
    livro = Livro(
        titulo=titulo,
        ano=int(ano) if ano else None,
        autor=autor
    )
    db.session.add(livro)
    db.session.commit()
    flash("Livro cadastrado!")
    return redirect(url_for("index"))

# Cadastra os leitores de livros
@app.route("/leitura", methods=["POST"])
def cadastrar_leitor():
    nome = request.form["nome"].strip()
    email = request.form["email"].strip()
    if not nome or not email:
        flash("Preencher por favor todos os dados solicitados.")
        return redirect(url_for("index"))
    if Leitor.query.filter_by(email=email).first():
        flash("Este e-mail já foi cadastrado por algum usuário.")
        return redirect(url_for("index"))
    leitor = Leitor(nome=nome, email=email)
    db.session.add(leitor)
    db.session.commit()
    flash("O leitor de livros foi cadastrado!")
    return redirect(url_for("index"))

# Cadastra o empréstimo (vínculo N:N).
@app.route("/temporaria_livros", methods=["POST"])
def cadastrar_emprestimo():
    leitor_id = request.form.get("leitor_id")
    livro_id = request.form.get("livro_id")
    data = request.form.get("data")
    if not leitor_id or not livro_id or not data:
        flash("Por favor preencha todos os dados para o empréstimo do livro.")
        return redirect(url_for("index"))
    leitor = db.session.get(Leitor, int(leitor_id))
    livro = db.session.get(Livro, int(livro_id))
    if not leitor or not livro:
        flash("O leitor ou livro não foram encontrados.")
        return redirect(url_for("index"))
    temporaria_livros = Emprestimo(
        leitor=leitor,
        livro=livro,
        data=data
    )
    db.session.add(temporaria_livros)
    db.session.commit()
    flash("O empréstimo foi registrado!")
    return redirect(url_for("index"))

# Registra a devolução do livro
@app.route("/temporaria_livros/devolver/<int:id>", methods=["POST"])
def devolver_livro(id):
    temporaria_livros = db.session.get(Emprestimo, id)
    if temporaria_livros:
        temporaria_livros.situacao = "Devolvido"
        db.session.commit()
        flash("A devolução foi registrada!")
    return redirect(url_for("index"))

# Remover o vínculo N:N
@app.route("/temporaria_livros/remover/<int:id>", methods=["POST"])
def remover_emprestimo(id):
    temporaria_livros = db.session.get(Emprestimo, id)
    if temporaria_livros:
        db.session.delete(temporaria_livros)
        db.session.commit()
        flash("O empréstimo foi resolvido!")
    return redirect(url_for("index"))

# Editar o autor do livro
@app.route("/autores/editar/<int:id>", methods=["GET", "POST"])
def editar_autor(id):
    autor = db.session.get(Autor, id)
    if not autor:
        flash("O autor do livro não foi localizado.")
        return redirect(url_for("index"))
    if request.method == "POST":
        autor.nome = request.form["nome"].strip()
        db.session.commit()
        flash("O autor do livro foi atualizado")
        return redirect(url_for("index"))
    return render_template(
        "editar.html",
        titulo="Editar autor",
        registro=autor,
        campo="nome"
    )

# Editar o leitor de livros
@app.route("/leitura/editar/<int:id>", methods=["GET", "POST"])
def editar_leitor(id):
    leitor = db.session.get(Leitor, id)
    if not leitor:
        flash("O leitor não foi localizado.")
        return redirect(url_for("index"))
    if request.method == "POST":
        leitor.nome = request.form["nome"].strip()
        leitor.email = request.form["email"].strip()
        extra = Leitor.query.filter_by(
            email=leitor.email
        ).first()
        if extra and extra.id != leitor.id:
            flash("Este e-mail já pertence a outro leitor, outro usuário.")
            return redirect(url_for("editar_leitor", id=id))
        db.session.commit()
        flash("O leitor foi atualizado!")
        return redirect(url_for("index"))
    return render_template(
        "editar.html",
        titulo="Editar leitor",
        registro=leitor,
        campo="nome"
    )

# Remover o autor
@app.route("/autores/remover/<int:id>", methods=["POST"])
def remover_autor(id):
    autor = db.session.get(Autor, id)
    if autor:
        if autor.livros:
            flash("Não é possível remover o autor com um livro cadastrado.")
        else:
            db.session.delete(autor)
            db.session.commit()
            flash("Autor foi removido!")
    return redirect(url_for("index"))


# Remover o livro
@app.route("/livros/remover/<int:id>", methods=["POST"])
def remover_livro(id):
    livro = db.session.get(Livro, id)
    if livro:
        if livro.temporaria_livros:
            flash("Não é possível remover um livro com empréstimos registrados.")
        else:
            db.session.delete(livro)
            db.session.commit()
            flash("Livro removido!")
    return redirect(url_for("index"))

# Remover o leitor do livro
@app.route("/leitura/remover/<int:id>", methods=["POST"])
def remover_leitor(id):
    leitor = db.session.get(Leitor, id)
    if leitor:
        if leitor.temporaria_livros:
            flash("Não é possível remover um leitor com empréstimos registrados.")
        else:
            db.session.delete(leitor)
            db.session.commit()
            flash("Leitor removido!")
    return redirect(url_for("index"))





