# 🎯 Sistema de Recomendação E-commerce - Análise Preditiva

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/atlas)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Completed-success.svg)](README.md)

## 📋 Visão Geral

Este projeto implementa um **Sistema de Recomendação de Produtos E-commerce** utilizando análise preditiva, demonstrando a aplicação prática de conceitos de análise de dados, modelos NoSQL/Relacionais e arquiteturas de dados modernas.

### 🎯 Objetivos
- **Análise Descritiva:** Entender comportamento de usuários e produtos
- **Análise Preditiva:** Predizer probabilidade de compra e churn
- **Clustering:** Segmentar usuários por comportamento
- **Recomendações:** Gerar recomendações personalizadas
- **Visualizações:** Criar dashboards interativos

### 🛠️ Tecnologias Utilizadas
- **MongoDB Atlas:** Dados não estruturados e comportamento
- **PostgreSQL:** Dados transacionais e relatórios
- **Python:** Análise de dados e machine learning
- **Scikit-learn:** Algoritmos de ML
- **Matplotlib/Seaborn:** Visualizações
- **Pandas:** Manipulação de dados

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- MongoDB Atlas (conta gratuita)
- PostgreSQL 12+ (opcional)
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/analise-preditiva-ecommerce.git
cd analise-preditiva-ecommerce
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Bancos de Dados

#### MongoDB Atlas (Recomendado)
1. Crie uma conta gratuita em [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crie um cluster gratuito
3. Configure as credenciais no arquivo `demo_mongodb_atlas.py`

#### PostgreSQL (Opcional)
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Criar banco de dados
sudo -u postgres createdb ecommerce_demo
```

## 🎮 Como Executar

### Opção 1: Demonstração Completa com MongoDB Atlas (Recomendada)
```bash
python demo_mongodb_atlas.py
```

### Opção 2: Demonstração com Dados Simulados
```bash
python demo_simulado.py
```

### Opção 3: Script Principal
```bash
python main.py
```

### Opção 4: Jupyter Notebook
```bash
jupyter notebook notebooks/demo_analise_preditiva.ipynb
```

## 📊 Funcionalidades Implementadas

### 🔍 Análise Descritiva
- **Comportamento de usuários:** Eventos, navegação, conversões
- **Produtos mais visualizados:** Análise de popularidade
- **Padrões de navegação:** Tempo por página, cliques
- **Segmentação:** Usuários por atividade e valor

### 🎯 Análise Preditiva
- **Clustering K-Means:** Segmentação automática de usuários
- **Predição de Churn:** Modelo Random Forest
- **Probabilidade de Compra:** Scoring baseado em histórico
- **Classificação:** Segmentos de usuários

### 🎯 Sistema de Recomendações
- **Algoritmo colaborativo:** Baseado em usuários similares
- **Scoring personalizado:** Combina comportamento e transações
- **Recomendações por cluster:** Adaptadas ao perfil
- **Integração híbrida:** MongoDB + PostgreSQL

### 📊 Visualizações
- **Dashboard interativo:** Gráficos e métricas
- **Análise de clusters:** Visualização de segmentos
- **Predições de churn:** Distribuição de risco
- **Comparação entre bancos:** MongoDB vs PostgreSQL

## 📈 Resultados da Execução

### 📊 Dados Processados
- **50 usuários** com perfis completos
- **5 produtos** analisados
- **892 eventos** de comportamento
- **3 clusters** de usuários identificados

### 🎯 Clustering K-Means
- **😴 Usuários Passivos:** 23 usuários (84,7% conversão)
- **👀 Usuários Ativos mas Baixa Conversão:** 19 usuários (102,6% conversão)
- **🔥 Usuários Ativos e Convertidos:** 8 usuários (285,4% conversão)

### 🤖 Predição de Churn
- **Taxa de churn:** 68%
- **Precisão do modelo:** 100%
- **34 usuários** identificados com alto risco de churn

### 📈 Análises por Segmento
- **High Value:** 11 usuários, R$ 10.699,84 valor médio
- **Medium Value:** 13 usuários, R$ 6.869,24 valor médio
- **Low Value:** 9 usuários, R$ 7.611,12 valor médio
- **New User:** 17 usuários, R$ 8.002,65 valor médio

## 📈 Avaliação N1 - Resposta Completa

### a) Tipos de Análise de Dados (0,5)
- **Análise Descritiva:** O que aconteceu
- **Análise Diagnóstica:** Por que aconteceu  
- **Análise Preditiva:** O que vai acontecer
- **Análise Prescritiva:** O que fazer

### b) Domínio de Problema (1,0)
**Sistema de Recomendação E-commerce** com:
- **Classificação:** Segmentação de usuários por comportamento
- **Predição:** Probabilidade de compra por produto
- **Recomendação:** Produtos personalizados por usuário

### c) Justificativa dos Modelos (0,5)
**Arquitetura híbrida** justificada por:
- **MongoDB Atlas:** Dados flexíveis e comportamento
- **PostgreSQL:** Integridade transacional
- **Integração:** APIs e sincronização

### d) Modelos de Dados (0,5)
**Esquemas completos** para ambos os bancos:
- **MongoDB:** Coleções flexíveis com documentos JSON
- **PostgreSQL:** Tabelas normalizadas com relacionamentos
- **Índices:** Otimizações para performance

### e) Manipulação de Dados (0,5)
**Exemplos práticos** de:
- **CRUD operations:** Create, Read, Update, Delete
- **Consultas analíticas:** Agregações e joins
- **Análise preditiva:** Clustering e classificação

### f) Ambiente de Dados (1,0)
**Data Lakehouse** escolhido por:
- **Flexibilidade:** Múltiplos formatos de dados
- **Performance:** Consultas SQL otimizadas
- **Escalabilidade:** Suporte a petabytes
- **ML Integration:** Feature Store nativo

## 🗄️ Arquitetura de Dados

### MongoDB Atlas (NoSQL)
```javascript
// Coleção: produtos
{
  "produto_id": "P001",
  "nome": "Smartphone Galaxy S24",
  "categoria": "Eletrônicos > Smartphones",
  "caracteristicas": {
    "tela": "6.2 polegadas",
    "processador": "Snapdragon 8 Gen 3"
  },
  "tags": ["smartphone", "android", "samsung"],
  "estoque": 45,
  "ativo": true
}

// Coleção: usuarios_comportamento
{
  "usuario_id": "U001",
  "sessao_id": "S001",
  "eventos": [
    {
      "tipo": "page_view",
      "produto_id": "P001",
      "tempo_pagina": 45
    }
  ]
}
```

### PostgreSQL (Relacional)
```sql
-- Tabela: usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    segmento VARCHAR(50),
    valor_total_compras DECIMAL(12,2) DEFAULT 0.00
);

-- Tabela: pedidos
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    pedido_id VARCHAR(50) UNIQUE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id),
    valor_total DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pendente',
    data_pedido TIMESTAMP DEFAULT NOW()
);
```

## 🎯 Casos de Uso

### 1. Análise de Comportamento
- Identificar usuários mais ativos
- Analisar padrões de navegação
- Calcular taxas de conversão
- Segmentar por atividade

### 2. Predição de Churn
- Identificar usuários em risco
- Calcular probabilidade de abandono
- Priorizar ações de retenção
- Otimizar campanhas de marketing

### 3. Recomendações Personalizadas
- Sugerir produtos relevantes
- Adaptar ao perfil do usuário
- Aumentar taxa de conversão
- Melhorar experiência do cliente

### 4. Análise de Produtos
- Identificar produtos populares
- Analisar performance por categoria
- Otimizar catálogo
- Prever demanda

## 📊 Métricas e KPIs

### Comportamento (MongoDB)
- **Total de eventos por usuário**
- **Taxa de conversão (page_view → add_to_cart)**
- **Tempo médio por sessão**
- **Produtos únicos visualizados**

### Transações (PostgreSQL)
- **Valor total de compras**
- **Ticket médio**
- **Frequência de compras**
- **Dias desde última compra**

### Predições
- **Precisão do modelo de churn**
- **Recall por segmento**
- **AUC-ROC**
- **Hit Rate @ K (recomendações)**

## 📁 Estrutura do Projeto

```
analise-preditiva-ecommerce/
├── 📄 README.md                          # Este arquivo
├── 📄 requirements.txt                   # Dependências Python
├── 📄 main.py                           # Script principal
├── 📄 demo_mongodb_atlas.py             # Demo MongoDB Atlas
├── 📄 demo_simulado.py                  # Demo com dados simulados
├── 📄 teste_bancos_reais.py             # Teste de conexão
├── 📁 docs/                             # Documentação
│   ├── conceitos_analise.md             # Tipos de análise
│   ├── dominio_problema.md              # Domínio detalhado
│   ├── justificativa_bancos.md         # Justificativa técnica
│   └── ambiente_dados.md                # Data Lakehouse
├── 📁 models/                           # Modelos de dados
│   └── modelos_dados.md
├── 📁 notebooks/                        # Jupyter Notebooks
│   └── demo_analise_preditiva.ipynb    # Demonstração principal
├── 📁 scripts/                          # Scripts Python
│   ├── setup_databases.py              # Setup bancos
│   ├── demo_mongodb.py                 # Demo MongoDB
│   ├── demo_postgresql.py              # Demo PostgreSQL
│   ├── exemplos_praticos.py            # Exemplos de código
│   └── exemplos_manipulacao.md         # Operações CRUD
├── 📁 data/                             # Dados de exemplo
│   └── dados_exemplo.md
├── 📄 GUIA_EXECUCAO.md                  # Guia de execução
├── 📄 SETUP.md                         # Instruções de instalação
└── 📄 INSTRUCOES_GITHUB.md             # Como subir para GitHub
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# MongoDB Atlas
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_demo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### Configuração de Logs
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## 🧪 Testes

### Executar Testes
```bash
# Teste de conexão com bancos
python teste_bancos_reais.py

# Teste do sistema completo
python test_system.py
```

### Testes de Integração
```bash
# Testar MongoDB Atlas
python -c "from pymongo import MongoClient; client = MongoClient('sua_uri'); print('MongoDB OK')"

# Testar PostgreSQL
python -c "import psycopg2; conn = psycopg2.connect('sua_string'); print('PostgreSQL OK')"
```

## 📈 Monitoramento

### Métricas de Performance
- **Tempo de resposta das consultas**
- **Uso de memória**
- **CPU utilization**
- **Throughput de requisições**

### Logs de Aplicação
- **Erros de conexão**
- **Consultas lentas**
- **Falhas de predição**
- **Recomendações geradas**

## 🚀 Deploy em Produção

### Docker
```bash
# Build da imagem
docker build -t ecommerce-analytics .

# Executar container
docker run -p 5000:5000 ecommerce-analytics
```

### Docker Compose
```bash
# Iniciar todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps
```

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Padrões de Código
- **PEP 8** para Python
- **Docstrings** para funções
- **Type hints** quando possível
- **Testes unitários** para novas funcionalidades

## 📚 Documentação Adicional

### Conceitos Teóricos
- [Tipos de Análise de Dados](docs/conceitos_analise.md)
- [Domínio do Problema](docs/dominio_problema.md)
- [Justificativa dos Bancos](docs/justificativa_bancos.md)
- [Ambiente de Dados](docs/ambiente_dados.md)

### Exemplos Práticos
- [Modelos de Dados](models/modelos_dados.md)
- [Manipulação de Dados](scripts/exemplos_manipulacao.md)
- [Exemplos de Código](scripts/exemplos_praticos.py)

### Guias de Execução
- [Guia de Execução](GUIA_EXECUCAO.md)
- [Setup Detalhado](SETUP.md)
- [Instruções GitHub](INSTRUCOES_GITHUB.md)

## 🐛 Troubleshooting

### Problemas Comuns

#### MongoDB Atlas não conecta
```bash
# Verificar URI de conexão
# Verificar credenciais
# Verificar whitelist de IPs
```

#### PostgreSQL não conecta
```bash
# Verificar se está rodando
sudo systemctl status postgresql

# Verificar configurações
sudo nano /etc/postgresql/*/main/postgresql.conf
```

#### Erro de dependências Python
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## 📞 Suporte

### Contato
- **Email:** seu-email@exemplo.com
- **GitHub Issues:** [Criar Issue](https://github.com/seu-usuario/analise-preditiva-ecommerce/issues)

### FAQ
- **P:** Como alterar a configuração dos bancos de dados?
- **R:** Edite o arquivo de configuração com suas credenciais.

- **P:** Posso usar outros bancos de dados?
- **R:** Sim, mas será necessário adaptar os scripts de conexão.

- **P:** Como escalar para mais usuários?
- **R:** Configure MongoDB Atlas em cluster e use load balancer.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Professor Luiz C. Camargo, PhD** - Orientação acadêmica
- **Comunidade Python** - Bibliotecas e ferramentas
- **MongoDB Inc.** - Banco NoSQL
- **PostgreSQL Global Development Group** - Banco relacional
- **Scikit-learn** - Machine learning

---

**Desenvolvido com ❤️ para a disciplina de Análise Preditiva - Engenharia de Software**

*Última atualização: Janeiro 2025*