#!/usr/bin/env python3
"""
Script para popular o banco de dados com produtos de exemplo
Execute este script após inicializar o banco de dados
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Produto
import random

def generate_barcode():
    """Gera um código de barras aleatório"""
    return f"789{random.randint(1000000000, 9999999999)}"

def create_sample_products():
    """Cria produtos de exemplo no banco de dados"""
    
    sample_products = [
        # Alimentação
        {"nome": "Arroz Branco 5kg", "preco": 18.90, "estoque": 50, "categoria": "Alimentação"},
        {"nome": "Feijão Preto 1kg", "preco": 8.50, "estoque": 30, "categoria": "Alimentação"},
        {"nome": "Açúcar Cristal 1kg", "preco": 4.20, "estoque": 40, "categoria": "Alimentação"},
        {"nome": "Óleo de Soja 900ml", "preco": 5.80, "estoque": 25, "categoria": "Alimentação"},
        {"nome": "Macarrão Espaguete 500g", "preco": 3.90, "estoque": 60, "categoria": "Alimentação"},
        {"nome": "Farinha de Trigo 1kg", "preco": 4.50, "estoque": 35, "categoria": "Alimentação"},
        {"nome": "Sal Refinado 1kg", "preco": 2.10, "estoque": 80, "categoria": "Alimentação"},
        {"nome": "Café Torrado 500g", "preco": 12.90, "estoque": 20, "categoria": "Alimentação"},
        {"nome": "Leite Integral 1L", "preco": 4.80, "estoque": 45, "categoria": "Alimentação"},
        {"nome": "Pão de Açúcar 500g", "preco": 3.50, "estoque": 25, "categoria": "Alimentação"},
        
        # Bebidas
        {"nome": "Coca-Cola 2L", "preco": 8.90, "estoque": 30, "categoria": "Bebidas"},
        {"nome": "Água Mineral 1.5L", "preco": 2.50, "estoque": 100, "categoria": "Bebidas"},
        {"nome": "Suco de Laranja 1L", "preco": 6.90, "estoque": 20, "categoria": "Bebidas"},
        {"nome": "Cerveja Lata 350ml", "preco": 3.20, "estoque": 150, "categoria": "Bebidas"},
        {"nome": "Guaraná Antarctica 2L", "preco": 7.50, "estoque": 25, "categoria": "Bebidas"},
        {"nome": "Água de Coco 200ml", "preco": 2.80, "estoque": 40, "categoria": "Bebidas"},
        {"nome": "Energético Lata 250ml", "preco": 8.50, "estoque": 15, "categoria": "Bebidas"},
        {"nome": "Chá Gelado 1.5L", "preco": 4.90, "estoque": 30, "categoria": "Bebidas"},
        
        # Limpeza
        {"nome": "Detergente Líquido 500ml", "preco": 2.90, "estoque": 50, "categoria": "Limpeza"},
        {"nome": "Sabão em Pó 1kg", "preco": 12.90, "estoque": 25, "categoria": "Limpeza"},
        {"nome": "Amaciante 2L", "preco": 8.90, "estoque": 20, "categoria": "Limpeza"},
        {"nome": "Desinfetante 1L", "preco": 6.50, "estoque": 30, "categoria": "Limpeza"},
        {"nome": "Papel Higiênico 4 rolos", "preco": 9.90, "estoque": 40, "categoria": "Limpeza"},
        {"nome": "Esponja de Aço 8 unidades", "preco": 3.50, "estoque": 60, "categoria": "Limpeza"},
        {"nome": "Água Sanitária 1L", "preco": 3.90, "estoque": 35, "categoria": "Limpeza"},
        {"nome": "Sabonete em Barra 90g", "preco": 1.80, "estoque": 80, "categoria": "Limpeza"},
        
        # Higiene
        {"nome": "Shampoo 400ml", "preco": 15.90, "estoque": 25, "categoria": "Higiene"},
        {"nome": "Condicionador 400ml", "preco": 16.90, "estoque": 20, "categoria": "Higiene"},
        {"nome": "Pasta de Dente 90g", "preco": 4.50, "estoque": 50, "categoria": "Higiene"},
        {"nome": "Escova de Dente", "preco": 8.90, "estoque": 30, "categoria": "Higiene"},
        {"nome": "Desodorante Spray 150ml", "preco": 12.90, "estoque": 25, "categoria": "Higiene"},
        {"nome": "Absorvente 8 unidades", "preco": 6.90, "estoque": 40, "categoria": "Higiene"},
        {"nome": "Fralda Descartável P 30un", "preco": 28.90, "estoque": 15, "categoria": "Higiene"},
        {"nome": "Lenço Umedecido 50un", "preco": 8.50, "estoque": 35, "categoria": "Higiene"},
        
        # Outros
        {"nome": "Pilha AA 4 unidades", "preco": 12.90, "estoque": 20, "categoria": "Outros"},
        {"nome": "Fósforo Caixa", "preco": 1.50, "estoque": 100, "categoria": "Outros"},
        {"nome": "Vela Comum 6 unidades", "preco": 4.90, "estoque": 30, "categoria": "Outros"},
        {"nome": "Saco de Lixo 50L 15un", "preco": 8.90, "estoque": 25, "categoria": "Outros"},
        {"nome": "Papel Alumínio 30m", "preco": 7.50, "estoque": 20, "categoria": "Outros"},
        {"nome": "Papel Filme 30m", "preco": 6.90, "estoque": 25, "categoria": "Outros"},
        {"nome": "Guardanapo 50 folhas", "preco": 3.20, "estoque": 40, "categoria": "Outros"},
        {"nome": "Copo Descartável 200ml 100un", "preco": 5.90, "estoque": 30, "categoria": "Outros"},
    ]
    
    print("🏪 Populando banco de dados com produtos de exemplo...")
    
    with app.app_context():
        # Verificar se já existem produtos
        existing_products = Produto.query.count()
        if existing_products > 0:
            print(f"❌ Banco já contém {existing_products} produtos. Cancelando operação.")
            print("💡 Para recriar os produtos, primeiro limpe o banco de dados.")
            return
        
        created_count = 0
        for product_data in sample_products:
            try:
                # Gerar código de barras único
                codigo_barras = generate_barcode()
                
                # Verificar se o código já existe (improvável, mas por segurança)
                while Produto.query.filter_by(codigo_barras=codigo_barras).first():
                    codigo_barras = generate_barcode()
                
                produto = Produto(
                    nome=product_data["nome"],
                    preco=product_data["preco"],
                    estoque=product_data["estoque"],
                    codigo_barras=codigo_barras,
                    categoria=product_data["categoria"]
                )
                
                db.session.add(produto)
                created_count += 1
                print(f"✅ Produto criado: {product_data['nome']} - Código: {codigo_barras}")
                
            except Exception as e:
                print(f"❌ Erro ao criar produto {product_data['nome']}: {str(e)}")
        
        try:
            db.session.commit()
            print(f"\n🎉 Sucesso! {created_count} produtos foram criados no banco de dados.")
            print("\n📊 Resumo por categoria:")
            
            # Mostrar resumo por categoria
            categorias = db.session.query(Produto.categoria, db.func.count(Produto.id)).group_by(Produto.categoria).all()
            for categoria, count in categorias:
                print(f"   • {categoria}: {count} produtos")
                
            print(f"\n💰 Valor total em estoque: R$ {sum(p.preco * p.estoque for p in Produto.query.all()):.2f}")
            print("🚀 Agora você pode testar o sistema com produtos reais!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar produtos no banco: {str(e)}")

def clear_products():
    """Remove todos os produtos do banco de dados"""
    print("🗑️  Limpando produtos do banco de dados...")
    
    with app.app_context():
        try:
            count = Produto.query.count()
            Produto.query.delete()
            db.session.commit()
            print(f"✅ {count} produtos foram removidos do banco de dados.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao limpar produtos: {str(e)}")

def show_stats():
    """Mostra estatísticas dos produtos no banco"""
    print("📊 Estatísticas do banco de dados:")
    
    with app.app_context():
        total_produtos = Produto.query.count()
        if total_produtos == 0:
            print("❌ Nenhum produto encontrado no banco de dados.")
            return
        
        print(f"📦 Total de produtos: {total_produtos}")
        
        # Produtos por categoria
        categorias = db.session.query(Produto.categoria, db.func.count(Produto.id)).group_by(Produto.categoria).all()
        print("\n📋 Produtos por categoria:")
        for categoria, count in categorias:
            print(f"   • {categoria}: {count} produtos")
        
        # Valor total em estoque
        valor_total = sum(p.preco * p.estoque for p in Produto.query.all())
        print(f"\n💰 Valor total em estoque: R$ {valor_total:.2f}")
        
        # Produtos com estoque baixo (menos de 20 unidades)
        produtos_baixo_estoque = Produto.query.filter(Produto.estoque < 20).all()
        if produtos_baixo_estoque:
            print(f"\n⚠️  Produtos com estoque baixo ({len(produtos_baixo_estoque)}):")
            for produto in produtos_baixo_estoque:
                print(f"   • {produto.nome}: {produto.estoque} unidades")

if __name__ == "__main__":
    print("🛒 Sistema de Supermercado - Utilitário de Banco de Dados")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Uso: python populate_db.py [comando]")
        print("\nComandos disponíveis:")
        print("  create  - Criar produtos de exemplo")
        print("  clear   - Limpar todos os produtos")
        print("  stats   - Mostrar estatísticas")
        print("\nExemplo: python populate_db.py create")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_sample_products()
    elif command == "clear":
        confirm = input("⚠️  Tem certeza que deseja remover TODOS os produtos? (digite 'sim'): ")
        if confirm.lower() == 'sim':
            clear_products()
        else:
            print("Operação cancelada.")
    elif command == "stats":
        show_stats()
    else:
        print(f"❌ Comando '{command}' não reconhecido.")
        print("Comandos válidos: create, clear, stats")