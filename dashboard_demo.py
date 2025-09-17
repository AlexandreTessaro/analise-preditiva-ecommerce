#!/usr/bin/env python3
"""
📊 DASHBOARD INTERATIVO - Sistema de Recomendação E-commerce
Streamlit + Análise Preditiva

Este dashboard interativo demonstra visualmente os resultados da análise
preditiva do sistema de recomendação de produtos e-commerce.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import requests
import time

# Importar a classe de demonstração
from demo_completo import EcommerceAnalyticsDemo

# Configuração da página
st.set_page_config(
    page_title="🎯 E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 0.5rem 0;
    }
    .success-card {
        border-left-color: #27ae60;
    }
    .warning-card {
        border-left-color: #f39c12;
    }
    .danger-card {
        border-left-color: #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_demo_data():
    """Carregar dados da demonstração"""
    demo = EcommerceAnalyticsDemo()
    demo.criar_dados_simulados()
    demo.clustering_usuarios()
    demo.predicao_churn()
    return demo

def create_metric_card(title, value, delta=None, delta_type="normal"):
    """Criar card de métrica"""
    delta_color = ""
    if delta_type == "success":
        delta_color = "success-card"
    elif delta_type == "warning":
        delta_color = "warning-card"
    elif delta_type == "danger":
        delta_color = "danger-card"
    
    st.markdown(f"""
    <div class="metric-card {delta_color}">
        <h4>{title}</h4>
        <h2>{value}</h2>
        {f'<p>Δ {delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Função principal do dashboard"""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 E-commerce Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Sistema de Recomendação de Produtos com Análise Preditiva")
    
    # Carregar dados
    with st.spinner("🔄 Carregando dados..."):
        demo = load_demo_data()
    
    # Sidebar
    st.sidebar.title("🎛️ Controles")
    st.sidebar.markdown("---")
    
    # Filtros
    st.sidebar.subheader("📊 Filtros")
    
    # Filtro de segmento
    segmentos = demo.usuarios_transacionais['segmento'].unique()
    segmento_selecionado = st.sidebar.selectbox(
        "Segmento de Usuário",
        ["Todos"] + list(segmentos)
    )
    
    # Filtro de cluster
    if 'cluster' in demo.comportamento_df.columns:
        cluster_names = {0: 'Passivos', 1: 'Ativos Baixa Conv.', 2: 'Ativos Convertidos'}
        clusters = list(cluster_names.values())
        cluster_selecionado = st.sidebar.selectbox(
            "Cluster de Comportamento",
            ["Todos"] + clusters
        )
    else:
        cluster_selecionado = "Todos"
    
    # Aplicar filtros
    df_comportamento_filtrado = demo.comportamento_df.copy()
    df_transacional_filtrado = demo.usuarios_transacionais.copy()
    
    if segmento_selecionado != "Todos":
        usuarios_segmento = df_transacional_filtrado[
            df_transacional_filtrado['segmento'] == segmento_selecionado
        ]['usuario_id'].tolist()
        df_comportamento_filtrado = df_comportamento_filtrado[
            df_comportamento_filtrado['usuario_id'].isin(usuarios_segmento)
        ]
        df_transacional_filtrado = df_transacional_filtrado[
            df_transacional_filtrado['usuario_id'].isin(usuarios_segmento)
        ]
    
    if cluster_selecionado != "Todos" and 'cluster' in demo.comportamento_df.columns:
        cluster_id = [k for k, v in cluster_names.items() if v == cluster_selecionado][0]
        usuarios_cluster = df_comportamento_filtrado[
            df_comportamento_filtrado['cluster'] == cluster_id
        ]['usuario_id'].tolist()
        df_comportamento_filtrado = df_comportamento_filtrado[
            df_comportamento_filtrado['usuario_id'].isin(usuarios_cluster)
        ]
        df_transacional_filtrado = df_transacional_filtrado[
            df_transacional_filtrado['usuario_id'].isin(usuarios_cluster)
        ]
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "👥 Total Usuários",
            f"{len(df_comportamento_filtrado):,}",
            delta=f"{len(df_comportamento_filtrado) - len(demo.comportamento_df):+}" if len(df_comportamento_filtrado) != len(demo.comportamento_df) else None
        )
    
    with col2:
        create_metric_card(
            "💰 Receita Total",
            f"R$ {df_transacional_filtrado['valor_total_compras'].sum():,.0f}",
            delta=f"R$ {df_transacional_filtrado['valor_total_compras'].sum() - demo.usuarios_transacionais['valor_total_compras'].sum():+,.0f}" if len(df_transacional_filtrado) != len(demo.usuarios_transacionais) else None
        )
    
    with col3:
        create_metric_card(
            "📊 Taxa Conversão",
            f"{df_comportamento_filtrado['taxa_conversao'].mean():.1%}",
            delta_type="success" if df_comportamento_filtrado['taxa_conversao'].mean() > demo.comportamento_df['taxa_conversao'].mean() else "warning"
        )
    
    with col4:
        if 'probabilidade_churn' in df_transacional_filtrado.columns:
            risco_churn = (df_transacional_filtrado['probabilidade_churn'] > 0.7).sum()
            create_metric_card(
                "🚨 Risco Churn Alto",
                f"{risco_churn}",
                delta_type="danger" if risco_churn > 0 else "success"
            )
        else:
            create_metric_card(
                "🛒 Total Produtos",
                f"{len(demo.produtos_df)}",
            )
    
    # Gráficos principais
    st.subheader("📊 Análises Visuais")
    
    # Tabs para diferentes análises
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Comportamento", "💰 Transações", "🎯 Clusters", "🚨 Churn"])
    
    with tab1:
        st.subheader("📱 Análise de Comportamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição de eventos
            fig_events = px.histogram(
                df_comportamento_filtrado,
                x='total_eventos',
                nbins=20,
                title='Distribuição de Eventos por Usuário',
                labels={'total_eventos': 'Total de Eventos', 'count': 'Frequência'}
            )
            fig_events.update_layout(showlegend=False)
            st.plotly_chart(fig_events, use_container_width=True)
        
        with col2:
            # Taxa de conversão vs Page Views
            fig_conversion = px.scatter(
                df_comportamento_filtrado,
                x='page_views',
                y='taxa_conversao',
                size='total_eventos',
                color='produtos_unicos',
                title='Taxa de Conversão vs Page Views',
                labels={'page_views': 'Page Views', 'taxa_conversao': 'Taxa de Conversão'}
            )
            st.plotly_chart(fig_conversion, use_container_width=True)
        
        # Top usuários mais ativos
        st.subheader("🏆 Top 10 Usuários Mais Ativos")
        top_ativos = df_comportamento_filtrado.nlargest(10, 'total_eventos')
        
        fig_top = px.bar(
            top_ativos,
            x='usuario_id',
            y='total_eventos',
            title='Usuários Mais Ativos',
            labels={'usuario_id': 'Usuário', 'total_eventos': 'Total de Eventos'}
        )
        fig_top.update_xaxis(tickangle=45)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with tab2:
        st.subheader("💰 Análise Transacional")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por segmento
            segmento_counts = df_transacional_filtrado['segmento'].value_counts()
            fig_segmento = px.pie(
                values=segmento_counts.values,
                names=segmento_counts.index,
                title='Distribuição por Segmento'
            )
            st.plotly_chart(fig_segmento, use_container_width=True)
        
        with col2:
            # Distribuição de valores
            fig_valores = px.histogram(
                df_transacional_filtrado,
                x='valor_total_compras',
                nbins=20,
                title='Distribuição de Valores de Compra',
                labels={'valor_total_compras': 'Valor Total Compras (R$)', 'count': 'Frequência'}
            )
            st.plotly_chart(fig_valores, use_container_width=True)
        
        # Correlação entre variáveis
        st.subheader("🔗 Matriz de Correlação")
        corr_vars = ['valor_total_compras', 'total_pedidos', 'ticket_medio', 'produtos_unicos_comprados']
        corr_matrix = df_transacional_filtrado[corr_vars].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlação entre Variáveis Transacionais"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab3:
        st.subheader("🎯 Análise de Clusters")
        
        if 'cluster' in df_comportamento_filtrado.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição de clusters
                cluster_counts = df_comportamento_filtrado['cluster'].value_counts()
                cluster_names = {0: 'Passivos', 1: 'Ativos Baixa Conv.', 2: 'Ativos Convertidos'}
                cluster_labels = [cluster_names[i] for i in cluster_counts.index]
                
                fig_clusters = px.pie(
                    values=cluster_counts.values,
                    names=cluster_labels,
                    title='Distribuição de Clusters'
                )
                st.plotly_chart(fig_clusters, use_container_width=True)
            
            with col2:
                # Scatter plot dos clusters
                df_cluster_plot = df_comportamento_filtrado.copy()
                df_cluster_plot['cluster_name'] = df_cluster_plot['cluster'].map(cluster_names)
                
                fig_scatter = px.scatter(
                    df_cluster_plot,
                    x='total_eventos',
                    y='taxa_conversao',
                    color='cluster_name',
                    size='produtos_unicos',
                    title='Clusters de Usuários',
                    labels={'total_eventos': 'Total de Eventos', 'taxa_conversao': 'Taxa de Conversão'}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Análise detalhada dos clusters
            st.subheader("📊 Análise Detalhada dos Clusters")
            
            cluster_stats = df_comportamento_filtrado.groupby('cluster').agg({
                'total_eventos': 'mean',
                'taxa_conversao': 'mean',
                'produtos_unicos': 'mean',
                'tempo_medio_evento': 'mean'
            }).round(2)
            
            cluster_stats.index = [cluster_names[i] for i in cluster_stats.index]
            
            st.dataframe(cluster_stats, use_container_width=True)
        else:
            st.warning("⚠️ Clusters não calculados. Execute a análise de clustering primeiro.")
    
    with tab4:
        st.subheader("🚨 Análise de Risco de Churn")
        
        if 'probabilidade_churn' in df_transacional_filtrado.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição de risco de churn
                bins = [0, 0.3, 0.7, 1.0]
                labels = ['Baixo Risco', 'Médio Risco', 'Alto Risco']
                df_transacional_filtrado['risco_churn'] = pd.cut(
                    df_transacional_filtrado['probabilidade_churn'], 
                    bins=bins, labels=labels, include_lowest=True
                )
                
                risco_counts = df_transacional_filtrado['risco_churn'].value_counts()
                
                fig_risco = px.bar(
                    x=risco_counts.index,
                    y=risco_counts.values,
                    title='Distribuição de Risco de Churn',
                    labels={'x': 'Nível de Risco', 'y': 'Número de Usuários'},
                    color=risco_counts.values,
                    color_continuous_scale=['green', 'yellow', 'red']
                )
                st.plotly_chart(fig_risco, use_container_width=True)
            
            with col2:
                # Scatter plot: probabilidade vs dias sem comprar
                fig_churn = px.scatter(
                    df_transacional_filtrado,
                    x='dias_sem_comprar',
                    y='probabilidade_churn',
                    color='segmento',
                    size='valor_total_compras',
                    title='Probabilidade de Churn vs Dias sem Comprar',
                    labels={'dias_sem_comprar': 'Dias sem Comprar', 'probabilidade_churn': 'Probabilidade de Churn'}
                )
                st.plotly_chart(fig_churn, use_container_width=True)
            
            # Usuários com alto risco de churn
            st.subheader("⚠️ Usuários com Alto Risco de Churn")
            risco_alto = df_transacional_filtrado[
                df_transacional_filtrado['probabilidade_churn'] > 0.7
            ].sort_values('probabilidade_churn', ascending=False)
            
            if len(risco_alto) > 0:
                st.dataframe(
                    risco_alto[['usuario_id', 'nome', 'segmento', 'probabilidade_churn', 
                              'dias_sem_comprar', 'valor_total_compras']].round(3),
                    use_container_width=True
                )
            else:
                st.success("✅ Nenhum usuário com alto risco de churn identificado!")
        else:
            st.warning("⚠️ Modelo de churn não treinado. Execute a predição de churn primeiro.")
    
    # Sistema de recomendações
    st.subheader("🎯 Sistema de Recomendações")
    
    # Selecionar usuário para recomendações
    usuario_selecionado = st.selectbox(
        "Selecione um usuário para ver recomendações:",
        df_comportamento_filtrado['usuario_id'].tolist()
    )
    
    if usuario_selecionado:
        # Implementar sistema de recomendações simplificado
        def calcular_recomendacoes(usuario_id):
            recomendacoes = []
            
            user_comp = df_comportamento_filtrado[
                df_comportamento_filtrado['usuario_id'] == usuario_id
            ].iloc[0]
            user_trans = df_transacional_filtrado[
                df_transacional_filtrado['usuario_id'] == usuario_id
            ].iloc[0]
            
            for _, produto in demo.produtos_df.iterrows():
                score = 0.0
                motivos = []
                
                # Score baseado em comportamento
                if user_comp['total_eventos'] > df_comportamento_filtrado['total_eventos'].mean():
                    score += 0.2
                    motivos.append("usuário_ativo")
                
                if user_comp['taxa_conversao'] > df_comportamento_filtrado['taxa_conversao'].mean():
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
                score += np.random.uniform(-0.05, 0.05)
                score = max(0, min(1, score))
                
                recomendacoes.append({
                    'produto': produto['nome'],
                    'categoria': produto['categoria'],
                    'preco': produto['preco'],
                    'marca': produto['marca'],
                    'score': score,
                    'motivos': motivos
                })
            
            # Ordenar por score
            recomendacoes.sort(key=lambda x: x['score'], reverse=True)
            return recomendacoes[:5]
        
        # Calcular e mostrar recomendações
        recomendacoes = calcular_recomendacoes(usuario_selecionado)
        
        # Informações do usuário
        user_info = df_transacional_filtrado[
            df_transacional_filtrado['usuario_id'] == usuario_selecionado
        ].iloc[0]
        
        st.info(f"""
        **👤 Usuário:** {user_info['nome']} ({usuario_selecionado})  
        **📊 Segmento:** {user_info['segmento']}  
        **💰 Histórico:** R$ {user_info['valor_total_compras']:,.2f}  
        **🛒 Pedidos:** {user_info['total_pedidos']}  
        **📈 Taxa Conversão:** {df_comportamento_filtrado[df_comportamento_filtrado['usuario_id'] == usuario_selecionado]['taxa_conversao'].iloc[0]:.1%}
        """)
        
        # Mostrar recomendações
        st.subheader("🎯 Top 5 Recomendações")
        
        for i, rec in enumerate(recomendacoes, 1):
            with st.expander(f"{i}. {rec['produto']} - Score: {rec['score']:.3f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Preço:** R$ {rec['preco']:,.2f}")
                    st.write(f"**Categoria:** {rec['categoria']}")
                    st.write(f"**Marca:** {rec['marca']}")
                
                with col2:
                    st.write(f"**Score:** {rec['score']:.3f}")
                    st.write(f"**Motivos:** {', '.join(rec['motivos'])}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>🎯 Dashboard de Análise Preditiva E-commerce</p>
        <p>📊 Sistema de Recomendação de Produtos | MongoDB + PostgreSQL + Machine Learning</p>
        <p>🚀 Desenvolvido para demonstração prática de análise preditiva</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
