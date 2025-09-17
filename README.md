# Avaliação N1 - Análise Preditiva
**Disciplina:** Análise Preditiva  
**Curso:** Engenharia de Software  
**Professor:** Luiz C. Camargo, PhD  
**Data:** 22/09/2025  

## Objetivo
Esta avaliação discute conceitos de análise de dados, exemplifica a utilização de modelos NoSQL como repositório para pipeline de Análise Preditiva, e apresenta justificativas para escolhas tecnológicas.

## Estrutura do Projeto

### Domínio Escolhido: **Sistema de Recomendação de Produtos E-commerce**

Este projeto utiliza um sistema de recomendação de produtos para e-commerce como domínio de problema, aplicando técnicas de classificação e predição para melhorar a experiência do usuário e aumentar vendas.

### Tecnologias Utilizadas
- **Banco NoSQL:** MongoDB (documentos flexíveis para dados de produtos e usuários)
- **Banco Relacional:** PostgreSQL (dados transacionais e relacionamentos)
- **Ambiente de Dados:** Data Lakehouse (combinação de Data Lake e Data Warehouse)
- **Linguagem:** Python com bibliotecas de análise de dados

## Atividades Desenvolvidas

### a) Tipos de Análise de Dados (0,5)
- Análise Descritiva
- Análise Diagnóstica  
- Análise Preditiva
- Análise Prescritiva

### b) Domínio de Problema (1,0)
Sistema de recomendação de produtos para e-commerce com foco em:
- Classificação de preferências de usuários
- Predição de probabilidade de compra
- Recomendação personalizada de produtos

### c) Justificativa dos Modelos de Banco (0,5)
- MongoDB: Flexibilidade para dados não estruturados (produtos, reviews, comportamento)
- PostgreSQL: Integridade para dados transacionais e relacionamentos

### d) Modelo de Dados (0,5)
Esquemas para ambos os bancos de dados

### e) Manipulação de Dados (0,5)
Exemplos práticos de CRUD e consultas

### f) Ambiente de Dados (1,0)
Data Lakehouse como solução híbrida para dados brutos e processados

## Como Executar

1. Instalar dependências: `pip install -r requirements.txt`
2. Configurar bancos de dados (MongoDB e PostgreSQL)
3. Executar scripts de exemplo: `python scripts/exemplos_manipulacao.py`
4. Visualizar análises: `python scripts/analise_dados.py`

## Arquivos Principais
- `docs/conceitos_analise.md` - Conceitos e tipos de análise
- `docs/dominio_problema.md` - Descrição detalhada do domínio
- `docs/justificativa_bancos.md` - Justificativa das escolhas
- `models/` - Modelos de dados
- `scripts/` - Exemplos práticos
- `data/` - Dados de exemplo
