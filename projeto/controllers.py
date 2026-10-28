emprestimo.situacao = "Devolvido"
        db.session.commit()
        flash("Devolução registrada!")

    return redirect(url_for("index"))
@app.route("/livros/remover/<int:id>", methods=["POST"])
def remover_livro(id):
    livro = db.session.get(Livro, id)
    if livro:
        if Emprestimo.query.filter_by(livro_id=id).first():
            flash("Não é possível remover um livro com empréstimos registrados.")
        else:
            livro.autores.clear()
            db.session.delete(livro)
            db.session.commit()
            flash("Livro removido!")
    return redirect(url_for("index"))
