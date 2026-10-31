from app import app
from database import db
from models import Autor, Livro, Leitor, Emprestimo

with app.app_context():
    db.create_all()
    if not Autor.query.first():
        autor = Autor(nome="Joanne Rowling")
        leitor = Leitor(
            nome="Laura Azevedo",
            email="laura@email.com"
        )
        livro = Livro(
            titulo="Harry Potter e o Prisioneiro de Azkaban",
            ano=1999,
            autor=autor
        )
        emprestimo = Emprestimo(
            leitor=leitor,
            livro=livro,
            data="2026-10-10"
        )
        db.session.add_all([
            autor, leitor, livro, emprestimo
        ])
        db.session.commit()
        print("Os dados iniciais já foram cadastrados!")
    else:
        print("O banco de dados já possui oregistro.")



