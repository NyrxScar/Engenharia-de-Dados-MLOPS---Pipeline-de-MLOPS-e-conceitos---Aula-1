import json
import random
import time

def carregar_configuração():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def simular_pipeline():
    config = carregar_configuração()
    print("\n +"=="*50")
    print(f"Simulador de Pipeline MLOps - Aluno: {config.get('nome_aluna')}")
    print(" +"=="*50")
    time.sleep(1)

    # Etapa 1 - Ingestão de Dados

print("\n Ingestão de Dados")
dados_brutos = [
    {"id": 1, "idade": 25, "renda": 3500},
    {"id": 2, "idade": None, "renda": 4200},
    {"id": 3, "idade": 45, "renda": 8900},
    {"id": 4, "idade": 19, "renda": None},
    {"id": 5, "idade": 31, "renda": 5100}
]
print(f"Recebidos {len(dados_brutos)} registros da fonte.")

# Etapa 2 - Engenharia de Dados (ETL)

print("\n Engenharia de Dados(ETL)")
time.sleep(1)
if config["limpar_dados_nulos"]:
    dados_limpos = [
        d
        for d in dados_brutos
        if d["idade"] is not None and d["renda"] is not None
    ]
    removidos = len(dados_brutos) - len(dados_limpos)
    print(f"Filtro Ativado {removidos} registros com Erro foram REMOVIDOS.")
else:
    dados_limpos = dados_brutos
    print(
        "Alerta: Filtro de dados nulos está DESATIVADO. Registros corrompidos passaram para o modelo."
    )

print(f"Base pronta para treino com {len(dados_limpos)} registros válidos.")

# Etapa 3 - Machine Learning

print("\n 3. Treinamento do Modelo (ML)")
time.sleep(1)
pct_treino = config["tamanho_treino_porcentagem"]
print(f"Usando {pct_treino}% dos dados para treinar o modelo.")