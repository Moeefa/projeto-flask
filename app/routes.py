from flask import request, redirect, url_for, render_template
from app import db
from . import app
from app.models import Item, Category

@app.route('/')
def index():
    items_ = Item.query.all()
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = request.form.get('category_id')

        new_item = Item(name=name, description=description, category_id=category_id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    categories = Category.query.all()
    return render_template('create.html', categories=categories)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form.get('category_id')  # Atualizar categoria
        db.session.commit()
        return redirect(url_for('index'))
    
    # Passar as categorias para o template
    categories = Category.query.all()
    return render_template('update.html', item=item, categories=categories)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/categories')
def category_index():
    categories = Category.query.all()
    return render_template('category/index.html', categories=categories)

@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('category_index'))
    return render_template('category/create.html')

@app.route('/category/update/<int:id>', methods=['GET', 'POST'])
def category_update(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        return redirect(url_for('category_index'))
    return render_template('category/update.html', category=category)

@app.route('/category/delete/<int:id>')
def category_delete(id):
    category = Category.query.get_or_404(id)
    
    # Verificar se a categoria tem itens associados
    if category.items:
        # Opção 1: Definir a categoria dos itens como nula
        for item in category.items:
            item.category_id = None
        
        # Opção 2 (alternativa): Excluir os itens associados à categoria
        # for item in category.items:
        #     db.session.delete(item)
    
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category_index'))

# Rota adicional para visualizar itens de uma categoria específica
@app.route('/category/<int:id>/items')
def category_items(id):
    category = Category.query.get_or_404(id)
    return render_template('category/items.html', category=category)
