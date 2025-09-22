#!/usr/bin/env python3
"""
Demonstração MongoDB - Análise Preditiva E-commerce
Script para demonstrar operações NoSQL com dados de comportamento e produtos
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

def conectar_mongodb():
    """Conectar ao MongoDB"""
    try:
        client = MongoClient('mongodb://localhost:27017')
        db = client['ecommerce_demo']
        
        # Testar conexão
        db.command('ping')
        print("✅ Conectado ao MongoDB com sucesso!")
        return client, db
    except Exception as e:
        print(f"❌ Erro ao conectar MongoDB: {e}")
        return None, None

def analisar_produtos(db):
    """Analisar dados de produtos"""
    print("\n📊 ANÁLISE DE PRODUTOS")
    print("=" * 50)
    
    produtos_collection = db['produtos']
    
    # Contar produtos
    total_produtos = produtos_collection.count_documents({})
    produtos_ativos = produtos_collection.count_documents({"ativo": True})
    
    print(f"📦 Total de produtos: {total_produtos}")
    print(f"✅ Produtos ativos: {produtos_ativos}")
    
    # Análise por categoria
    pipeline_categoria = [
        {"$group": {
            "_id": "$categoria",
            "total_produtos": {"$sum": 1},
            "preco_medio": {"$avg": "$preco"},
            "estoque_total": {"$sum": "$estoque"},
            "avaliacao_media": {"$avg": "$avaliacao_media"}
        }},
        {"$sort": {"total_produtos": -1}}
    ]
    
    resultado_categoria = list(produtos_collection.aggregate(pipeline_categoria))
    
    print("\n📈 Análise por Categoria:")
    for cat in resultado_categoria:
        print(f"  {cat['_id']}:")
        print(f"    Produtos: {cat['total_produtos']}")
        print(f"    Preço médio: R$ {cat['preco_medio']:.2f}")
        print(f"    Estoque total: {cat['estoque_total']}")
        print(f"    Avaliação média: {cat['avaliacao_media']:.1f}")
    
    # Produtos mais caros
    produtos_caros = produtos_collection.find({"ativo": True}).sort("preco", -1).limit(3)
    
    print("\n💰 Top 3 Produtos Mais Caros:")
    for produto in produtos_caros:
        print(f"  {produto['nome']}: R$ {produto['preco']:.2f}")
    
    return resultado_categoria

def analisar_comportamento(db):
    """Analisar comportamento dos usuários"""
    print("\n👥 ANÁLISE DE COMPORTAMENTO")
    print("=" * 50)
    
    comportamento_collection = db['usuarios_comportamento']
    
    # Pipeline para análise de comportamento
    pipeline_comportamento = [
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
            "searches": {
                "$sum": {"$cond": [{"$eq": ["$eventos.tipo", "search"]}, 1, 0]}
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
            "searches": 1,
            "tempo_total": 1,
            "produtos_unicos": {"$size": "$produtos_unicos"},
            "taxa_conversao": {
                "$cond": [
                    {"$gt": ["$page_views", 0]},
                    {"$divide": ["$add_to_cart", "$page_views"]},
                    0
                ]
            },
            "tempo_medio_evento": {
                "$cond": [
                    {"$gt": ["$total_eventos", 0]},
                    {"$divide": ["$tempo_total", "$total_eventos"]},
                    0
                ]
            }
        }},
        {"$sort": {"total_eventos": -1}}
    ]
    
    # Executar pipeline
    comportamento_data = list(comportamento_collection.aggregate(pipeline_comportamento))
    
    if comportamento_data:
        comportamento_df = pd.DataFrame(comportamento_data)
        
        print(f"👤 Usuários analisados: {len(comportamento_df)}")
        print(f"📊 Total de eventos: {comportamento_df['total_eventos'].sum()}")
        print(f"👀 Page views: {comportamento_df['page_views'].sum()}")
        print(f"🛒 Add to cart: {comportamento_df['add_to_cart'].sum()}")
        print(f"🔍 Searches: {comportamento_df['searches'].sum()}")
        
        # Estatísticas descritivas
        print("\n📈 Estatísticas Descritivas:")
        print(f"  Eventos por usuário (média): {comportamento_df['total_eventos'].mean():.1f}")
        print(f"  Taxa de conversão (média): {comportamento_df['taxa_conversao'].mean():.1%}")
        print(f"  Tempo médio por evento: {comportamento_df['tempo_medio_evento'].mean():.1f}s")
        print(f"  Produtos únicos (média): {comportamento_df['produtos_unicos'].mean():.1f}")
        
        # Top usuários mais ativos
        print("\n🏆 Top 5 Usuários Mais Ativos:")
        top_usuarios = comportamento_df.head()
        for _, user in top_usuarios.iterrows():
            print(f"  {user['usuario_id']}: {user['total_eventos']} eventos, "
                  f"{user['taxa_conversao']:.1%} conversão")
        
        return comportamento_df
    else:
        print("❌ Nenhum dado de comportamento encontrado")
        return None

def analisar_recomendacoes(db):
    """Analisar sistema de recomendações"""
    print("\n🎯 ANÁLISE DE RECOMENDAÇÕES")
    print("=" * 50)
    
    recomendacoes_collection = db['recomendacoes']
    
    # Contar recomendações
    total_recomendacoes = recomendacoes_collection.count_documents({})
    print(f"🎯 Total de recomendações: {total_recomendacoes}")
    
    # Pipeline para análise de recomendações
    pipeline_recomendacoes = [
        {"$unwind": "$recomendacoes"},
        {"$group": {
            "_id": "$recomendacoes.produto_id",
            "total_recomendacoes": {"$sum": 1},
            "score_medio": {"$avg": "$recomendacoes.score"},
            "score_maximo": {"$max": "$recomendacoes.score"},
            "score_minimo": {"$min": "$recomendacoes.score"}
        }},
        {"$sort": {"total_recomendacoes": -1}}
    ]
    
    resultado_recomendacoes = list(recomendacoes_collection.aggregate(pipeline_recomendacoes))
    
    print("\n📊 Produtos Mais Recomendados:")
    for rec in resultado_recomendacoes:
        print(f"  {rec['_id']}:")
        print(f"    Recomendações: {rec['total_recomendacoes']}")
        print(f"    Score médio: {rec['score_medio']:.3f}")
        print(f"    Score máximo: {rec['score_maximo']:.3f}")
        print(f"    Score mínimo: {rec['score_minimo']:.3f}")
    
    # Análise por algoritmo
    pipeline_algoritmo = [
        {"$group": {
            "_id": "$algoritmo",
            "total_recomendacoes": {"$sum": 1},
            "usuarios_unicos": {"$addToSet": "$usuario_id"}
        }},
        {"$project": {
            "algoritmo": "$_id",
            "total_recomendacoes": 1,
            "usuarios_unicos": {"$size": "$usuarios_unicos"}
        }}
    ]
    
    resultado_algoritmo = list(recomendacoes_collection.aggregate(pipeline_algoritmo))
    
    print("\n🤖 Análise por Algoritmo:")
    for algo in resultado_algoritmo:
        print(f"  {algo['algoritmo']}:")
        print(f"    Total recomendações: {algo['total_recomendacoes']}")
        print(f"    Usuários únicos: {algo['usuarios_unicos']}")
    
    return resultado_recomendacoes

def criar_visualizacoes(comportamento_df, produtos_data):
    """Criar visualizações dos dados"""
    print("\n📊 CRIANDO VISUALIZAÇÕES")
    print("=" * 50)
    
    if comportamento_df is None or comportamento_df.empty:
        print("❌ Dados insuficientes para visualizações")
        return
    
    # Configurar figura
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('📊 Dashboard MongoDB - Análise Preditiva E-commerce', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Distribuição de eventos
    axes[0, 0].hist(comportamento_df['total_eventos'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('📱 Distribuição de Eventos por Usuário', fontweight='bold')
    axes[0, 0].set_xlabel('Total de Eventos')
    axes[0, 0].set_ylabel('Frequência')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Adicionar estatísticas
    mean_events = comportamento_df['total_eventos'].mean()
    axes[0, 0].axvline(mean_events, color='red', linestyle='--', linewidth=2, label=f'Média: {mean_events:.1f}')
    axes[0, 0].legend()
    
    # Gráfico 2: Taxa de conversão vs Page Views
    scatter = axes[0, 1].scatter(comportamento_df['page_views'], comportamento_df['taxa_conversao'], 
                               alpha=0.7, s=100, c=comportamento_df['total_eventos'], 
                               cmap='viridis', edgecolors='black')
    axes[0, 1].set_title('🎯 Taxa de Conversão vs Page Views', fontweight='bold')
    axes[0, 1].set_xlabel('Page Views')
    axes[0, 1].set_ylabel('Taxa de Conversão')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Adicionar colorbar
    cbar = plt.colorbar(scatter, ax=axes[0, 1])
    cbar.set_label('Total de Eventos')
    
    # Gráfico 3: Tempo médio por evento
    axes[1, 0].boxplot(comportamento_df['tempo_medio_evento'], patch_artist=True, 
                      boxprops=dict(facecolor='lightgreen', alpha=0.7))
    axes[1, 0].set_title('⏱️ Tempo Médio por Evento', fontweight='bold')
    axes[1, 0].set_ylabel('Tempo (segundos)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Gráfico 4: Produtos únicos vs Total de eventos
    axes[1, 1].scatter(comportamento_df['total_eventos'], comportamento_df['produtos_unicos'], 
                      alpha=0.7, s=100, c=comportamento_df['taxa_conversao'], 
                      cmap='plasma', edgecolors='black')
    axes[1, 1].set_title('🛍️ Produtos Únicos vs Total de Eventos', fontweight='bold')
    axes[1, 1].set_xlabel('Total de Eventos')
    axes[1, 1].set_ylabel('Produtos Únicos')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Adicionar colorbar
    cbar2 = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
    cbar2.set_label('Taxa de Conversão')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('dashboard_mongodb.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard salvo como 'dashboard_mongodb.png'")
    
    # Mostrar gráfico
    plt.show()

def demonstrar_operacoes_crud(db):
    """Demonstrar operações CRUD no MongoDB"""
    print("\n🔧 DEMONSTRAÇÃO DE OPERAÇÕES CRUD")
    print("=" * 50)
    
    produtos_collection = db['produtos']
    
    # CREATE - Inserir novo produto
    print("📝 CREATE - Inserindo novo produto...")
    novo_produto = {
        "produto_id": "P999",
        "nome": "Produto Demo",
        "categoria": "Eletrônicos > Demo",
        "marca": "Demo",
        "preco": 999.99,
        "caracteristicas": {
            "demo": "true",
            "criado_em": datetime.now().isoformat()
        },
        "tags": ["demo", "teste"],
        "estoque": 10,
        "ativo": True,
        "data_criacao": datetime.now()
    }
    
    result = produtos_collection.insert_one(novo_produto)
    print(f"✅ Produto inserido com ID: {result.inserted_id}")
    
    # READ - Buscar produto
    print("\n🔍 READ - Buscando produto...")
    produto_encontrado = produtos_collection.find_one({"produto_id": "P999"})
    if produto_encontrado:
        print(f"✅ Produto encontrado: {produto_encontrado['nome']}")
    
    # UPDATE - Atualizar produto
    print("\n✏️ UPDATE - Atualizando produto...")
    result = produtos_collection.update_one(
        {"produto_id": "P999"},
        {"$set": {
            "preco": 1299.99,
            "estoque": 15,
            "data_atualizacao": datetime.now()
        }}
    )
    print(f"✅ Produto atualizado: {result.modified_count} documento(s)")
    
    # DELETE - Remover produto
    print("\n🗑️ DELETE - Removendo produto...")
    result = produtos_collection.delete_one({"produto_id": "P999"})
    print(f"✅ Produto removido: {result.deleted_count} documento(s)")
    
    # Agregação complexa
    print("\n📊 AGREGAÇÃO COMPLEXA - Produtos por marca...")
    pipeline_marca = [
        {"$match": {"ativo": True}},
        {"$group": {
            "_id": "$marca",
            "total_produtos": {"$sum": 1},
            "preco_medio": {"$avg": "$preco"},
            "estoque_total": {"$sum": "$estoque"},
            "avaliacao_media": {"$avg": "$avaliacao_media"}
        }},
        {"$sort": {"total_produtos": -1}}
    ]
    
    resultado_marca = list(produtos_collection.aggregate(pipeline_marca))
    print("📈 Análise por Marca:")
    for marca in resultado_marca:
        print(f"  {marca['_id']}:")
        print(f"    Produtos: {marca['total_produtos']}")
        print(f"    Preço médio: R$ {marca['preco_medio']:.2f}")
        print(f"    Estoque total: {marca['estoque_total']}")
        print(f"    Avaliação média: {marca['avaliacao_media']:.1f}")

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO MONGODB - ANÁLISE PREDITIVA E-COMMERCE")
    print("=" * 60)
    
    # Conectar ao MongoDB
    client, db = conectar_mongodb()
    if not client or not db:
        print("❌ Não foi possível conectar ao MongoDB")
        return False
    
    try:
        # Análise de produtos
        produtos_data = analisar_produtos(db)
        
        # Análise de comportamento
        comportamento_df = analisar_comportamento(db)
        
        # Análise de recomendações
        recomendacoes_data = analisar_recomendacoes(db)
        
        # Criar visualizações
        criar_visualizacoes(comportamento_df, produtos_data)
        
        # Demonstrar operações CRUD
        demonstrar_operacoes_crud(db)
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO MONGODB CONCLUÍDA COM SUCESSO!")
        print("📊 Análise preditiva implementada com dados NoSQL")
        print("🎯 Sistema de recomendações funcionando")
        print("📈 Visualizações criadas e salvas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        return False
    
    finally:
        # Fechar conexão
        if client:
            client.close()
            print("\n🔌 Conexão MongoDB fechada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)