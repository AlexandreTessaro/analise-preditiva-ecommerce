# e) Exemplos de Manipulação de Dados

## MongoDB - Operações NoSQL

### 1. Inserção de Dados (Create)

#### Inserir um novo produto
```javascript
// Inserir produto único
db.produtos.insertOne({
  "produto_id": "P001",
  "nome": "Smartphone Galaxy S24",
  "categoria": "Eletrônicos > Smartphones",
  "marca": "Samsung",
  "preco": 2999.99,
  "moeda": "BRL",
  "caracteristicas": {
    "tela": "6.2 polegadas",
    "processador": "Snapdragon 8 Gen 3",
    "ram": "8GB",
    "armazenamento": "128GB"
  },
  "tags": ["smartphone", "android", "samsung"],
  "avaliacao_media": 4.5,
  "total_avaliacoes": 1250,
  "estoque": 45,
  "ativo": true,
  "data_criacao": new Date(),
  "data_atualizacao": new Date()
});

// Inserir múltiplos produtos
db.produtos.insertMany([
  {
    "produto_id": "P002",
    "nome": "iPhone 15 Pro",
    "categoria": "Eletrônicos > Smartphones",
    "marca": "Apple",
    "preco": 8999.99,
    "caracteristicas": {
      "tela": "6.1 polegadas",
      "processador": "A17 Pro",
      "ram": "8GB",
      "armazenamento": "128GB"
    },
    "tags": ["smartphone", "ios", "apple"],
    "estoque": 30,
    "ativo": true
  },
  {
    "produto_id": "P003",
    "nome": "Notebook Dell XPS 13",
    "categoria": "Eletrônicos > Notebooks",
    "marca": "Dell",
    "preco": 5999.99,
    "caracteristicas": {
      "tela": "13.4 polegadas",
      "processador": "Intel i7",
      "ram": "16GB",
      "armazenamento": "512GB SSD"
    },
    "tags": ["notebook", "windows", "dell"],
    "estoque": 20,
    "ativo": true
  }
]);
```

#### Inserir comportamento de usuário
```javascript
db.usuarios_comportamento.insertOne({
  "usuario_id": "U001",
  "sessao_id": "S001",
  "timestamp": new Date(),
  "eventos": [
    {
      "tipo": "page_view",
      "produto_id": "P001",
      "tempo_pagina": 45,
      "timestamp": new Date()
    },
    {
      "tipo": "click",
      "elemento": "add_to_cart",
      "produto_id": "P001",
      "timestamp": new Date()
    }
  ],
  "pagina_atual": "/produto/P001",
  "referrer": "https://google.com/search?q=samsung+galaxy",
  "localizacao": {
    "pais": "Brasil",
    "estado": "São Paulo",
    "cidade": "São Paulo"
  }
});
```

### 2. Consultas (Read)

#### Buscar produtos por categoria
```javascript
// Buscar todos os smartphones
db.produtos.find({
  "categoria": { $regex: "Smartphones", $options: "i" },
  "ativo": true
});

// Buscar produtos por faixa de preço
db.produtos.find({
  "preco": { $gte: 1000, $lte: 5000 },
  "ativo": true
}).sort({ "preco": 1 });

// Buscar produtos com características específicas
db.produtos.find({
  "caracteristicas.ram": "8GB",
  "caracteristicas.armazenamento": { $regex: "128GB" }
});
```

#### Agregação para análise de produtos
```javascript
// Produtos mais vendidos por categoria
db.produtos.aggregate([
  {
    $match: { "ativo": true }
  },
  {
    $group: {
      "_id": "$categoria",
      "total_produtos": { $sum: 1 },
      "preco_medio": { $avg: "$preco" },
      "avaliacao_media": { $avg: "$avaliacao_media" }
    }
  },
  {
    $sort: { "total_produtos": -1 }
  }
]);

// Análise de comportamento por usuário
db.usuarios_comportamento.aggregate([
  {
    $unwind: "$eventos"
  },
  {
    $group: {
      "_id": "$usuario_id",
      "total_eventos": { $sum: 1 },
      "page_views": {
        $sum: {
          $cond: [{ $eq: ["$eventos.tipo", "page_view"] }, 1, 0]
        }
      },
      "clicks": {
        $sum: {
          $cond: [{ $eq: ["$eventos.tipo", "click"] }, 1, 0]
        }
      }
    }
  },
  {
    $sort: { "total_eventos": -1 }
  }
]);
```

#### Busca textual
```javascript
// Criar índice de texto
db.produtos.createIndex({
  "nome": "text",
  "descricao": "text",
  "tags": "text"
});

// Busca por texto
db.produtos.find({
  $text: { $search: "smartphone samsung" }
}, {
  score: { $meta: "textScore" }
}).sort({ score: { $meta: "textScore" } });
```

### 3. Atualização (Update)

#### Atualizar informações do produto
```javascript
// Atualizar preço e estoque
db.produtos.updateOne(
  { "produto_id": "P001" },
  {
    $set: {
      "preco": 2799.99,
      "estoque": 50,
      "data_atualizacao": new Date()
    }
  }
);

// Atualizar avaliação média
db.produtos.updateOne(
  { "produto_id": "P001" },
  {
    $set: {
      "avaliacao_media": 4.6,
      "total_avaliacoes": 1300
    }
  }
);

// Adicionar nova tag
db.produtos.updateOne(
  { "produto_id": "P001" },
  {
    $addToSet: { "tags": "premium" }
  }
);

// Incrementar estoque
db.produtos.updateOne(
  { "produto_id": "P001" },
  {
    $inc: { "estoque": 10 }
  }
);
```

#### Atualizar recomendações
```javascript
db.recomendacoes.updateOne(
  { "usuario_id": "U001" },
  {
    $set: {
      "recomendacoes": [
        {
          "produto_id": "P002",
          "score": 0.95,
          "motivo": "usuarios_similares",
          "timestamp": new Date()
        },
        {
          "produto_id": "P003",
          "score": 0.87,
          "motivo": "produtos_similares",
          "timestamp": new Date()
        }
      ],
      "data_geracao": new Date(),
      "valido_ate": new Date(Date.now() + 2 * 60 * 60 * 1000) // 2 horas
    }
  },
  { upsert: true }
);
```

### 4. Exclusão (Delete)

#### Remover produtos inativos
```javascript
// Remover produtos inativos há mais de 30 dias
db.produtos.deleteMany({
  "ativo": false,
  "data_atualizacao": { $lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
});

// Remover recomendações expiradas
db.recomendacoes.deleteMany({
  "valido_ate": { $lt: new Date() }
});
```

## PostgreSQL - Operações Relacionais

### 1. Inserção de Dados (Create)

#### Inserir usuário
```sql
-- Inserir usuário
INSERT INTO usuarios (usuario_id, email, nome, sobrenome, data_nascimento, genero, telefone, cpf, endereco)
VALUES (
    'U001',
    'joao.silva@email.com',
    'João',
    'Silva',
    '1990-05-15',
    'M',
    '(11) 99999-9999',
    '123.456.789-00',
    '{"rua": "Rua das Flores, 123", "cidade": "São Paulo", "estado": "SP", "cep": "01234-567"}'
);

-- Inserir categoria
INSERT INTO categorias (categoria_id, nome, descricao, nivel)
VALUES ('CAT001', 'Eletrônicos', 'Produtos eletrônicos em geral', 1);

INSERT INTO categorias (categoria_id, nome, categoria_pai_id, nivel)
VALUES ('CAT002', 'Smartphones', (SELECT id FROM categorias WHERE categoria_id = 'CAT001'), 2);
```

#### Inserir produto
```sql
INSERT INTO produtos_relacional (
    produto_id, nome, categoria_id, marca, preco, preco_original, 
    descricao, sku, peso, dimensoes, estoque, estoque_minimo
)
VALUES (
    'P001',
    'Smartphone Galaxy S24',
    (SELECT id FROM categorias WHERE categoria_id = 'CAT002'),
    'Samsung',
    2999.99,
    3299.99,
    'Smartphone com tela de 6.2 polegadas, 128GB de armazenamento',
    'SAM-GAL-S24-128',
    168.0,
    '{"largura": 70.6, "altura": 147.0, "profundidade": 7.6}',
    45,
    5
);
```

#### Inserir pedido completo
```sql
-- Inserir pedido
INSERT INTO pedidos (pedido_id, usuario_id, status, valor_total, valor_frete, metodo_pagamento, endereco_entrega)
VALUES (
    'PED001',
    (SELECT id FROM usuarios WHERE usuario_id = 'U001'),
    'pendente',
    2999.99,
    15.00,
    'cartao_credito',
    '{"rua": "Rua das Flores, 123", "cidade": "São Paulo", "estado": "SP", "cep": "01234-567"}'
);

-- Inserir itens do pedido
INSERT INTO itens_pedido (pedido_id, produto_id, nome_produto, preco_unitario, quantidade, valor_total)
VALUES (
    (SELECT id FROM pedidos WHERE pedido_id = 'PED001'),
    'P001',
    'Smartphone Galaxy S24',
    2999.99,
    1,
    2999.99
);
```

### 2. Consultas (Read)

#### Consultas básicas
```sql
-- Buscar usuários por segmento
SELECT usuario_id, nome, email, segmento, valor_total_compras
FROM usuarios
WHERE segmento = 'high_value'
ORDER BY valor_total_compras DESC;

-- Buscar produtos por categoria
SELECT p.produto_id, p.nome, p.preco, c.nome as categoria_nome
FROM produtos_relacional p
JOIN categorias c ON p.categoria_id = c.id
WHERE c.nome = 'Smartphones'
AND p.ativo = true
ORDER BY p.preco;

-- Buscar pedidos por período
SELECT p.pedido_id, u.nome, p.valor_total, p.status, p.data_pedido
FROM pedidos p
JOIN usuarios u ON p.usuario_id = u.id
WHERE p.data_pedido >= '2024-01-01'
AND p.data_pedido < '2024-02-01'
ORDER BY p.data_pedido DESC;
```

#### Consultas analíticas
```sql
-- Análise de vendas por produto
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
ORDER BY receita_total DESC;

-- Análise de usuários por valor
SELECT 
    u.usuario_id,
    u.nome,
    u.email,
    COUNT(p.id) as total_pedidos,
    SUM(p.valor_total) as valor_total_compras,
    AVG(p.valor_total) as ticket_medio,
    MAX(p.data_pedido) as ultima_compra
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE p.status = 'concluido'
GROUP BY u.usuario_id, u.nome, u.email
HAVING SUM(p.valor_total) > 1000
ORDER BY valor_total_compras DESC;

-- Produtos mais vendidos por categoria
SELECT 
    c.nome as categoria,
    COUNT(DISTINCT p.produto_id) as total_produtos,
    SUM(ip.quantidade) as total_vendido,
    SUM(ip.valor_total) as receita_categoria
FROM categorias c
JOIN produtos_relacional p ON c.id = p.categoria_id
JOIN itens_pedido ip ON p.produto_id = ip.produto_id
JOIN pedidos ped ON ip.pedido_id = ped.id
WHERE ped.status = 'concluido'
GROUP BY c.nome
ORDER BY receita_categoria DESC;
```

#### Consultas com JSON
```sql
-- Buscar usuários por cidade (dados JSON)
SELECT usuario_id, nome, email, endereco->>'cidade' as cidade
FROM usuarios
WHERE endereco->>'cidade' = 'São Paulo';

-- Buscar produtos por dimensões específicas
SELECT produto_id, nome, dimensoes
FROM produtos_relacional
WHERE (dimensoes->>'largura')::numeric < 80
AND (dimensoes->>'altura')::numeric < 160;
```

### 3. Atualização (Update)

#### Atualizar informações
```sql
-- Atualizar preço e estoque do produto
UPDATE produtos_relacional
SET 
    preco = 2799.99,
    estoque = 50,
    data_atualizacao = NOW()
WHERE produto_id = 'P001';

-- Atualizar status do pedido
UPDATE pedidos
SET 
    status = 'concluido',
    data_pagamento = NOW()
WHERE pedido_id = 'PED001';

-- Atualizar segmento do usuário baseado em compras
UPDATE usuarios
SET segmento = CASE
    WHEN valor_total_compras >= 5000 THEN 'high_value'
    WHEN valor_total_compras >= 1000 THEN 'medium_value'
    ELSE 'low_value'
END
WHERE valor_total_compras > 0;

-- Atualizar dados JSON
UPDATE usuarios
SET endereco = jsonb_set(endereco, '{cidade}', '"São Paulo"')
WHERE usuario_id = 'U001';
```

#### Atualizações em lote
```sql
-- Atualizar estoque baseado em vendas
UPDATE produtos_relacional
SET estoque = estoque - (
    SELECT COALESCE(SUM(ip.quantidade), 0)
    FROM itens_pedido ip
    JOIN pedidos p ON ip.pedido_id = p.id
    WHERE ip.produto_id = produtos_relacional.produto_id
    AND p.status = 'concluido'
    AND p.data_pedido >= CURRENT_DATE - INTERVAL '7 days'
)
WHERE ativo = true;
```

### 4. Exclusão (Delete)

#### Exclusões condicionais
```sql
-- Remover produtos inativos há mais de 30 dias
DELETE FROM produtos_relacional
WHERE ativo = false
AND data_atualizacao < NOW() - INTERVAL '30 days';

-- Remover pedidos cancelados antigos
DELETE FROM pedidos
WHERE status = 'cancelado'
AND data_cancelamento < NOW() - INTERVAL '1 year';

-- Remover itens de carrinho antigos
DELETE FROM carrinho_compras
WHERE data_atualizacao < NOW() - INTERVAL '30 days';
```

## Operações de Análise Preditiva

### MongoDB - Pipeline de Agregação para Recomendações
```javascript
// Pipeline para encontrar usuários similares
db.usuarios_comportamento.aggregate([
  {
    $unwind: "$eventos"
  },
  {
    $match: {
      "eventos.tipo": "page_view",
      "eventos.produto_id": { $exists: true }
    }
  },
  {
    $group: {
      "_id": "$usuario_id",
      "produtos_visualizados": { $addToSet: "$eventos.produto_id" }
    }
  },
  {
    $project: {
      "usuario_id": "$_id",
      "produtos_visualizados": 1,
      "total_produtos": { $size: "$produtos_visualizados" }
    }
  },
  {
    $match: { "total_produtos": { $gte: 5 } }
  }
]);
```

### PostgreSQL - Consultas para Análise Preditiva
```sql
-- Calcular probabilidade de compra baseada em histórico
WITH user_behavior AS (
    SELECT 
        u.usuario_id,
        COUNT(p.id) as total_pedidos,
        AVG(p.valor_total) as ticket_medio,
        MAX(p.data_pedido) as ultima_compra,
        EXTRACT(DAYS FROM NOW() - MAX(p.data_pedido)) as dias_sem_comprar
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.usuario_id AND p.status = 'concluido'
    GROUP BY u.usuario_id
)
SELECT 
    usuario_id,
    total_pedidos,
    ticket_medio,
    dias_sem_comprar,
    CASE
        WHEN total_pedidos >= 10 AND dias_sem_comprar <= 30 THEN 0.9
        WHEN total_pedidos >= 5 AND dias_sem_comprar <= 60 THEN 0.7
        WHEN total_pedidos >= 1 AND dias_sem_comprar <= 90 THEN 0.5
        ELSE 0.2
    END as probabilidade_compra
FROM user_behavior
ORDER BY probabilidade_compra DESC;
```

## Conclusão

Os exemplos demonstram como cada banco de dados é otimizado para diferentes tipos de operações:

- **MongoDB:** Excelente para dados não estruturados, agregações complexas e análises de comportamento
- **PostgreSQL:** Ideal para consultas analíticas, relacionamentos complexos e integridade transacional

Esta combinação permite uma manipulação eficiente dos dados necessários para análise preditiva, aproveitando as características específicas de cada tecnologia.
