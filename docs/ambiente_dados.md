# f) Ambiente para Dados Brutos e Pré-processados: Data Lakehouse

## Escolha: Data Lakehouse

Para o domínio de Sistema de Recomendação de Produtos E-commerce, escolhemos o **Data Lakehouse** como ambiente para abrigar dados brutos e pré-processados que alimentarão os modelos de análise preditiva.

## Justificativa da Escolha

### Por que Data Lakehouse?

O Data Lakehouse combina as melhores características do Data Lake e Data Warehouse, oferecendo:

1. **Flexibilidade do Data Lake:** Armazenamento de dados brutos em formatos diversos
2. **Performance do Data Warehouse:** Consultas SQL otimizadas e ACID transactions
3. **Economia de custos:** Elimina duplicação de dados entre ambientes
4. **Escalabilidade:** Suporta petabytes de dados com performance consistente
5. **Modernidade:** Arquitetura preparada para ML e análise preditiva

## Arquitetura do Data Lakehouse

### Camadas de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAKEHOUSE                           │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE SERVIÇO (Service Layer)                         │
│  • APIs REST/GraphQL                                       │
│  • Serviços de ML                                          │
│  • Dashboards e BI                                         │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE PROCESSAMENTO (Processing Layer)                │
│  • Apache Spark                                            │
│  • Apache Flink                                            │
│  • Python/R/Scala Jobs                                     │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE METADADOS (Metadata Layer)                      │
│  • Apache Hive Metastore                                  │
│  • Delta Lake Metadata                                     │
│  • Data Catalog                                            │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE ARMAZENAMENTO (Storage Layer)                   │
│  • Raw Data (JSON, CSV, Parquet)                          │
│  • Processed Data (Delta Tables)                          │
│  • Feature Store                                           │
└─────────────────────────────────────────────────────────────┘
```

### Tecnologias Escolhidas

#### 1. Apache Delta Lake
**Justificativa:** 
- **ACID Transactions:** Garantia de consistência para dados críticos
- **Time Travel:** Versionamento e auditoria de dados
- **Schema Evolution:** Adaptação automática a mudanças de schema
- **Performance:** Otimizações automáticas (Z-ordering, Bloom filters)

```python
# Exemplo de criação de tabela Delta
from delta import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EcommerceDataLakehouse") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

# Criar tabela Delta para produtos
spark.sql("""
CREATE TABLE IF NOT EXISTS produtos_raw (
    produto_id STRING,
    nome STRING,
    categoria STRING,
    marca STRING,
    preco DOUBLE,
    caracteristicas MAP<STRING, STRING>,
    tags ARRAY<STRING>,
    timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (categoria)
LOCATION '/data/ecommerce/produtos_raw'
""")
```

#### 2. Apache Spark
**Justificativa:**
- **Processamento distribuído:** Escala horizontalmente
- **Múltiplas linguagens:** Python, Scala, R, SQL
- **MLlib:** Biblioteca de machine learning integrada
- **Streaming:** Processamento em tempo real

#### 3. Apache Hive Metastore
**Justificativa:**
- **Catálogo centralizado:** Metadados unificados
- **Compatibilidade:** Integração com ferramentas BI
- **Governança:** Controle de acesso e auditoria

## Estrutura de Dados no Data Lakehouse

### 1. Camada Raw (Bronze)
**Propósito:** Armazenar dados brutos exatamente como recebidos

```
/data/ecommerce/raw/
├── produtos/
│   ├── year=2024/month=01/day=15/
│   │   ├── produtos_20240115_001.json
│   │   ├── produtos_20240115_002.json
│   │   └── produtos_20240115_003.json
│   └── year=2024/month=01/day=16/
├── usuarios/
│   ├── year=2024/month=01/day=15/
│   │   ├── usuarios_20240115_001.json
│   │   └── usuarios_20240115_002.json
├── comportamento/
│   ├── year=2024/month=01/day=15/
│   │   ├── eventos_20240115_001.json
│   │   └── eventos_20240115_002.json
└── transacoes/
    ├── year=2024/month=01/day=15/
    │   ├── pedidos_20240115_001.csv
    │   └── pagamentos_20240115_001.csv
```

**Exemplo de dados brutos:**
```json
// produtos_20240115_001.json
{
  "produto_id": "P001",
  "nome": "Smartphone Galaxy S24",
  "categoria": "Eletrônicos > Smartphones",
  "marca": "Samsung",
  "preco": 2999.99,
  "caracteristicas": {
    "tela": "6.2 polegadas",
    "processador": "Snapdragon 8 Gen 3"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "source": "api_produtos",
  "version": "v1.0"
}
```

### 2. Camada Processed (Silver)
**Propósito:** Dados limpos, validados e padronizados

```python
# Processamento de dados brutos para camada Silver
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Schema para produtos processados
produtos_schema = StructType([
    StructField("produto_id", StringType(), False),
    StructField("nome", StringType(), False),
    StructField("categoria", StringType(), False),
    StructField("marca", StringType(), False),
    StructField("preco", DoubleType(), False),
    StructField("caracteristicas_json", StringType(), True),
    StructField("tags_array", StringType(), True),
    StructField("data_processamento", TimestampType(), False)
])

# Ler dados brutos
produtos_raw = spark.read.json("/data/ecommerce/raw/produtos/")

# Processar e limpar dados
produtos_processed = produtos_raw.select(
    F.col("produto_id"),
    F.trim(F.col("nome")).alias("nome"),
    F.col("categoria"),
    F.upper(F.col("marca")).alias("marca"),
    F.col("preco").cast(DoubleType()),
    F.to_json(F.col("caracteristicas")).alias("caracteristicas_json"),
    F.to_json(F.col("tags")).alias("tags_array"),
    F.current_timestamp().alias("data_processamento")
).filter(
    F.col("produto_id").isNotNull() &
    F.col("nome").isNotNull() &
    F.col("preco") > 0
)

# Salvar como tabela Delta
produtos_processed.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("produtos_silver")
```

### 3. Camada Analytics (Gold)
**Propósito:** Dados agregados e otimizados para análise preditiva

```python
# Criar tabelas agregadas para análise preditiva
spark.sql("""
CREATE TABLE IF NOT EXISTS produtos_analytics AS
SELECT 
    produto_id,
    nome,
    categoria,
    marca,
    preco,
    AVG(rating) as avaliacao_media,
    COUNT(review_id) as total_reviews,
    SUM(quantidade_vendida) as total_vendas,
    SUM(receita_total) as receita_total,
    AVG(tempo_visualizacao) as tempo_medio_visualizacao,
    COUNT(DISTINCT usuario_id) as usuarios_unicos,
    -- Features para ML
    CASE 
        WHEN AVG(rating) >= 4.5 THEN 'high_rating'
        WHEN AVG(rating) >= 3.5 THEN 'medium_rating'
        ELSE 'low_rating'
    END as categoria_rating,
    CASE 
        WHEN SUM(receita_total) >= 100000 THEN 'high_revenue'
        WHEN SUM(receita_total) >= 10000 THEN 'medium_revenue'
        ELSE 'low_revenue'
    END as categoria_receita
FROM produtos_silver p
LEFT JOIN reviews_silver r ON p.produto_id = r.produto_id
LEFT JOIN vendas_silver v ON p.produto_id = v.produto_id
LEFT JOIN comportamento_silver c ON p.produto_id = c.produto_id
GROUP BY produto_id, nome, categoria, marca, preco
""")
```

## Feature Store para ML

### Estrutura do Feature Store
```python
# Feature Store para recomendações
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# Definir feature store para usuários
@fs.feature_table(
    name="ecommerce.user_features",
    primary_keys=["usuario_id"],
    description="Features de usuários para modelos de recomendação"
)
def create_user_features():
    return spark.sql("""
        SELECT 
            usuario_id,
            COUNT(DISTINCT produto_id) as produtos_unicos_visualizados,
            AVG(tempo_sessao) as tempo_medio_sessao,
            COUNT(DISTINCT categoria) as categorias_interesse,
            SUM(valor_compras) as valor_total_compras,
            COUNT(pedido_id) as total_pedidos,
            AVG(ticket_medio) as ticket_medio,
            DATEDIFF(CURRENT_DATE(), MAX(data_ultima_compra)) as dias_sem_comprar,
            -- Features categóricas
            CASE 
                WHEN SUM(valor_compras) >= 5000 THEN 'high_value'
                WHEN SUM(valor_compras) >= 1000 THEN 'medium_value'
                ELSE 'low_value'
            END as segmento_valor,
            CASE 
                WHEN COUNT(pedido_id) >= 10 THEN 'frequent_buyer'
                WHEN COUNT(pedido_id) >= 3 THEN 'regular_buyer'
                ELSE 'occasional_buyer'
            END as segmento_frequencia
        FROM usuarios_silver u
        LEFT JOIN comportamento_silver c ON u.usuario_id = c.usuario_id
        LEFT JOIN pedidos_silver p ON u.usuario_id = p.usuario_id
        GROUP BY usuario_id
    """)

# Definir feature store para produtos
@fs.feature_table(
    name="ecommerce.product_features",
    primary_keys=["produto_id"],
    description="Features de produtos para modelos de recomendação"
)
def create_product_features():
    return spark.sql("""
        SELECT 
            produto_id,
            categoria,
            marca,
            preco,
            AVG(rating) as avaliacao_media,
            COUNT(review_id) as total_reviews,
            SUM(quantidade_vendida) as total_vendas,
            SUM(receita_total) as receita_total,
            AVG(tempo_visualizacao) as tempo_medio_visualizacao,
            COUNT(DISTINCT usuario_id) as usuarios_unicos,
            -- Features derivadas
            preco / AVG(rating) as preco_por_rating,
            COUNT(review_id) / NULLIF(SUM(quantidade_vendida), 0) as taxa_review_venda,
            -- Features temporais
            DATEDIFF(CURRENT_DATE(), MIN(data_criacao)) as dias_no_catalogo
        FROM produtos_silver p
        LEFT JOIN reviews_silver r ON p.produto_id = r.produto_id
        LEFT JOIN vendas_silver v ON p.produto_id = v.produto_id
        LEFT JOIN comportamento_silver c ON p.produto_id = c.produto_id
        GROUP BY produto_id, categoria, marca, preco
    """)
```

## Pipeline de Dados para Análise Preditiva

### 1. Ingestão de Dados
```python
# Pipeline de ingestão em tempo real
from pyspark.sql import functions as F
from pyspark.sql.streaming import StreamingQuery

# Stream de eventos de comportamento
comportamento_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ecommerce-comportamento") \
    .load()

# Processar stream
processed_stream = comportamento_stream.select(
    F.from_json(F.col("value").cast("string"), comportamento_schema).alias("data")
).select("data.*")

# Salvar no Data Lakehouse
query = processed_stream.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/checkpoints/comportamento") \
    .option("path", "/data/ecommerce/raw/comportamento") \
    .trigger(processingTime='1 minute') \
    .start()
```

### 2. Processamento Batch
```python
# Job diário para processar dados
def process_daily_data():
    # Processar dados de produtos
    produtos_raw = spark.read.json("/data/ecommerce/raw/produtos/")
    produtos_processed = clean_and_validate_products(produtos_raw)
    produtos_processed.write.mode("append").saveAsTable("produtos_silver")
    
    # Processar dados de comportamento
    comportamento_raw = spark.read.json("/data/ecommerce/raw/comportamento/")
    comportamento_processed = aggregate_user_behavior(comportamento_raw)
    comportamento_processed.write.mode("append").saveAsTable("comportamento_silver")
    
    # Atualizar features
    update_user_features()
    update_product_features()
    
    # Gerar recomendações
    generate_recommendations()

# Executar job diário
process_daily_data()
```

### 3. Monitoramento e Qualidade
```python
# Validação de qualidade dos dados
from great_expectations import DataContext

context = DataContext()

# Validar dados de produtos
produtos_batch = context.get_batch(
    datasource_name="ecommerce_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="produtos_silver"
)

# Expectativas de qualidade
produtos_batch.expect_column_values_to_not_be_null("produto_id")
produtos_batch.expect_column_values_to_be_between("preco", min_value=0, max_value=100000)
produtos_batch.expect_column_values_to_be_in_set("categoria", ["Eletrônicos", "Roupas", "Casa"])

# Executar validação
validation_result = context.run_validation_operator(
    "action_list_operator",
    assets_to_validate=[produtos_batch]
)
```

## Vantagens do Data Lakehouse para Análise Preditiva

### 1. Flexibilidade de Dados
- **Múltiplos formatos:** JSON, Parquet, CSV, Avro
- **Schema evolution:** Adaptação automática a mudanças
- **Dados não estruturados:** Suporte a logs, imagens, textos

### 2. Performance Otimizada
- **Indexação automática:** Bloom filters e Z-ordering
- **Cache inteligente:** Dados frequentes em memória
- **Compressão:** Redução de custos de armazenamento

### 3. Governança e Segurança
- **ACID transactions:** Consistência garantida
- **Time travel:** Auditoria e rollback
- **Controle de acesso:** Segurança granular
- **Lineage:** Rastreabilidade de dados

### 4. Integração com ML
- **Feature Store:** Reutilização de features
- **MLflow:** Gestão de modelos
- **Delta Sharing:** Compartilhamento seguro
- **Real-time:** Processamento em tempo real

## Comparação com Outras Opções

### Data Lake vs Data Lakehouse
| Aspecto | Data Lake | Data Lakehouse |
|---------|-----------|----------------|
| **Consistência** | Eventual | ACID |
| **Performance** | Variável | Consistente |
| **Governança** | Limitada | Avançada |
| **ML Integration** | Básica | Nativa |

### Data Warehouse vs Data Lakehouse
| Aspecto | Data Warehouse | Data Lakehouse |
|---------|----------------|----------------|
| **Flexibilidade** | Limitada | Alta |
| **Custo** | Alto | Médio |
| **Escalabilidade** | Vertical | Horizontal |
| **Dados Não Estruturados** | Limitado | Nativo |

## Conclusão

O Data Lakehouse é a escolha ideal para o domínio de Sistema de Recomendação E-commerce porque:

1. **Suporta dados heterogêneos:** Produtos, comportamento, transações
2. **Performance consistente:** Consultas SQL otimizadas
3. **Flexibilidade para ML:** Feature Store integrado
4. **Economia de custos:** Elimina duplicação de dados
5. **Escalabilidade:** Suporta crescimento do negócio
6. **Modernidade:** Arquitetura preparada para o futuro

Esta arquitetura permite uma análise preditiva eficiente, com dados sempre atualizados e prontos para alimentar modelos de machine learning em tempo real, garantindo recomendações precisas e personalizadas para os usuários do e-commerce.
