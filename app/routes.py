from flask import (request, redirect, url_for, render_template, flash,
                   jsonify)
from app import db
from . import app
from app.models import (Funcionarios, Produtos, Filial, Sensores,
                        Ambiente, Movimentacao, Estoque)
from datetime import datetime


# Dashboard Principal
@app.route('/')
def index():
    """Dashboard principal com estatísticas gerais"""
    total_produtos = Produtos.query.filter_by(ativo=True).count()
    total_funcionarios = Funcionarios.query.filter_by(ativo=True).count()
    total_filiais = Filial.query.filter_by(ativo=True).count()
    total_ambientes = Ambiente.query.filter_by(ativo=True).count()

    # Últimas movimentações
    ultimas_movimentacoes = Movimentacao.query.order_by(
        Movimentacao.data_movimentacao.desc()
    ).limit(10).all()

    # Produtos com estoque baixo
    query = (db.session.query(Estoque).join(Produtos)
             .filter(Estoque.quantidade_atual <= Estoque.quantidade_minima,
                     Produtos.ativo is True))
    produtos_estoque_baixo = query.all()

    return render_template('dashboard.html',
                           total_produtos=total_produtos,
                           total_funcionarios=total_funcionarios,
                           total_filiais=total_filiais,
                           total_ambientes=total_ambientes,
                           ultimas_movimentacoes=ultimas_movimentacoes,
                           produtos_estoque_baixo=produtos_estoque_baixo)


# ==================== FUNCIONARIOS ====================


@app.route('/funcionarios')
def funcionarios_index():
    funcionarios = Funcionarios.query.filter_by(ativo=True).all()
    return render_template('funcionarios/index.html',
                           funcionarios=funcionarios)


@app.route('/funcionarios/create', methods=['GET', 'POST'])
def funcionarios_create():
    if request.method == 'POST':
        name = request.form['name']
        cod_func = request.form['cod_func']
        role = request.form['role']
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        # Verificar se código já existe
        if Funcionarios.query.filter_by(cod_func=cod_func).first():
            flash('Código de funcionário já existe!', 'error')
            return render_template('funcionarios/create.html')

        new_funcionario = Funcionarios(
            name=name,
            cod_func=cod_func,
            role=role,
            email=email,
            telefone=telefone
        )
        db.session.add(new_funcionario)
        db.session.commit()
        flash('Funcionário criado com sucesso!', 'success')
        return redirect(url_for('funcionarios_index'))

    return render_template('funcionarios/create.html')


@app.route('/funcionarios/update/<int:id>', methods=['GET', 'POST'])
def funcionarios_update(id):
    funcionario = Funcionarios.query.get_or_404(id)
    if request.method == 'POST':
        funcionario.name = request.form['name']
        funcionario.role = request.form['role']
        funcionario.email = request.form.get('email')
        funcionario.telefone = request.form.get('telefone')
        db.session.commit()
        flash('Funcionário atualizado com sucesso!', 'success')
        return redirect(url_for('funcionarios_index'))
    return render_template('funcionarios/update.html',
                           funcionario=funcionario)


@app.route('/funcionarios/delete/<int:id>')
def funcionarios_delete(id):
    funcionario = Funcionarios.query.get_or_404(id)
    funcionario.ativo = False  # Soft delete
    db.session.commit()
    flash('Funcionário removido com sucesso!', 'success')
    return redirect(url_for('funcionarios_index'))


# ==================== PRODUTOS ====================


@app.route('/produtos')
def produtos_index():
    produtos = Produtos.query.filter_by(ativo=True).all()
    return render_template('produtos/index.html', produtos=produtos)


@app.route('/produtos/create', methods=['GET', 'POST'])
def produtos_create():
    if request.method == 'POST':
        nome = request.form['nome']
        cod_prod = request.form['cod_prod']
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        valor = request.form.get('valor')

        # Verificar se código já existe
        if Produtos.query.filter_by(cod_prod=cod_prod).first():
            flash('Código de produto já existe!', 'error')
            return render_template('produtos/create.html')

        new_produto = Produtos(
            nome=nome,
            cod_prod=cod_prod,
            descricao=descricao,
            categoria=categoria,
            valor=float(valor) if valor else None
        )
        db.session.add(new_produto)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('produtos_index'))

    return render_template('produtos/create.html')


@app.route('/produtos/update/<int:id>', methods=['GET', 'POST'])
def produtos_update(id):
    produto = Produtos.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        valor = request.form.get('valor')
        produto.valor = float(valor) if valor else None
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos_index'))
    return render_template('produtos/update.html', produto=produto)


@app.route('/produtos/delete/<int:id>')
def produtos_delete(id):
    produto = Produtos.query.get_or_404(id)
    produto.ativo = False  # Soft delete
    db.session.commit()
    flash('Produto removido com sucesso!', 'success')
    return redirect(url_for('produtos_index'))


# ==================== FILIAIS ====================


@app.route('/filiais')
def filiais_index():
    filiais = Filial.query.filter_by(ativo=True).all()
    return render_template('filiais/index.html', filiais=filiais)


@app.route('/filiais/create', methods=['GET', 'POST'])
def filiais_create():
    if request.method == 'POST':
        nome = request.form['nome']
        cod_filial = request.form['cod_filial']
        uf = request.form['uf']
        cidade = request.form.get('cidade')
        endereco = request.form.get('endereco')
        phone = request.form['phone']

        # Verificar se código já existe
        if Filial.query.filter_by(cod_filial=cod_filial).first():
            flash('Código de filial já existe!', 'error')
            return render_template('filiais/create.html')

        new_filial = Filial(
            nome=nome,
            cod_filial=cod_filial,
            uf=uf,
            cidade=cidade,
            endereco=endereco,
            phone=phone
        )
        db.session.add(new_filial)
        db.session.commit()
        flash('Filial criada com sucesso!', 'success')
        return redirect(url_for('filiais_index'))

    return render_template('filiais/create.html')


@app.route('/filiais/update/<int:id>', methods=['GET', 'POST'])
def filiais_update(id):
    filial = Filial.query.get_or_404(id)
    if request.method == 'POST':
        filial.nome = request.form['nome']
        filial.uf = request.form['uf']
        filial.cidade = request.form.get('cidade')
        filial.endereco = request.form.get('endereco')
        filial.phone = request.form['phone']
        db.session.commit()
        flash('Filial atualizada com sucesso!', 'success')
        return redirect(url_for('filiais_index'))
    return render_template('filiais/update.html', filial=filial)


@app.route('/filiais/delete/<int:id>')
def filiais_delete(id):
    filial = Filial.query.get_or_404(id)
    filial.ativo = False  # Soft delete
    db.session.commit()
    flash('Filial removida com sucesso!', 'success')
    return redirect(url_for('filiais_index'))


# ==================== AMBIENTES ====================


@app.route('/ambientes')
def ambientes_index():
    ambientes = Ambiente.query.filter_by(ativo=True).all()
    return render_template('ambientes/index.html', ambientes=ambientes)


@app.route('/ambientes/create', methods=['GET', 'POST'])
def ambientes_create():
    if request.method == 'POST':
        nome = request.form['nome']
        type = request.form['type']
        num_ambiente = request.form['num_ambiente']
        descricao = request.form.get('descricao')
        capacidade = request.form.get('capacidade')
        id_filial = request.form['id_filial']

        new_ambiente = Ambiente(
            nome=nome,
            type=type,
            num_ambiente=num_ambiente,
            descricao=descricao,
            capacidade=int(capacidade) if capacidade else None,
            id_filial=id_filial
        )
        db.session.add(new_ambiente)
        db.session.commit()
        flash('Ambiente criado com sucesso!', 'success')
        return redirect(url_for('ambientes_index'))

    filiais = Filial.query.filter_by(ativo=True).all()
    return render_template('ambientes/create.html', filiais=filiais)


@app.route('/ambientes/update/<int:id>', methods=['GET', 'POST'])
def ambientes_update(id):
    ambiente = Ambiente.query.get_or_404(id)
    if request.method == 'POST':
        ambiente.nome = request.form['nome']
        ambiente.type = request.form['type']
        ambiente.num_ambiente = request.form['num_ambiente']
        ambiente.descricao = request.form.get('descricao')
        capacidade = request.form.get('capacidade')
        ambiente.capacidade = int(capacidade) if capacidade else None
        ambiente.id_filial = request.form['id_filial']
        db.session.commit()
        flash('Ambiente atualizado com sucesso!', 'success')
        return redirect(url_for('ambientes_index'))

    filiais = Filial.query.filter_by(ativo=True).all()
    return render_template('ambientes/update.html',
                           ambiente=ambiente, filiais=filiais)


@app.route('/ambientes/delete/<int:id>')
def ambientes_delete(id):
    ambiente = Ambiente.query.get_or_404(id)
    ambiente.ativo = False  # Soft delete
    db.session.commit()
    flash('Ambiente removido com sucesso!', 'success')
    return redirect(url_for('ambientes_index'))


# ==================== SENSORES ====================


@app.route('/sensores')
def sensores_index():
    sensores = Sensores.query.all()
    return render_template('sensores/index.html', sensores=sensores)


@app.route('/sensores/create', methods=['GET', 'POST'])
def sensores_create():
    if request.method == 'POST':
        cod_sensor = request.form['cod_sensor']
        tipo = request.form['tipo']
        id_func = request.form['id_func']
        id_prod = request.form['id_prod']

        # Verificar se código já existe
        if Sensores.query.filter_by(cod_sensor=cod_sensor).first():
            flash('Código de sensor já existe!', 'error')
            return redirect(url_for('sensores_create'))

        new_sensor = Sensores(
            cod_sensor=cod_sensor,
            tipo=tipo,
            id_func=id_func,
            id_prod=id_prod
        )
        db.session.add(new_sensor)
        db.session.commit()
        flash('Sensor criado com sucesso!', 'success')
        return redirect(url_for('sensores_index'))

    funcionarios = Funcionarios.query.filter_by(ativo=True).all()
    produtos = Produtos.query.filter_by(ativo=True).all()
    return render_template('sensores/create.html',
                           funcionarios=funcionarios, produtos=produtos)


@app.route('/sensores/update/<int:id>', methods=['GET', 'POST'])
def sensores_update(id):
    sensor = Sensores.query.get_or_404(id)
    if request.method == 'POST':
        sensor.tipo = request.form['tipo']
        sensor.status = request.form['status']
        sensor.id_func = request.form['id_func']
        sensor.id_prod = request.form['id_prod']
        db.session.commit()
        flash('Sensor atualizado com sucesso!', 'success')
        return redirect(url_for('sensores_index'))

    funcionarios = Funcionarios.query.filter_by(ativo=True).all()
    produtos = Produtos.query.filter_by(ativo=True).all()
    return render_template('sensores/update.html',
                           sensor=sensor,
                           funcionarios=funcionarios,
                           produtos=produtos)


@app.route('/sensores/delete/<int:id>')
def sensores_delete(id):
    sensor = Sensores.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
    flash('Sensor removido com sucesso!', 'success')
    return redirect(url_for('sensores_index'))


# ==================== MOVIMENTAÇÕES ====================


@app.route('/movimentacoes')
def movimentacoes_index():
    movimentacoes = Movimentacao.query.order_by(
        Movimentacao.data_movimentacao.desc()
    ).all()
    return render_template('movimentacoes/index.html',
                           movimentacoes=movimentacoes)


@app.route('/movimentacoes/create', methods=['GET', 'POST'])
def movimentacoes_create():
    if request.method == 'POST':
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        observacao = request.form.get('observacao')
        id_produto = request.form['id_produto']
        id_funcionario = request.form['id_funcionario']
        id_ambiente_origem = request.form.get('id_ambiente_origem')
        id_ambiente_destino = request.form.get('id_ambiente_destino')

        new_movimentacao = Movimentacao(
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao,
            id_produto=id_produto,
            id_funcionario=id_funcionario,
            id_ambiente_origem=(id_ambiente_origem
                                if id_ambiente_origem else None),
            id_ambiente_destino=(id_ambiente_destino
                                 if id_ambiente_destino else None)
        )
        db.session.add(new_movimentacao)

        # Atualizar estoque
        atualizar_estoque(tipo, quantidade, id_produto,
                          id_ambiente_origem, id_ambiente_destino)

        db.session.commit()
        flash('Movimentação registrada com sucesso!', 'success')
        return redirect(url_for('movimentacoes_index'))

    produtos = Produtos.query.filter_by(ativo=True).all()
    funcionarios = Funcionarios.query.filter_by(ativo=True).all()
    ambientes = Ambiente.query.filter_by(ativo=True).all()
    return render_template('movimentacoes/create.html',
                           produtos=produtos,
                           funcionarios=funcionarios,
                           ambientes=ambientes)


def atualizar_estoque(tipo, quantidade, id_produto,
                      id_ambiente_origem, id_ambiente_destino):
    """Função para atualizar o estoque baseado na movimentação"""
    if tipo == 'entrada' and id_ambiente_destino:
        # Entrada: aumenta estoque no ambiente destino
        estoque = Estoque.query.filter_by(
            id_produto=id_produto, id_ambiente=id_ambiente_destino
        ).first()
        if not estoque:
            estoque = Estoque(
                id_produto=id_produto,
                id_ambiente=id_ambiente_destino,
                quantidade_atual=0
            )
            db.session.add(estoque)
        estoque.quantidade_atual += quantidade
        estoque.ultima_atualizacao = datetime.utcnow()

    elif tipo == 'saida' and id_ambiente_origem:
        # Saída: diminui estoque no ambiente origem
        estoque = Estoque.query.filter_by(
            id_produto=id_produto, id_ambiente=id_ambiente_origem
        ).first()
        if estoque:
            valor_atual = estoque.quantidade_atual - quantidade
            estoque.quantidade_atual = max(0, valor_atual)
            estoque.ultima_atualizacao = datetime.utcnow()

    elif (tipo == 'transferencia' and id_ambiente_origem
          and id_ambiente_destino):
        # Transferência: diminui origem e aumenta destino
        # Origem
        estoque_origem = Estoque.query.filter_by(
            id_produto=id_produto, id_ambiente=id_ambiente_origem
        ).first()
        if estoque_origem:
            valor_origem = estoque_origem.quantidade_atual - quantidade
            estoque_origem.quantidade_atual = max(0, valor_origem)
            estoque_origem.ultima_atualizacao = datetime.utcnow()

        # Destino
        estoque_destino = Estoque.query.filter_by(
            id_produto=id_produto, id_ambiente=id_ambiente_destino
        ).first()
        if not estoque_destino:
            estoque_destino = Estoque(
                id_produto=id_produto,
                id_ambiente=id_ambiente_destino,
                quantidade_atual=0
            )
            db.session.add(estoque_destino)
        estoque_destino.quantidade_atual += quantidade
        estoque_destino.ultima_atualizacao = datetime.utcnow()


# ==================== ESTOQUE ====================


@app.route('/estoque')
def estoque_index():
    query = (db.session.query(Estoque).join(Produtos).join(Ambiente)
             .filter(Produtos.ativo is True, Ambiente.ativo is True))
    estoques = query.all()
    return render_template('estoque/index.html', estoques=estoques)


@app.route('/estoque/config/<int:id_produto>/<int:id_ambiente>',
           methods=['GET', 'POST'])
def estoque_config(id_produto, id_ambiente):
    estoque = Estoque.query.filter_by(
        id_produto=id_produto, id_ambiente=id_ambiente
    ).first()

    if not estoque:
        estoque = Estoque(
            id_produto=id_produto,
            id_ambiente=id_ambiente,
            quantidade_atual=0
        )
        db.session.add(estoque)
        db.session.commit()

    if request.method == 'POST':
        estoque.quantidade_minima = int(request.form['quantidade_minima'])
        quantidade_maxima = request.form.get('quantidade_maxima')
        maxima = int(quantidade_maxima) if quantidade_maxima else None
        estoque.quantidade_maxima = maxima
        db.session.commit()
        flash('Configuração de estoque atualizada!', 'success')
        return redirect(url_for('estoque_index'))

    return render_template('estoque/config.html', estoque=estoque)


# ==================== RELATÓRIOS ====================


@app.route('/relatorios')
def relatorios_index():
    return render_template('relatorios/index.html')


@app.route('/relatorios/estoque')
def relatorio_estoque():
    query = (db.session.query(Estoque).join(Produtos)
             .join(Ambiente).join(Filial)
             .filter(Produtos.ativo is True,
                     Ambiente.ativo is True,
                     Filial.ativo is True))
    estoques = query.all()
    return render_template('relatorios/estoque.html',
                           estoques=estoques, now=datetime.now())


@app.route('/relatorios/movimentacoes')
def relatorio_movimentacoes():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    query = Movimentacao.query

    if data_inicio:
        query = query.filter(Movimentacao.data_movimentacao >= data_inicio)
    if data_fim:
        query = query.filter(Movimentacao.data_movimentacao <= data_fim)

    movimentacoes = query.order_by(
        Movimentacao.data_movimentacao.desc()
    ).all()
    return render_template('relatorios/movimentacoes.html',
                           movimentacoes=movimentacoes,
                           data_inicio=data_inicio,
                           data_fim=data_fim)


# ==================== API ENDPOINTS ====================


@app.route('/api/produto/<cod_prod>')
def api_produto_info(cod_prod):
    """API para consultar informações de produto por código"""
    produto = Produtos.query.filter_by(cod_prod=cod_prod,
                                       ativo=True).first()
    if produto:
        return jsonify({
            'id': produto.id,
            'nome': produto.nome,
            'cod_prod': produto.cod_prod,
            'categoria': produto.categoria,
            'valor': float(produto.valor) if produto.valor else None
        })
    return jsonify({'error': 'Produto não encontrado'}), 404


@app.route('/api/estoque/<int:id_produto>/<int:id_ambiente>')
def api_estoque_info(id_produto, id_ambiente):
    """API para consultar estoque de um produto em um ambiente"""
    estoque = Estoque.query.filter_by(
        id_produto=id_produto, id_ambiente=id_ambiente
    ).first()
    if estoque:
        return jsonify({
            'quantidade_atual': estoque.quantidade_atual,
            'quantidade_minima': estoque.quantidade_minima,
            'quantidade_maxima': estoque.quantidade_maxima,
            'ultima_atualizacao': estoque.ultima_atualizacao.isoformat()
        })
    return jsonify({'quantidade_atual': 0}), 200
