from app import db
from datetime import datetime


class Funcionarios(db.Model):           #tabela de funcionarios
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cod_func = db.Column(db.Integer, nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(15), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    sensores = db.relationship('Sensores', backref='funcionario', lazy=True)
    movimentacoes = db.relationship('Movimentacao',
                                    backref='funcionario', lazy=True)

    def __repr__(self):
        return f'<Funcionario {self.name}>'


class Produtos(db.Model):           #tabela de produtos
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cod_prod = db.Column(db.Integer, nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    sensores = db.relationship('Sensores', backref='produto', lazy=True)
    movimentacoes = db.relationship('Movimentacao', backref='produto',
                                    lazy=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'


class Filial(db.Model):             #tabela das filiais
    __tablename__ = 'filial'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cod_filial = db.Column(db.Integer, nullable=False, unique=True)
    uf = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    ambientes = db.relationship('Ambiente', backref='filial', lazy=True)

    def __repr__(self):
        return f'<Filial {self.nome}>'


class Sensores(db.Model):               #tabela dos sensores
    __tablename__ = 'sensores'
    id = db.Column(db.Integer, primary_key=True)
    cod_sensor = db.Column(db.Integer, nullable=False, unique=True)
    # RFID, Barcode, QR Code, etc.
    tipo = db.Column(db.String(50), nullable=False)
    # ativo, inativo, manutencao
    status = db.Column(db.String(20), default='ativo')
    id_func = db.Column(db.Integer, db.ForeignKey('funcionarios.id'),
                        nullable=False)
    id_prod = db.Column(db.Integer, db.ForeignKey('produtos.id'),
                        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    ambientes = db.relationship('Ambiente', backref='sensor', lazy=True)

    def __repr__(self):
        return f'<Sensor {self.cod_sensor}>'


class Ambiente(db.Model):               #tabela dos ambientes\lugares
    __tablename__ = 'ambiente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    # deposito, sala, corredor, etc.
    type = db.Column(db.String(50), nullable=False)
    num_ambiente = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    capacidade = db.Column(db.Integer, nullable=True)
    id_filial = db.Column(db.Integer, db.ForeignKey('filial.id'),
                          nullable=False)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensores.id'),
                          nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos específicos para movimentações
    movimentacoes_origem = db.relationship(
        'Movimentacao',
        foreign_keys='Movimentacao.id_ambiente_origem',
        lazy=True
    )
    movimentacoes_destino = db.relationship(
        'Movimentacao',
        foreign_keys='Movimentacao.id_ambiente_destino',
        lazy=True
    )

    def __repr__(self):
        return f'<Ambiente {self.nome}>'


class Movimentacao(db.Model):               #tabela da movimentaçaõ dos produtos (joao marcelo esteve aqui)
    __tablename__ = 'movimentacao'
    id = db.Column(db.Integer, primary_key=True)
    # entrada, saida, transferencia
    tipo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacao = db.Column(db.Text, nullable=True)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'),
                           nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id'),
                               nullable=False)
    id_ambiente_origem = db.Column(db.Integer, db.ForeignKey('ambiente.id'),
                                   nullable=True)
    id_ambiente_destino = db.Column(db.Integer, db.ForeignKey('ambiente.id'),
                                    nullable=True)

    # Relacionamentos adicionais para origem/destino
    ambiente_origem = db.relationship('Ambiente',
                                      foreign_keys=[id_ambiente_origem],
                                      lazy=True)
    ambiente_destino = db.relationship('Ambiente',
                                       foreign_keys=[id_ambiente_destino],
                                       lazy=True)

    def __repr__(self):
        return f'<Movimentacao {self.tipo} - {self.data_movimentacao}>'


class Estoque(db.Model):                #tabela para controle de estoque
    __tablename__ = 'estoque'
    id = db.Column(db.Integer, primary_key=True)
    quantidade_atual = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, nullable=False, default=0)
    quantidade_maxima = db.Column(db.Integer, nullable=True)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'),
                           nullable=False)
    id_ambiente = db.Column(db.Integer, db.ForeignKey('ambiente.id'),
                            nullable=False)

    # Relacionamentos
    produto = db.relationship('Produtos', backref='estoques', lazy=True)
    ambiente = db.relationship('Ambiente', backref='estoques', lazy=True)

    # Unique constraint para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('id_produto', 'id_ambiente'),)

    def __repr__(self):
        return (f'<Estoque Produto:{self.id_produto} '
                f'Ambiente:{self.id_ambiente} '
                f'Qty:{self.quantidade_atual}>')
