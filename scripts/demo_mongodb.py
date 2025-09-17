#!/usr/bin/env python3
"""
Demonstração Prática - Sistema de Recomendação E-commerce
MongoDB + Análise Preditiva

Este script demonstra operações práticas com MongoDB para análise preditiva
de um sistema de recomendação de produtos e-commerce.
"""

import json
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class EcommerceMongoDB:
    def __init__(self, connection_string="mongodb://localhost:27017"):
        """Inicializar conexão com MongoDB"""
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client['ecommerce_demo']
            print("✅ Conectado ao MongoDB com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar MongoDB: {e}")
            print("💡 Certifique-se de que o MongoDB está rodando")
    
    def criar_dados_exemplo(self):
        """Criar dados de exemplo para demonstração"""
        print("\n🔄 Criando dados de exemplo...")
        
        # Limpar coleções existentes
        self.db.produtos.drop()
        self.db.usuarios_comportamento.drop()
        self.db.recomendacoes.drop()
        
        # Dados de produtos
        produtos = [
            {
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
                "tags": ["smartphone", "android", "samsung"],
                "avaliacao_media": 4.5,
                "total_avaliacoes": 1250,
                "estoque": 45,
                "ativo": True,
                "data_criacao": datetime.now()
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
                    "armazenamento": "128GB"
                },
                "tags": ["smartphone", "ios", "apple"],
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
                    "processador": "Intel Core i7",
                    "ram": "16GB",
                    "armazenamento": "512GB SSD"
                },
                "tags": ["notebook", "windows", "dell"],
                "avaliacao_media": 4.3,
                "total_avaliacoes": 567,
                "estoque": 20,
                "ativo": True,
                "data_criacao": datetime.now()
            }
        ]
        
        # Inserir produtos
        self.db.produtos.insert_many(produtos)
        print(f"✅ {len(produtos)} produtos inseridos")
        
        # Gerar dados de comportamento simulados
        usuarios = ["U001", "U002", "U003", "U004", "U005"]
        produtos_ids = ["P001", "P002", "P003"]
        
        comportamentos = []
        for i in range(50):  # 50 eventos de comportamento
            comportamento = {
                "usuario_id": random.choice(usuarios),
                "sessao_id": f"S{i:03d}",
                "timestamp": datetime.now() - timedelta(days=random.randint(0, 30)),
                "eventos": [
                    {
                        "tipo": random.choice(["page_view", "click", "add_to_cart", "search"]),
                        "produto_id": random.choice(produtos_ids),
                        "tempo_pagina": random.randint(10, 300),
                        "timestamp": datetime.now() - timedelta(days=random.randint(0, 30))
                    }
                ]
            }
            comportamentos.append(comportamento)
        
        self.db.usuarios_comportamento.insert_many(comportamentos)
        print(f"✅ {len(comportamentos)} eventos de comportamento inseridos")
        
        return True
    
    def analisar_produtos(self):
        """Análise descritiva dos produtos"""
        print("\n📊 ANÁLISE DESCRITIVA - PRODUTOS")
        print("=" * 50)
        
        # Estatísticas básicas
        total_produtos = self.db.produtos.count_documents({"ativo": True})
        print(f"Total de produtos ativos: {total_produtos}")
        
        # Preço médio por categoria
        pipeline = [
            {"$match": {"ativo": True}},
            {"$group": {
                "_id": "$categoria",
                "total_produtos": {"$sum": 1},
                "preco_medio": {"$avg": "$preco"},
                "avaliacao_media": {"$avg": "$avaliacao_media"},
                "estoque_total": {"$sum": "$estoque"}
            }},
            {"$sort": {"preco_medio": -1}}
        ]
        
        resultado = list(self.db.produtos.aggregate(pipeline))
        
        print("\n📈 Análise por Categoria:")
        for item in resultado:
            print(f"Categoria: {item['_id']}")
            print(f"  Produtos: {item['total_produtos']}")
            print(f"  Preço médio: R$ {item['preco_medio']:.2f}")
            print(f"  Avaliação média: {item['avaliacao_media']:.1f}")
            print(f"  Estoque total: {item['estoque_total']}")
            print()
    
    def analisar_comportamento(self):
        """Análise preditiva do comportamento dos usuários"""
        print("\n🔍 ANÁLISE PREDITIVA - COMPORTAMENTO")
        print("=" * 50)
        
        # Pipeline para análise de comportamento
        pipeline = [
            {"$unwind": "$eventos"},
            {"$group": {
                "_id": "$usuario_id",
                "total_eventos": {"$sum": 1},
                "page_views": {
                    "$sum": {"$cond": [{"$eq": ["$eventos.tipo", "page_view"]}, 1, 0]}
                },
                "clicks": {
                    "$sum": {"$cond": [{"$eq": ["$eventos.tipo", "click"]}, 1, 0]}
                },
                "add_to_cart": {
                    "$sum": {"$cond": [{"$eq": ["$eventos.tipo", "add_to_cart"]}, 1, 0]}
                },
                "tempo_total": {"$sum": "$eventos.tempo_pagina"},
                "produtos_unicos": {"$addToSet": "$eventos.produto_id"}
            }},
            {"$project": {
                "usuario_id": "$_id",
                "total_eventos": 1,
                "page_views": 1,
                "clicks": 1,
                "add_to_cart": 1,
                "tempo_total": 1,
                "produtos_unicos": {"$size": "$produtos_unicos"},
                "taxa_conversao": {
                    "$cond": [
                        {"$gt": ["$page_views", 0]},
                        {"$divide": ["$add_to_cart", "$page_views"]},
                        0
                    ]
                }
            }},
            {"$sort": {"total_eventos": -1}}
        ]
        
        comportamento_df = pd.DataFrame(list(self.db.usuarios_comportamento.aggregate(pipeline)))
        
        if not comportamento_df.empty:
            print("👥 Análise de Comportamento por Usuário:")
            print(comportamento_df.to_string(index=False))
            
            # Estatísticas descritivas
            print(f"\n📊 Estatísticas Descritivas:")
            print(f"Usuários analisados: {len(comportamento_df)}")
            print(f"Eventos médios por usuário: {comportamento_df['total_eventos'].mean():.1f}")
            print(f"Taxa de conversão média: {comportamento_df['taxa_conversao'].mean():.2%}")
            print(f"Produtos únicos médios: {comportamento_df['produtos_unicos'].mean():.1f}")
            
            return comportamento_df
        else:
            print("❌ Nenhum dado de comportamento encontrado")
            return None
    
    def clustering_usuarios(self, comportamento_df):
        """Clustering de usuários para segmentação"""
        if comportamento_df is None or comportamento_df.empty:
            print("❌ Dados insuficientes para clustering")
            return
        
        print("\n🎯 CLUSTERING DE USUÁRIOS")
        print("=" * 50)
        
        # Preparar features para clustering
        features = ['total_eventos', 'page_views', 'clicks', 'add_to_cart', 'produtos_unicos']
        X = comportamento_df[features].fillna(0)
        
        # Normalizar dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar K-Means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        comportamento_df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Análise dos clusters
        cluster_analysis = comportamento_df.groupby('cluster')[features].mean()
        
        print("📈 Análise de Clusters:")
        print(cluster_analysis.round(2))
        
        # Interpretar clusters
        print("\n🏷️ Interpretação dos Clusters:")
        for cluster_id in range(3):
            cluster_data = comportamento_df[comportamento_df['cluster'] == cluster_id]
            avg_events = cluster_data['total_eventos'].mean()
            avg_conversion = cluster_data['taxa_conversao'].mean()
            
            if avg_events > comportamento_df['total_eventos'].mean():
                if avg_conversion > comportamento_df['taxa_conversao'].mean():
                    segmento = "🔥 Usuários Ativos e Convertidos"
                else:
                    segmento = "👀 Usuários Ativos mas Baixa Conversão"
            else:
                segmento = "😴 Usuários Passivos"
            
            print(f"Cluster {cluster_id}: {segmento}")
            print(f"  Usuários: {len(cluster_data)}")
            print(f"  Eventos médios: {avg_events:.1f}")
            print(f"  Taxa conversão: {avg_conversion:.2%}")
            print()
        
        return comportamento_df
    
    def gerar_recomendacoes(self, comportamento_df):
        """Gerar recomendações baseadas em análise preditiva"""
        print("\n🎯 GERAÇÃO DE RECOMENDAÇÕES")
        print("=" * 50)
        
        if comportamento_df is None or comportamento_df.empty:
            print("❌ Dados insuficientes para recomendações")
            return
        
        # Simular algoritmo de recomendação colaborativa
        usuarios = comportamento_df['usuario_id'].unique()
        produtos = ["P001", "P002", "P003"]
        
        recomendacoes = []
        
        for usuario in usuarios:
            # Simular scores de recomendação
            scores = []
            for produto in produtos:
                # Score baseado em comportamento do usuário
                user_data = comportamento_df[comportamento_df['usuario_id'] == usuario]
                if not user_data.empty:
                    base_score = random.uniform(0.3, 0.9)
                    # Ajustar score baseado na atividade do usuário
                    if user_data['total_eventos'].iloc[0] > comportamento_df['total_eventos'].mean():
                        base_score += 0.1
                    if user_data['taxa_conversao'].iloc[0] > comportamento_df['taxa_conversao'].mean():
                        base_score += 0.1
                else:
                    base_score = random.uniform(0.2, 0.6)
                
                scores.append({
                    "produto_id": produto,
                    "score": min(base_score, 1.0),
                    "motivo": "collaborative_filtering"
                })
            
            # Ordenar por score
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            recomendacao = {
                "usuario_id": usuario,
                "algoritmo": "collaborative_filtering",
                "recomendacoes": scores[:2],  # Top 2 produtos
                "data_geracao": datetime.now(),
                "valido_ate": datetime.now() + timedelta(hours=2)
            }
            
            recomendacoes.append(recomendacao)
        
        # Salvar recomendações no MongoDB
        self.db.recomendacoes.insert_many(recomendacoes)
        
        print(f"✅ {len(recomendacoes)} recomendações geradas")
        
        # Mostrar exemplo de recomendação
        if recomendacoes:
            exemplo = recomendacoes[0]
            print(f"\n📋 Exemplo de Recomendação para {exemplo['usuario_id']}:")
            for rec in exemplo['recomendacoes']:
                produto = self.db.produtos.find_one({"produto_id": rec['produto_id']})
                if produto:
                    print(f"  {produto['nome']} - Score: {rec['score']:.2f}")
    
    def visualizar_dados(self, comportamento_df):
        """Criar visualizações dos dados"""
        if comportamento_df is None or comportamento_df.empty:
            print("❌ Dados insuficientes para visualização")
            return
        
        print("\n📊 CRIANDO VISUALIZAÇÕES")
        print("=" * 50)
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Análise Preditiva - Sistema de Recomendação E-commerce', fontsize=16)
        
        # Gráfico 1: Distribuição de eventos por usuário
        axes[0, 0].hist(comportamento_df['total_eventos'], bins=10, alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Distribuição de Eventos por Usuário')
        axes[0, 0].set_xlabel('Total de Eventos')
        axes[0, 0].set_ylabel('Frequência')
        
        # Gráfico 2: Taxa de conversão por usuário
        axes[0, 1].scatter(comportamento_df['page_views'], comportamento_df['taxa_conversao'], 
                          alpha=0.7, color='green')
        axes[0, 1].set_title('Taxa de Conversão vs Page Views')
        axes[0, 1].set_xlabel('Page Views')
        axes[0, 1].set_ylabel('Taxa de Conversão')
        
        # Gráfico 3: Clusters (se existir)
        if 'cluster' in comportamento_df.columns:
            scatter = axes[1, 0].scatter(comportamento_df['total_eventos'], 
                                       comportamento_df['taxa_conversao'],
                                       c=comportamento_df['cluster'], 
                                       cmap='viridis', alpha=0.7)
            axes[1, 0].set_title('Clusters de Usuários')
            axes[1, 0].set_xlabel('Total de Eventos')
            axes[1, 0].set_ylabel('Taxa de Conversão')
            plt.colorbar(scatter, ax=axes[1, 0])
        
        # Gráfico 4: Produtos mais visualizados
        produtos_stats = []
        for produto_id in ["P001", "P002", "P003"]:
            produto = self.db.produtos.find_one({"produto_id": produto_id})
            if produto:
                produtos_stats.append({
                    'nome': produto['nome'][:20] + '...',
                    'preco': produto['preco'],
                    'avaliacao': produto['avaliacao_media']
                })
        
        if produtos_stats:
            nomes = [p['nome'] for p in produtos_stats]
            precos = [p['preco'] for p in produtos_stats]
            axes[1, 1].bar(nomes, precos, color=['red', 'blue', 'green'], alpha=0.7)
            axes[1, 1].set_title('Preços dos Produtos')
            axes[1, 1].set_ylabel('Preço (R$)')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('analise_preditiva_demo.png', dpi=300, bbox_inches='tight')
        print("✅ Gráficos salvos em 'analise_preditiva_demo.png'")
        plt.show()
    
    def demonstrar_operacoes(self):
        """Demonstrar operações CRUD básicas"""
        print("\n🔧 DEMONSTRAÇÃO DE OPERAÇÕES CRUD")
        print("=" * 50)
        
        # CREATE - Inserir novo produto
        print("1️⃣ CREATE - Inserindo novo produto...")
        novo_produto = {
            "produto_id": "P004",
            "nome": "Tablet iPad Air",
            "categoria": "Eletrônicos > Tablets",
            "marca": "Apple",
            "preco": 3999.99,
            "caracteristicas": {
                "tela": "10.9 polegadas",
                "processador": "M1",
                "armazenamento": "64GB"
            },
            "tags": ["tablet", "ios", "apple"],
            "avaliacao_media": 4.6,
            "total_avaliacoes": 234,
            "estoque": 15,
            "ativo": True,
            "data_criacao": datetime.now()
        }
        
        result = self.db.produtos.insert_one(novo_produto)
        print(f"✅ Produto inserido com ID: {result.inserted_id}")
        
        # READ - Buscar produtos
        print("\n2️⃣ READ - Buscando produtos por categoria...")
        smartphones = list(self.db.produtos.find({
            "categoria": {"$regex": "Smartphones", "$options": "i"},
            "ativo": True
        }))
        
        print(f"📱 Encontrados {len(smartphones)} smartphones:")
        for produto in smartphones:
            print(f"  - {produto['nome']} - R$ {produto['preco']}")
        
        # UPDATE - Atualizar produto
        print("\n3️⃣ UPDATE - Atualizando preço do produto...")
        result = self.db.produtos.update_one(
            {"produto_id": "P001"},
            {
                "$set": {
                    "preco": 2799.99,
                    "data_atualizacao": datetime.now()
                }
            }
        )
        print(f"✅ {result.modified_count} produto(s) atualizado(s)")
        
        # DELETE - Remover produto (soft delete)
        print("\n4️⃣ DELETE - Desativando produto...")
        result = self.db.produtos.update_one(
            {"produto_id": "P004"},
            {"$set": {"ativo": False}}
        )
        print(f"✅ {result.modified_count} produto(s) desativado(s)")
    
    def executar_demonstracao_completa(self):
        """Executar demonstração completa"""
        print("🚀 DEMONSTRAÇÃO PRÁTICA - SISTEMA DE RECOMENDAÇÃO E-COMMERCE")
        print("=" * 70)
        
        try:
            # 1. Criar dados de exemplo
            self.criar_dados_exemplo()
            
            # 2. Análise descritiva
            self.analisar_produtos()
            
            # 3. Análise preditiva
            comportamento_df = self.analisar_comportamento()
            
            # 4. Clustering
            if comportamento_df is not None:
                comportamento_df = self.clustering_usuarios(comportamento_df)
            
            # 5. Recomendações
            self.gerar_recomendacoes(comportamento_df)
            
            # 6. Operações CRUD
            self.demonstrar_operacoes()
            
            # 7. Visualizações
            self.visualizar_dados(comportamento_df)
            
            print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print("📊 Dados analisados:")
            print(f"  - Produtos: {self.db.produtos.count_documents({})}")
            print(f"  - Eventos de comportamento: {self.db.usuarios_comportamento.count_documents({})}")
            print(f"  - Recomendações: {self.db.recomendacoes.count_documents({})}")
            print("\n💡 Próximos passos:")
            print("  - Integrar com PostgreSQL para dados transacionais")
            print("  - Implementar algoritmos de ML mais avançados")
            print("  - Deploy em produção com monitoramento")
            
        except Exception as e:
            print(f"❌ Erro durante demonstração: {e}")
        finally:
            self.client.close()

def main():
    """Função principal"""
    print("🎯 Iniciando Demonstração Prática MongoDB + Análise Preditiva")
    
    # Criar instância da classe
    demo = EcommerceMongoDB()
    
    # Executar demonstração
    demo.executar_demonstracao_completa()

if __name__ == "__main__":
    main()
