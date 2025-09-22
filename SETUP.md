# ⚙️ SETUP Detalhado - Análise Preditiva E-commerce

## 📋 Visão Geral

Este guia fornece instruções detalhadas para configurar e executar o projeto de Análise Preditiva E-commerce em diferentes sistemas operacionais.

## 🖥️ Sistemas Suportados

- ✅ **Windows 10/11**
- ✅ **Ubuntu 20.04+**
- ✅ **macOS 10.15+**
- ✅ **Docker** (opcional)

## 🛠️ Instalação por Sistema Operacional

### Windows 10/11

#### 1. Instalar Python
```powershell
# Baixar Python 3.8+ do site oficial
# https://www.python.org/downloads/

# Verificar instalação
python --version
pip --version

# Atualizar pip
python -m pip install --upgrade pip
```

#### 2. Instalar MongoDB
```powershell
# Baixar MongoDB Community Server
# https://www.mongodb.com/try/download/community

# Instalar como serviço Windows
# Durante a instalação, marque "Install MongoDB as a Service"

# Verificar se está rodando
Get-Service MongoDB

# Iniciar se necessário
Start-Service MongoDB

# Testar conexão
mongosh --version
```

#### 3. Instalar PostgreSQL
```powershell
# Baixar PostgreSQL
# https://www.postgresql.org/download/windows/

# Durante a instalação:
# - Definir senha para usuário 'postgres'
# - Porta padrão: 5432
# - Instalar pgAdmin (opcional)

# Verificar instalação
psql --version

# Criar banco de dados
createdb -U postgres ecommerce_demo
```

#### 4. Instalar Git
```powershell
# Baixar Git
# https://git-scm.com/download/win

# Verificar instalação
git --version
```

### Ubuntu 20.04+

#### 1. Atualizar Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Instalar Python
```bash
# Instalar Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Verificar instalação
python3 --version
pip3 --version

# Criar alias (opcional)
echo 'alias python=python3' >> ~/.bashrc
echo 'alias pip=pip3' >> ~/.bashrc
source ~/.bashrc
```

#### 3. Instalar MongoDB
```bash
# Importar chave pública
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Adicionar repositório
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Atualizar e instalar
sudo apt update
sudo apt install mongodb-org -y

# Iniciar e habilitar serviço
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar status
sudo systemctl status mongod

# Testar conexão
mongosh --version
```

#### 4. Instalar PostgreSQL
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Iniciar e habilitar serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar status
sudo systemctl status postgresql

# Criar banco de dados
sudo -u postgres createdb ecommerce_demo

# Verificar instalação
psql --version
```

#### 5. Instalar Git
```bash
sudo apt install git -y
git --version
```

### macOS 10.15+

#### 1. Instalar Homebrew
```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Adicionar ao PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### 2. Instalar Python
```bash
# Instalar Python
brew install python@3.9

# Verificar instalação
python3 --version
pip3 --version
```

#### 3. Instalar MongoDB
```bash
# Instalar MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Iniciar serviço
brew services start mongodb/brew/mongodb-community

# Verificar status
brew services list | grep mongodb

# Testar conexão
mongosh --version
```

#### 4. Instalar PostgreSQL
```bash
# Instalar PostgreSQL
brew install postgresql

# Iniciar serviço
brew services start postgresql

# Criar banco de dados
createdb ecommerce_demo

# Verificar instalação
psql --version
```

#### 5. Instalar Git
```bash
brew install git
git --version
```

## 🐳 Instalação com Docker (Opcional)

### 1. Instalar Docker
```bash
# Windows: Baixar Docker Desktop
# https://www.docker.com/products/docker-desktop

# Ubuntu:
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# macOS: Instalar Docker Desktop
brew install --cask docker
```

### 2. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: ecommerce_mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_DATABASE: ecommerce_demo
    volumes:
      - mongodb_data:/data/db

  postgresql:
    image: postgres:13
    container_name: ecommerce_postgresql
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ecommerce_demo
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgresql_data:/var/lib/postgresql/data

volumes:
  mongodb_data:
  postgresql_data:
```

```bash
# Executar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Parar containers
docker-compose down
```

## 🐍 Configuração do Ambiente Python

### 1. Criar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Verificar ativação
which python
# Deve mostrar o caminho do venv
```

### 2. Instalar Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de configuração
cp config.env .env

# Editar configurações (opcional)
# Windows:
notepad .env
# Linux/macOS:
nano .env
```

## 🗄️ Configuração dos Bancos de Dados

### 1. Configurar MongoDB
```bash
# Conectar ao MongoDB
mongosh

# Criar banco de dados
use ecommerce_demo

# Verificar banco
db.stats()

# Sair
exit
```

### 2. Configurar PostgreSQL
```bash
# Conectar ao PostgreSQL
psql -U postgres -d ecommerce_demo

# Verificar conexão
\conninfo

# Listar tabelas
\dt

# Sair
\q
```

### 3. Executar Setup Automático
```bash
# Executar script de configuração
python scripts/setup_databases.py

# Verificar se funcionou
python test_system.py
```

## 🧪 Testes e Verificação

### 1. Teste Completo do Sistema
```bash
# Executar testes
python test_system.py

# Deve mostrar:
# ✅ Importações
# ✅ Estrutura de arquivos
# ✅ Funcionalidades ML
# ✅ Visualizações
# ✅ Conexões BD
```

### 2. Teste Individual dos Componentes
```bash
# Testar MongoDB
python scripts/demo_mongodb.py

# Testar PostgreSQL
python scripts/demo_postgresql.py

# Testar notebook
jupyter notebook notebooks/demo_analise_preditiva.ipynb
```

### 3. Execução Completa
```bash
# Executar sistema completo
python main.py

# Deve gerar:
# - dashboard_mongodb.png
# - dashboard_postgresql.png
# - logs/app.log
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. MongoDB não conecta
```bash
# Verificar se está rodando
# Windows:
Get-Service MongoDB
# Linux:
sudo systemctl status mongod
# macOS:
brew services list | grep mongodb

# Reiniciar serviço
# Windows:
Restart-Service MongoDB
# Linux:
sudo systemctl restart mongod
# macOS:
brew services restart mongodb/brew/mongodb-community

# Verificar logs
# Windows: Event Viewer
# Linux:
sudo journalctl -u mongod
# macOS:
brew services info mongodb/brew/mongodb-community
```

#### 2. PostgreSQL não conecta
```bash
# Verificar se está rodando
# Windows: Services
# Linux:
sudo systemctl status postgresql
# macOS:
brew services list | grep postgresql

# Reiniciar serviço
# Windows: Services
# Linux:
sudo systemctl restart postgresql
# macOS:
brew services restart postgresql

# Verificar logs
# Linux:
sudo journalctl -u postgresql
# macOS:
brew services info postgresql
```

#### 3. Erro de dependências Python
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar versão do Python
python --version

# Verificar ambiente virtual
which python
which pip
```

#### 4. Erro de permissões
```bash
# Linux: Dar permissões de execução
chmod +x scripts/*.py
chmod +x main.py
chmod +x test_system.py

# Windows: Executar como administrador se necessário
```

#### 5. Erro de porta em uso
```bash
# Verificar portas em uso
# Windows:
netstat -ano | findstr :27017
netstat -ano | findstr :5432
# Linux/macOS:
lsof -i :27017
lsof -i :5432

# Parar processos se necessário
# Windows:
taskkill /PID <PID> /F
# Linux/macOS:
kill -9 <PID>
```

## 📊 Verificação Final

### Checklist de Instalação
- [ ] ✅ Python 3.8+ instalado
- [ ] ✅ MongoDB 4.4+ instalado e rodando
- [ ] ✅ PostgreSQL 12+ instalado e rodando
- [ ] ✅ Git instalado
- [ ] ✅ Ambiente virtual Python criado
- [ ] ✅ Dependências instaladas
- [ ] ✅ Bancos de dados configurados
- [ ] ✅ Testes passando
- [ ] ✅ Sistema executando

### Comandos de Verificação
```bash
# Verificar versões
python --version
mongosh --version
psql --version
git --version

# Verificar serviços
# Windows:
Get-Service MongoDB, postgresql-x64-13
# Linux:
sudo systemctl status mongod postgresql
# macOS:
brew services list | grep -E "mongodb|postgresql"

# Verificar ambiente Python
pip list | grep -E "pandas|numpy|scikit-learn|pymongo|psycopg2"

# Executar testes
python test_system.py
```

## 🚀 Próximos Passos

Após a instalação bem-sucedida:

1. **Execute o sistema:** `python main.py`
2. **Explore os notebooks:** `jupyter notebook`
3. **Consulte a documentação:** `docs/`
4. **Teste as APIs:** `python api/app.py`
5. **Visualize os dashboards:** `streamlit run dashboard/app.py`

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs:** `logs/app.log`
2. **Execute os testes:** `python test_system.py`
3. **Consulte a documentação:** `docs/`
4. **Abra uma issue no GitHub**

---

**Desenvolvido com ❤️ para a disciplina de Análise Preditiva - Engenharia de Software**