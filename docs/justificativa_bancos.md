# c) Justificativa da Escolha dos Modelos de Banco de Dados

## Arquitetura Híbrida: MongoDB + PostgreSQL

Para o domínio de Sistema de Recomendação de Produtos E-commerce, optamos por uma **arquitetura híbrida** que combina MongoDB (NoSQL) e PostgreSQL (Relacional), aproveitando as vantagens de cada modelo para diferentes aspectos do sistema.

## Justificativa da Escolha

### Por que MongoDB (NoSQL)?

#### 1. Flexibilidade para Dados Não Estruturados
**Aplicação:** Dados de produtos, reviews, comportamento de usuários
```json
{
  "produto_id": "P001",
  "nome": "Smartphone XYZ",
  "caracteristicas": {
    "tela": "6.1 polegadas",
    "processador": "Snapdragon 888",
    "camera": {
      "principal": "108MP",
      "frontal": "32MP",
      "zoom": "10x"
    }
  },
  "reviews": [
    {
      "usuario_id": "U001",
      "rating": 5,
      "comentario": "Excelente produto!",
      "data": "2024-01-15"
    }
  ]
}
```

**Vantagens:**
- **Schema flexível:** Adapta-se a mudanças nos dados de produtos
- **Dados aninhados:** Reviews e características em estrutura natural
- **Escalabilidade horizontal:** Suporta milhões de produtos
- **Performance:** Consultas rápidas em documentos JSON

#### 2. Dados de Comportamento e Interações
**Aplicação:** Histórico de navegação, cliques, sessões
```json
{
  "sessao_id": "S001",
  "usuario_id": "U001",
  "timestamp": "2024-01-15T10:30:00Z",
  "eventos": [
    {
      "tipo": "page_view",
      "produto_id": "P001",
      "tempo_pagina": 45
    },
    {
      "tipo": "click",
      "elemento": "add_to_cart",
      "produto_id": "P001"
    }
  ]
}
```

**Vantagens:**
- **Volume alto:** Milhões de eventos diários
- **Variabilidade:** Diferentes tipos de eventos
- **Agregação:** Pipeline de agregação eficiente
- **Time-series:** Otimizado para dados temporais

#### 3. Recomendações e Scores
**Aplicação:** Scores de recomendação, matrizes de similaridade
```json
{
  "usuario_id": "U001",
  "recomendacoes": [
    {
      "produto_id": "P002",
      "score": 0.95,
      "algoritmo": "collaborative_filtering",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Vantagens:**
- **Atualização rápida:** Scores recalculados frequentemente
- **Cache natural:** Estrutura otimizada para leitura
- **Flexibilidade:** Diferentes algoritmos de recomendação

### Por que PostgreSQL (Relacional)?

#### 1. Integridade Transacional
**Aplicação:** Pedidos, pagamentos, estoque, usuários
```sql
-- Tabela de usuários com integridade referencial
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT NOW()
);

-- Tabela de pedidos com relacionamentos
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    valor_total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    data_pedido TIMESTAMP DEFAULT NOW()
);
```

**Vantagens:**
- **ACID:** Garantia de consistência transacional
- **Integridade referencial:** Relacionamentos validados
- **Auditoria:** Histórico completo de mudanças
- **Conformidade:** Atende regulamentações (LGPD, PCI-DSS)

#### 2. Relatórios e Analytics
**Aplicação:** Dashboards, KPIs, análises financeiras
```sql
-- Consulta complexa para relatório de vendas
SELECT 
    DATE_TRUNC('month', data_pedido) as mes,
    COUNT(*) as total_pedidos,
    SUM(valor_total) as receita_total,
    AVG(valor_total) as ticket_medio
FROM pedidos 
WHERE status = 'concluido'
GROUP BY DATE_TRUNC('month', data_pedido)
ORDER BY mes;
```

**Vantagens:**
- **SQL avançado:** Consultas complexas e analíticas
- **Joins eficientes:** Relacionamentos otimizados
- **Agregações:** Funções analíticas poderosas
- **Padronização:** Linguagem SQL universal

#### 3. Dados Estruturados Críticos
**Aplicação:** Catálogo de produtos, categorias, preços
```sql
-- Estrutura hierárquica de categorias
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria_pai_id INTEGER REFERENCES categorias(id),
    nivel INTEGER NOT NULL
);

-- Produtos com preços e estoque
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(id),
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE
);
```

**Vantagens:**
- **Consistência:** Dados sempre válidos
- **Normalização:** Evita redundância
- **Performance:** Índices otimizados
- **Manutenibilidade:** Schema bem definido

## Arquitetura de Integração

### Fluxo de Dados
```
[Frontend] → [API Gateway] → [Serviços de Aplicação]
                                    ↓
[MongoDB] ← [Serviço de Recomendações] → [PostgreSQL]
    ↑                                           ↓
[Dados de Comportamento]              [Dados Transacionais]
```

### Responsabilidades por Banco

#### MongoDB (NoSQL)
- **Produtos:** Catálogo com características flexíveis
- **Comportamento:** Eventos de navegação e interação
- **Recomendações:** Scores e matrizes de similaridade
- **Reviews:** Comentários e avaliações
- **Sessões:** Dados de navegação em tempo real

#### PostgreSQL (Relacional)
- **Usuários:** Dados pessoais e autenticação
- **Pedidos:** Transações e histórico de compras
- **Pagamentos:** Dados financeiros e métodos
- **Estoque:** Controle de inventário
- **Categorias:** Estrutura hierárquica de produtos

## Vantagens da Arquitetura Híbrida

### 1. Performance Otimizada
- **MongoDB:** Consultas rápidas para recomendações
- **PostgreSQL:** Relatórios analíticos eficientes
- **Cache:** Dados frequentes em MongoDB
- **Persistência:** Dados críticos em PostgreSQL

### 2. Escalabilidade
- **Horizontal:** MongoDB escala facilmente
- **Vertical:** PostgreSQL otimizado para consultas complexas
- **Distribuição:** Carga distribuída entre bancos
- **Elasticidade:** Recursos ajustáveis por demanda

### 3. Flexibilidade
- **Evolução:** Schema flexível para novos produtos
- **Integração:** APIs REST para ambos os bancos
- **Migração:** Dados podem ser movidos entre bancos
- **Manutenção:** Atualizações independentes

### 4. Confiabilidade
- **Backup:** Estratégias diferentes por banco
- **Recuperação:** Pontos de restauração específicos
- **Monitoramento:** Métricas separadas
- **Disaster Recovery:** Planos independentes

## Desafios e Mitigações

### 1. Complexidade de Integração
**Desafio:** Manter consistência entre bancos
**Mitigação:** 
- Event Sourcing para sincronização
- APIs de consistência eventual
- Monitoramento de integridade

### 2. Duplicação de Dados
**Desafio:** Dados podem existir em ambos os bancos
**Mitigação:**
- Master-slave para dados críticos
- Cache inteligente para dados frequentes
- Limpeza periódica de dados obsoletos

### 3. Curva de Aprendizado
**Desafio:** Equipe precisa conhecer ambos os bancos
**Mitigação:**
- Treinamento especializado
- Documentação detalhada
- Ferramentas de abstração (ORM/ODM)

## Conclusão

A escolha de uma arquitetura híbrida MongoDB + PostgreSQL é justificada pela natureza diversa dos dados no sistema de recomendação e-commerce. MongoDB oferece flexibilidade e performance para dados não estruturados e recomendações, enquanto PostgreSQL garante integridade e consistência para dados transacionais críticos. Esta combinação maximiza as vantagens de cada modelo, resultando em uma solução robusta, escalável e eficiente para análise preditiva.
