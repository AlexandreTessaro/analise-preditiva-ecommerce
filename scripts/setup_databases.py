#!/usr/bin/env python3
"""
Script de Configuração dos Bancos de Dados
Configura MongoDB e PostgreSQL para o projeto de análise preditiva e-commerce
"""

import os
import sys
import time
from datetime import datetime
import json

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_mongodb():
    """Configurar MongoDB com dados de exemplo"""
    try:
        from pymongo import MongoClient
        
        print("🔌 Conectando ao MongoDB...")
        client = MongoClient('mongodb://localhost:27017')
        db = client['ecommerce_demo']
        
        # Testar conexão
        db.command('ping')
        print("✅ MongoDB conectado com sucesso!")
        
        # Criar coleções e inserir dados de exemplo
        print("📊 Criando dados de exemplo no MongoDB...")
        
        # Coleção: produtos
        produtos_collection = db['produtos']
        produtos_exemplo = [
            {
                "produto_id": "P001",
                "nome": "Smartphone Galaxy S24",
                "categoria": "Eletrônicos > Smartphones",
                "marca": "Samsung",
                "preco": 2999.99,
                "moeda": "BRL",
                "caracteristicas": {
                    "tela": "6.2 polegadas",
                    "processador": "Snapdragon 8 Gen 3",
                    "ram": "8GB",
                    "armazenamento": "128GB",
                    "camera_principal": "50MP",
                    "camera_frontal": "12MP",
                    "bateria": "4000mAh"
                },
                "tags": ["smartphone", "android", "samsung", "premium"],
                "avaliacao_media": 4.5,
                "total_avaliacoes": 1250,
                "estoque": 45,
                "ativo": True,
                "data_criacao": datetime.now(),
                "data_atualizacao": datetime.now()
            },
            {
                "produto_id": "P002",
                "nome": "iPhone 15 Pro",
                "categoria": "Eletrônicos > Smartphones",
                "marca": "Apple",
                "preco": 8999.99,
                "caracteristicas": {
                    "tela": "6.1 polegadas",
                    "processador": "A17 Pro",
                    "ram": "8GB",
                    "armazenamento": "128GB",
                    "camera_principal": "48MP",
                    "camera_frontal": "12MP",
                    "bateria": "3274mAh"
                },
                "tags": ["smartphone", "ios", "apple", "premium"],
                "avaliacao_media": 4.7,
                "total_avaliacoes": 890,
                "estoque": 30,
                "ativo": True,
                "data_criacao": datetime.now()
            },
            {
                "produto_id": "P003",
                "nome": "Notebook Dell XPS 13",
                "categoria": "Eletrônicos > Notebooks",
                "marca": "Dell",
                "preco": 5999.99,
                "caracteristicas": {
                    "tela": "13.4 polegadas",
                    "processador": "Intel i7",
                    "ram": "16GB",
                    "armazenamento": "512GB SSD",
                    "sistema_operacional": "Windows 11",
                    "peso": "1.27kg"
                },
                "tags": ["notebook", "windows", "dell", "premium"],
                "avaliacao_media": 4.3,
                "total_avaliacoes": 567,
                "estoque": 20,
                "ativo": True,
                "data_criacao": datetime.now()
            }
        ]
        
        # Inserir produtos
        produtos_collection.insert_many(produtos_exemplo)
        print(f"✅ {len(produtos_exemplo)} produtos inseridos")
        
        # Coleção: usuarios_comportamento
        comportamento_collection = db['usuarios_comportamento']
        comportamento_exemplo = []
        
        # Gerar dados de comportamento para 20 usuários
        for i in range(1, 21):
            usuario_id = f"U{i:03d}"
            eventos = []
            
            # Gerar eventos aleatórios
            import random
            num_eventos = random.randint(5, 25)
            
            for j in range(num_eventos):
                tipos_evento = ["page_view", "click", "add_to_cart", "search"]
                tipo = random.choice(tipos_evento)
                
                evento = {
                    "tipo": tipo,
                    "timestamp": datetime.now(),
                    "tempo_pagina": random.randint(10, 120)
                }
                
                if tipo in ["page_view", "click", "add_to_cart"]:
                    evento["produto_id"] = random.choice(["P001", "P002", "P003"])
                
                if tipo == "search":
                    evento["termo"] = random.choice(["smartphone", "notebook", "tablet", "eletrônicos"])
                
                eventos.append(evento)
            
            comportamento = {
                "usuario_id": usuario_id,
                "sessao_id": f"S{i:03d}",
                "timestamp": datetime.now(),
                "eventos": eventos,
                "pagina_atual": f"/produto/P{random.randint(1,3):03d}",
                "referrer": "https://google.com/search",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "localizacao": {
                    "pais": "Brasil",
                    "estado": random.choice(["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia"]),
                    "cidade": random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador"])
                }
            }
            
            comportamento_exemplo.append(comportamento)
        
        # Inserir comportamento
        comportamento_collection.insert_many(comportamento_exemplo)
        print(f"✅ {len(comportamento_exemplo)} registros de comportamento inseridos")
        
        # Coleção: recomendacoes
        recomendacoes_collection = db['recomendacoes']
        recomendacoes_exemplo = []
        
        for i in range(1, 11):  # Recomendações para 10 usuários
            usuario_id = f"U{i:03d}"
            recomendacoes = []
            
            # Gerar recomendações aleatórias
            produtos_ids = ["P001", "P002", "P003"]
            random.shuffle(produtos_ids)
            
            for j, produto_id in enumerate(produtos_ids[:3]):
                score = random.uniform(0.6, 0.95)
                motivos = random.sample(["usuarios_similares", "produtos_similares", "categoria_preferida", "tendencia"], 1)
                
                recomendacao = {
                    "produto_id": produto_id,
                    "score": score,
                    "motivo": motivos[0],
                    "timestamp": datetime.now()
                }
                recomendacoes.append(recomendacao)
            
            doc_recomendacao = {
                "usuario_id": usuario_id,
                "algoritmo": "collaborative_filtering",
                "versao": "v2.1",
                "recomendacoes": recomendacoes,
                "contexto": {
                    "pagina": "home",
                    "categoria_filtro": "eletrônicos",
                    "preco_maximo": 10000.00
                },
                "data_geracao": datetime.now(),
                "valido_ate": datetime.now()
            }
            
            recomendacoes_exemplo.append(doc_recomendacao)
        
        # Inserir recomendações
        recomendacoes_collection.insert_many(recomendacoes_exemplo)
        print(f"✅ {len(recomendacoes_exemplo)} recomendações inseridas")
        
        client.close()
        print("🎉 MongoDB configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar MongoDB: {e}")
        return False

def setup_postgresql():
    """Configurar PostgreSQL com dados de exemplo"""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        print("🔌 Conectando ao PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            database='ecommerce_demo',
            user='postgres',
            password='postgres'
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ PostgreSQL conectado com sucesso!")
        
        # Criar tabelas
        print("📊 Criando tabelas no PostgreSQL...")
        
        # Tabela: usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario_id VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                sobrenome VARCHAR(255),
                data_nascimento DATE,
                genero VARCHAR(10),
                telefone VARCHAR(20),
                cpf VARCHAR(14) UNIQUE,
                endereco JSONB,
                data_cadastro TIMESTAMP DEFAULT NOW(),
                ultimo_login TIMESTAMP,
                ativo BOOLEAN DEFAULT TRUE,
                segmento VARCHAR(50),
                valor_total_compras DECIMAL(12,2) DEFAULT 0.00
            )
        """)
        
        # Tabela: categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                categoria_id VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                descricao TEXT,
                categoria_pai_id INTEGER REFERENCES categorias(id),
                nivel INTEGER NOT NULL DEFAULT 1,
                ordem INTEGER DEFAULT 0,
                ativo BOOLEAN DEFAULT TRUE,
                data_criacao TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Tabela: produtos_relacional
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos_relacional (
                id SERIAL PRIMARY KEY,
                produto_id VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                categoria_id INTEGER REFERENCES categorias(id),
                marca VARCHAR(100),
                preco DECIMAL(10,2) NOT NULL,
                preco_original DECIMAL(10,2),
                moeda VARCHAR(3) DEFAULT 'BRL',
                descricao TEXT,
                descricao_curta VARCHAR(500),
                sku VARCHAR(100) UNIQUE,
                peso DECIMAL(8,3),
                dimensoes JSONB,
                estoque INTEGER DEFAULT 0,
                estoque_minimo INTEGER DEFAULT 5,
                ativo BOOLEAN DEFAULT TRUE,
                destaque BOOLEAN DEFAULT FALSE,
                data_criacao TIMESTAMP DEFAULT NOW(),
                data_atualizacao TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Tabela: pedidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id SERIAL PRIMARY KEY,
                pedido_id VARCHAR(50) UNIQUE NOT NULL,
                usuario_id INTEGER REFERENCES usuarios(id),
                status VARCHAR(50) NOT NULL DEFAULT 'pendente',
                valor_total DECIMAL(12,2) NOT NULL,
                valor_desconto DECIMAL(12,2) DEFAULT 0.00,
                valor_frete DECIMAL(10,2) DEFAULT 0.00,
                metodo_pagamento VARCHAR(50),
                endereco_entrega JSONB,
                observacoes TEXT,
                data_pedido TIMESTAMP DEFAULT NOW(),
                data_pagamento TIMESTAMP,
                data_entrega TIMESTAMP,
                data_cancelamento TIMESTAMP,
                motivo_cancelamento TEXT
            )
        """)
        
        # Tabela: itens_pedido
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id SERIAL PRIMARY KEY,
                pedido_id INTEGER REFERENCES pedidos(id),
                produto_id VARCHAR(50) NOT NULL,
                nome_produto VARCHAR(255) NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total DECIMAL(12,2) NOT NULL,
                desconto DECIMAL(10,2) DEFAULT 0.00
            )
        """)
        
        # Tabela: carrinho_compras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carrinho_compras (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                produto_id VARCHAR(50) NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                preco_unitario DECIMAL(10,2) NOT NULL,
                data_adicao TIMESTAMP DEFAULT NOW(),
                data_atualizacao TIMESTAMP DEFAULT NOW(),
                UNIQUE(usuario_id, produto_id)
            )
        """)
        
        conn.commit()
        print("✅ Tabelas criadas com sucesso!")
        
        # Inserir dados de exemplo
        print("📊 Inserindo dados de exemplo...")
        
        # Inserir categorias
        cursor.execute("""
            INSERT INTO categorias (categoria_id, nome, descricao, nivel) 
            VALUES ('CAT001', 'Eletrônicos', 'Produtos eletrônicos em geral', 1)
            ON CONFLICT (categoria_id) DO NOTHING
        """)
        
        cursor.execute("""
            INSERT INTO categorias (categoria_id, nome, categoria_pai_id, nivel) 
            VALUES ('CAT002', 'Smartphones', (SELECT id FROM categorias WHERE categoria_id = 'CAT001'), 2)
            ON CONFLICT (categoria_id) DO NOTHING
        """)
        
        cursor.execute("""
            INSERT INTO categorias (categoria_id, nome, categoria_pai_id, nivel) 
            VALUES ('CAT003', 'Notebooks', (SELECT id FROM categorias WHERE categoria_id = 'CAT001'), 2)
            ON CONFLICT (categoria_id) DO NOTHING
        """)
        
        # Inserir usuários
        usuarios_exemplo = []
        for i in range(1, 21):
            usuario_id = f"U{i:03d}"
            email = f"usuario{i}@exemplo.com"
            nome = f"Usuário {i}"
            
            # Gerar dados aleatórios
            import random
            segmentos = ['high_value', 'medium_value', 'low_value', 'new_user']
            segmento = random.choice(segmentos)
            
            valor_compras = random.uniform(0, 10000)
            
            cursor.execute("""
                INSERT INTO usuarios (usuario_id, email, nome, segmento, valor_total_compras, endereco)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (usuario_id) DO NOTHING
            """, (
                usuario_id,
                email,
                nome,
                segmento,
                valor_compras,
                json.dumps({
                    "rua": f"Rua {i}, {random.randint(1, 999)}",
                    "cidade": random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte"]),
                    "estado": random.choice(["SP", "RJ", "MG"]),
                    "cep": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"
                })
            ))
        
        # Inserir produtos
        produtos_exemplo = [
            ('P001', 'Smartphone Galaxy S24', 'CAT002', 'Samsung', 2999.99, 3299.99, 'Smartphone premium', 'SAM-GAL-S24-128', 168.0, json.dumps({"largura": 70.6, "altura": 147.0, "profundidade": 7.6}), 45),
            ('P002', 'iPhone 15 Pro', 'CAT002', 'Apple', 8999.99, 9999.99, 'Smartphone premium Apple', 'APP-IPH-15P-128', 187.0, json.dumps({"largura": 71.6, "altura": 146.6, "profundidade": 8.25}), 30),
            ('P003', 'Notebook Dell XPS 13', 'CAT003', 'Dell', 5999.99, 6999.99, 'Notebook premium', 'DEL-XPS-13-512', 1270.0, json.dumps({"largura": 295.7, "altura": 199.0, "profundidade": 14.8}), 20)
        ]
        
        for produto in produtos_exemplo:
            cursor.execute("""
                INSERT INTO produtos_relacional (produto_id, nome, categoria_id, marca, preco, preco_original, descricao, sku, peso, dimensoes, estoque)
                VALUES (%s, %s, (SELECT id FROM categorias WHERE categoria_id = %s), %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (produto_id) DO NOTHING
            """, produto)
        
        # Inserir pedidos de exemplo
        import random
        for i in range(1, 16):  # 15 pedidos
            usuario_id = random.randint(1, 20)
            valor_total = random.uniform(100, 5000)
            status = random.choice(['concluido', 'pendente', 'cancelado'])
            
            cursor.execute("""
                INSERT INTO pedidos (pedido_id, usuario_id, status, valor_total, metodo_pagamento, endereco_entrega)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                f'PED{i:03d}',
                usuario_id,
                status,
                valor_total,
                random.choice(['cartao_credito', 'pix', 'boleto']),
                json.dumps({
                    "rua": f"Rua {i}, {random.randint(1, 999)}",
                    "cidade": random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte"]),
                    "estado": random.choice(["SP", "RJ", "MG"]),
                    "cep": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"
                })
            ))
            
            # Inserir itens do pedido
            produto_id = random.choice(['P001', 'P002', 'P003'])
            quantidade = random.randint(1, 3)
            preco_unitario = random.uniform(100, 3000)
            valor_total_item = preco_unitario * quantidade
            
            cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, produto_id, nome_produto, preco_unitario, quantidade, valor_total)
                VALUES ((SELECT id FROM pedidos WHERE pedido_id = %s), %s, %s, %s, %s, %s)
            """, (
                f'PED{i:03d}',
                produto_id,
                f'Produto {produto_id}',
                preco_unitario,
                quantidade,
                valor_total_item
            ))
        
        conn.commit()
        print("✅ Dados de exemplo inseridos com sucesso!")
        
        # Criar índices para performance
        print("🔍 Criando índices para performance...")
        
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)",
            "CREATE INDEX IF NOT EXISTS idx_usuarios_usuario_id ON usuarios(usuario_id)",
            "CREATE INDEX IF NOT EXISTS idx_usuarios_segmento ON usuarios(segmento)",
            "CREATE INDEX IF NOT EXISTS idx_pedidos_usuario ON pedidos(usuario_id)",
            "CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status)",
            "CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos(data_pedido)",
            "CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos_relacional(categoria_id)",
            "CREATE INDEX IF NOT EXISTS idx_produtos_marca ON produtos_relacional(marca)",
            "CREATE INDEX IF NOT EXISTS idx_produtos_preco ON produtos_relacional(preco)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        
        conn.commit()
        print("✅ Índices criados com sucesso!")
        
        cursor.close()
        conn.close()
        print("🎉 PostgreSQL configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar PostgreSQL: {e}")
        return False

def main():
    """Função principal para configurar ambos os bancos"""
    print("🚀 Iniciando configuração dos bancos de dados...")
    print("=" * 60)
    
    # Configurar MongoDB
    print("\n📊 Configurando MongoDB...")
    mongo_success = setup_mongodb()
    
    # Configurar PostgreSQL
    print("\n📊 Configurando PostgreSQL...")
    postgres_success = setup_postgresql()
    
    # Resumo
    print("\n" + "=" * 60)
    print("📋 RESUMO DA CONFIGURAÇÃO:")
    print(f"MongoDB: {'✅ Sucesso' if mongo_success else '❌ Falha'}")
    print(f"PostgreSQL: {'✅ Sucesso' if postgres_success else '❌ Falha'}")
    
    if mongo_success and postgres_success:
        print("\n🎉 Ambos os bancos foram configurados com sucesso!")
        print("🚀 Pronto para executar a análise preditiva!")
        print("\n📝 Próximos passos:")
        print("1. Execute: python scripts/demo_mongodb.py")
        print("2. Execute: python scripts/demo_postgresql.py")
        print("3. Execute: jupyter notebook notebooks/demo_analise_preditiva.ipynb")
    else:
        print("\n⚠️ Alguns bancos falharam na configuração.")
        print("Verifique os logs acima e tente novamente.")
    
    return mongo_success and postgres_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

