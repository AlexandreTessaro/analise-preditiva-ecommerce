#!/usr/bin/env python3
"""
Script Principal - Análise Preditiva E-commerce
Executa toda a demonstração do sistema de recomendação
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header():
    """Imprimir cabeçalho"""
    print("=" * 80)
    print("🎯 SISTEMA DE RECOMENDAÇÃO E-COMMERCE - ANÁLISE PREDITIVA")
    print("=" * 80)
    print("📅 Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("👨‍💻 Desenvolvido para: Disciplina de Análise Preditiva")
    print("🏫 Curso: Engenharia de Software")
    print("👨‍🏫 Professor: Luiz C. Camargo, PhD")
    print("=" * 80)

def check_dependencies():
    """Verificar dependências"""
    print("\n🔍 VERIFICANDO DEPENDÊNCIAS...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Verificar bibliotecas
    required_libs = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'sklearn', 'pymongo'
    ]
    
    missing_libs = []
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"✅ {lib}")
        except ImportError:
            print(f"❌ {lib}")
            missing_libs.append(lib)
    
    if missing_libs:
        print(f"\n⚠️ Bibliotecas faltando: {', '.join(missing_libs)}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    return True

def check_mongodb():
    """Verificar MongoDB Atlas"""
    print("\n🗄️ VERIFICANDO MONGODB ATLAS...")
    
    try:
        from pymongo import MongoClient
        
        # URI do MongoDB Atlas
        MONGODB_URI = "mongodb+srv://alexandretassaro_db_user:rMJmQ6bzbbKDaQb3@cluster0.f7g7lad.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        client = MongoClient(MONGODB_URI)
        db = client['ecommerce_demo']
        
        # Testar conexão
        db.command('ping')
        print("✅ MongoDB Atlas conectado")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Atlas: {e}")
        return False

def run_demo():
    """Executar demonstração"""
    print("\n🚀 EXECUTANDO DEMONSTRAÇÃO...")
    print("=" * 50)
    
    try:
        # Executar demo MongoDB Atlas
        result = subprocess.run([sys.executable, "demo_mongodb_simples.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Demonstração executada com sucesso!")
            print("\n📊 Resultados:")
            print(result.stdout)
        else:
            print("❌ Erro na demonstração:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout na execução da demonstração")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar demonstração: {e}")
        return False
    
    return True

def show_results():
    """Mostrar resultados"""
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print("📊 Análise preditiva implementada com MongoDB Atlas")
    print("🎯 Dados reais inseridos e analisados")
    print("📈 Dashboard visual criado")
    print("🔧 Operações CRUD demonstradas")
    print("\n📚 Este projeto demonstra:")
    print("   • Tipos de análise de dados (Descritiva, Diagnóstica, Preditiva, Prescritiva)")
    print("   • Banco NoSQL MongoDB Atlas em produção")
    print("   • Modelos de dados flexíveis e escaláveis")
    print("   • Manipulação de dados com CRUD e agregações")
    print("   • Ambiente Data Lakehouse")
    print("   • Sistema de recomendações com ML")
    print("\n🎓 Avaliação N1 - Análise Preditiva")
    print("   • Domínio: Sistema de Recomendação E-commerce")
    print("   • Tecnologias: MongoDB Atlas, Python, Scikit-learn")
    print("   • Pontuação: 4,0 pontos")
    print("=" * 80)

def main():
    """Função principal"""
    print_header()
    
    # Verificar dependências
    if not check_dependencies():
        print("\n❌ Dependências não atendidas. Instale as bibliotecas necessárias.")
        return False
    
    # Verificar MongoDB
    if not check_mongodb():
        print("\n❌ MongoDB Atlas não está disponível.")
        print("💡 Verifique sua conexão com a internet e as credenciais.")
        return False
    
    print("\n✅ Todas as verificações passaram!")
    print("🚀 Iniciando demonstração...")
    
    # Executar demonstração
    if run_demo():
        show_results()
        return True
    else:
        print("\n❌ Falha na demonstração.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)