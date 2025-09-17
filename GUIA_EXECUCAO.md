# 🚀 GUIA DE EXECUÇÃO - Demonstrações Práticas

## 📋 Visão Geral

Este projeto contém **demonstrações práticas completas** de análise preditiva para um sistema de recomendação e-commerce, incluindo:

- ✅ **Script Python completo** (`demo_completo.py`)
- ✅ **API REST** (`api_demo.py`) 
- ✅ **Dashboard interativo** (`dashboard_demo.py`)
- ✅ **Scripts MongoDB** (`scripts/demo_mongodb.py`)
- ✅ **Scripts PostgreSQL** (`scripts/demo_postgresql.py`)

## 🎯 Demonstração Principal (Recomendada)

### `demo_completo.py` - Demonstração Completa
**Este é o script principal que você deve executar para a apresentação!**

```bash
# Instalar dependências
pip install pandas numpy matplotlib seaborn scikit-learn

# Executar demonstração completa
python demo_completo.py
```

**O que este script faz:**
- ✅ Cria dados simulados realistas (50 usuários, 10 produtos)
- ✅ Análise descritiva completa
- ✅ Clustering de usuários (K-Means)
- ✅ Predição de churn (Random Forest)
- ✅ Sistema de recomendações personalizadas
- ✅ Visualizações interativas
- ✅ Relatório final com insights

**Resultados:**
- 📊 Dashboard visual salvo como `dashboard_analise_preditiva_completo.png`
- 📈 Análise completa no terminal
- 🎯 Recomendações personalizadas para cada usuário

## 🌐 Demonstrações Adicionais

### 1. API REST (`api_demo.py`)
```bash
# Instalar FastAPI
pip install fastapi uvicorn

# Executar API
python api_demo.py
```

**Acesse:**
- 🌐 API: http://localhost:8000
- 📚 Documentação: http://localhost:8000/docs
- 🔍 Endpoints: `/usuarios`, `/recomendacoes/{id}`, `/analytics/overview`

### 2. Dashboard Interativo (`dashboard_demo.py`)
```bash
# Instalar Streamlit
pip install streamlit plotly

# Executar dashboard
streamlit run dashboard_demo.py
```

**Acesse:** http://localhost:8501

**Features:**
- 📊 Métricas em tempo real
- 🎯 Filtros interativos
- 📈 Gráficos dinâmicos
- 🎯 Sistema de recomendações

### 3. Scripts de Banco de Dados

#### MongoDB (`scripts/demo_mongodb.py`)
```bash
# Instalar MongoDB e PyMongo
pip install pymongo

# Executar (requer MongoDB rodando)
python scripts/demo_mongodb.py
```

#### PostgreSQL (`scripts/demo_postgresql.py`)
```bash
# Instalar PostgreSQL e psycopg2
pip install psycopg2-binary

# Executar (requer PostgreSQL rodando)
python scripts/demo_postgresql.py
```

## 📊 Dados Simulados

Todos os scripts funcionam com **dados simulados realistas**:

### Usuários (50)
- **Segmentos:** high_value, medium_value, low_value, new_user
- **Comportamento:** eventos, page_views, clicks, conversões
- **Transações:** pedidos, valores, frequência

### Produtos (10)
- **Categorias:** smartphones, notebooks, tablets
- **Marcas:** Apple, Samsung, Dell, Xiaomi, etc.
- **Preços:** R$ 1.999 a R$ 8.999

### Análises Implementadas
- 🎯 **Clustering:** 3 grupos de usuários
- 🤖 **Predição de Churn:** Random Forest
- 🎯 **Recomendações:** Algoritmo híbrido
- 📊 **Visualizações:** 6 gráficos diferentes

## 🎯 Para a Apresentação

### Opção 1: Demonstração Simples (Recomendada)
```bash
python demo_completo.py
```
- ✅ Funciona sem instalar bancos de dados
- ✅ Demonstração completa em 2-3 minutos
- ✅ Visualizações automáticas
- ✅ Relatório final com insights

### Opção 2: Demonstração Interativa
```bash
streamlit run dashboard_demo.py
```
- ✅ Interface web interativa
- ✅ Filtros dinâmicos
- ✅ Gráficos interativos
- ✅ Sistema de recomendações em tempo real

### Opção 3: API + Dashboard
```bash
# Terminal 1: API
python api_demo.py

# Terminal 2: Dashboard
streamlit run dashboard_demo.py
```
- ✅ Arquitetura completa
- ✅ API REST + Frontend
- ✅ Demonstração profissional

## 📁 Estrutura de Arquivos

```
analise_preditiva/
├── demo_completo.py              # 🎯 DEMONSTRAÇÃO PRINCIPAL
├── api_demo.py                   # 🌐 API REST
├── dashboard_demo.py             # 📊 Dashboard interativo
├── scripts/
│   ├── demo_mongodb.py          # 🗄️ Demonstração MongoDB
│   ├── demo_postgresql.py       # 🗄️ Demonstração PostgreSQL
│   └── exemplos_praticos.py     # 📚 Exemplos de código
├── docs/                        # 📚 Documentação completa
├── models/                      # 🗄️ Modelos de dados
├── data/                        # 📊 Dados de exemplo
└── requirements.txt             # 📦 Dependências
```

## 🚀 Execução Rápida para Apresentação

### 1. Preparação (2 minutos)
```bash
# Instalar dependências básicas
pip install pandas numpy matplotlib seaborn scikit-learn

# Verificar se tudo está funcionando
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('✅ Todas as dependências OK!')"
```

### 2. Demonstração (3 minutos)
```bash
# Executar demonstração principal
python demo_completo.py
```

### 3. Resultados
- 📊 Gráfico salvo: `dashboard_analise_preditiva_completo.png`
- 📈 Análise completa no terminal
- 🎯 Recomendações personalizadas
- 📋 Relatório final com insights

## 💡 Dicas para Apresentação

### Pontos Fortes a Destacar:
1. **Dados Realistas:** 50 usuários com comportamento variado
2. **Análise Completa:** Descritiva + Preditiva + Prescritiva
3. **Tecnologias Modernas:** ML + Visualizações + APIs
4. **Arquitetura Híbrida:** MongoDB + PostgreSQL
5. **Sistema Funcional:** Recomendações personalizadas

### Demonstração Sugerida:
1. **Executar** `python demo_completo.py`
2. **Explicar** cada etapa da análise
3. **Mostrar** visualizações geradas
4. **Destacar** insights de negócio
5. **Demonstrar** sistema de recomendações

## 🎉 Conclusão

Este projeto oferece uma **demonstração prática completa** de análise preditiva aplicada a um cenário real de e-commerce. Todos os scripts são executáveis e demonstram conceitos teóricos na prática.

**Recomendação:** Use `demo_completo.py` como demonstração principal - é completo, rápido e impressionante! 🚀
