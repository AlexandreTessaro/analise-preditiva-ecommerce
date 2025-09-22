# 🚀 Guia de Execução - Análise Preditiva E-commerce

## 📋 Pré-requisitos

### 1. Software Necessário
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **MongoDB 4.4+** - [Download](https://www.mongodb.com/try/download/community)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

### 2. Instalação dos Bancos de Dados

#### MongoDB (Windows)
```bash
# Baixar e instalar MongoDB Community Server
# Iniciar o serviço MongoDB
net start MongoDB

# Verificar se está rodando
mongosh --version
```

#### PostgreSQL (Windows)
```bash
# Baixar e instalar PostgreSQL
# Durante a instalação, definir senha para usuário 'postgres'
# Criar banco de dados
createdb -U postgres ecommerce_demo
```

#### MongoDB (Linux/Ubuntu)
```bash
# Instalar MongoDB
sudo apt-get update
sudo apt-get install -y mongodb

# Iniciar MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verificar status
sudo systemctl status mongodb
```

#### PostgreSQL (Linux/Ubuntu)
```bash
# Instalar PostgreSQL
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar banco de dados
sudo -u postgres createdb ecommerce_demo

# Verificar status
sudo systemctl status postgresql
```

## 🛠️ Instalação do Projeto

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/analise-preditiva-ecommerce.git
cd analise-preditiva-ecommerce
```

### 2. Instalar Dependências Python
```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de configuração
cp config.env .env

# Editar configurações se necessário
nano .env
```

## 🎮 Execução

### Opção 1: Execução Automática (Recomendada)
```bash
# Executar script principal
python main.py
```

Este script irá:
- ✅ Verificar dependências
- ✅ Conectar aos bancos de dados
- ✅ Configurar dados de exemplo
- ✅ Executar demonstrações MongoDB e PostgreSQL
- ✅ Gerar dashboards e visualizações
- ✅ Mostrar resumo dos resultados

### Opção 2: Execução Manual

#### 1. Configurar Bancos de Dados
```bash
python scripts/setup_databases.py
```

#### 2. Executar Demonstração MongoDB
```bash
python scripts/demo_mongodb.py
```

#### 3. Executar Demonstração PostgreSQL
```bash
python scripts/demo_postgresql.py
```

#### 4. Executar Jupyter Notebook
```bash
jupyter notebook notebooks/demo_analise_preditiva.ipynb
```

## 📊 Resultados Esperados

### Arquivos Gerados
- `dashboard_mongodb.png` - Dashboard de análise MongoDB
- `dashboard_postgresql.png` - Dashboard de análise PostgreSQL
- `logs/app.log` - Logs da aplicação

### Funcionalidades Demonstradas
- ✅ **Análise Descritiva:** Comportamento de usuários e produtos
- ✅ **Análise Preditiva:** Clustering K-Means e predição de churn
- ✅ **Sistema de Recomendações:** Algoritmo colaborativo
- ✅ **Visualizações:** Dashboards interativos
- ✅ **Operações CRUD:** MongoDB e PostgreSQL
- ✅ **Modelos de ML:** Random Forest para churn

## 🔧 Troubleshooting

### Problema: MongoDB não conecta
```bash
# Verificar se está rodando
# Windows:
net start MongoDB
# Linux:
sudo systemctl start mongodb

# Verificar logs
# Windows: Verificar Event Viewer
# Linux:
sudo journalctl -u mongodb
```

### Problema: PostgreSQL não conecta
```bash
# Verificar se está rodando
# Windows: Verificar Services
# Linux:
sudo systemctl start postgresql

# Verificar logs
# Linux:
sudo journalctl -u postgresql
```

### Problema: Erro de dependências Python
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar versão do Python
python --version
```

### Problema: Erro de permissões
```bash
# Linux: Dar permissões de execução
chmod +x scripts/*.py
chmod +x main.py

# Windows: Executar como administrador se necessário
```

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

## 🎯 Avaliação N1

### Pontos Atendidos
- **a) Tipos de Análise de Dados (0,5)** ✅
- **b) Domínio de Problema (1,0)** ✅
- **c) Justificativa dos Modelos (0,5)** ✅
- **d) Modelos de Dados (0,5)** ✅
- **e) Manipulação de Dados (0,5)** ✅
- **f) Ambiente de Dados (1,0)** ✅

**Total: 4,0 pontos**

### Domínio Escolhido
**Sistema de Recomendação de Produtos E-commerce**
- Classificação de usuários por comportamento
- Predição de probabilidade de compra
- Recomendação personalizada de produtos

### Tecnologias Utilizadas
- **MongoDB:** Dados não estruturados e comportamento
- **PostgreSQL:** Dados transacionais e relatórios
- **Data Lakehouse:** Ambiente para dados brutos e processados
- **Python:** Análise de dados e machine learning

## 🚀 Próximos Passos

### Para N3 (Ciência de Dados)
1. **Engenharia de Features:** Criar variáveis preditivas mais sofisticadas
2. **Modelagem Avançada:** Implementar algoritmos de deep learning
3. **Validação:** Testes A/B e métricas de negócio
4. **Deploy:** Sistema em produção com monitoramento

### Melhorias Futuras
1. **Real-time:** Processamento em tempo real
2. **Escalabilidade:** Suporte a milhões de usuários
3. **Integração:** APIs REST e microserviços
4. **Monitoramento:** Dashboards de produção

## 📞 Suporte

### Contato
- **Email:** seu-email@exemplo.com
- **GitHub Issues:** [Criar Issue](https://github.com/seu-usuario/analise-preditiva-ecommerce/issues)

### FAQ
- **P:** Como alterar a configuração dos bancos?
- **R:** Edite o arquivo `.env` com suas configurações.

- **P:** Posso usar outros bancos de dados?
- **R:** Sim, mas será necessário adaptar os scripts de conexão.

- **P:** Como escalar para mais usuários?
- **R:** Configure MongoDB e PostgreSQL em cluster.

---

**Desenvolvido com ❤️ para a disciplina de Análise Preditiva - Engenharia de Software**

*Última atualização: Janeiro 2025*
