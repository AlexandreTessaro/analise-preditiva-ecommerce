#!/usr/bin/env python3
"""
Demonstração Simplificada - Análise Preditiva E-commerce
Versão que funciona sem bancos de dados, usando apenas dados simulados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

def gerar_dados_simulados():
    """Gerar dados simulados para demonstração"""
    print("📊 Gerando dados simulados...")
    
    # Configurar seed para reprodutibilidade
    np.random.seed(42)
    random.seed(42)
    
    # Dados de usuários
    usuarios = []
    for i in range(1, 101):
        usuario = {
            'usuario_id': f'U{i:03d}',
            'nome': f'Usuário {i}',
            'email': f'usuario{i}@exemplo.com',
            'segmento': random.choice(['high_value', 'medium_value', 'low_value', 'new_user']),
            'valor_total_compras': np.random.exponential(2000),
            'total_pedidos': np.random.poisson(5),
            'ticket_medio': np.random.normal(500, 200),
            'produtos_unicos': np.random.randint(1, 15),
            'dias_sem_comprar': np.random.exponential(30),
            'pedidos_concluidos': np.random.poisson(4),
            'pedidos_pendentes': np.random.poisson(1),
            'variabilidade_gastos': np.random.exponential(100)
        }
        usuarios.append(usuario)
    
    usuarios_df = pd.DataFrame(usuarios)
    
    # Dados de comportamento
    comportamento = []
    for i in range(1, 101):
        comp = {
            'usuario_id': f'U{i:03d}',
            'total_eventos': np.random.poisson(15),
            'page_views': np.random.poisson(10),
            'clicks': np.random.poisson(8),
            'add_to_cart': np.random.poisson(2),
            'searches': np.random.poisson(3),
            'produtos_unicos': np.random.randint(1, 8),
            'taxa_conversao': np.random.beta(2, 8),
            'tempo_medio_evento': np.random.normal(45, 15)
        }
        comportamento.append(comp)
    
    comportamento_df = pd.DataFrame(comportamento)
    
    # Dados de produtos
    produtos = []
    categorias = ['Smartphones', 'Notebooks', 'Tablets', 'Acessórios']
    marcas = ['Samsung', 'Apple', 'Dell', 'Xiaomi', 'LG']
    
    for i in range(1, 21):
        produto = {
            'produto_id': f'P{i:03d}',
            'nome': f'Produto {i}',
            'categoria': random.choice(categorias),
            'marca': random.choice(marcas),
            'preco': np.random.uniform(100, 5000),
            'estoque': np.random.randint(0, 100),
            'avaliacao_media': np.random.uniform(3, 5),
            'total_avaliacoes': np.random.randint(10, 1000),
            'total_vendas': np.random.randint(0, 500),
            'receita_total': np.random.uniform(1000, 50000)
        }
        produtos.append(produto)
    
    produtos_df = pd.DataFrame(produtos)
    
    print(f"✅ {len(usuarios_df)} usuários gerados")
    print(f"✅ {len(comportamento_df)} registros de comportamento gerados")
    print(f"✅ {len(produtos_df)} produtos gerados")
    
    return usuarios_df, comportamento_df, produtos_df

def analise_descritiva(usuarios_df, comportamento_df, produtos_df):
    """Realizar análise descritiva"""
    print("\n📊 ANÁLISE DESCRITIVA")
    print("=" * 50)
    
    # Análise de usuários
    print("👥 Análise de Usuários:")
    print(f"  Total de usuários: {len(usuarios_df)}")
    print(f"  Valor médio de compras: R$ {usuarios_df['valor_total_compras'].mean():,.2f}")
    print(f"  Pedidos médios por usuário: {usuarios_df['total_pedidos'].mean():.1f}")
    print(f"  Ticket médio: R$ {usuarios_df['ticket_medio'].mean():,.2f}")
    
    # Análise por segmento
    print("\n📈 Análise por Segmento:")
    segmentos = usuarios_df.groupby('segmento').agg({
        'valor_total_compras': ['count', 'mean', 'sum'],
        'total_pedidos': 'mean',
        'ticket_medio': 'mean'
    }).round(2)
    print(segmentos)
    
    # Análise de comportamento
    print("\n👀 Análise de Comportamento:")
    print(f"  Total de eventos: {comportamento_df['total_eventos'].sum()}")
    print(f"  Page views: {comportamento_df['page_views'].sum()}")
    print(f"  Add to cart: {comportamento_df['add_to_cart'].sum()}")
    print(f"  Taxa de conversão média: {comportamento_df['taxa_conversao'].mean():.1%}")
    
    # Análise de produtos
    print("\n🛍️ Análise de Produtos:")
    print(f"  Total de produtos: {len(produtos_df)}")
    print(f"  Preço médio: R$ {produtos_df['preco'].mean():,.2f}")
    print(f"  Estoque total: {produtos_df['estoque'].sum()}")
    print(f"  Receita total: R$ {produtos_df['receita_total'].sum():,.2f}")
    
    # Top produtos
    print("\n🏆 Top 5 Produtos por Receita:")
    top_produtos = produtos_df.nlargest(5, 'receita_total')
    for _, produto in top_produtos.iterrows():
        print(f"  {produto['nome']}: R$ {produto['receita_total']:,.2f}")

def clustering_usuarios(comportamento_df):
    """Aplicar clustering K-Means"""
    print("\n🎯 CLUSTERING DE USUÁRIOS")
    print("=" * 50)
    
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Preparar features para clustering
        features = ['total_eventos', 'page_views', 'clicks', 'add_to_cart', 'produtos_unicos', 'taxa_conversao']
        X = comportamento_df[features].fillna(0)
        
        # Normalizar dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar K-Means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        comportamento_df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Análise dos clusters
        cluster_analysis = comportamento_df.groupby('cluster')[features].mean()
        
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
            cluster_data = comportamento_df[comportamento_df['cluster'] == cluster_id]
            avg_events = cluster_data['total_eventos'].mean()
            avg_conversion = cluster_data['taxa_conversao'].mean()
            
            print(f"\n{cluster_names[cluster_id]}:")
            print(f"  Usuários: {len(cluster_data)}")
            print(f"  Eventos médios: {avg_events:.1f}")
            print(f"  Taxa conversão: {avg_conversion:.1%}")
            print(f"  Produtos únicos: {cluster_data['produtos_unicos'].mean():.1f}")
        
        return comportamento_df
        
    except ImportError:
        print("❌ Scikit-learn não disponível - pulando clustering")
        return comportamento_df

def predicao_churn(usuarios_df):
    """Implementar predição de churn"""
    print("\n🎯 PREDIÇÃO DE CHURN")
    print("=" * 50)
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report
        
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
        
    except ImportError:
        print("❌ Scikit-learn não disponível - pulando predição de churn")
        return usuarios_df, None

def sistema_recomendacoes(usuarios_df, comportamento_df, produtos_df):
    """Sistema de recomendações"""
    print("\n🎯 SISTEMA DE RECOMENDAÇÕES")
    print("=" * 50)
    
    def gerar_recomendacoes(usuario_id, usuarios_df, comportamento_df, produtos_df):
        """Gerar recomendações para um usuário específico"""
        
        # Buscar dados do usuário
        user_data = usuarios_df[usuarios_df['usuario_id'] == usuario_id]
        user_comp = comportamento_df[comportamento_df['usuario_id'] == usuario_id]
        
        recomendacoes = []
        
        for _, produto in produtos_df.iterrows():
            score = 0.0
            motivos = []
            
            # Score baseado em comportamento
            if not user_comp.empty:
                comp_data = user_comp.iloc[0]
                
                # Usuários ativos têm preferência por produtos similares
                if comp_data['total_eventos'] > comportamento_df['total_eventos'].mean():
                    score += 0.3
                    motivos.append("usuário_ativo")
                
                # Usuários com alta conversão preferem produtos premium
                if comp_data['taxa_conversao'] > comportamento_df['taxa_conversao'].mean():
                    if produto['preco'] > 2000:
                        score += 0.2
                        motivos.append("preferencia_premium")
                    else:
                        score += 0.1
                        motivos.append("produto_acessivel")
            
            # Score baseado em dados transacionais
            if not user_data.empty:
                user_trans = user_data.iloc[0]
                
                # Usuários high_value preferem produtos caros
                if user_trans['segmento'] == 'high_value':
                    if produto['preco'] > 2000:
                        score += 0.4
                        motivos.append("segmento_high_value")
                    else:
                        score += 0.1
                        motivos.append("produto_economico")
                
                # Usuários com muitos pedidos preferem produtos populares
                if user_trans['total_pedidos'] > usuarios_df['total_pedidos'].mean():
                    score += 0.2
                    motivos.append("cliente_frequente")
            
            # Score baseado em cluster (se disponível)
            if 'cluster' in comportamento_df.columns and not user_comp.empty:
                cluster = user_comp.iloc[0]['cluster']
                
                if cluster == 2:  # Usuários ativos e convertidos
                    score += 0.25
                    motivos.append("cluster_ativo_convertido")
                elif cluster == 1:  # Usuários ativos mas baixa conversão
                    if produto['preco'] < 1500:  # Produtos mais baratos
                        score += 0.2
                        motivos.append("cluster_ativo_baixa_conv")
                elif cluster == 0:  # Usuários passivos
                    if produto['preco'] < 1000:  # Produtos muito baratos
                        score += 0.15
                        motivos.append("cluster_passivo")
            
            # Adicionar ruído aleatório para simular variação
            score += random.uniform(-0.1, 0.1)
            score = max(0, min(1, score))  # Manter entre 0 e 1
            
            recomendacoes.append({
                'produto_id': produto['produto_id'],
                'nome': produto['nome'],
                'categoria': produto['categoria'],
                'preco': produto['preco'],
                'score': score,
                'motivos': motivos
            })
        
        # Ordenar por score e retornar top 5
        recomendacoes.sort(key=lambda x: x['score'], reverse=True)
        return recomendacoes[:5]
    
    # Gerar recomendações para alguns usuários
    usuarios_exemplo = ['U001', 'U002', 'U003', 'U004', 'U005']
    
    print("🎯 Recomendações Personalizadas:")
    print("=" * 60)
    
    for usuario in usuarios_exemplo:
        print(f"\n👤 Usuário: {usuario}")
        
        # Buscar informações do usuário
        user_info = ""
        user_data = usuarios_df[usuarios_df['usuario_id'] == usuario]
        user_comp = comportamento_df[comportamento_df['usuario_id'] == usuario]
        
        if not user_data.empty:
            user_info += f"Segmento: {user_data.iloc[0]['segmento']}, "
            user_info += f"Valor: R$ {user_data.iloc[0]['valor_total_compras']:,.2f}"
        
        if not user_comp.empty:
            user_info += f", Eventos: {user_comp.iloc[0]['total_eventos']}, "
            user_info += f"Conversão: {user_comp.iloc[0]['taxa_conversao']:.1%}"
            if 'cluster' in user_comp.columns:
                cluster_names = {0: 'Passivo', 1: 'Ativo Baixa Conv.', 2: 'Ativo Convertido'}
                user_info += f", Cluster: {cluster_names.get(user_comp.iloc[0]['cluster'], 'N/A')}"
        
        print(f"📊 Perfil: {user_info}")
        
        # Gerar recomendações
        recomendacoes = gerar_recomendacoes(usuario, usuarios_df, comportamento_df, produtos_df)
        
        print("🎯 Top 3 Recomendações:")
        for i, rec in enumerate(recomendacoes[:3], 1):
            print(f"  {i}. {rec['nome']}")
            print(f"     Preço: R$ {rec['preco']:,.2f}")
            print(f"     Score: {rec['score']:.2f}")
            print(f"     Motivos: {', '.join(rec['motivos'])}")
            print()

def criar_visualizacoes(usuarios_df, comportamento_df, produtos_df):
    """Criar visualizações dos dados"""
    print("\n📊 CRIANDO VISUALIZAÇÕES")
    print("=" * 50)
    
    try:
        # Configurar figura
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('📊 Dashboard - Análise Preditiva E-commerce (Dados Simulados)', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Distribuição de valores de compra
        axes[0, 0].hist(usuarios_df['valor_total_compras'], bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 0].set_title('💰 Distribuição de Valores de Compra', fontweight='bold')
        axes[0, 0].set_xlabel('Valor Total Compras (R$)')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Adicionar estatísticas
        mean_value = usuarios_df['valor_total_compras'].mean()
        axes[0, 0].axvline(mean_value, color='red', linestyle='--', linewidth=2, label=f'Média: R$ {mean_value:,.0f}')
        axes[0, 0].legend()
        
        # Gráfico 2: Segmentos de usuários
        segmentos = usuarios_df['segmento'].value_counts()
        colors = ['gold', 'lightblue', 'lightcoral', 'lightgreen']
        wedges, texts, autotexts = axes[0, 1].pie(segmentos.values, labels=segmentos.index, 
                                                autopct='%1.1f%%', startangle=90, colors=colors)
        axes[0, 1].set_title('👥 Distribuição por Segmento', fontweight='bold')
        
        # Melhorar legibilidade
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Gráfico 3: Taxa de conversão vs Page Views
        scatter = axes[0, 2].scatter(comportamento_df['page_views'], comportamento_df['taxa_conversao'], 
                                   alpha=0.7, s=100, c=comportamento_df['total_eventos'], 
                                   cmap='viridis', edgecolors='black')
        axes[0, 2].set_title('🎯 Taxa de Conversão vs Page Views', fontweight='bold')
        axes[0, 2].set_xlabel('Page Views')
        axes[0, 2].set_ylabel('Taxa de Conversão')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Adicionar colorbar
        cbar = plt.colorbar(scatter, ax=axes[0, 2])
        cbar.set_label('Total de Eventos')
        
        # Gráfico 4: Total de pedidos vs Valor total
        scatter2 = axes[1, 0].scatter(usuarios_df['total_pedidos'], usuarios_df['valor_total_compras'], 
                                    alpha=0.7, s=100, c=usuarios_df['ticket_medio'], 
                                    cmap='plasma', edgecolors='black')
        axes[1, 0].set_title('📦 Total de Pedidos vs Valor Total', fontweight='bold')
        axes[1, 0].set_xlabel('Total de Pedidos')
        axes[1, 0].set_ylabel('Valor Total Compras (R$)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Adicionar colorbar
        cbar2 = plt.colorbar(scatter2, ax=axes[1, 0])
        cbar2.set_label('Ticket Médio (R$)')
        
        # Gráfico 5: Produtos por categoria
        categoria_counts = produtos_df['categoria'].value_counts()
        bars = axes[1, 1].bar(categoria_counts.index, categoria_counts.values, 
                             color='lightblue', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('🛍️ Produtos por Categoria', fontweight='bold')
        axes[1, 1].set_ylabel('Número de Produtos')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 6: Preço vs Receita
        scatter3 = axes[1, 2].scatter(produtos_df['preco'], produtos_df['receita_total'], 
                                    alpha=0.7, s=100, c=produtos_df['avaliacao_media'], 
                                    cmap='coolwarm', edgecolors='black')
        axes[1, 2].set_title('💰 Preço vs Receita Total', fontweight='bold')
        axes[1, 2].set_xlabel('Preço (R$)')
        axes[1, 2].set_ylabel('Receita Total (R$)')
        axes[1, 2].grid(True, alpha=0.3)
        
        # Adicionar colorbar
        cbar3 = plt.colorbar(scatter3, ax=axes[1, 2])
        cbar3.set_label('Avaliação Média')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar gráfico
        plt.savefig('dashboard_simulado.png', dpi=300, bbox_inches='tight')
        print("✅ Dashboard salvo como 'dashboard_simulado.png'")
        
        # Mostrar gráfico
        plt.show()
        
    except Exception as e:
        print(f"❌ Erro ao criar visualizações: {e}")

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO SIMPLIFICADA - ANÁLISE PREDITIVA E-COMMERCE")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("👨‍💻 Desenvolvido para: Disciplina de Análise Preditiva")
    print("🏫 Curso: Engenharia de Software")
    print("👨‍🏫 Professor: Luiz C. Camargo, PhD")
    print("=" * 70)
    
    try:
        # Gerar dados simulados
        usuarios_df, comportamento_df, produtos_df = gerar_dados_simulados()
        
        # Análise descritiva
        analise_descritiva(usuarios_df, comportamento_df, produtos_df)
        
        # Clustering
        comportamento_df = clustering_usuarios(comportamento_df)
        
        # Predição de churn
        usuarios_df, model = predicao_churn(usuarios_df)
        
        # Sistema de recomendações
        sistema_recomendacoes(usuarios_df, comportamento_df, produtos_df)
        
        # Visualizações
        criar_visualizacoes(usuarios_df, comportamento_df, produtos_df)
        
        print("\n" + "=" * 70)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("📊 Análise preditiva implementada com dados simulados")
        print("🎯 Sistema de recomendações funcionando")
        print("📈 Dashboard criado e salvo")
        print("\n📚 Este projeto demonstra:")
        print("   • Tipos de análise de dados (Descritiva, Diagnóstica, Preditiva, Prescritiva)")
        print("   • Arquitetura híbrida MongoDB + PostgreSQL")
        print("   • Modelos de dados NoSQL e Relacional")
        print("   • Manipulação de dados com CRUD")
        print("   • Ambiente Data Lakehouse")
        print("   • Sistema de recomendações com ML")
        print("\n🎓 Avaliação N1 - Análise Preditiva")
        print("   • Domínio: Sistema de Recomendação E-commerce")
        print("   • Tecnologias: MongoDB, PostgreSQL, Python, Scikit-learn")
        print("   • Pontuação: 4,0 pontos")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
