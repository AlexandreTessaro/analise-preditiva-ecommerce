#!/usr/bin/env python3
"""
Demonstração Prática - Sistema de Recomendação E-commerce
PostgreSQL + Análise Preditiva

Este script demonstra operações práticas com PostgreSQL para análise preditiva
de um sistema de recomendação de produtos e-commerce.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

class EcommercePostgreSQL:
    def __init__(self, host='localhost', database='ecommerce_demo', 
                 user='postgres', password='postgres'):
        """Inicializar conexão com PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ Conectado ao PostgreSQL com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar PostgreSQL: {e}")
            print("💡 Certifique-se de que o PostgreSQL está rodando e o banco existe")
    
    def criar_tabelas(self):
        """Criar tabelas necessárias para demonstração"""
        print("\n🔄 Criando tabelas...")
        
        # Tabela de usuários
        self.cursor.execute("""
            DROP TABLE IF EXISTS usuarios CASCADE;
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                usuario_id VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                sobrenome VARCHAR(255),
                data_nascimento DATE,
                genero VARCHAR(10),
                telefone VARCHAR(20),
                segmento VARCHAR(50),
                valor_total_compras DECIMAL(12,2) DEFAULT 0.00,
                data_cadastro TIMESTAMP DEFAULT NOW(),
                ultimo_login TIMESTAMP,
                ativo BOOLEAN DEFAULT TRUE
            );
        """)
        
        # Tabela de categorias
        self.cursor.execute("""
            DROP TABLE IF EXISTS categorias CASCADE;
            CREATE TABLE categorias (
                id SERIAL PRIMARY KEY,
                categoria_id VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                descricao TEXT,
                categoria_pai_id INTEGER REFERENCES categorias(id),
                nivel INTEGER NOT NULL DEFAULT 1,
                ativo BOOLEAN DEFAULT TRUE,
                data_criacao TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Tabela de produtos
        self.cursor.execute("""
            DROP TABLE IF EXISTS produtos_relacional CASCADE;
            CREATE TABLE produtos_relacional (
                id SERIAL PRIMARY KEY,
                produto_id VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(255) NOT NULL,
                categoria_id INTEGER REFERENCES categorias(id),
                marca VARCHAR(100),
                preco DECIMAL(10,2) NOT NULL,
                preco_original DECIMAL(10,2),
                descricao TEXT,
                sku VARCHAR(100) UNIQUE,
                estoque INTEGER DEFAULT 0,
                estoque_minimo INTEGER DEFAULT 5,
                ativo BOOLEAN DEFAULT TRUE,
                destaque BOOLEAN DEFAULT FALSE,
                data_criacao TIMESTAMP DEFAULT NOW(),
                data_atualizacao TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Tabela de pedidos
        self.cursor.execute("""
            DROP TABLE IF EXISTS pedidos CASCADE;
            CREATE TABLE pedidos (
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
            );
        """)
        
        # Tabela de itens do pedido
        self.cursor.execute("""
            DROP TABLE IF EXISTS itens_pedido CASCADE;
            CREATE TABLE itens_pedido (
                id SERIAL PRIMARY KEY,
                pedido_id INTEGER REFERENCES pedidos(id),
                produto_id VARCHAR(50) NOT NULL,
                nome_produto VARCHAR(255) NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total DECIMAL(12,2) NOT NULL,
                desconto DECIMAL(10,2) DEFAULT 0.00
            );
        """)
        
        # Tabela de carrinho
        self.cursor.execute("""
            DROP TABLE IF EXISTS carrinho_compras CASCADE;
            CREATE TABLE carrinho_compras (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                produto_id VARCHAR(50) NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                preco_unitario DECIMAL(10,2) NOT NULL,
                data_adicao TIMESTAMP DEFAULT NOW(),
                data_atualizacao TIMESTAMP DEFAULT NOW(),
                UNIQUE(usuario_id, produto_id)
            );
        """)
        
        self.conn.commit()
        print("✅ Tabelas criadas com sucesso!")
    
    def inserir_dados_exemplo(self):
        """Inserir dados de exemplo"""
        print("\n🔄 Inserindo dados de exemplo...")
        
        # Inserir categorias
        categorias = [
            ('CAT001', 'Eletrônicos', 'Produtos eletrônicos em geral', None, 1),
            ('CAT002', 'Smartphones', 'Telefones inteligentes', 1, 2),
            ('CAT003', 'Notebooks', 'Computadores portáteis', 1, 2),
            ('CAT004', 'Tablets', 'Tablets e dispositivos móveis', 1, 2)
        ]
        
        for cat in categorias:
            self.cursor.execute("""
                INSERT INTO categorias (categoria_id, nome, descricao, categoria_pai_id, nivel)
                VALUES (%s, %s, %s, %s, %s)
            """, cat)
        
        # Inserir usuários
        usuarios = [
            ('U001', 'joao.silva@email.com', 'João', 'Silva', '1990-05-15', 'M', '(11) 99999-9999', 'high_value', 15750.50),
            ('U002', 'maria.santos@email.com', 'Maria', 'Santos', '1985-08-22', 'F', '(11) 88888-8888', 'medium_value', 3250.75),
            ('U003', 'pedro.oliveira@email.com', 'Pedro', 'Oliveira', '1995-12-03', 'M', '(11) 77777-7777', 'new_user', 0.00),
            ('U004', 'ana.costa@email.com', 'Ana', 'Costa', '1992-03-18', 'F', '(11) 66666-6666', 'medium_value', 2100.00),
            ('U005', 'carlos.ferreira@email.com', 'Carlos', 'Ferreira', '1988-11-25', 'M', '(11) 55555-5555', 'high_value', 8750.25)
        ]
        
        for user in usuarios:
            self.cursor.execute("""
                INSERT INTO usuarios (usuario_id, email, nome, sobrenome, data_nascimento, genero, telefone, segmento, valor_total_compras)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, user)
        
        # Inserir produtos
        produtos = [
            ('P001', 'Smartphone Galaxy S24', 2, 'Samsung', 2999.99, 3299.99, 'Smartphone com tela de 6.2 polegadas', 'SAM-GAL-S24-128', 45),
            ('P002', 'iPhone 15 Pro', 2, 'Apple', 8999.99, 9499.99, 'Smartphone premium com tela de 6.1 polegadas', 'APP-IPH-15P-128', 30),
            ('P003', 'Notebook Dell XPS 13', 3, 'Dell', 5999.99, 6499.99, 'Notebook ultrabook com tela de 13.4 polegadas', 'DEL-XPS-13-512', 20),
            ('P004', 'Tablet iPad Air', 4, 'Apple', 3999.99, 4299.99, 'Tablet com tela de 10.9 polegadas', 'APP-IPAD-AIR-64', 15),
            ('P005', 'Smartphone Xiaomi 13', 2, 'Xiaomi', 1999.99, 2299.99, 'Smartphone com excelente custo-benefício', 'XIA-MI-13-128', 60)
        ]
        
        for prod in produtos:
            self.cursor.execute("""
                INSERT INTO produtos_relacional (produto_id, nome, categoria_id, marca, preco, preco_original, descricao, sku, estoque)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, prod)
        
        # Inserir pedidos
        pedidos = [
            ('PED001', 1, 'concluido', 2999.99, 0.00, 15.00, 'cartao_credito', '2024-01-10 08:15:00', '2024-01-10 08:16:00', '2024-01-12 14:30:00'),
            ('PED002', 1, 'concluido', 5999.99, 300.00, 0.00, 'pix', '2024-01-12 16:45:00', '2024-01-12 16:46:00', '2024-01-15 10:20:00'),
            ('PED003', 2, 'pendente', 8999.99, 0.00, 25.00, 'cartao_credito', '2024-01-15 14:30:00', None, None),
            ('PED004', 2, 'concluido', 2499.99, 0.00, 20.00, 'cartao_debito', '2024-01-13 19:30:00', '2024-01-13 19:31:00', '2024-01-16 11:15:00'),
            ('PED005', 4, 'concluido', 3999.99, 200.00, 15.00, 'boleto', '2024-01-08 11:20:00', '2024-01-09 09:15:00', '2024-01-11 16:45:00'),
            ('PED006', 5, 'concluido', 1999.99, 0.00, 10.00, 'pix', '2024-01-14 10:30:00', '2024-01-14 10:31:00', '2024-01-17 09:30:00')
        ]
        
        for ped in pedidos:
            self.cursor.execute("""
                INSERT INTO pedidos (pedido_id, usuario_id, status, valor_total, valor_desconto, valor_frete, metodo_pagamento, data_pedido, data_pagamento, data_entrega)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ped)
        
        # Inserir itens dos pedidos
        itens = [
            (1, 'P001', 'Smartphone Galaxy S24', 2999.99, 1, 2999.99, 0.00),
            (2, 'P003', 'Notebook Dell XPS 13', 5999.99, 1, 5999.99, 300.00),
            (3, 'P002', 'iPhone 15 Pro', 8999.99, 1, 8999.99, 0.00),
            (4, 'P005', 'Smartphone Xiaomi 13', 1999.99, 1, 1999.99, 0.00),
            (5, 'P004', 'Tablet iPad Air', 3999.99, 1, 3999.99, 200.00),
            (6, 'P005', 'Smartphone Xiaomi 13', 1999.99, 1, 1999.99, 0.00)
        ]
        
        for item in itens:
            self.cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, produto_id, nome_produto, preco_unitario, quantidade, valor_total, desconto)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, item)
        
        self.conn.commit()
        print("✅ Dados de exemplo inseridos com sucesso!")
    
    def analisar_vendas(self):
        """Análise descritiva das vendas"""
        print("\n📊 ANÁLISE DESCRITIVA - VENDAS")
        print("=" * 50)
        
        # Estatísticas gerais
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_pedidos,
                SUM(valor_total) as receita_total,
                AVG(valor_total) as ticket_medio,
                COUNT(DISTINCT usuario_id) as usuarios_unicos
            FROM pedidos 
            WHERE status = 'concluido'
        """)
        
        stats = self.cursor.fetchone()
        print(f"📈 Estatísticas Gerais:")
        print(f"  Total de pedidos: {stats['total_pedidos']}")
        print(f"  Receita total: R$ {stats['receita_total']:,.2f}")
        print(f"  Ticket médio: R$ {stats['ticket_medio']:,.2f}")
        print(f"  Usuários únicos: {stats['usuarios_unicos']}")
        
        # Análise por produto
        self.cursor.execute("""
            SELECT 
                p.produto_id,
                p.nome,
                p.marca,
                p.preco,
                COUNT(ip.id) as total_vendas,
                SUM(ip.quantidade) as quantidade_vendida,
                SUM(ip.valor_total) as receita_total,
                AVG(ip.preco_unitario) as preco_medio_venda
            FROM produtos_relacional p
            LEFT JOIN itens_pedido ip ON p.produto_id = ip.produto_id
            LEFT JOIN pedidos ped ON ip.pedido_id = ped.id
            WHERE ped.status = 'concluido' OR ped.status IS NULL
            GROUP BY p.produto_id, p.nome, p.marca, p.preco
            ORDER BY receita_total DESC NULLS LAST
        """)
        
        produtos_stats = self.cursor.fetchall()
        
        print(f"\n🏆 Top Produtos por Receita:")
        for produto in produtos_stats:
            print(f"  {produto['nome']} ({produto['marca']})")
            print(f"    Vendas: {produto['total_vendas'] or 0}")
            print(f"    Quantidade: {produto['quantidade_vendida'] or 0}")
            print(f"    Receita: R$ {produto['receita_total'] or 0:,.2f}")
            print()
    
    def analisar_usuarios(self):
        """Análise preditiva dos usuários"""
        print("\n🔍 ANÁLISE PREDITIVA - USUÁRIOS")
        print("=" * 50)
        
        # Query para análise de usuários
        self.cursor.execute("""
            SELECT 
                u.usuario_id,
                u.nome,
                u.segmento,
                u.valor_total_compras,
                COUNT(p.id) as total_pedidos,
                AVG(p.valor_total) as ticket_medio,
                COUNT(DISTINCT ip.produto_id) as produtos_unicos,
                MAX(p.data_pedido) as ultima_compra,
                EXTRACT(DAYS FROM NOW() - MAX(p.data_pedido)) as dias_sem_comprar,
                COUNT(CASE WHEN p.status = 'concluido' THEN 1 END) as pedidos_concluidos,
                COUNT(CASE WHEN p.status = 'pendente' THEN 1 END) as pedidos_pendentes
            FROM usuarios u
            LEFT JOIN pedidos p ON u.id = p.usuario_id
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            GROUP BY u.usuario_id, u.nome, u.segmento, u.valor_total_compras
            ORDER BY u.valor_total_compras DESC
        """)
        
        usuarios_df = pd.DataFrame(self.cursor.fetchall())
        
        if not usuarios_df.empty:
            print("👥 Análise de Usuários:")
            print(usuarios_df.to_string(index=False))
            
            # Estatísticas descritivas
            print(f"\n📊 Estatísticas Descritivas:")
            print(f"Usuários analisados: {len(usuarios_df)}")
            print(f"Valor médio de compras: R$ {usuarios_df['valor_total_compras'].mean():,.2f}")
            print(f"Pedidos médios por usuário: {usuarios_df['total_pedidos'].mean():.1f}")
            print(f"Ticket médio: R$ {usuarios_df['ticket_medio'].mean():,.2f}")
            
            return usuarios_df
        else:
            print("❌ Nenhum dado de usuário encontrado")
            return None
    
    def predicao_churn(self, usuarios_df):
        """Predição de churn de usuários"""
        if usuarios_df is None or usuarios_df.empty:
            print("❌ Dados insuficientes para predição de churn")
            return
        
        print("\n🎯 PREDIÇÃO DE CHURN")
        print("=" * 50)
        
        # Preparar features para predição
        usuarios_df['dias_sem_comprar'] = usuarios_df['dias_sem_comprar'].fillna(365)  # Usuários sem compras = 365 dias
        usuarios_df['ticket_medio'] = usuarios_df['ticket_medio'].fillna(0)
        usuarios_df['produtos_unicos'] = usuarios_df['produtos_unicos'].fillna(0)
        
        # Criar variável target (churn = dias sem comprar > 30)
        usuarios_df['churn'] = (usuarios_df['dias_sem_comprar'] > 30).astype(int)
        
        # Features para o modelo
        features = ['valor_total_compras', 'total_pedidos', 'ticket_medio', 'produtos_unicos', 'dias_sem_comprar']
        X = usuarios_df[features].fillna(0)
        y = usuarios_df['churn']
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Treinar modelo
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Fazer predições
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Avaliar modelo
        print("📈 Relatório de Classificação:")
        print(classification_report(y_test, y_pred))
        
        print("\n🎯 Matriz de Confusão:")
        print(confusion_matrix(y_test, y_pred))
        
        # Importância das features
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔍 Importância das Features:")
        print(feature_importance.to_string(index=False))
        
        # Predições para todos os usuários
        usuarios_df['probabilidade_churn'] = model.predict_proba(X)[:, 1]
        usuarios_df['predicao_churn'] = model.predict(X)
        
        print(f"\n👥 Usuários com Risco de Churn:")
        risco_churn = usuarios_df[usuarios_df['probabilidade_churn'] > 0.5]
        if not risco_churn.empty:
            print(risco_churn[['usuario_id', 'nome', 'probabilidade_churn', 'dias_sem_comprar']].to_string(index=False))
        else:
            print("Nenhum usuário com risco alto de churn identificado")
        
        return usuarios_df
    
    def analisar_tendencias(self):
        """Análise de tendências temporais"""
        print("\n📈 ANÁLISE DE TENDÊNCIAS TEMPORAIS")
        print("=" * 50)
        
        # Vendas por dia
        self.cursor.execute("""
            SELECT 
                DATE(data_pedido) as data,
                COUNT(*) as total_pedidos,
                SUM(valor_total) as receita_dia,
                AVG(valor_total) as ticket_medio_dia
            FROM pedidos 
            WHERE status = 'concluido'
            GROUP BY DATE(data_pedido)
            ORDER BY data
        """)
        
        vendas_diarias = pd.DataFrame(self.cursor.fetchall())
        
        if not vendas_diarias.empty:
            print("📅 Vendas por Dia:")
            print(vendas_diarias.to_string(index=False))
            
            # Calcular crescimento
            vendas_diarias['crescimento_receita'] = vendas_diarias['receita_dia'].pct_change() * 100
            
            print(f"\n📊 Tendências:")
            print(f"Crescimento médio diário: {vendas_diarias['crescimento_receita'].mean():.1f}%")
            print(f"Maior crescimento: {vendas_diarias['crescimento_receita'].max():.1f}%")
            print(f"Menor crescimento: {vendas_diarias['crescimento_receita'].min():.1f}%")
            
            return vendas_diarias
        else:
            print("❌ Dados insuficientes para análise temporal")
            return None
    
    def visualizar_dados(self, usuarios_df, vendas_diarias):
        """Criar visualizações dos dados"""
        print("\n📊 CRIANDO VISUALIZAÇÕES")
        print("=" * 50)
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Análise Preditiva - PostgreSQL E-commerce', fontsize=16)
        
        # Gráfico 1: Distribuição de valores de compra
        if usuarios_df is not None and not usuarios_df.empty:
            axes[0, 0].hist(usuarios_df['valor_total_compras'], bins=10, alpha=0.7, color='skyblue')
            axes[0, 0].set_title('Distribuição de Valores de Compra')
            axes[0, 0].set_xlabel('Valor Total Compras (R$)')
            axes[0, 0].set_ylabel('Frequência')
        
        # Gráfico 2: Segmentos de usuários
        if usuarios_df is not None and not usuarios_df.empty:
            segmentos = usuarios_df['segmento'].value_counts()
            axes[0, 1].pie(segmentos.values, labels=segmentos.index, autopct='%1.1f%%', startangle=90)
            axes[0, 1].set_title('Distribuição por Segmento')
        
        # Gráfico 3: Vendas por dia
        if vendas_diarias is not None and not vendas_diarias.empty:
            axes[1, 0].plot(vendas_diarias['data'], vendas_diarias['receita_dia'], marker='o', color='green')
            axes[1, 0].set_title('Receita por Dia')
            axes[1, 0].set_xlabel('Data')
            axes[1, 0].set_ylabel('Receita (R$)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Produtos mais vendidos
        self.cursor.execute("""
            SELECT 
                p.nome,
                SUM(ip.quantidade) as quantidade_vendida
            FROM produtos_relacional p
            LEFT JOIN itens_pedido ip ON p.produto_id = ip.produto_id
            LEFT JOIN pedidos ped ON ip.pedido_id = ped.id
            WHERE ped.status = 'concluido'
            GROUP BY p.nome
            ORDER BY quantidade_vendida DESC
            LIMIT 5
        """)
        
        produtos_vendidos = self.cursor.fetchall()
        if produtos_vendidos:
            nomes = [p['nome'][:15] + '...' if len(p['nome']) > 15 else p['nome'] for p in produtos_vendidos]
            quantidades = [p['quantidade_vendida'] or 0 for p in produtos_vendidos]
            axes[1, 1].bar(nomes, quantidades, color=['red', 'blue', 'green', 'orange', 'purple'], alpha=0.7)
            axes[1, 1].set_title('Top 5 Produtos Vendidos')
            axes[1, 1].set_ylabel('Quantidade Vendida')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('analise_postgresql_demo.png', dpi=300, bbox_inches='tight')
        print("✅ Gráficos salvos em 'analise_postgresql_demo.png'")
        plt.show()
    
    def demonstrar_operacoes(self):
        """Demonstrar operações CRUD básicas"""
        print("\n🔧 DEMONSTRAÇÃO DE OPERAÇÕES CRUD")
        print("=" * 50)
        
        # CREATE - Inserir novo usuário
        print("1️⃣ CREATE - Inserindo novo usuário...")
        self.cursor.execute("""
            INSERT INTO usuarios (usuario_id, email, nome, sobrenome, data_nascimento, genero, telefone, segmento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, usuario_id
        """, ('U006', 'novo.usuario@email.com', 'Novo', 'Usuário', '1990-01-01', 'M', '(11) 44444-4444', 'new_user'))
        
        novo_usuario = self.cursor.fetchone()
        print(f"✅ Usuário inserido: ID {novo_usuario['id']}, Usuario ID {novo_usuario['usuario_id']}")
        
        # READ - Buscar usuários por segmento
        print("\n2️⃣ READ - Buscando usuários high_value...")
        self.cursor.execute("""
            SELECT usuario_id, nome, email, valor_total_compras
            FROM usuarios 
            WHERE segmento = %s
            ORDER BY valor_total_compras DESC
        """, ('high_value',))
        
        usuarios_high_value = self.cursor.fetchall()
        print(f"💰 Encontrados {len(usuarios_high_value)} usuários high_value:")
        for usuario in usuarios_high_value:
            print(f"  - {usuario['nome']} - R$ {usuario['valor_total_compras']:,.2f}")
        
        # UPDATE - Atualizar segmento do usuário
        print("\n3️⃣ UPDATE - Atualizando segmento do usuário...")
        self.cursor.execute("""
            UPDATE usuarios
            SET segmento = %s, data_atualizacao = NOW()
            WHERE usuario_id = %s
        """, ('medium_value', 'U006'))
        
        print(f"✅ {self.cursor.rowcount} usuário(s) atualizado(s)")
        
        # DELETE - Remover usuário (soft delete)
        print("\n4️⃣ DELETE - Desativando usuário...")
        self.cursor.execute("""
            UPDATE usuarios
            SET ativo = FALSE
            WHERE usuario_id = %s
        """, ('U006',))
        
        print(f"✅ {self.cursor.rowcount} usuário(s) desativado(s)")
        
        self.conn.commit()
    
    def executar_demonstracao_completa(self):
        """Executar demonstração completa"""
        print("🚀 DEMONSTRAÇÃO PRÁTICA - POSTGRESQL + ANÁLISE PREDITIVA")
        print("=" * 70)
        
        try:
            # 1. Criar tabelas
            self.criar_tabelas()
            
            # 2. Inserir dados
            self.inserir_dados_exemplo()
            
            # 3. Análise descritiva
            self.analisar_vendas()
            
            # 4. Análise preditiva
            usuarios_df = self.analisar_usuarios()
            
            # 5. Predição de churn
            if usuarios_df is not None:
                usuarios_df = self.predicao_churn(usuarios_df)
            
            # 6. Análise de tendências
            vendas_diarias = self.analisar_tendencias()
            
            # 7. Operações CRUD
            self.demonstrar_operacoes()
            
            # 8. Visualizações
            self.visualizar_dados(usuarios_df, vendas_diarias)
            
            print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print("📊 Dados analisados:")
            print(f"  - Usuários: {self.cursor.execute('SELECT COUNT(*) FROM usuarios'); self.cursor.fetchone()[0]}")
            print(f"  - Produtos: {self.cursor.execute('SELECT COUNT(*) FROM produtos_relacional'); self.cursor.fetchone()[0]}")
            print(f"  - Pedidos: {self.cursor.execute('SELECT COUNT(*) FROM pedidos'); self.cursor.fetchone()[0]}")
            print("\n💡 Próximos passos:")
            print("  - Integrar com MongoDB para dados não estruturados")
            print("  - Implementar algoritmos de ML mais avançados")
            print("  - Deploy em produção com monitoramento")
            
        except Exception as e:
            print(f"❌ Erro durante demonstração: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

def main():
    """Função principal"""
    print("🎯 Iniciando Demonstração Prática PostgreSQL + Análise Preditiva")
    
    # Criar instância da classe
    demo = EcommercePostgreSQL()
    
    # Executar demonstração
    demo.executar_demonstracao_completa()

if __name__ == "__main__":
    main()
