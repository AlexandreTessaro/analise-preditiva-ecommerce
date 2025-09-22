#!/usr/bin/env python3
"""
Demonstração PostgreSQL - Análise Preditiva E-commerce
Script para demonstrar operações relacionais com dados transacionais
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from psycopg2.extras import RealDictCursor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

def conectar_postgresql():
    """Conectar ao PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='ecommerce_demo',
            user='postgres',
            password='postgres'
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Testar conexão
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Conectado ao PostgreSQL com sucesso!")
        print(f"📊 Versão: {version[0][:50]}...")
        
        return conn, cursor
    except Exception as e:
        print(f"❌ Erro ao conectar PostgreSQL: {e}")
        return None, None

def analisar_usuarios(cursor):
    """Analisar dados de usuários"""
    print("\n👥 ANÁLISE DE USUÁRIOS")
    print("=" * 50)
    
    # Query para análise de usuários
    query_usuarios = """
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
            COUNT(CASE WHEN p.status = 'pendente' THEN 1 END) as pedidos_pendentes,
            COUNT(CASE WHEN p.status = 'cancelado' THEN 1 END) as pedidos_cancelados,
            STDDEV(p.valor_total) as variabilidade_gastos
        FROM usuarios u
        LEFT JOIN pedidos p ON u.id = p.usuario_id
        LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
        GROUP BY u.usuario_id, u.nome, u.segmento, u.valor_total_compras
        ORDER BY u.valor_total_compras DESC
    """
    
    cursor.execute(query_usuarios)
    usuarios_df = pd.DataFrame(cursor.fetchall())
    
    if not usuarios_df.empty:
        print(f"👤 Usuários analisados: {len(usuarios_df)}")
        print(f"💰 Valor total de compras: R$ {usuarios_df['valor_total_compras'].sum():,.2f}")
        print(f"📦 Total de pedidos: {usuarios_df['total_pedidos'].sum()}")
        
        # Estatísticas por segmento
        print("\n📊 Análise por Segmento:")
        segmentos = usuarios_df.groupby('segmento').agg({
            'valor_total_compras': ['count', 'mean', 'sum'],
            'total_pedidos': 'mean',
            'ticket_medio': 'mean'
        }).round(2)
        
        print(segmentos)
        
        # Top usuários por valor
        print("\n🏆 Top 5 Usuários por Valor:")
        top_usuarios = usuarios_df.head()
        for _, user in top_usuarios.iterrows():
            print(f"  {user['nome']}: R$ {user['valor_total_compras']:,.2f}, "
                  f"{user['total_pedidos']} pedidos")
        
        return usuarios_df
    else:
        print("❌ Nenhum usuário encontrado")
        return None

def predicao_churn(usuarios_df):
    """Implementar predição de churn"""
    print("\n🎯 PREDIÇÃO DE CHURN")
    print("=" * 50)
    
    if usuarios_df is None or usuarios_df.empty:
        print("❌ Dados insuficientes para predição de churn")
        return None
    
    # Preparar dados
    usuarios_df['dias_sem_comprar'] = usuarios_df['dias_sem_comprar'].fillna(365)
    usuarios_df['ticket_medio'] = usuarios_df['ticket_medio'].fillna(0)
    usuarios_df['produtos_unicos'] = usuarios_df['produtos_unicos'].fillna(0)
    usuarios_df['variabilidade_gastos'] = usuarios_df['variabilidade_gastos'].fillna(0)
    
    # Criar variável target (churn = dias sem comprar > 30)
    usuarios_df['churn'] = (usuarios_df['dias_sem_comprar'] > 30).astype(int)
    
    print(f"📊 Taxa de churn: {usuarios_df['churn'].mean():.1%}")
    print(f"👥 Usuários em risco: {usuarios_df['churn'].sum()}")
    
    # Features para o modelo
    features = ['valor_total_compras', 'total_pedidos', 'ticket_medio', 'produtos_unicos', 'dias_sem_comprar', 'variabilidade_gastos']
    X = usuarios_df[features].fillna(0)
    y = usuarios_df['churn']
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Treinar modelo Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    
    # Fazer predições
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Avaliar modelo
    print("\n📈 Relatório de Classificação:")
    print(classification_report(y_test, y_pred))
    
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
    
    # Mostrar usuários com maior risco de churn
    risco_alto = usuarios_df[usuarios_df['probabilidade_churn'] > 0.7].sort_values('probabilidade_churn', ascending=False)
    print(f"\n🚨 Usuários com Alto Risco de Churn ({len(risco_alto)} usuários):")
    for _, user in risco_alto.head(5).iterrows():
        print(f"  {user['nome']}: {user['probabilidade_churn']:.1%} probabilidade, "
              f"{user['dias_sem_comprar']:.0f} dias sem comprar")
    
    return usuarios_df, model

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO POSTGRESQL - ANÁLISE PREDITIVA E-COMMERCE")
    print("=" * 60)
    
    # Conectar ao PostgreSQL
    conn, cursor = conectar_postgresql()
    if not conn or not cursor:
        print("❌ Não foi possível conectar ao PostgreSQL")
        return False
    
    try:
        # Análise de usuários
        usuarios_df = analisar_usuarios(cursor)
        
        # Predição de churn
        usuarios_df, model = predicao_churn(usuarios_df)
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO POSTGRESQL CONCLUÍDA COM SUCESSO!")
        print("📊 Análise preditiva implementada com dados relacionais")
        print("🎯 Modelo de churn treinado e avaliado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        return False
    
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\n🔌 Conexão PostgreSQL fechada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)