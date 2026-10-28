from app import db
livros_autores = db.Table(
    "livros_autores",
    db.Column("livro_id", db.Integer, db.ForeignKey("livro.id")),
    db.Column("autor_id", db.Integer, db.ForeignKey("autor.id"))
)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer)
    autores = db.relationship(
        "Autor",
        secondary=livros_autores,
        back_populates="livros"
    )

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    livros = db.relationship(
        "Livro",
        secondary=livros_autores,
        back_populates="autores"
    )

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"))
    situacao = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    situacao = db.Column(db.String(30), default="Emprestado")
    livro = db.relationship("Livro")
    usuario = db.relationship("Usuario", back_populates="emprestimos")

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)


    
