import json
import random
import time


def carregar_configuração():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def simular_pipeline():
    config = carregar_configuração()
    print("\n" + "=" * 50)
    print(f"Simulador de Pipeline MLOps - Aluna: {config.get('nome_aluna')}")
    print("=" * 50)
    time.sleep(1)

    # Etapa 1 - Ingestão de Dados
    print("\n Ingestão de Dados")
    dados_brutos = [
        {"id": 1, "idade": 25, "renda": 3500},
        {"id": 2, "idade": None, "renda": 4200},
        {"id": 3, "idade": 45, "renda": 8900},
        {"id": 4, "idade": 19, "renda": None},
        {"id": 5, "idade": 31, "renda": 5100},
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
    pct_treino = config["tamanho_treino_porcentagens"]
    print(f"Usando {pct_treino}% dos dados para treinar o modelo.")

    # Causalidade Simples para acurácia simulada
    if not config["limpar_dados_nulos"]:
        acuracia = random.randint(
            40, 55
        )  # Acurácia ruim devido aos dados sujos
        status_dados = "Sujos"
    else:
        # Acurácia melhora com mais dados do treino
        acuracia = min(
            98,
            int(
                (pct_treino * 0.8) + (config["fator_qualidade_modelo"] * 15)
            ),
        )
        status_dados = "Limpos"

    print(f"Modelo Treinando! Acurácia Obtida: {acuracia}%")

    # Etapa 4 - MLOPS & Monitoração
    print("\n 4. MLOPS & Deploy (MLOPS)")
    time.sleep(1)
    print(" Salvando registro do experimento - (Log)...")
    print(f"     |--> Status dos Dados: {status_dados}")
    print(f"     |--> Acurácia Final do Modelo: {acuracia}%")

    if acuracia >= 75:
        print(
            "\n [SISTEMA]: Acurácia alta! Modelo APROVADO para ir para produção"
        )
    else:
        print(
            "\n [SISTEMA]: Acurácia baixa! Modelo REPROVADO. Necessário ajustes."
        )

        print("=" * 50 + "\n")


if __name__ == "__main__":
    simular_pipeline()