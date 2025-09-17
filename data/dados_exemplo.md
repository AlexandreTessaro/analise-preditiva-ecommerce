# Dados de Exemplo para o Projeto

## Produtos de Exemplo (produtos_sample.json)
```json
[
  {
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
    "data_criacao": "2024-01-15T10:30:00Z",
    "data_atualizacao": "2024-01-20T14:22:00Z"
  },
  {
    "produto_id": "P002",
    "nome": "iPhone 15 Pro",
    "categoria": "Eletrônicos > Smartphones",
    "marca": "Apple",
    "preco": 8999.99,
    "moeda": "BRL",
    "descricao": "Smartphone premium com tela de 6.1 polegadas",
    "caracteristicas": {
      "tela": "6.1 polegadas",
      "resolucao": "2556x1179",
      "processador": "A17 Pro",
      "ram": "8GB",
      "armazenamento": "128GB",
      "camera_principal": "48MP",
      "camera_frontal": "12MP",
      "bateria": "3274mAh",
      "sistema_operacional": "iOS 17"
    },
    "imagens": [
      "https://example.com/iphone-15-pro-1.jpg",
      "https://example.com/iphone-15-pro-2.jpg"
    ],
    "tags": ["smartphone", "ios", "apple", "premium"],
    "avaliacao_media": 4.7,
    "total_avaliacoes": 890,
    "estoque": 30,
    "ativo": true,
    "data_criacao": "2024-01-10T08:15:00Z",
    "data_atualizacao": "2024-01-18T16:45:00Z"
  },
  {
    "produto_id": "P003",
    "nome": "Notebook Dell XPS 13",
    "categoria": "Eletrônicos > Notebooks",
    "marca": "Dell",
    "preco": 5999.99,
    "moeda": "BRL",
    "descricao": "Notebook ultrabook com tela de 13.4 polegadas",
    "caracteristicas": {
      "tela": "13.4 polegadas",
      "resolucao": "1920x1200",
      "processador": "Intel Core i7",
      "ram": "16GB",
      "armazenamento": "512GB SSD",
      "placa_video": "Intel Iris Xe",
      "bateria": "52Wh",
      "sistema_operacional": "Windows 11"
    },
    "imagens": [
      "https://example.com/dell-xps-13-1.jpg",
      "https://example.com/dell-xps-13-2.jpg"
    ],
    "tags": ["notebook", "windows", "dell", "ultrabook"],
    "avaliacao_media": 4.3,
    "total_avaliacoes": 567,
    "estoque": 20,
    "ativo": true,
    "data_criacao": "2024-01-12T14:20:00Z",
    "data_atualizacao": "2024-01-19T11:30:00Z"
  }
]
```

## Usuários de Exemplo (usuarios_sample.json)
```json
[
  {
    "usuario_id": "U001",
    "email": "joao.silva@email.com",
    "nome": "João",
    "sobrenome": "Silva",
    "data_nascimento": "1990-05-15",
    "genero": "M",
    "telefone": "(11) 99999-9999",
    "cpf": "123.456.789-00",
    "endereco": {
      "rua": "Rua das Flores, 123",
      "cidade": "São Paulo",
      "estado": "SP",
      "cep": "01234-567",
      "pais": "Brasil"
    },
    "data_cadastro": "2023-06-15T10:30:00Z",
    "ultimo_login": "2024-01-15T14:22:00Z",
    "ativo": true,
    "segmento": "high_value",
    "valor_total_compras": 15750.50
  },
  {
    "usuario_id": "U002",
    "email": "maria.santos@email.com",
    "nome": "Maria",
    "sobrenome": "Santos",
    "data_nascimento": "1985-08-22",
    "genero": "F",
    "telefone": "(11) 88888-8888",
    "cpf": "987.654.321-00",
    "endereco": {
      "rua": "Avenida Paulista, 1000",
      "cidade": "São Paulo",
      "estado": "SP",
      "cep": "01310-100",
      "pais": "Brasil"
    },
    "data_cadastro": "2023-08-20T16:45:00Z",
    "ultimo_login": "2024-01-14T09:15:00Z",
    "ativo": true,
    "segmento": "medium_value",
    "valor_total_compras": 3250.75
  },
  {
    "usuario_id": "U003",
    "email": "pedro.oliveira@email.com",
    "nome": "Pedro",
    "sobrenome": "Oliveira",
    "data_nascimento": "1995-12-03",
    "genero": "M",
    "telefone": "(11) 77777-7777",
    "cpf": "456.789.123-00",
    "endereco": {
      "rua": "Rua Augusta, 500",
      "cidade": "São Paulo",
      "estado": "SP",
      "cep": "01305-000",
      "pais": "Brasil"
    },
    "data_cadastro": "2024-01-05T12:00:00Z",
    "ultimo_login": "2024-01-15T18:30:00Z",
    "ativo": true,
    "segmento": "new_user",
    "valor_total_compras": 0.00
  }
]
```

## Comportamento de Exemplo (comportamento_sample.json)
```json
[
  {
    "usuario_id": "U001",
    "sessao_id": "S001",
    "timestamp": "2024-01-15T10:30:00Z",
    "eventos": [
      {
        "tipo": "page_view",
        "produto_id": "P001",
        "tempo_pagina": 45,
        "timestamp": "2024-01-15T10:30:00Z"
      },
      {
        "tipo": "click",
        "elemento": "add_to_cart",
        "produto_id": "P001",
        "timestamp": "2024-01-15T10:30:45Z"
      },
      {
        "tipo": "search",
        "termo": "smartphone samsung",
        "resultados": 15,
        "timestamp": "2024-01-15T10:25:00Z"
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
  },
  {
    "usuario_id": "U002",
    "sessao_id": "S002",
    "timestamp": "2024-01-15T14:15:00Z",
    "eventos": [
      {
        "tipo": "page_view",
        "produto_id": "P002",
        "tempo_pagina": 120,
        "timestamp": "2024-01-15T14:15:00Z"
      },
      {
        "tipo": "page_view",
        "produto_id": "P003",
        "tempo_pagina": 90,
        "timestamp": "2024-01-15T14:17:00Z"
      },
      {
        "tipo": "click",
        "elemento": "add_to_cart",
        "produto_id": "P002",
        "timestamp": "2024-01-15T14:17:30Z"
      }
    ],
    "pagina_atual": "/produto/P002",
    "referrer": "https://example.com/categoria/smartphones",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "ip_address": "192.168.1.101",
    "localizacao": {
      "pais": "Brasil",
      "estado": "São Paulo",
      "cidade": "São Paulo"
    }
  }
]
```

## Pedidos de Exemplo (pedidos_sample.csv)
```csv
pedido_id,usuario_id,status,valor_total,valor_desconto,valor_frete,metodo_pagamento,data_pedido,data_pagamento,data_entrega
PED001,U001,concluido,2999.99,0.00,15.00,cartao_credito,2024-01-10T08:15:00Z,2024-01-10T08:16:00Z,2024-01-12T14:30:00Z
PED002,U001,concluido,5999.99,300.00,0.00,pix,2024-01-12T16:45:00Z,2024-01-12T16:46:00Z,2024-01-15T10:20:00Z
PED003,U002,pendente,8999.99,0.00,25.00,cartao_credito,2024-01-15T14:30:00Z,,,
PED004,U001,concluido,1299.99,50.00,10.00,boleto,2024-01-08T11:20:00Z,2024-01-09T09:15:00Z,2024-01-11T16:45:00Z
PED005,U002,concluido,2499.99,0.00,20.00,cartao_debito,2024-01-13T19:30:00Z,2024-01-13T19:31:00Z,2024-01-16T11:15:00Z
```

## Reviews de Exemplo (reviews_sample.json)
```json
[
  {
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
    "data_compra": "2024-01-10T08:15:00Z",
    "data_review": "2024-01-15T16:45:00Z",
    "moderado": false
  },
  {
    "review_id": "R002",
    "produto_id": "P002",
    "usuario_id": "U002",
    "rating": 4,
    "titulo": "Bom produto, mas caro",
    "comentario": "O iPhone é excelente, mas o preço está muito alto. Funcionalidades são ótimas.",
    "aspectos": {
      "qualidade": 5,
      "preco": 2,
      "entrega": 4,
      "atendimento": 4
    },
    "util": {
      "sim": 8,
      "nao": 1
    },
    "verificado": true,
    "data_compra": "2024-01-13T19:30:00Z",
    "data_review": "2024-01-16T12:20:00Z",
    "moderado": false
  }
]
```

## Recomendações de Exemplo (recomendacoes_sample.json)
```json
[
  {
    "usuario_id": "U001",
    "algoritmo": "collaborative_filtering",
    "versao": "v2.1",
    "recomendacoes": [
      {
        "produto_id": "P002",
        "score": 0.95,
        "motivo": "usuarios_similares",
        "timestamp": "2024-01-15T10:30:00Z"
      },
      {
        "produto_id": "P003",
        "score": 0.87,
        "motivo": "produtos_similares",
        "timestamp": "2024-01-15T10:30:00Z"
      },
      {
        "produto_id": "P004",
        "score": 0.82,
        "motivo": "categoria_preferida",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ],
    "contexto": {
      "pagina": "home",
      "categoria_filtro": "eletrônicos",
      "preco_maximo": 5000.00
    },
    "data_geracao": "2024-01-15T10:30:00Z",
    "valido_ate": "2024-01-15T12:30:00Z"
  },
  {
    "usuario_id": "U002",
    "algoritmo": "content_based",
    "versao": "v2.1",
    "recomendacoes": [
      {
        "produto_id": "P001",
        "score": 0.91,
        "motivo": "produtos_similares",
        "timestamp": "2024-01-15T14:15:00Z"
      },
      {
        "produto_id": "P005",
        "score": 0.78,
        "motivo": "categoria_preferida",
        "timestamp": "2024-01-15T14:15:00Z"
      }
    ],
    "contexto": {
      "pagina": "produto",
      "produto_atual": "P002",
      "categoria_filtro": "smartphones"
    },
    "data_geracao": "2024-01-15T14:15:00Z",
    "valido_ate": "2024-01-15T16:15:00Z"
  }
]
```

## Instruções de Uso

1. **Salvar os dados:** Copie cada seção para arquivos separados na pasta `data/`
2. **Importar no MongoDB:** Use os scripts Python para importar os dados JSON
3. **Importar no PostgreSQL:** Use os scripts SQL para criar as tabelas e importar os dados CSV
4. **Executar análises:** Use os scripts de exemplo para testar as operações

Estes dados de exemplo fornecem uma base sólida para testar todas as funcionalidades do sistema de recomendação e-commerce, incluindo operações CRUD, análises preditivas e geração de recomendações.
