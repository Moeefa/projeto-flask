from flask import request, redirect, url_for, render_template
from app import db
from . import app
from app.models import Item, Pessoa

@app.route('/')
def index():
    items_ = Item.query.all()
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

#Rotas da Model Pessoa

@app.route('/pessoas')
def pessoa_index():
    pessoas = Pessoa.query.all()
    return render_template('pessoa/index.html', pessoas=pessoas)

@app.route('/pessoa/create',  methods=['GET', 'POST'])
def pessoa_create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        new_pessoa = Pessoa(
            nome=nome, 
            email=email, 
            telefone=telefone,
            endereco=endereco
        )
        db.session.add(new_pessoa)
        db.session.commit()
        return redirect(url_for('pessoa_index')) 
    return render_template('pessoa/create.html')

@app.route('/pessoa/update/<int:id>', methods=['GET', 'POST'])
def pessoa_update(id):
    pessoa = Pessoa.query.get_or_404(id)
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.email = request.form.get('email')
        pessoa.telefone = request.form.get('telefone')
        pessoa.endereco = request.form.get('endereco')
        db.session.commit()
        return redirect(url_for('pessoa_index'))
    return render_template('pessoa/update.html', pessoa=pessoa)

@app.route('/pessoa/delete/<int:id>')
def pessoa_delete(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('pessoa_index'))