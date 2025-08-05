# 🛒 Sistema de Supermercado

Um sistema completo de supermercado desenvolvido com Flask, PostgreSQL e interface moderna. Inclui funcionalidades de PDV (Ponto de Venda), gerenciamento de produtos, usuários e geração de notas fiscais em PDF.

## ✨ Características

### 🔐 Sistema de Autenticação
- Login seguro com hash de senhas
- Níveis de acesso: **Admin** e **Operador**
- Sessões protegidas com Flask-Login

### 👥 Gestão de Usuários
- Cadastro de usuários (Admin/Operador)
- Controle de permissões por tipo de usuário
- Interface intuitiva para gerenciamento

### 📦 Gerenciamento de Produtos
- Cadastro completo de produtos
- Código de barras (gerado automaticamente ou manual)
- Controle de estoque em tempo real
- Categorização de produtos
- Busca por nome ou código de barras

### 💰 PDV (Ponto de Venda)
- Interface moderna e responsiva
- Leitura de código de barras (input simulado)
- Carrinho de compras interativo
- Cálculo automático de totais
- Controle de quantidade de produtos
- Finalização de vendas

### 📄 Notas Fiscais
- Geração automática de PDF
- Layout profissional
- Dados completos da venda
- Download direto após finalização

### 🎨 Interface Moderna
- Design responsivo para desktop e mobile
- Tema claro com gradientes modernos
- Ícones Font Awesome
- Alertas elegantes com SweetAlert2
- Animações suaves com CSS

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **PostgreSQL** - Banco de dados principal
- **ReportLab** - Geração de PDFs
- **Werkzeug** - Segurança e utilitários

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização moderna
- **JavaScript ES6+** - Interatividade
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Ícones
- **SweetAlert2** - Alertas elegantes

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd supermercado
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados PostgreSQL

#### Instalar PostgreSQL (se necessário)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Windows - Baixar do site oficial
# https://www.postgresql.org/download/windows/

# macOS
brew install postgresql
```

#### Criar banco de dados
```sql
-- Conectar ao PostgreSQL como superusuário
sudo -u postgres psql

-- Criar usuário e banco
CREATE USER supermercado_user WITH PASSWORD 'supermercado_pass';
CREATE DATABASE supermercado_db OWNER supermercado_user;
GRANT ALL PRIVILEGES ON DATABASE supermercado_db TO supermercado_user;

-- Sair do PostgreSQL
\q
```

### 5. Configure as variáveis de ambiente

Edite o arquivo `.env` com suas configurações:

```env
DATABASE_URL=postgresql://supermercado_user:supermercado_pass@localhost:5432/supermercado_db
SECRET_KEY=sua_chave_secreta_muito_segura_aqui_123456789
FLASK_ENV=development
FLASK_DEBUG=True
```

### 6. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 👤 Usuários Padrão

O sistema cria automaticamente dois usuários para demonstração:

### Administrador
- **Login:** `admin`
- **Senha:** `admin123`
- **Permissões:** Acesso completo ao sistema

### Operador
- **Login:** `operador`
- **Senha:** `op123`
- **Permissões:** Acesso apenas ao PDV

## 📱 Como Usar

### 1. Login
- Acesse `http://localhost:5000`
- Use as credenciais padrão ou crie novos usuários

### 2. Dashboard Administrativo (Admin)
- Visualize estatísticas do sistema
- Acesse rapidamente as funcionalidades
- Monitore atividades recentes

### 3. Gerenciar Produtos
- **Adicionar:** Clique em "Novo Produto"
- **Editar:** Clique no ícone de edição na tabela
- **Excluir:** Clique no ícone de lixeira
- **Buscar:** Use a barra de pesquisa por nome ou código

### 4. Gerenciar Usuários
- **Adicionar:** Clique em "Novo Usuário"
- **Visualizar:** Veja todos os usuários cadastrados
- **Tipos:** Admin (acesso total) ou Operador (apenas PDV)

### 5. PDV (Ponto de Venda)
- **Escanear:** Digite o código de barras e pressione Enter
- **Buscar:** Use o botão "Buscar Produto" para pesquisar
- **Quantidade:** Ajuste a quantidade com os botões +/-
- **Finalizar:** Clique em "Finalizar Compra"
- **Nota Fiscal:** Gere o PDF após a venda

## 🗂️ Estrutura do Projeto

```
supermercado/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── .env                  # Variáveis de ambiente
├── README.md             # Este arquivo
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Estilos personalizados
│   │   ├── js/
│   │   │   └── main.js       # JavaScript principal
│   │   └── images/           # Imagens do sistema
│   └── templates/
│       ├── base.html         # Template base
│       ├── login.html        # Página de login
│       ├── admin_dashboard.html    # Dashboard admin
│       ├── admin_produtos.html     # Gestão de produtos
│       ├── admin_usuarios.html     # Gestão de usuários
│       └── pdv.html         # Ponto de venda
├── database/             # Scripts de banco (futuro)
└── docs/                # Documentação adicional
```

## 🔧 Funcionalidades Detalhadas

### Sistema de Login
- Autenticação segura com hash bcrypt
- Sessões persistentes
- Redirecionamento baseado no tipo de usuário
- Logout seguro

### Gerenciamento de Produtos
- **Campos:** Nome, Preço, Estoque, Código de Barras, Categoria
- **Validações:** Preço positivo, estoque não negativo
- **Busca:** Por nome ou código de barras
- **Filtros:** Por categoria
- **Geração:** Código de barras automático

### PDV Avançado
- **Interface intuitiva:** Layout otimizado para velocidade
- **Carrinho dinâmico:** Adição/remoção em tempo real
- **Cálculos automáticos:** Subtotais e total geral
- **Validações:** Estoque disponível, quantidades válidas
- **Atalhos:** Enter para buscar, Ctrl+K para focar busca

### Notas Fiscais
- **Formato PDF:** Layout profissional
- **Informações completas:** Produtos, quantidades, preços
- **Numeração sequencial:** Controle de vendas
- **Download automático:** Após finalização

## 🔒 Segurança

- **Senhas:** Hash bcrypt para armazenamento seguro
- **Sessões:** Flask-Login para controle de acesso
- **Validações:** Frontend e backend
- **SQL Injection:** Proteção via SQLAlchemy ORM
- **CSRF:** Tokens de segurança em formulários

## 🚀 Melhorias Futuras

- [ ] Relatórios avançados de vendas
- [ ] Dashboard com gráficos
- [ ] Backup automático do banco
- [ ] API REST completa
- [ ] App mobile
- [ ] Integração com balanças
- [ ] Códigos de barras reais
- [ ] Sistema de promoções
- [ ] Controle de fornecedores
- [ ] Módulo financeiro

## 🐛 Resolução de Problemas

### Erro de Conexão com PostgreSQL
```bash
# Verificar se o PostgreSQL está rodando
sudo systemctl status postgresql

# Iniciar o PostgreSQL
sudo systemctl start postgresql

# Verificar conexão
psql -h localhost -U supermercado_user -d supermercado_db
```

### Erro de Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de Permissões
```bash
# Verificar permissões do usuário no banco
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE supermercado_db TO supermercado_user;
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs da aplicação
2. Consulte a documentação do PostgreSQL
3. Verifique as configurações do `.env`
4. Teste a conexão com o banco separadamente

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📊 Status do Projeto

- ✅ **Backend Flask:** Completo
- ✅ **Interface de usuário:** Completo
- ✅ **Sistema de login:** Completo
- ✅ **Gerenciamento de produtos:** Completo
- ✅ **PDV:** Completo
- ✅ **Geração de PDF:** Completo
- ✅ **Design responsivo:** Completo
- ⏳ **Relatórios avançados:** Em desenvolvimento
- ⏳ **Testes automatizados:** Planejado

---

**Desenvolvido com ❤️ para facilitar a gestão de supermercados**