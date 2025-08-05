#!/usr/bin/env python3
"""
Script de inicialização rápida do Sistema de Supermercado
Este script facilita a configuração inicial do sistema
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Exibe o banner do sistema"""
    print("=" * 70)
    print("🛒 SISTEMA DE SUPERMERCADO - INICIALIZAÇÃO RÁPIDA")
    print("=" * 70)
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print("💡 Tente executar manualmente: pip install -r requirements.txt")
        return False

def check_postgresql():
    """Verifica se o PostgreSQL está disponível"""
    print("🐘 Verificando PostgreSQL...")
    try:
        import psycopg2
        print("✅ Driver PostgreSQL (psycopg2) instalado!")
        return True
    except ImportError:
        print("❌ Driver PostgreSQL não encontrado!")
        print("💡 Instale com: pip install psycopg2-binary")
        return False

def create_database():
    """Cria o banco de dados se não existir"""
    print("🗄️  Configurando banco de dados...")
    
    # Importar após instalar dependências
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("✅ Tabelas do banco de dados criadas!")
            return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        print("💡 Verifique as configurações no arquivo .env")
        return False

def populate_sample_data():
    """Pergunta se deseja popular com dados de exemplo"""
    print("\n📦 Dados de exemplo")
    response = input("Deseja adicionar produtos de exemplo ao banco? (s/N): ").lower()
    
    if response in ['s', 'sim', 'y', 'yes']:
        try:
            subprocess.run([sys.executable, "populate_db.py", "create"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao criar produtos de exemplo")
            return False
    else:
        print("⏭️  Pulando criação de dados de exemplo")
        return True

def show_instructions():
    """Mostra as instruções finais"""
    print("\n" + "=" * 70)
    print("🎉 SISTEMA CONFIGURADO COM SUCESSO!")
    print("=" * 70)
    print()
    print("🚀 Para iniciar o sistema:")
    print("   python app.py")
    print()
    print("🌐 Acesse no navegador:")
    print("   http://localhost:5000")
    print()
    print("👤 Usuários padrão:")
    print("   Admin:    login=admin,    senha=admin123")
    print("   Operador: login=operador, senha=op123")
    print()
    print("📚 Funcionalidades:")
    print("   • Login com níveis de acesso")
    print("   • Gerenciamento de produtos e usuários")
    print("   • PDV (Ponto de Venda) completo")
    print("   • Geração de notas fiscais em PDF")
    print("   • Interface moderna e responsiva")
    print()
    print("🔧 Comandos úteis:")
    print("   python populate_db.py create  # Criar produtos de exemplo")
    print("   python populate_db.py stats   # Ver estatísticas")
    print("   python populate_db.py clear   # Limpar produtos")
    print()
    print("📖 Para mais informações, consulte o README.md")
    print("=" * 70)

def main():
    """Função principal"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        print("\n⚠️  Continuando mesmo com erro nas dependências...")
    
    # Verificar PostgreSQL
    if not check_postgresql():
        print("\n⚠️  PostgreSQL pode não estar configurado corretamente")
        print("💡 Configure o banco conforme instruções no README.md")
    
    # Criar banco de dados
    if not create_database():
        print("\n❌ Falha na configuração do banco de dados")
        print("💡 Verifique:")
        print("   1. PostgreSQL está rodando")
        print("   2. Credenciais no arquivo .env estão corretas")
        print("   3. Banco de dados foi criado")
        sys.exit(1)
    
    # Popular dados de exemplo
    populate_sample_data()
    
    # Mostrar instruções finais
    show_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuração interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Execute os comandos manualmente conforme README.md")
        sys.exit(1)