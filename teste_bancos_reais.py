#!/usr/bin/env python3
"""
Teste de Conexão - Bancos Reais
MongoDB Atlas + PostgreSQL
"""

from pymongo import MongoClient
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import json
from datetime import datetime

# Configurações
MONGODB_URI = "mongodb+srv://alexandretassaro_db_user:rMJmQ6bzbbKDaQb3@cluster0.f7g7lad.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'gajseEwNF2KO0a2KfW1w',
    'database': 'n1-camargo'
}

def testar_mongodb():
    """Testar MongoDB Atlas"""
    print("🔌 Testando MongoDB Atlas...")
    
    try:
        client = MongoClient(MONGODB_URI)
        db = client['ecommerce_demo']
        
        # Testar conexão
        db.command('ping')
        print("✅ MongoDB Atlas conectado!")
        
        # Inserir dados de teste
        produtos_collection = db['produtos']
        
        # Limpar dados existentes
        produtos_collection.delete_many({})
        
        # Inserir produto de teste
        produto_teste = {
            "produto_id": "P001",
            "nome": "Smartphone Galaxy S24",
            "categoria": "Eletrônicos > Smartphones",
            "marca": "Samsung",
            "preco": 2999.99,
            "caracteristicas": {
                "tela": "6.2 polegadas",
                "processador": "Snapdragon 8 Gen 3",
                "ram": "8GB",
                "armazenamento": "128GB"
            },
            "tags": ["smartphone", "android", "samsung", "premium"],
            "avaliacao_media": 4.5,
            "total_avaliacoes": 1250,
            "estoque": 45,
            "ativo": True,
            "data_criacao": datetime.now()
        }
        
        result = produtos_collection.insert_one(produto_teste)
        print(f"✅ Produto inserido com ID: {result.inserted_id}")
        
        # Buscar produto
        produto_encontrado = produtos_collection.find_one({"produto_id": "P001"})
        if produto_encontrado:
            print(f"✅ Produto encontrado: {produto_encontrado['nome']}")
            print(f"   Preço: R$ {produto_encontrado['preco']}")
            print(f"   Marca: {produto_encontrado['marca']}")
        
        # Contar produtos
        total_produtos = produtos_collection.count_documents({})
        print(f"📊 Total de produtos no MongoDB: {total_produtos}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro MongoDB: {e}")
        return False

def testar_postgresql():
    """Testar PostgreSQL"""
    print("\n🔌 Testando PostgreSQL...")
    
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Testar conexão
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ PostgreSQL conectado!")
        print(f"📊 Versão: {version[0][:50]}...")
        
        # Criar tabela de teste
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_teste (
                id SERIAL PRIMARY KEY,
                usuario_id VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                segmento VARCHAR(50),
                valor_total_compras DECIMAL(12,2) DEFAULT 0.00,
                data_cadastro TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Limpar dados existentes
        cursor.execute("DELETE FROM usuarios_teste")
        
        # Inserir usuário de teste
        cursor.execute("""
            INSERT INTO usuarios_teste (usuario_id, nome, email, segmento, valor_total_compras)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            'U001',
            'João Silva',
            'joao@exemplo.com',
            'high_value',
            5000.00
        ))
        
        user_id = cursor.fetchone()['id']
        print(f"✅ Usuário inserido com ID: {user_id}")
        
        # Buscar usuário
        cursor.execute("SELECT * FROM usuarios_teste WHERE id = %s", (user_id,))
        usuario_encontrado = cursor.fetchone()
        if usuario_encontrado:
            print(f"✅ Usuário encontrado: {usuario_encontrado['nome']}")
            print(f"   Email: {usuario_encontrado['email']}")
            print(f"   Segmento: {usuario_encontrado['segmento']}")
            print(f"   Valor: R$ {usuario_encontrado['valor_total_compras']}")
        
        # Contar usuários
        cursor.execute("SELECT COUNT(*) as total FROM usuarios_teste")
        total_usuarios = cursor.fetchone()['total']
        print(f"📊 Total de usuários no PostgreSQL: {total_usuarios}")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro PostgreSQL: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE DE CONEXÃO - BANCOS REAIS")
    print("=" * 50)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("👨‍💻 Desenvolvido para: Disciplina de Análise Preditiva")
    print("🏫 Curso: Engenharia de Software")
    print("👨‍🏫 Professor: Luiz C. Camargo, PhD")
    print("=" * 50)
    
    # Testar MongoDB
    mongo_ok = testar_mongodb()
    
    # Testar PostgreSQL
    postgres_ok = testar_postgresql()
    
    print("\n" + "=" * 50)
    if mongo_ok and postgres_ok:
        print("🎉 AMBOS OS BANCOS FUNCIONANDO!")
        print("✅ MongoDB Atlas: OK")
        print("✅ PostgreSQL: OK")
        print("\n📚 Próximos passos:")
        print("1. Implementar análise preditiva completa")
        print("2. Criar sistema de recomendações")
        print("3. Gerar dashboards visuais")
        print("4. Demonstrar operações CRUD")
    else:
        print("⚠️ ALGUNS BANCOS COM PROBLEMAS")
        print(f"MongoDB Atlas: {'✅ OK' if mongo_ok else '❌ ERRO'}")
        print(f"PostgreSQL: {'✅ OK' if postgres_ok else '❌ ERRO'}")
    
    print("\n🎓 Avaliação N1 - Análise Preditiva")
    print("   • Domínio: Sistema de Recomendação E-commerce")
    print("   • Tecnologias: MongoDB Atlas, PostgreSQL, Python")
    print("   • Status: Bancos conectados e funcionando")
    print("=" * 50)
    
    return mongo_ok and postgres_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
