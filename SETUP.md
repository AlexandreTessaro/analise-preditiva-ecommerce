# Configuração do Ambiente

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=ecommerce_db

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Data Lakehouse
SPARK_MASTER=local[*]
DELTA_LAKE_PATH=/data/ecommerce
CHECKPOINT_PATH=/checkpoints

# APIs
API_HOST=localhost
API_PORT=8000
API_DEBUG=True
```

## Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar MongoDB:**
```bash
# Instalar MongoDB
# Windows: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
# Linux: sudo apt-get install mongodb
# macOS: brew install mongodb

# Iniciar serviço
mongod --dbpath /data/db
```

3. **Configurar PostgreSQL:**
```bash
# Instalar PostgreSQL
# Windows: https://www.postgresql.org/download/windows/
# Linux: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql

# Criar banco de dados
createdb ecommerce_db
```

4. **Configurar Data Lakehouse:**
```bash
# Instalar Apache Spark
# Download: https://spark.apache.org/downloads.html
# Configurar variáveis de ambiente:
export SPARK_HOME=/path/to/spark
export PATH=$PATH:$SPARK_HOME/bin
```

## Estrutura de Diretórios

```
analise_preditiva/
├── docs/                    # Documentação
├── models/                  # Modelos de dados
├── scripts/                 # Scripts de exemplo
├── data/                    # Dados de exemplo
├── notebooks/               # Jupyter notebooks
├── tests/                   # Testes unitários
├── requirements.txt         # Dependências
├── README.md               # Documentação principal
└── .env                    # Configurações (criar)
```

## Execução dos Exemplos

1. **Executar exemplos MongoDB:**
```bash
python scripts/exemplos_mongodb.py
```

2. **Executar exemplos PostgreSQL:**
```bash
python scripts/exemplos_postgresql.py
```

3. **Executar análise de dados:**
```bash
python scripts/analise_dados.py
```

4. **Iniciar API:**
```bash
uvicorn main:app --reload
```

## Dados de Exemplo

Os dados de exemplo estão disponíveis na pasta `data/`:
- `produtos_sample.json` - Produtos de exemplo
- `usuarios_sample.json` - Usuários de exemplo
- `comportamento_sample.json` - Dados de comportamento
- `pedidos_sample.csv` - Pedidos de exemplo

## Troubleshooting

### Problemas Comuns

1. **Erro de conexão MongoDB:**
   - Verificar se o MongoDB está rodando
   - Verificar URI de conexão no `.env`

2. **Erro de conexão PostgreSQL:**
   - Verificar se o PostgreSQL está rodando
   - Verificar credenciais no `.env`

3. **Erro de memória Spark:**
   - Ajustar `SPARK_DRIVER_MEMORY` e `SPARK_EXECUTOR_MEMORY`
   - Reduzir tamanho dos dados de exemplo

4. **Dependências não encontradas:**
   - Executar `pip install -r requirements.txt`
   - Verificar versão do Python (recomendado: 3.8+)
