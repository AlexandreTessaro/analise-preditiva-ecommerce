# a) Conceitos e Tipos de Análise de Dados

## Definição de Análise de Dados

Análise de dados é o processo de inspeção, limpeza, transformação e modelagem de dados com o objetivo de descobrir informações úteis, sugerir conclusões e apoiar a tomada de decisões.

## Tipos de Análise de Dados

### 1. Análise Descritiva (What happened?)
**Conceito:** Foca em descrever o que aconteceu no passado, resumindo dados históricos para identificar padrões e tendências.

**Exemplos:**
- Relatórios de vendas mensais de uma loja online
- Dashboard com métricas de usuários ativos
- Estatísticas de produtos mais vendidos
- Análise de sazonalidade nas vendas

**Características:**
- Utiliza técnicas de agregação e sumarização
- Gera insights sobre o estado atual
- Base para outros tipos de análise

### 2. Análise Diagnóstica (Why did it happen?)
**Conceito:** Investiga as causas raiz dos eventos identificados na análise descritiva, buscando entender por que algo aconteceu.

**Exemplos:**
- Investigar por que as vendas caíram em determinado período
- Analisar fatores que influenciam o abandono de carrinho
- Identificar causas de churn de clientes
- Correlacionar campanhas de marketing com aumento de vendas

**Características:**
- Utiliza técnicas de correlação e causalidade
- Requer dados detalhados e contexto
- Fundamental para entender problemas

### 3. Análise Preditiva (What will happen?)
**Conceito:** Utiliza dados históricos e técnicas estatísticas para prever eventos futuros ou tendências.

**Exemplos:**
- Prever demanda de produtos para gestão de estoque
- Predizer probabilidade de churn de clientes
- Prever vendas para planejamento orçamentário
- Classificar leads em hot/warm/cold

**Características:**
- Utiliza algoritmos de machine learning
- Requer dados históricos de qualidade
- Foco em precisão das previsões

### 4. Análise Prescritiva (What should we do?)
**Conceito:** Recomenda ações específicas para otimizar resultados futuros, combinando análise preditiva com regras de negócio.

**Exemplos:**
- Recomendar produtos para usuários específicos
- Sugerir preços dinâmicos para maximizar receita
- Otimizar rotas de entrega
- Prescrever tratamentos médicos personalizados

**Características:**
- Combina predição com otimização
- Requer modelos complexos
- Foco em ação e impacto

## Hierarquia dos Tipos de Análise

```
Análise Descritiva (Base)
    ↓
Análise Diagnóstica (Entendimento)
    ↓
Análise Preditiva (Previsão)
    ↓
Análise Prescritiva (Ação)
```

## Técnicas Utilizadas por Tipo

### Análise Descritiva
- Agregações (SUM, AVG, COUNT)
- Visualizações (gráficos, dashboards)
- Estatísticas descritivas
- Segmentação

### Análise Diagnóstica
- Análise de correlação
- Análise de regressão
- Drill-down
- Análise de coorte

### Análise Preditiva
- Regressão linear/logística
- Árvores de decisão
- Redes neurais
- Algoritmos de ensemble

### Análise Prescritiva
- Otimização linear
- Algoritmos genéticos
- Simulação Monte Carlo
- Sistemas de recomendação

## Importância para Análise Preditiva

A análise preditiva é fundamental para:
- **Tomada de decisão proativa:** Antecipar problemas e oportunidades
- **Otimização de recursos:** Alocar recursos de forma eficiente
- **Personalização:** Oferecer experiências customizadas
- **Gestão de risco:** Identificar e mitigar riscos futuros

## Conclusão

Cada tipo de análise tem seu papel específico no processo de descoberta de insights. A análise preditiva, foco desta disciplina, depende da qualidade das análises descritiva e diagnóstica para gerar previsões precisas e úteis para a tomada de decisões estratégicas.
