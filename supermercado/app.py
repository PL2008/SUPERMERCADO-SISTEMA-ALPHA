"""
Sistema de Supermercado - Aplicação Flask Principal
Desenvolvido com Flask, PostgreSQL e interface moderna
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from reportlab.lib.colors import black, blue

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao-desenvolvimento')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///supermercado.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização das extensões
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# ==================== MODELOS DO BANCO DE DADOS ====================

class Usuario(UserMixin, db.Model):
    """Modelo para usuários do sistema (Admin/Operador)"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'admin' ou 'operador'
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, senha):
        """Define a senha do usuário com hash"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_password(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.tipo == 'admin'

class Produto(db.Model):
    """Modelo para produtos do supermercado"""
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    codigo_barras = db.Column(db.String(50), unique=True, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o produto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': float(self.preco),
            'estoque': self.estoque,
            'codigo_barras': self.codigo_barras,
            'categoria': self.categoria,
            'ativo': self.ativo
        }

class Venda(db.Model):
    """Modelo para vendas realizadas"""
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True)
    operador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    itens_json = db.Column(db.Text)  # JSON com os itens da venda
    
    # Relacionamentos
    operador = db.relationship('Usuario', backref='vendas')
    itens = db.relationship('ItemVenda', backref='venda', cascade='all, delete-orphan')

class ItemVenda(db.Model):
    """Modelo para itens individuais de uma venda"""
    __tablename__ = 'itens_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relacionamentos
    produto = db.relationship('Produto', backref='vendas_item')

# ==================== CONFIGURAÇÃO DO LOGIN MANAGER ====================

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário pelo ID"""
    return Usuario.query.get(int(user_id))

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/')
def index():
    """Página inicial - redireciona para login se não autenticado"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('pdv'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        login_usuario = data.get('login')
        senha = data.get('senha')
        
        usuario = Usuario.query.filter_by(login=login_usuario, ativo=True).first()
        
        if usuario and usuario.check_password(senha):
            login_user(usuario)
            if usuario.is_admin():
                return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
            else:
                return jsonify({'success': True, 'redirect': url_for('pdv')})
        else:
            return jsonify({'success': False, 'message': 'Login ou senha incorretos'})
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    return redirect(url_for('login'))

# ==================== ROTAS DO PAINEL ADMINISTRATIVO ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    """Dashboard administrativo"""
    if not current_user.is_admin():
        return redirect(url_for('pdv'))
    
    # Estatísticas básicas
    total_produtos = Produto.query.filter_by(ativo=True).count()
    total_usuarios = Usuario.query.filter_by(ativo=True).count()
    vendas_hoje = Venda.query.filter(
        db.func.date(Venda.data_venda) == datetime.now().date()
    ).count()
    
    return render_template('admin_dashboard.html', 
                         total_produtos=total_produtos,
                         total_usuarios=total_usuarios,
                         vendas_hoje=vendas_hoje)

@app.route('/admin/produtos')
@login_required
def admin_produtos():
    """Gerenciamento de produtos"""
    if not current_user.is_admin():
        return redirect(url_for('pdv'))
    
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template('admin_produtos.html', produtos=produtos)

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    """Gerenciamento de usuários"""
    if not current_user.is_admin():
        return redirect(url_for('pdv'))
    
    usuarios = Usuario.query.filter_by(ativo=True).all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

# ==================== ROTAS DO PDV ====================

@app.route('/pdv')
@login_required
def pdv():
    """Tela do Ponto de Venda"""
    return render_template('pdv.html')

# ==================== APIs REST ====================

@app.route('/api/produtos', methods=['GET', 'POST'])
@login_required
def api_produtos():
    """API para gerenciar produtos"""
    if request.method == 'GET':
        # Buscar produtos
        busca = request.args.get('busca', '')
        if busca:
            produtos = Produto.query.filter(
                db.or_(
                    Produto.nome.ilike(f'%{busca}%'),
                    Produto.codigo_barras.ilike(f'%{busca}%')
                ),
                Produto.ativo == True
            ).all()
        else:
            produtos = Produto.query.filter_by(ativo=True).all()
        
        return jsonify([produto.to_dict() for produto in produtos])
    
    elif request.method == 'POST':
        # Criar novo produto
        if not current_user.is_admin():
            return jsonify({'success': False, 'message': 'Acesso negado'})
        
        data = request.get_json()
        
        # Gerar código de barras se não fornecido
        if not data.get('codigo_barras'):
            import random
            data['codigo_barras'] = f"7891234{random.randint(100000, 999999)}"
        
        produto = Produto(
            nome=data['nome'],
            preco=data['preco'],
            estoque=data['estoque'],
            codigo_barras=data['codigo_barras'],
            categoria=data['categoria']
        )
        
        try:
            db.session.add(produto)
            db.session.commit()
            return jsonify({'success': True, 'produto': produto.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Erro ao salvar produto'})

@app.route('/api/produtos/<int:produto_id>', methods=['PUT', 'DELETE'])
@login_required
def api_produto_item(produto_id):
    """API para atualizar ou deletar produto específico"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Acesso negado'})
    
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        produto.nome = data.get('nome', produto.nome)
        produto.preco = data.get('preco', produto.preco)
        produto.estoque = data.get('estoque', produto.estoque)
        produto.categoria = data.get('categoria', produto.categoria)
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'produto': produto.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Erro ao atualizar produto'})
    
    elif request.method == 'DELETE':
        produto.ativo = False
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Erro ao deletar produto'})

@app.route('/api/produto/<codigo_barras>')
@login_required
def api_produto_por_codigo(codigo_barras):
    """API para buscar produto por código de barras"""
    produto = Produto.query.filter_by(codigo_barras=codigo_barras, ativo=True).first()
    if produto:
        return jsonify({'success': True, 'produto': produto.to_dict()})
    else:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})

@app.route('/api/venda', methods=['POST'])
@login_required
def api_finalizar_venda():
    """API para finalizar uma venda"""
    data = request.get_json()
    itens = data.get('itens', [])
    
    if not itens:
        return jsonify({'success': False, 'message': 'Carrinho vazio'})
    
    # Criar a venda
    venda = Venda(
        operador_id=current_user.id,
        valor_total=data['total'],
        itens_json=json.dumps(itens)
    )
    
    try:
        db.session.add(venda)
        db.session.flush()  # Para obter o ID da venda
        
        # Criar itens da venda e atualizar estoque
        for item in itens:
            produto = Produto.query.get(item['id'])
            if produto.estoque < item['quantidade']:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Estoque insuficiente para {produto.nome}'})
            
            # Criar item da venda
            item_venda = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=item['quantidade'],
                preco_unitario=produto.preco,
                subtotal=item['subtotal']
            )
            db.session.add(item_venda)
            
            # Atualizar estoque
            produto.estoque -= item['quantidade']
        
        db.session.commit()
        return jsonify({'success': True, 'venda_id': venda.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Erro ao processar venda'})

@app.route('/api/nota-fiscal/<int:venda_id>')
@login_required
def api_gerar_nota_fiscal(venda_id):
    """API para gerar nota fiscal em PDF"""
    venda = Venda.query.get_or_404(venda_id)
    
    # Criar PDF em memória
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "SUPERMERCADO SISTEMA")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, "Nota Fiscal Simplificada")
    
    # Informações da venda
    p.drawString(50, height - 100, f"Venda Nº: {venda.id:06d}")
    p.drawString(50, height - 120, f"Data: {venda.data_venda.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(50, height - 140, f"Operador: {venda.operador.nome}")
    
    # Linha separadora
    p.line(50, height - 160, width - 50, height - 160)
    
    # Cabeçalho da tabela
    y = height - 190
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Produto")
    p.drawString(300, y, "Qtd")
    p.drawString(350, y, "Preço Unit.")
    p.drawString(450, y, "Subtotal")
    
    # Itens da venda
    p.setFont("Helvetica", 9)
    y -= 20
    for item in venda.itens:
        p.drawString(50, y, item.produto.nome[:35])
        p.drawString(300, y, str(item.quantidade))
        p.drawString(350, y, f"R$ {item.preco_unitario:.2f}")
        p.drawString(450, y, f"R$ {item.subtotal:.2f}")
        y -= 15
    
    # Total
    p.line(50, y - 10, width - 50, y - 10)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y - 30, f"TOTAL: R$ {venda.valor_total:.2f}")
    
    # Rodapé
    p.setFont("Helvetica", 8)
    p.drawString(50, 50, "Obrigado pela preferência!")
    
    p.save()
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'nota_fiscal_{venda.id:06d}.pdf',
        mimetype='application/pdf'
    )

@app.route('/api/usuarios', methods=['GET', 'POST'])
@login_required
def api_usuarios():
    """API para gerenciar usuários"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Acesso negado'})
    
    if request.method == 'GET':
        usuarios = Usuario.query.filter_by(ativo=True).all()
        return jsonify([{
            'id': u.id,
            'nome': u.nome,
            'login': u.login,
            'tipo': u.tipo,
            'data_criacao': u.data_criacao.strftime('%d/%m/%Y')
        } for u in usuarios])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Verificar se login já existe
        if Usuario.query.filter_by(login=data['login']).first():
            return jsonify({'success': False, 'message': 'Login já existe'})
        
        usuario = Usuario(
            nome=data['nome'],
            login=data['login'],
            tipo=data['tipo']
        )
        usuario.set_password(data['senha'])
        
        try:
            db.session.add(usuario)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Erro ao criar usuário'})

# ==================== INICIALIZAÇÃO DO BANCO DE DADOS ====================

def init_db():
    """Inicializa o banco de dados e cria usuário admin padrão"""
    db.create_all()
    
    # Criar usuário admin padrão se não existir
    admin = Usuario.query.filter_by(login='admin').first()
    if not admin:
        admin = Usuario(
            nome='Administrador',
            login='admin',
            tipo='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Criar usuário operador padrão
        operador = Usuario(
            nome='Operador',
            login='operador',
            tipo='operador'
        )
        operador.set_password('op123')
        db.session.add(operador)
        
        db.session.commit()
        print("Usuários padrão criados:")
        print("Admin - Login: admin, Senha: admin123")
        print("Operador - Login: operador, Senha: op123")

# ==================== EXECUÇÃO DA APLICAÇÃO ====================

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)