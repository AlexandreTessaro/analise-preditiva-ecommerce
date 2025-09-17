# Exemplos Práticos de Manipulação de Dados

## MongoDB - Exemplos Python

### Conexão e Configuração
```python
from pymongo import MongoClient
from datetime import datetime
import json

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['ecommerce_db']

# Coleções
produtos = db['produtos']
usuarios_comportamento = db['usuarios_comportamento']
recomendacoes = db['recomendacoes']
```

### Inserção de Dados
```python
# Inserir produto
produto = {
    "produto_id": "P001",
    "nome": "Smartphone Galaxy S24",
    "categoria": "Eletrônicos > Smartphones",
    "marca": "Samsung",
    "preco": 2999.99,
    "caracteristicas": {
        "tela": "6.2 polegadas",
        "processador": "Snapdragon 8 Gen 3",
        "ram": "8GB",
        "armazenamento": "128GB"
    },
    "tags": ["smartphone", "android", "samsung"],
    "estoque": 45,
    "ativo": True,
    "data_criacao": datetime.now()
}

result = produtos.insert_one(produto)
print(f"Produto inserido com ID: {result.inserted_id}")

# Inserir comportamento de usuário
comportamento = {
    "usuario_id": "U001",
    "sessao_id": "S001",
    "timestamp": datetime.now(),
    "eventos": [
        {
            "tipo": "page_view",
            "produto_id": "P001",
            "tempo_pagina": 45,
            "timestamp": datetime.now()
        },
        {
            "tipo": "click",
            "elemento": "add_to_cart",
            "produto_id": "P001",
            "timestamp": datetime.now()
        }
    ]
}

result = usuarios_comportamento.insert_one(comportamento)
print(f"Comportamento inserido com ID: {result.inserted_id}")
```

### Consultas
```python
# Buscar produtos por categoria
smartphones = produtos.find({
    "categoria": {"$regex": "Smartphones", "$options": "i"},
    "ativo": True
})

for produto in smartphones:
    print(f"Produto: {produto['nome']} - Preço: R$ {produto['preco']}")

# Buscar produtos por faixa de preço
produtos_faixa = produtos.find({
    "preco": {"$gte": 1000, "$lte": 5000},
    "ativo": True
}).sort("preco", 1)

# Agregação para análise
pipeline = [
    {"$match": {"ativo": True}},
    {"$group": {
        "_id": "$categoria",
        "total_produtos": {"$sum": 1},
        "preco_medio": {"$avg": "$preco"},
        "estoque_total": {"$sum": "$estoque"}
    }},
    {"$sort": {"total_produtos": -1}}
]

resultado = produtos.aggregate(pipeline)
for item in resultado:
    print(f"Categoria: {item['_id']}")
    print(f"Total produtos: {item['total_produtos']}")
    print(f"Preço médio: R$ {item['preco_medio']:.2f}")
    print(f"Estoque total: {item['estoque_total']}")
    print("-" * 40)
```

### Atualizações
```python
# Atualizar preço e estoque
result = produtos.update_one(
    {"produto_id": "P001"},
    {
        "$set": {
            "preco": 2799.99,
            "estoque": 50,
            "data_atualizacao": datetime.now()
        }
    }
)

print(f"Produtos atualizados: {result.modified_count}")

# Incrementar estoque
result = produtos.update_one(
    {"produto_id": "P001"},
    {"$inc": {"estoque": 10}}
)

# Adicionar nova tag
result = produtos.update_one(
    {"produto_id": "P001"},
    {"$addToSet": {"tags": "premium"}}
)
```

## PostgreSQL - Exemplos Python

### Conexão e Configuração
```python
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    database='ecommerce_db',
    user='postgres',
    password='your_password'
)

cursor = conn.cursor(cursor_factory=RealDictCursor)
```

### Inserção de Dados
```python
# Inserir usuário
usuario_sql = """
INSERT INTO usuarios (usuario_id, email, nome, sobrenome, data_nascimento, genero, telefone, cpf, endereco)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

usuario_data = (
    'U001',
    'joao.silva@email.com',
    'João',
    'Silva',
    '1990-05-15',
    'M',
    '(11) 99999-9999',
    '123.456.789-00',
    json.dumps({
        "rua": "Rua das Flores, 123",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234-567"
    })
)

cursor.execute(usuario_sql, usuario_data)
conn.commit()

# Inserir produto
produto_sql = """
INSERT INTO produtos_relacional (produto_id, nome, categoria_id, marca, preco, descricao, estoque)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

produto_data = (
    'P001',
    'Smartphone Galaxy S24',
    1,  # ID da categoria
    'Samsung',
    2999.99,
    'Smartphone com tela de 6.2 polegadas',
    45
)

cursor.execute(produto_sql, produto_data)
conn.commit()
```

### Consultas
```python
# Buscar usuários por segmento
cursor.execute("""
    SELECT usuario_id, nome, email, segmento, valor_total_compras
    FROM usuarios
    WHERE segmento = %s
    ORDER BY valor_total_compras DESC
""", ('high_value',))

usuarios = cursor.fetchall()
for usuario in usuarios:
    print(f"Usuário: {usuario['nome']} - Segmento: {usuario['segmento']}")

# Análise de vendas por produto
cursor.execute("""
    SELECT 
        p.produto_id,
        p.nome,
        COUNT(ip.id) as total_vendas,
        SUM(ip.quantidade) as quantidade_vendida,
        SUM(ip.valor_total) as receita_total,
        AVG(ip.preco_unitario) as preco_medio
    FROM produtos_relacional p
    LEFT JOIN itens_pedido ip ON p.produto_id = ip.produto_id
    LEFT JOIN pedidos ped ON ip.pedido_id = ped.id
    WHERE ped.status = 'concluido'
    GROUP BY p.produto_id, p.nome
    ORDER BY receita_total DESC
""")

vendas = cursor.fetchall()
for venda in vendas:
    print(f"Produto: {venda['nome']}")
    print(f"Total vendas: {venda['total_vendas']}")
    print(f"Receita total: R$ {venda['receita_total']:.2f}")
    print("-" * 40)

# Usar pandas para análise
df = pd.read_sql_query("""
    SELECT 
        u.usuario_id,
        u.nome,
        u.segmento,
        COUNT(p.id) as total_pedidos,
        SUM(p.valor_total) as valor_total_compras,
        AVG(p.valor_total) as ticket_medio
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.usuario_id
    WHERE p.status = 'concluido'
    GROUP BY u.usuario_id, u.nome, u.segmento
    ORDER BY valor_total_compras DESC
""", conn)

print(df.head())
print(f"\nEstatísticas descritivas:")
print(df.describe())
```

### Atualizações
```python
# Atualizar preço e estoque
cursor.execute("""
    UPDATE produtos_relacional
    SET 
        preco = %s,
        estoque = %s,
        data_atualizacao = NOW()
    WHERE produto_id = %s
""", (2799.99, 50, 'P001'))

conn.commit()
print(f"Produtos atualizados: {cursor.rowcount}")

# Atualizar segmento do usuário
cursor.execute("""
    UPDATE usuarios
    SET segmento = CASE
        WHEN valor_total_compras >= 5000 THEN 'high_value'
        WHEN valor_total_compras >= 1000 THEN 'medium_value'
        ELSE 'low_value'
    END
    WHERE valor_total_compras > 0
""")

conn.commit()
print(f"Usuários atualizados: {cursor.rowcount}")
```

## Análise Preditiva - Exemplos

### Análise de Comportamento
```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Carregar dados de comportamento
comportamento_df = pd.read_sql_query("""
    SELECT 
        u.usuario_id,
        u.nome,
        u.segmento,
        COUNT(p.id) as total_pedidos,
        SUM(p.valor_total) as valor_total_compras,
        AVG(p.valor_total) as ticket_medio,
        COUNT(DISTINCT ip.produto_id) as produtos_unicos,
        MAX(p.data_pedido) as ultima_compra
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.usuario_id
    LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
    WHERE p.status = 'concluido'
    GROUP BY u.usuario_id, u.nome, u.segmento
""", conn)

# Preparar dados para clustering
features = ['total_pedidos', 'valor_total_compras', 'ticket_medio', 'produtos_unicos']
X = comportamento_df[features].fillna(0)

# Normalizar dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
comportamento_df['cluster'] = kmeans.fit_predict(X_scaled)

# Analisar clusters
cluster_analysis = comportamento_df.groupby('cluster')[features].mean()
print("Análise de Clusters:")
print(cluster_analysis)

# Visualizar clusters
plt.figure(figsize=(12, 8))
plt.scatter(comportamento_df['valor_total_compras'], 
           comportamento_df['total_pedidos'], 
           c=comportamento_df['cluster'], 
           cmap='viridis')
plt.xlabel('Valor Total Compras')
plt.ylabel('Total Pedidos')
plt.title('Clusters de Usuários')
plt.colorbar()
plt.show()
```

### Predição de Probabilidade de Compra
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Preparar dados para predição
prediction_df = pd.read_sql_query("""
    SELECT 
        u.usuario_id,
        u.segmento,
        COUNT(p.id) as total_pedidos,
        SUM(p.valor_total) as valor_total_compras,
        AVG(p.valor_total) as ticket_medio,
        EXTRACT(DAYS FROM NOW() - MAX(p.data_pedido)) as dias_sem_comprar,
        CASE 
            WHEN COUNT(p.id) > 0 THEN 1 
            ELSE 0 
        END as comprou_ultimo_mes
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.usuario_id
    WHERE p.status = 'concluido'
    GROUP BY u.usuario_id, u.segmento
""", conn)

# Preparar features
feature_columns = ['total_pedidos', 'valor_total_compras', 'ticket_medio', 'dias_sem_comprar']
X = prediction_df[feature_columns].fillna(0)
y = prediction_df['comprou_ultimo_mes']

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fazer predições
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Avaliar modelo
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))

print("\nMatriz de Confusão:")
print(confusion_matrix(y_test, y_pred))

# Importância das features
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nImportância das Features:")
print(feature_importance)
```

## Fechamento de Conexões
```python
# Fechar conexões
cursor.close()
conn.close()
client.close()
```

## Conclusão

Estes exemplos demonstram como manipular dados tanto no MongoDB quanto no PostgreSQL, incluindo operações básicas de CRUD e análises mais complexas para análise preditiva. A combinação de ambos os bancos permite aproveitar as vantagens de cada tecnologia para diferentes aspectos do sistema de recomendação e-commerce.
