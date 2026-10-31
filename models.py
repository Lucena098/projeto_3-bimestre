from database import db

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    livros = db.relationship(
        "Livro",
        back_populates="autor"
    )

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer)
    autores_id = db.Column(
        db.Integer,
        db.ForeignKey("autor.id"),
        nullable=False
    )
    autor = db.relationship(
        "Autor",
        back_populates="livros"
    )
    temporaria_livros = db.relationship(
        "Emprestimo",
        back_populates="livro"
    )

class Leitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    temporaria_livros = db.relationship(
        "Emprestimo",
        back_populates="leitor"
    )

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leitor_id = db.Column(
        db.Integer,
        db.ForeignKey("leitor.id"),
        nullable=False
    )
    livro_id = db.Column(
        db.Integer,
        db.ForeignKey("livro.id"),
        nullable=False
    )
    data = db.Column(db.String(10), nullable=False)
    situacao = db.Column(
        db.String(30),
        default="Emprestado"
    )
    leitor = db.relationship(
        "Leitor",
        back_populates="temporaria_livros"
    )
    livro = db.relationship(
        "Livro",
        back_populates="temporaria_livros"
    )




