#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO PRÁTICA COMPLETA - ANÁLISE PREDITIVA E-COMMERCE
Sistema de Recomendação de Produtos com MongoDB + PostgreSQL

Este script demonstra uma aplicação prática completa de análise preditiva
para um sistema de recomendação de produtos e-commerce, funcionando mesmo
sem bancos de dados instalados (usa dados simulados).

Autor: Sistema de Análise Preditiva
Data: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import warnings
import json
import os
from typing import Dict, List, Tuple, Optional

# Machine Learning
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Configurações
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 10)

class EcommerceAnalyticsDemo:
    """Classe principal para demonstração de análise preditiva e-commerce"""
    
    def __init__(self):
        """Inicializar demonstração"""
        self.comportamento_df = None
        self.usuarios_transacionais = None
        self.produtos_df = None
        self.recomendacoes = {}
        
        print("🚀 DEMONSTRAÇÃO PRÁTICA - ANÁLISE PREDITIVA E-COMMERCE")
        print("=" * 70)
        print("📊 Sistema de Recomendação de Produtos")
        print("🗄️ Arquitetura: MongoDB (comportamento) + PostgreSQL (transações)")
        print("🎯 Objetivo: Demonstrar análise preditiva em cenário real")
        print("=" * 70)
    
    def criar_dados_simulados(self):
        """Criar dados simulados realistas para demonstração"""
        print("\n🔄 Criando dados simulados...")
        
        # Configurar seed para reprodutibilidade
        np.random.seed(42)
        random.seed(42)
        
        # 1. Dados de comportamento (MongoDB)
        n_usuarios = 50
        usuarios_ids = [f'U{i:03d}' for i in range(1, n_usuarios + 1)]
        
        self.comportamento_df = pd.DataFrame({
            'usuario_id': usuarios_ids,
            'total_eventos': np.random.poisson(20, n_usuarios),
            'page_views': np.random.poisson(15, n_usuarios),
            'clicks': np.random.poisson(12, n_usuarios),
            'add_to_cart': np.random.poisson(3, n_usuarios),
            'searches': np.random.poisson(5, n_usuarios),
            'produtos_unicos': np.random.randint(2, 15, n_usuarios),
            'tempo_total_sessao': np.random.normal(300, 100, n_usuarios),
            'sessoes_mes': np.random.poisson(8, n_usuarios)
        })
        
        # Calcular taxa de conversão
        self.comportamento_df['taxa_conversao'] = (
            self.comportamento_df['add_to_cart'] / 
            self.comportamento_df['page_views'].replace(0, 1)
        )
        
        # Calcular tempo médio por evento
        self.comportamento_df['tempo_medio_evento'] = (
            self.comportamento_df['tempo_total_sessao'] / 
            self.comportamento_df['total_eventos'].replace(0, 1)
        )
        
        # 2. Dados transacionais (PostgreSQL)
        segmentos = ['high_value', 'medium_value', 'low_value', 'new_user']
        segmento_weights = [0.15, 0.35, 0.35, 0.15]
        
        self.usuarios_transacionais = pd.DataFrame({
            'usuario_id': usuarios_ids,
            'nome': [f'Usuário {i}' for i in range(1, n_usuarios + 1)],
            'email': [f'usuario{i:03d}@email.com' for i in range(1, n_usuarios + 1)],
            'segmento': np.random.choice(segmentos, n_usuarios, p=segmento_weights),
            'valor_total_compras': np.random.exponential(3000, n_usuarios),
            'total_pedidos': np.random.poisson(6, n_usuarios),
            'ticket_medio': np.random.normal(600, 200, n_usuarios),
            'produtos_unicos_comprados': np.random.randint(1, 12, n_usuarios),
            'dias_sem_comprar': np.random.exponential(25, n_usuarios),
            'pedidos_concluidos': np.random.poisson(5, n_usuarios),
            'pedidos_pendentes': np.random.poisson(1, n_usuarios),
            'variabilidade_gastos': np.random.exponential(150, n_usuarios),
            'data_cadastro': [datetime.now() - timedelta(days=np.random.randint(30, 365)) 
                            for _ in range(n_usuarios)]
        })
        
        # Ajustar valores baseados no segmento
        for segmento in segmentos:
            mask = self.usuarios_transacionais['segmento'] == segmento
            if segmento == 'high_value':
                self.usuarios_transacionais.loc[mask, 'valor_total_compras'] *= 3
                self.usuarios_transacionais.loc[mask, 'ticket_medio'] *= 1.5
                self.usuarios_transacionais.loc[mask, 'dias_sem_comprar'] *= 0.5
            elif segmento == 'new_user':
                self.usuarios_transacionais.loc[mask, 'valor_total_compras'] *= 0.1
                self.usuarios_transacionais.loc[mask, 'total_pedidos'] = np.random.poisson(1, mask.sum())
                self.usuarios_transacionais.loc[mask, 'dias_sem_comprar'] *= 2
        
        # Criar variável churn
        self.usuarios_transacionais['churn'] = (
            self.usuarios_transacionais['dias_sem_comprar'] > 30
        ).astype(int)
        
        # 3. Dados de produtos
        produtos_data = [
            {'id': 'P001', 'nome': 'Smartphone Galaxy S24', 'categoria': 'smartphones', 'preco': 2999.99, 'marca': 'Samsung'},
            {'id': 'P002', 'nome': 'iPhone 15 Pro', 'categoria': 'smartphones', 'preco': 8999.99, 'marca': 'Apple'},
            {'id': 'P003', 'nome': 'Notebook Dell XPS 13', 'categoria': 'notebooks', 'preco': 5999.99, 'marca': 'Dell'},
            {'id': 'P004', 'nome': 'Tablet iPad Air', 'categoria': 'tablets', 'preco': 3999.99, 'marca': 'Apple'},
            {'id': 'P005', 'nome': 'Smartphone Xiaomi 13', 'categoria': 'smartphones', 'preco': 1999.99, 'marca': 'Xiaomi'},
            {'id': 'P006', 'nome': 'Notebook MacBook Air', 'categoria': 'notebooks', 'preco': 7999.99, 'marca': 'Apple'},
            {'id': 'P007', 'nome': 'Tablet Samsung Galaxy Tab', 'categoria': 'tablets', 'preco': 2499.99, 'marca': 'Samsung'},
            {'id': 'P008', 'nome': 'Smartphone Pixel 8', 'categoria': 'smartphones', 'preco': 3499.99, 'marca': 'Google'},
            {'id': 'P009', 'nome': 'Notebook Lenovo ThinkPad', 'categoria': 'notebooks', 'preco': 4999.99, 'marca': 'Lenovo'},
            {'id': 'P010', 'nome': 'Tablet Microsoft Surface', 'categoria': 'tablets', 'preco': 5499.99, 'marca': 'Microsoft'}
        ]
        
        self.produtos_df = pd.DataFrame(produtos_data)
        
        print(f"✅ Dados criados:")
        print(f"  👥 Usuários: {len(self.comportamento_df)}")
        print(f"  🛒 Produtos: {len(self.produtos_df)}")
        print(f"  📊 Eventos de comportamento: {self.comportamento_df['total_eventos'].sum()}")
        print(f"  💰 Valor total compras: R$ {self.usuarios_transacionais['valor_total_compras'].sum():,.2f}")
    
    def analisar_comportamento(self):
        """Análise descritiva do comportamento dos usuários"""
        print("\n📊 ANÁLISE DESCRITIVA - COMPORTAMENTO DOS USUÁRIOS")
        print("=" * 60)
        
        # Estatísticas básicas
        print("📈 Estatísticas Gerais:")
        stats = self.comportamento_df.describe()
        print(stats.round(2))
        
        # Top usuários mais ativos
        print("\n🏆 Top 10 Usuários Mais Ativos:")
        top_ativos = self.comportamento_df.nlargest(10, 'total_eventos')
        for _, user in top_ativos.iterrows():
            print(f"  {user['usuario_id']}: {user['total_eventos']} eventos, "
                  f"{user['taxa_conversao']:.1%} conversão, "
                  f"{user['produtos_unicos']} produtos únicos")
        
        # Análise de conversão
        print(f"\n🎯 Análise de Conversão:")
        print(f"  Taxa média de conversão: {self.comportamento_df['taxa_conversao'].mean():.1%}")
        print(f"  Taxa mediana de conversão: {self.comportamento_df['taxa_conversao'].median():.1%}")
        print(f"  Usuários com conversão > 20%: {(self.comportamento_df['taxa_conversao'] > 0.2).sum()}")
        
        # Correlações
        print(f"\n🔗 Correlações Importantes:")
        corr_matrix = self.comportamento_df[['total_eventos', 'page_views', 'clicks', 
                                            'add_to_cart', 'taxa_conversao', 'produtos_unicos']].corr()
        print(f"  Eventos vs Conversão: {corr_matrix.loc['total_eventos', 'taxa_conversao']:.3f}")
        print(f"  Page Views vs Conversão: {corr_matrix.loc['page_views', 'taxa_conversao']:.3f}")
        print(f"  Produtos Únicos vs Conversão: {corr_matrix.loc['produtos_unicos', 'taxa_conversao']:.3f}")
    
    def clustering_usuarios(self):
        """Clustering de usuários usando K-Means"""
        print("\n🎯 ANÁLISE PREDITIVA - CLUSTERING DE USUÁRIOS")
        print("=" * 60)
        
        # Preparar features para clustering
        features = ['total_eventos', 'page_views', 'clicks', 'add_to_cart', 
                   'produtos_unicos', 'taxa_conversao', 'tempo_medio_evento']
        X = self.comportamento_df[features].fillna(0)
        
        # Normalizar dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar K-Means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.comportamento_df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Análise dos clusters
        cluster_analysis = self.comportamento_df.groupby('cluster')[features].mean()
        
        print("📊 Análise de Clusters:")
        print(cluster_analysis.round(2))
        
        # Interpretar clusters
        print("\n🏷️ Interpretação dos Clusters:")
        cluster_names = {
            0: "😴 Usuários Passivos",
            1: "👀 Usuários Ativos mas Baixa Conversão", 
            2: "🔥 Usuários Ativos e Convertidos"
        }
        
        for cluster_id in range(3):
            cluster_data = self.comportamento_df[self.comportamento_df['cluster'] == cluster_id]
            
            print(f"\n{cluster_names[cluster_id]}:")
            print(f"  Usuários: {len(cluster_data)} ({len(cluster_data)/len(self.comportamento_df)*100:.1f}%)")
            print(f"  Eventos médios: {cluster_data['total_eventos'].mean():.1f}")
            print(f"  Taxa conversão: {cluster_data['taxa_conversao'].mean():.1%}")
            print(f"  Produtos únicos: {cluster_data['produtos_unicos'].mean():.1f}")
            print(f"  Tempo médio/evento: {cluster_data['tempo_medio_evento'].mean():.1f}s")
            
            # Mostrar alguns usuários do cluster
            sample_users = cluster_data['usuario_id'].head(3).tolist()
            print(f"  Exemplos: {', '.join(sample_users)}")
        
        print(f"\n✅ Clustering concluído! {len(self.comportamento_df)} usuários segmentados em 3 grupos")
    
    def analisar_transacoes(self):
        """Análise preditiva dos dados transacionais"""
        print("\n📈 ANÁLISE PREDITIVA - DADOS TRANSACIONAIS")
        print("=" * 60)
        
        # Estatísticas por segmento
        print("📊 Análise por Segmento:")
        segmento_stats = self.usuarios_transacionais.groupby('segmento').agg({
            'valor_total_compras': ['count', 'mean', 'sum'],
            'total_pedidos': 'mean',
            'ticket_medio': 'mean',
            'dias_sem_comprar': 'mean',
            'churn': 'mean'
        }).round(2)
        
        print(segmento_stats)
        
        # Usuários com risco de churn
        risco_churn = self.usuarios_transacionais[self.usuarios_transacionais['churn'] == 1]
        print(f"\n⚠️ Usuários com Risco de Churn: {len(risco_churn)} ({len(risco_churn)/len(self.usuarios_transacionais)*100:.1f}%)")
        
        if len(risco_churn) > 0:
            print("Top 5 usuários com maior risco:")
            top_risco = risco_churn.nlargest(5, 'dias_sem_comprar')
            for _, user in top_risco.iterrows():
                print(f"  {user['nome']}: {user['dias_sem_comprar']:.0f} dias sem comprar, "
                      f"R$ {user['valor_total_compras']:,.2f} histórico")
        
        # Análise de valor por usuário
        print(f"\n💰 Análise de Valor:")
        print(f"  Valor médio por usuário: R$ {self.usuarios_transacionais['valor_total_compras'].mean():,.2f}")
        print(f"  Valor mediano por usuário: R$ {self.usuarios_transacionais['valor_total_compras'].median():,.2f}")
        print(f"  Usuários high_value: {(self.usuarios_transacionais['segmento'] == 'high_value').sum()}")
        print(f"  Receita total: R$ {self.usuarios_transacionais['valor_total_compras'].sum():,.2f}")
    
    def predicao_churn(self):
        """Modelo de predição de churn"""
        print("\n🤖 MODELO DE PREDIÇÃO DE CHURN")
        print("=" * 60)
        
        # Features para o modelo
        features = ['valor_total_compras', 'total_pedidos', 'ticket_medio', 
                   'produtos_unicos_comprados', 'dias_sem_comprar', 'variabilidade_gastos']
        X = self.usuarios_transacionais[features].fillna(0)
        y = self.usuarios_transacionais['churn']
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        
        # Treinar modelo Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        model.fit(X_train, y_train)
        
        # Fazer predições
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Avaliar modelo
        print("📈 Relatório de Classificação:")
        print(classification_report(y_test, y_pred))
        
        # Importância das features
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔍 Importância das Features:")
        print(feature_importance.to_string(index=False))
        
        # Predições para todos os usuários
        self.usuarios_transacionais['probabilidade_churn'] = model.predict_proba(X)[:, 1]
        self.usuarios_transacionais['predicao_churn'] = model.predict(X)
        
        # Mostrar usuários com maior probabilidade de churn
        risco_alto = self.usuarios_transacionais[self.usuarios_transacionais['probabilidade_churn'] > 0.7].sort_values('probabilidade_churn', ascending=False)
        print(f"\n🚨 Usuários com Alto Risco de Churn ({len(risco_alto)} usuários):")
        for _, user in risco_alto.head(5).iterrows():
            print(f"  {user['nome']}: {user['probabilidade_churn']:.1%} probabilidade, "
                  f"{user['dias_sem_comprar']:.0f} dias sem comprar")
        
        print(f"\n✅ Modelo treinado com {len(X_train)} amostras de treino e {len(X_test)} de teste")
        print(f"📊 Acurácia: {(y_pred == y_test).mean():.1%}")
    
    def sistema_recomendacoes(self):
        """Sistema de recomendações personalizadas"""
        print("\n🎯 SISTEMA DE RECOMENDAÇÕES PERSONALIZADAS")
        print("=" * 60)
        
        def calcular_score_recomendacao(usuario_id, produto_id):
            """Calcular score de recomendação para um usuário e produto"""
            score = 0.0
            motivos = []
            
            # Buscar dados do usuário
            user_comp = self.comportamento_df[self.comportamento_df['usuario_id'] == usuario_id]
            user_trans = self.usuarios_transacionais[self.usuarios_transacionais['usuario_id'] == usuario_id]
            
            if user_comp.empty or user_trans.empty:
                return 0.0, []
            
            user_comp = user_comp.iloc[0]
            user_trans = user_trans.iloc[0]
            produto = self.produtos_df[self.produtos_df['id'] == produto_id].iloc[0]
            
            # Score baseado em comportamento
            if user_comp['total_eventos'] > self.comportamento_df['total_eventos'].mean():
                score += 0.2
                motivos.append("usuário_ativo")
            
            if user_comp['taxa_conversao'] > self.comportamento_df['taxa_conversao'].mean():
                score += 0.15
                motivos.append("alta_conversão")
            
            # Score baseado em segmento
            if user_trans['segmento'] == 'high_value':
                if produto['preco'] > 5000:
                    score += 0.3
                    motivos.append("segmento_premium")
                else:
                    score += 0.1
                    motivos.append("produto_acessível")
            elif user_trans['segmento'] == 'new_user':
                if produto['preco'] < 3000:
                    score += 0.25
                    motivos.append("novo_usuário")
                else:
                    score += 0.05
                    motivos.append("produto_caro")
            
            # Score baseado em cluster
            if 'cluster' in user_comp:
                cluster = user_comp['cluster']
                if cluster == 2:  # Ativos e convertidos
                    score += 0.2
                    motivos.append("cluster_ativo_convertido")
                elif cluster == 1:  # Ativos mas baixa conversão
                    if produto['preco'] < 4000:
                        score += 0.15
                        motivos.append("cluster_ativo_baixa_conv")
                elif cluster == 0:  # Passivos
                    if produto['preco'] < 2500:
                        score += 0.1
                        motivos.append("cluster_passivo")
            
            # Score baseado em categoria preferida
            categoria_scores = {'smartphones': 0.1, 'notebooks': 0.08, 'tablets': 0.06}
            score += categoria_scores.get(produto['categoria'], 0.03)
            
            # Score baseado em histórico de compras
            if user_trans['produtos_unicos_comprados'] > self.usuarios_transacionais['produtos_unicos_comprados'].mean():
                score += 0.1
                motivos.append("cliente_diversificado")
            
            # Adicionar ruído aleatório
            score += random.uniform(-0.05, 0.05)
            score = max(0, min(1, score))
            
            return score, motivos
        
        # Gerar recomendações para alguns usuários
        usuarios_exemplo = self.comportamento_df['usuario_id'].head(5).tolist()
        
        print("🎯 Recomendações Personalizadas:")
        print("=" * 40)
        
        for usuario in usuarios_exemplo:
            print(f"\n👤 Usuário: {usuario}")
            
            # Buscar informações do usuário
            user_comp = self.comportamento_df[self.comportamento_df['usuario_id'] == usuario].iloc[0]
            user_trans = self.usuarios_transacionais[self.usuarios_transacionais['usuario_id'] == usuario].iloc[0]
            
            cluster_names = {0: 'Passivo', 1: 'Ativo Baixa Conv.', 2: 'Ativo Convertido'}
            cluster_name = cluster_names.get(user_comp.get('cluster', 0), 'N/A')
            
            print(f"📊 Perfil: {user_trans['segmento']}, Cluster: {cluster_name}")
            print(f"    Eventos: {user_comp['total_eventos']}, Conversão: {user_comp['taxa_conversao']:.1%}")
            print(f"    Histórico: R$ {user_trans['valor_total_compras']:,.2f}, Pedidos: {user_trans['total_pedidos']}")
            
            # Calcular scores para todos os produtos
            recomendacoes = []
            for _, produto in self.produtos_df.iterrows():
                score, motivos = calcular_score_recomendacao(usuario, produto['id'])
                recomendacoes.append({
                    'produto': produto['nome'],
                    'categoria': produto['categoria'],
                    'preco': produto['preco'],
                    'score': score,
                    'motivos': motivos
                })
            
            # Ordenar por score e mostrar top 3
            recomendacoes.sort(key=lambda x: x['score'], reverse=True)
            
            print("🎯 Top 3 Recomendações:")
            for i, rec in enumerate(recomendacoes[:3], 1):
                print(f"  {i}. {rec['produto']}")
                print(f"     Preço: R$ {rec['preco']:,.2f}")
                print(f"     Score: {rec['score']:.3f}")
                print(f"     Motivos: {', '.join(rec['motivos'])}")
        
        print(f"\n✅ Sistema de recomendações implementado!")
        print(f"🎯 Recomendações baseadas em análise preditiva integrada")
    
    def criar_visualizacoes(self):
        """Criar visualizações interativas"""
        print("\n📊 CRIANDO VISUALIZAÇÕES INTERATIVAS")
        print("=" * 60)
        
        # Configurar figura com subplots
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle('🎯 Dashboard - Análise Preditiva E-commerce', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Distribuição de eventos por usuário
        axes[0, 0].hist(self.comportamento_df['total_eventos'], bins=15, alpha=0.7, 
                       color='skyblue', edgecolor='black')
        axes[0, 0].set_title('📱 Distribuição de Eventos por Usuário', fontweight='bold')
        axes[0, 0].set_xlabel('Total de Eventos')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].grid(True, alpha=0.3)
        
        mean_events = self.comportamento_df['total_eventos'].mean()
        axes[0, 0].axvline(mean_events, color='red', linestyle='--', linewidth=2, 
                          label=f'Média: {mean_events:.1f}')
        axes[0, 0].legend()
        
        # Gráfico 2: Taxa de conversão vs Page Views
        scatter = axes[0, 1].scatter(self.comportamento_df['page_views'], 
                                    self.comportamento_df['taxa_conversao'], 
                                    alpha=0.7, s=100, 
                                    c=self.comportamento_df['total_eventos'], 
                                    cmap='viridis', edgecolors='black')
        axes[0, 1].set_title('🎯 Taxa de Conversão vs Page Views', fontweight='bold')
        axes[0, 1].set_xlabel('Page Views')
        axes[0, 1].set_ylabel('Taxa de Conversão')
        axes[0, 1].grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=axes[0, 1])
        cbar.set_label('Total de Eventos')
        
        # Gráfico 3: Clusters de usuários
        if 'cluster' in self.comportamento_df.columns:
            cluster_colors = {0: 'lightcoral', 1: 'gold', 2: 'lightgreen'}
            cluster_labels = {0: 'Passivos', 1: 'Ativos Baixa Conv.', 2: 'Ativos Convertidos'}
            
            for cluster_id in range(3):
                cluster_data = self.comportamento_df[self.comportamento_df['cluster'] == cluster_id]
                axes[1, 0].scatter(cluster_data['total_eventos'], cluster_data['taxa_conversao'],
                                 c=cluster_colors[cluster_id], label=cluster_labels[cluster_id],
                                 alpha=0.7, s=100, edgecolors='black')
            
            axes[1, 0].set_title('🎯 Clusters de Usuários', fontweight='bold')
            axes[1, 0].set_xlabel('Total de Eventos')
            axes[1, 0].set_ylabel('Taxa de Conversão')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfico 4: Distribuição de valores de compra
        axes[1, 1].hist(self.usuarios_transacionais['valor_total_compras'], bins=15, alpha=0.7, 
                       color='lightgreen', edgecolor='black')
        axes[1, 1].set_title('💰 Distribuição de Valores de Compra', fontweight='bold')
        axes[1, 1].set_xlabel('Valor Total Compras (R$)')
        axes[1, 1].set_ylabel('Frequência')
        axes[1, 1].grid(True, alpha=0.3)
        
        mean_value = self.usuarios_transacionais['valor_total_compras'].mean()
        axes[1, 1].axvline(mean_value, color='red', linestyle='--', linewidth=2, 
                          label=f'Média: R$ {mean_value:,.0f}')
        axes[1, 1].legend()
        
        # Gráfico 5: Segmentos de usuários
        segmentos = self.usuarios_transacionais['segmento'].value_counts()
        colors = ['gold', 'lightblue', 'lightcoral', 'lightgreen']
        wedges, texts, autotexts = axes[2, 0].pie(segmentos.values, labels=segmentos.index, 
                                                 autopct='%1.1f%%', startangle=90, colors=colors)
        axes[2, 0].set_title('👥 Distribuição por Segmento', fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Gráfico 6: Probabilidade de churn
        if 'probabilidade_churn' in self.usuarios_transacionais.columns:
            bins = [0, 0.3, 0.7, 1.0]
            labels = ['Baixo Risco', 'Médio Risco', 'Alto Risco']
            self.usuarios_transacionais['risco_churn'] = pd.cut(
                self.usuarios_transacionais['probabilidade_churn'], 
                bins=bins, labels=labels, include_lowest=True
            )
            
            risco_counts = self.usuarios_transacionais['risco_churn'].value_counts()
            colors = ['lightgreen', 'gold', 'lightcoral']
            
            bars = axes[2, 1].bar(risco_counts.index, risco_counts.values, 
                                color=colors, alpha=0.7, edgecolor='black')
            axes[2, 1].set_title('🚨 Distribuição de Risco de Churn', fontweight='bold')
            axes[2, 1].set_ylabel('Número de Usuários')
            axes[2, 1].grid(True, alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                              f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar gráfico
        plt.savefig('dashboard_analise_preditiva_completo.png', dpi=300, bbox_inches='tight')
        print("✅ Dashboard salvo como 'dashboard_analise_preditiva_completo.png'")
        
        # Mostrar gráfico
        plt.show()
        
        print("🎨 Visualizações criadas com sucesso!")
    
    def gerar_relatorio(self):
        """Gerar relatório final da análise"""
        print("\n📋 RELATÓRIO FINAL DA ANÁLISE")
        print("=" * 60)
        
        # Estatísticas gerais
        print("📊 ESTATÍSTICAS GERAIS:")
        print(f"  👥 Total de usuários analisados: {len(self.comportamento_df)}")
        print(f"  🛒 Total de produtos: {len(self.produtos_df)}")
        print(f"  📱 Total de eventos: {self.comportamento_df['total_eventos'].sum()}")
        print(f"  💰 Receita total: R$ {self.usuarios_transacionais['valor_total_compras'].sum():,.2f}")
        print(f"  📈 Taxa média de conversão: {self.comportamento_df['taxa_conversao'].mean():.1%}")
        
        # Análise de clusters
        if 'cluster' in self.comportamento_df.columns:
            print(f"\n🎯 ANÁLISE DE CLUSTERS:")
            cluster_names = {0: "Passivos", 1: "Ativos Baixa Conv.", 2: "Ativos Convertidos"}
            for cluster_id in range(3):
                cluster_data = self.comportamento_df[self.comportamento_df['cluster'] == cluster_id]
                print(f"  {cluster_names[cluster_id]}: {len(cluster_data)} usuários "
                      f"({len(cluster_data)/len(self.comportamento_df)*100:.1f}%)")
        
        # Análise de churn
        if 'probabilidade_churn' in self.usuarios_transacionais.columns:
            risco_alto = (self.usuarios_transacionais['probabilidade_churn'] > 0.7).sum()
            print(f"\n🚨 ANÁLISE DE CHURN:")
            print(f"  Usuários com alto risco de churn: {risco_alto}")
            print(f"  Taxa de churn atual: {self.usuarios_transacionais['churn'].mean():.1%}")
        
        # Segmentação
        print(f"\n👥 SEGMENTAÇÃO:")
        segmentos = self.usuarios_transacionais['segmento'].value_counts()
        for segmento, count in segmentos.items():
            print(f"  {segmento}: {count} usuários ({count/len(self.usuarios_transacionais)*100:.1f}%)")
        
        # Recomendações de ação
        print(f"\n💡 RECOMENDAÇÕES DE AÇÃO:")
        print(f"  1. Focar em usuários 'Ativos e Convertidos' para upsell")
        print(f"  2. Implementar campanhas para usuários 'Ativos mas Baixa Conversão'")
        print(f"  3. Criar estratégias de retenção para usuários com alto risco de churn")
        print(f"  4. Personalizar recomendações baseadas em segmento e comportamento")
        print(f"  5. Monitorar métricas de conversão e ajustar estratégias")
        
        print(f"\n🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
        print(f"📊 Todos os dados foram analisados e visualizados")
        print(f"🎯 Sistema de recomendações implementado")
        print(f"📈 Modelos preditivos treinados e avaliados")
    
    def executar_demonstracao_completa(self):
        """Executar demonstração completa"""
        try:
            # 1. Criar dados simulados
            self.criar_dados_simulados()
            
            # 2. Análise descritiva
            self.analisar_comportamento()
            
            # 3. Clustering
            self.clustering_usuarios()
            
            # 4. Análise transacional
            self.analisar_transacoes()
            
            # 5. Predição de churn
            self.predicao_churn()
            
            # 6. Sistema de recomendações
            self.sistema_recomendacoes()
            
            # 7. Visualizações
            self.criar_visualizacoes()
            
            # 8. Relatório final
            self.gerar_relatorio()
            
        except Exception as e:
            print(f"❌ Erro durante demonstração: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Função principal"""
    print("🎯 Iniciando Demonstração Prática Completa")
    print("📊 Análise Preditiva E-commerce")
    print("🗄️ MongoDB + PostgreSQL + Machine Learning")
    print()
    
    # Criar instância da classe
    demo = EcommerceAnalyticsDemo()
    
    # Executar demonstração
    demo.executar_demonstracao_completa()
    
    print("\n" + "="*70)
    print("🎉 DEMONSTRAÇÃO FINALIZADA!")
    print("📁 Arquivos gerados:")
    print("  📊 dashboard_analise_preditiva_completo.png")
    print("📚 Documentação completa disponível na pasta docs/")
    print("🚀 Pronto para apresentação!")

if __name__ == "__main__":
    main()
