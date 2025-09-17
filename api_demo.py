#!/usr/bin/env python3
"""
🚀 API DEMO - Sistema de Recomendação E-commerce
FastAPI + Análise Preditiva

Esta API demonstra endpoints práticos para um sistema de recomendação
de produtos e-commerce com análise preditiva.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import json
from datetime import datetime
import uvicorn

# Importar a classe de demonstração
from demo_completo import EcommerceAnalyticsDemo

# Criar instância da API
app = FastAPI(
    title="🎯 E-commerce Analytics API",
    description="API para Sistema de Recomendação de Produtos com Análise Preditiva",
    version="1.0.0"
)

# Instância global da demonstração
demo_instance = None

# Modelos Pydantic
class UsuarioResponse(BaseModel):
    usuario_id: str
    nome: str
    segmento: str
    valor_total_compras: float
    total_pedidos: int
    taxa_conversao: float
    cluster: Optional[str] = None
    probabilidade_churn: Optional[float] = None

class ProdutoResponse(BaseModel):
    produto_id: str
    nome: str
    categoria: str
    preco: float
    marca: str

class RecomendacaoResponse(BaseModel):
    usuario_id: str
    recomendacoes: List[Dict]
    algoritmo: str
    timestamp: str

class AnalyticsResponse(BaseModel):
    total_usuarios: int
    total_produtos: int
    receita_total: float
    taxa_conversao_media: float
    usuarios_churn_alto: int

@app.on_event("startup")
async def startup_event():
    """Inicializar dados na startup"""
    global demo_instance
    print("🚀 Inicializando API...")
    demo_instance = EcommerceAnalyticsDemo()
    demo_instance.criar_dados_simulados()
    demo_instance.clustering_usuarios()
    demo_instance.predicao_churn()
    print("✅ API inicializada com sucesso!")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página inicial da API"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎯 E-commerce Analytics API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #27ae60; font-weight: bold; }
            .url { color: #3498db; font-family: monospace; }
            .description { color: #7f8c8d; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 E-commerce Analytics API</h1>
            <p>Sistema de Recomendação de Produtos com Análise Preditiva</p>
            
            <h2>📚 Endpoints Disponíveis:</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/analytics/overview</span>
                <div class="description">Visão geral das métricas do sistema</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/usuarios</span>
                <div class="description">Listar todos os usuários com suas métricas</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/usuarios/{usuario_id}</span>
                <div class="description">Detalhes de um usuário específico</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/produtos</span>
                <div class="description">Listar todos os produtos disponíveis</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/recomendacoes/{usuario_id}</span>
                <div class="description">Recomendações personalizadas para um usuário</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/clusters</span>
                <div class="description">Análise de clusters de usuários</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/churn</span>
                <div class="description">Análise de risco de churn</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/docs</span>
                <div class="description">Documentação interativa da API (Swagger)</div>
            </div>
            
            <h2>🔧 Como usar:</h2>
            <p>1. Acesse <a href="/docs">/docs</a> para documentação interativa</p>
            <p>2. Use os endpoints acima para obter dados e análises</p>
            <p>3. Exemplo: <code>GET /usuarios/U001</code> para dados do usuário U001</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/analytics/overview", response_model=AnalyticsResponse)
async def get_analytics_overview():
    """Obter visão geral das métricas do sistema"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    return AnalyticsResponse(
        total_usuarios=len(demo_instance.comportamento_df),
        total_produtos=len(demo_instance.produtos_df),
        receita_total=demo_instance.usuarios_transacionais['valor_total_compras'].sum(),
        taxa_conversao_media=demo_instance.comportamento_df['taxa_conversao'].mean(),
        usuarios_churn_alto=(demo_instance.usuarios_transacionais['probabilidade_churn'] > 0.7).sum()
    )

@app.get("/usuarios", response_model=List[UsuarioResponse])
async def get_usuarios(limit: int = Query(10, description="Número máximo de usuários")):
    """Listar usuários com suas métricas"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    usuarios = []
    for _, user_comp in demo_instance.comportamento_df.head(limit).iterrows():
        user_trans = demo_instance.usuarios_transacionais[
            demo_instance.usuarios_transacionais['usuario_id'] == user_comp['usuario_id']
        ].iloc[0]
        
        cluster_names = {0: 'Passivo', 1: 'Ativo Baixa Conv.', 2: 'Ativo Convertido'}
        cluster_name = cluster_names.get(user_comp.get('cluster', 0), 'N/A')
        
        usuarios.append(UsuarioResponse(
            usuario_id=user_comp['usuario_id'],
            nome=user_trans['nome'],
            segmento=user_trans['segmento'],
            valor_total_compras=user_trans['valor_total_compras'],
            total_pedidos=user_trans['total_pedidos'],
            taxa_conversao=user_comp['taxa_conversao'],
            cluster=cluster_name,
            probabilidade_churn=user_trans.get('probabilidade_churn', 0)
        ))
    
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: str):
    """Obter detalhes de um usuário específico"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    user_comp = demo_instance.comportamento_df[
        demo_instance.comportamento_df['usuario_id'] == usuario_id
    ]
    
    if user_comp.empty:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user_trans = demo_instance.usuarios_transacionais[
        demo_instance.usuarios_transacionais['usuario_id'] == usuario_id
    ].iloc[0]
    
    user_comp = user_comp.iloc[0]
    
    cluster_names = {0: 'Passivo', 1: 'Ativo Baixa Conv.', 2: 'Ativo Convertido'}
    cluster_name = cluster_names.get(user_comp.get('cluster', 0), 'N/A')
    
    return UsuarioResponse(
        usuario_id=usuario_id,
        nome=user_trans['nome'],
        segmento=user_trans['segmento'],
        valor_total_compras=user_trans['valor_total_compras'],
        total_pedidos=user_trans['total_pedidos'],
        taxa_conversao=user_comp['taxa_conversao'],
        cluster=cluster_name,
        probabilidade_churn=user_trans.get('probabilidade_churn', 0)
    )

@app.get("/produtos", response_model=List[ProdutoResponse])
async def get_produtos():
    """Listar todos os produtos disponíveis"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    produtos = []
    for _, produto in demo_instance.produtos_df.iterrows():
        produtos.append(ProdutoResponse(
            produto_id=produto['id'],
            nome=produto['nome'],
            categoria=produto['categoria'],
            preco=produto['preco'],
            marca=produto['marca']
        ))
    
    return produtos

@app.get("/recomendacoes/{usuario_id}", response_model=RecomendacaoResponse)
async def get_recomendacoes(usuario_id: str, limit: int = Query(5, description="Número de recomendações")):
    """Obter recomendações personalizadas para um usuário"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    # Verificar se usuário existe
    user_exists = usuario_id in demo_instance.comportamento_df['usuario_id'].values
    if not user_exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Implementar sistema de recomendações (versão simplificada)
    def calcular_score_recomendacao(usuario_id, produto_id):
        score = 0.0
        motivos = []
        
        user_comp = demo_instance.comportamento_df[
            demo_instance.comportamento_df['usuario_id'] == usuario_id
        ].iloc[0]
        user_trans = demo_instance.usuarios_transacionais[
            demo_instance.usuarios_transacionais['usuario_id'] == usuario_id
        ].iloc[0]
        produto = demo_instance.produtos_df[demo_instance.produtos_df['id'] == produto_id].iloc[0]
        
        # Score baseado em comportamento
        if user_comp['total_eventos'] > demo_instance.comportamento_df['total_eventos'].mean():
            score += 0.2
            motivos.append("usuário_ativo")
        
        if user_comp['taxa_conversao'] > demo_instance.comportamento_df['taxa_conversao'].mean():
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
        
        # Adicionar score baseado em categoria
        categoria_scores = {'smartphones': 0.1, 'notebooks': 0.08, 'tablets': 0.06}
        score += categoria_scores.get(produto['categoria'], 0.03)
        
        # Adicionar ruído aleatório
        import random
        score += random.uniform(-0.05, 0.05)
        score = max(0, min(1, score))
        
        return score, motivos
    
    # Calcular recomendações
    recomendacoes = []
    for _, produto in demo_instance.produtos_df.iterrows():
        score, motivos = calcular_score_recomendacao(usuario_id, produto['id'])
        recomendacoes.append({
            'produto_id': produto['id'],
            'nome': produto['nome'],
            'categoria': produto['categoria'],
            'preco': produto['preco'],
            'marca': produto['marca'],
            'score': round(score, 3),
            'motivos': motivos
        })
    
    # Ordenar por score e limitar
    recomendacoes.sort(key=lambda x: x['score'], reverse=True)
    recomendacoes = recomendacoes[:limit]
    
    return RecomendacaoResponse(
        usuario_id=usuario_id,
        recomendacoes=recomendacoes,
        algoritmo="collaborative_filtering + content_based",
        timestamp=datetime.now().isoformat()
    )

@app.get("/clusters")
async def get_clusters():
    """Obter análise de clusters de usuários"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    if 'cluster' not in demo_instance.comportamento_df.columns:
        raise HTTPException(status_code=500, detail="Clusters não calculados")
    
    cluster_analysis = {}
    cluster_names = {0: "Passivos", 1: "Ativos Baixa Conv.", 2: "Ativos Convertidos"}
    
    for cluster_id in range(3):
        cluster_data = demo_instance.comportamento_df[
            demo_instance.comportamento_df['cluster'] == cluster_id
        ]
        
        cluster_analysis[cluster_names[cluster_id]] = {
            'total_usuarios': len(cluster_data),
            'percentual': round(len(cluster_data) / len(demo_instance.comportamento_df) * 100, 1),
            'eventos_medios': round(cluster_data['total_eventos'].mean(), 1),
            'taxa_conversao_media': round(cluster_data['taxa_conversao'].mean(), 3),
            'produtos_unicos_medios': round(cluster_data['produtos_unicos'].mean(), 1),
            'tempo_medio_evento': round(cluster_data['tempo_medio_evento'].mean(), 1)
        }
    
    return {
        'clusters': cluster_analysis,
        'total_usuarios': len(demo_instance.comportamento_df),
        'algoritmo': 'K-Means',
        'features': ['total_eventos', 'page_views', 'clicks', 'add_to_cart', 'produtos_unicos', 'taxa_conversao']
    }

@app.get("/churn")
async def get_churn_analysis():
    """Obter análise de risco de churn"""
    if demo_instance is None:
        raise HTTPException(status_code=500, detail="Sistema não inicializado")
    
    if 'probabilidade_churn' not in demo_instance.usuarios_transacionais.columns:
        raise HTTPException(status_code=500, detail="Modelo de churn não treinado")
    
    # Usuários com alto risco de churn
    risco_alto = demo_instance.usuarios_transacionais[
        demo_instance.usuarios_transacionais['probabilidade_churn'] > 0.7
    ].sort_values('probabilidade_churn', ascending=False)
    
    # Usuários com médio risco
    risco_medio = demo_instance.usuarios_transacionais[
        (demo_instance.usuarios_transacionais['probabilidade_churn'] > 0.3) &
        (demo_instance.usuarios_transacionais['probabilidade_churn'] <= 0.7)
    ]
    
    # Usuários com baixo risco
    risco_baixo = demo_instance.usuarios_transacionais[
        demo_instance.usuarios_transacionais['probabilidade_churn'] <= 0.3
    ]
    
    return {
        'resumo': {
            'total_usuarios': len(demo_instance.usuarios_transacionais),
            'risco_alto': len(risco_alto),
            'risco_medio': len(risco_medio),
            'risco_baixo': len(risco_baixo),
            'taxa_churn_atual': round(demo_instance.usuarios_transacionais['churn'].mean(), 3)
        },
        'usuarios_risco_alto': [
            {
                'usuario_id': user['usuario_id'],
                'nome': user['nome'],
                'probabilidade_churn': round(user['probabilidade_churn'], 3),
                'dias_sem_comprar': int(user['dias_sem_comprar']),
                'valor_total_compras': round(user['valor_total_compras'], 2),
                'segmento': user['segmento']
            }
            for _, user in risco_alto.head(10).iterrows()
        ],
        'modelo': {
            'algoritmo': 'Random Forest',
            'features': ['valor_total_compras', 'total_pedidos', 'ticket_medio', 'produtos_unicos_comprados', 'dias_sem_comprar', 'variabilidade_gastos'],
            'acuracia': 'Calculada durante treinamento'
        }
    }

@app.get("/health")
async def health_check():
    """Verificar saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "sistema_inicializado": demo_instance is not None
    }

if __name__ == "__main__":
    print("🚀 Iniciando API de Demonstração...")
    print("📊 Sistema de Recomendação E-commerce")
    print("🔗 Acesse: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_demo:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
