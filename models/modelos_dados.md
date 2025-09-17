# d) Modelos de Dados para Instanciação

## Modelo MongoDB (NoSQL) - Documentos Flexíveis

### 1. Coleção: produtos
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "produto_id": "P001",
  "nome": "Smartphone Galaxy S24",
  "categoria": "Eletrônicos > Smartphones",
  "marca": "Samsung",
  "preco": 2999.99,
  "moeda": "BRL",
  "descricao": "Smartphone com tela de 6.2 polegadas, 128GB de armazenamento",
  "caracteristicas": {
    "tela": "6.2 polegadas",
    "resolucao": "2340x1080",
    "processador": "Snapdragon 8 Gen 3",
    "ram": "8GB",
    "armazenamento": "128GB",
    "camera_principal": "50MP",
    "camera_frontal": "12MP",
    "bateria": "4000mAh",
    "sistema_operacional": "Android 14"
  },
  "imagens": [
    "https://example.com/galaxy-s24-1.jpg",
    "https://example.com/galaxy-s24-2.jpg"
  ],
  "tags": ["smartphone", "android", "samsung", "premium"],
  "avaliacao_media": 4.5,
  "total_avaliacoes": 1250,
  "estoque": 45,
  "ativo": true,
  "data_criacao": ISODate("2024-01-15T10:30:00Z"),
  "data_atualizacao": ISODate("2024-01-20T14:22:00Z")
}
```

### 2. Coleção: usuarios_comportamento
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "usuario_id": "U001",
  "sessao_id": "S001",
  "timestamp": ISODate("2024-01-15T10:30:00Z"),
  "eventos": [
    {
      "tipo": "page_view",
      "produto_id": "P001",
      "tempo_pagina": 45,
      "timestamp": ISODate("2024-01-15T10:30:00Z")
    },
    {
      "tipo": "click",
      "elemento": "add_to_cart",
      "produto_id": "P001",
      "timestamp": ISODate("2024-01-15T10:30:45Z")
    },
    {
      "tipo": "search",
      "termo": "smartphone samsung",
      "resultados": 15,
      "timestamp": ISODate("2024-01-15T10:25:00Z")
    }
  ],
  "pagina_atual": "/produto/P001",
  "referrer": "https://google.com/search?q=samsung+galaxy",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "ip_address": "192.168.1.100",
  "localizacao": {
    "pais": "Brasil",
    "estado": "São Paulo",
    "cidade": "São Paulo"
  }
}
```

### 3. Coleção: recomendacoes
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "usuario_id": "U001",
  "algoritmo": "collaborative_filtering",
  "versao": "v2.1",
  "recomendacoes": [
    {
      "produto_id": "P002",
      "score": 0.95,
      "motivo": "usuarios_similares",
      "timestamp": ISODate("2024-01-15T10:30:00Z")
    },
    {
      "produto_id": "P003",
      "score": 0.87,
      "motivo": "produtos_similares",
      "timestamp": ISODate("2024-01-15T10:30:00Z")
    },
    {
      "produto_id": "P004",
      "score": 0.82,
      "motivo": "categoria_preferida",
      "timestamp": ISODate("2024-01-15T10:30:00Z")
    }
  ],
  "contexto": {
    "pagina": "home",
    "categoria_filtro": "eletrônicos",
    "preco_maximo": 5000.00
  },
  "data_geracao": ISODate("2024-01-15T10:30:00Z"),
  "valido_ate": ISODate("2024-01-15T12:30:00Z")
}
```

### 4. Coleção: reviews
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439014"),
  "review_id": "R001",
  "produto_id": "P001",
  "usuario_id": "U001",
  "rating": 5,
  "titulo": "Excelente smartphone!",
  "comentario": "Produto de alta qualidade, entrega rápida e atendimento excelente. Recomendo!",
  "aspectos": {
    "qualidade": 5,
    "preco": 4,
    "entrega": 5,
    "atendimento": 5
  },
  "util": {
    "sim": 15,
    "nao": 2
  },
  "verificado": true,
  "data_compra": ISODate("2024-01-10T08:15:00Z"),
  "data_review": ISODate("2024-01-15T16:45:00Z"),
  "moderado": false
}
```

## Modelo PostgreSQL (Relacional) - Estrutura Normalizada

### 1. Tabela: usuarios
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255),
    data_nascimento DATE,
    genero VARCHAR(10),
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    endereco JSONB,
    data_cadastro TIMESTAMP DEFAULT NOW(),
    ultimo_login TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    segmento VARCHAR(50),
    valor_total_compras DECIMAL(12,2) DEFAULT 0.00
);

-- Índices para performance
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_usuario_id ON usuarios(usuario_id);
CREATE INDEX idx_usuarios_segmento ON usuarios(segmento);
```

### 2. Tabela: categorias
```sql
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    categoria_id VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria_pai_id INTEGER REFERENCES categorias(id),
    nivel INTEGER NOT NULL DEFAULT 1,
    ordem INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT NOW()
);

-- Índices hierárquicos
CREATE INDEX idx_categorias_pai ON categorias(categoria_pai_id);
CREATE INDEX idx_categorias_nivel ON categorias(nivel);
```

### 3. Tabela: produtos_relacional
```sql
CREATE TABLE produtos_relacional (
    id SERIAL PRIMARY KEY,
    produto_id VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(id),
    marca VARCHAR(100),
    preco DECIMAL(10,2) NOT NULL,
    preco_original DECIMAL(10,2),
    moeda VARCHAR(3) DEFAULT 'BRL',
    descricao TEXT,
    descricao_curta VARCHAR(500),
    sku VARCHAR(100) UNIQUE,
    peso DECIMAL(8,3),
    dimensoes JSONB, -- {largura, altura, profundidade}
    estoque INTEGER DEFAULT 0,
    estoque_minimo INTEGER DEFAULT 5,
    ativo BOOLEAN DEFAULT TRUE,
    destaque BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT NOW(),
    data_atualizacao TIMESTAMP DEFAULT NOW()
);

-- Índices para consultas frequentes
CREATE INDEX idx_produtos_categoria ON produtos_relacional(categoria_id);
CREATE INDEX idx_produtos_marca ON produtos_relacional(marca);
CREATE INDEX idx_produtos_preco ON produtos_relacional(preco);
CREATE INDEX idx_produtos_ativo ON produtos_relacional(ativo);
```

### 4. Tabela: pedidos
```sql
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    pedido_id VARCHAR(50) UNIQUE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pendente',
    valor_total DECIMAL(12,2) NOT NULL,
    valor_desconto DECIMAL(12,2) DEFAULT 0.00,
    valor_frete DECIMAL(10,2) DEFAULT 0.00,
    metodo_pagamento VARCHAR(50),
    endereco_entrega JSONB,
    observacoes TEXT,
    data_pedido TIMESTAMP DEFAULT NOW(),
    data_pagamento TIMESTAMP,
    data_entrega TIMESTAMP,
    data_cancelamento TIMESTAMP,
    motivo_cancelamento TEXT
);

-- Índices para relatórios
CREATE INDEX idx_pedidos_usuario ON pedidos(usuario_id);
CREATE INDEX idx_pedidos_status ON pedidos(status);
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);
CREATE INDEX idx_pedidos_valor ON pedidos(valor_total);
```

### 5. Tabela: itens_pedido
```sql
CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER REFERENCES pedidos(id),
    produto_id VARCHAR(50) NOT NULL,
    nome_produto VARCHAR(255) NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total DECIMAL(12,2) NOT NULL,
    desconto DECIMAL(10,2) DEFAULT 0.00
);

-- Índices para análise de vendas
CREATE INDEX idx_itens_pedido_pedido ON itens_pedido(pedido_id);
CREATE INDEX idx_itens_pedido_produto ON itens_pedido(produto_id);
```

### 6. Tabela: carrinho_compras
```sql
CREATE TABLE carrinho_compras (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    produto_id VARCHAR(50) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    data_adicao TIMESTAMP DEFAULT NOW(),
    data_atualizacao TIMESTAMP DEFAULT NOW(),
    UNIQUE(usuario_id, produto_id)
);

-- Índices para performance
CREATE INDEX idx_carrinho_usuario ON carrinho_compras(usuario_id);
CREATE INDEX idx_carrinho_produto ON carrinho_compras(produto_id);
```

## Relacionamentos e Integridade

### Chaves Estrangeiras
```sql
-- Relacionamentos principais
ALTER TABLE produtos_relacional 
ADD CONSTRAINT fk_produtos_categoria 
FOREIGN KEY (categoria_id) REFERENCES categorias(id);

ALTER TABLE pedidos 
ADD CONSTRAINT fk_pedidos_usuario 
FOREIGN KEY (usuario_id) REFERENCES usuarios(id);

ALTER TABLE itens_pedido 
ADD CONSTRAINT fk_itens_pedido 
FOREIGN KEY (pedido_id) REFERENCES pedidos(id);

ALTER TABLE carrinho_compras 
ADD CONSTRAINT fk_carrinho_usuario 
FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
```

### Triggers para Auditoria
```sql
-- Trigger para atualizar data_atualizacao
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_produtos_updated_at 
    BEFORE UPDATE ON produtos_relacional 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Índices Compostos para Performance

```sql
-- Índices compostos para consultas complexas
CREATE INDEX idx_pedidos_usuario_data ON pedidos(usuario_id, data_pedido);
CREATE INDEX idx_produtos_categoria_ativo ON produtos_relacional(categoria_id, ativo);
CREATE INDEX idx_itens_pedido_produto_quantidade ON itens_pedido(produto_id, quantidade);
```

## Views para Análise

```sql
-- View para análise de vendas por produto
CREATE VIEW v_vendas_produto AS
SELECT 
    p.produto_id,
    p.nome,
    p.categoria_id,
    c.nome as categoria_nome,
    COUNT(ip.id) as total_vendas,
    SUM(ip.quantidade) as quantidade_vendida,
    SUM(ip.valor_total) as receita_total,
    AVG(ip.preco_unitario) as preco_medio
FROM produtos_relacional p
LEFT JOIN itens_pedido ip ON p.produto_id = ip.produto_id
LEFT JOIN categorias c ON p.categoria_id = c.id
GROUP BY p.produto_id, p.nome, p.categoria_id, c.nome;

-- View para análise de usuários
CREATE VIEW v_analise_usuarios AS
SELECT 
    u.usuario_id,
    u.nome,
    u.email,
    u.segmento,
    COUNT(p.id) as total_pedidos,
    SUM(p.valor_total) as valor_total_compras,
    AVG(p.valor_total) as ticket_medio,
    MAX(p.data_pedido) as ultima_compra
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE p.status = 'concluido'
GROUP BY u.usuario_id, u.nome, u.email, u.segmento;
```

## Conclusão

Os modelos apresentados demonstram como a arquitetura híbrida aproveita as características de cada banco:

- **MongoDB:** Flexibilidade para dados não estruturados, comportamento de usuários e recomendações
- **PostgreSQL:** Integridade transacional, relacionamentos complexos e análises estruturadas

Esta estrutura suporta eficientemente o pipeline de análise preditiva, permitindo tanto a flexibilidade necessária para dados dinâmicos quanto a consistência requerida para operações críticas do negócio.
