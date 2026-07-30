# 🚀 Simulação de Pipeline MLOps

Este projeto é uma simulação didática de uma **pipeline de MLOps (Machine Learning Operations)** desenvolvida em Python. Seu objetivo é demonstrar, de forma simples, como funciona o ciclo de vida de um projeto de Machine Learning e como a qualidade dos dados influencia diretamente o desempenho do modelo.

A aplicação utiliza um arquivo **`config.json`** para controlar o comportamento da pipeline, permitindo ativar ou desativar a limpeza dos dados e configurar parâmetros que influenciam a acurácia simulada do modelo.

## Etapas da Pipeline

### 1. Ingestão de Dados

A primeira etapa simula a coleta de dados de clientes.

Cada registro possui:

* ID
* Idade
* Renda

Alguns registros contêm valores `None`, representando dados incompletos ou corrompidos, situação comum em bases reais.

---

###  2. Engenharia de Dados (ETL)

Nesta etapa, a aplicação consulta o arquivo **`config.json`** para verificar se a limpeza de dados está habilitada.

**Se `limpar_dados_nulos` for `true`:**

* Registros com idade ou renda ausentes são removidos.
* Apenas dados válidos seguem para o treinamento.

**Se `false`:**

* Os registros incompletos permanecem na base.
* O sistema exibe um alerta informando que dados corrompidos seguirão para o modelo.

Essa etapa demonstra a importância da qualidade dos dados em uma pipeline de Machine Learning.

---

### 3. Treinamento do Modelo

O treinamento é uma simulação e utiliza as configurações definidas em **`config.json`**.

Durante essa etapa:

* É exibida a porcentagem de dados utilizada para treinamento (`tamanho_treino_porcentagens`).
* O modelo gera uma acurácia simulada.

O comportamento varia conforme a qualidade dos dados:

**Dados sem limpeza**

* A acurácia é gerada aleatoriamente entre **40% e 55%**, simulando um modelo prejudicado por dados inconsistentes.

**Dados limpos**

* A acurácia é calculada utilizando:

  * a porcentagem de treinamento (`tamanho_treino_porcentagens`);
  * o fator de qualidade do modelo (`fator_qualidade_modelo`).

O resultado é limitado a **98%** como valor máximo.

---

### 4. MLOps e Monitoramento

Após o treinamento, o sistema simula uma etapa de monitoramento registrando informações do experimento no terminal.

São exibidos:

* Status dos dados (Limpos ou Sujos);
* Acurácia final obtida.

Em seguida, ocorre uma validação automática do modelo:

* ✅ **Acurácia maior ou igual a 75%:** modelo aprovado para produção.
* ❌ **Acurácia menor que 75%:** modelo reprovado, indicando necessidade de ajustes.

Essa etapa representa uma prática comum em pipelines de MLOps, onde modelos só são promovidos para produção após atenderem critérios mínimos de desempenho.

---

## Arquivo de Configuração

O comportamento da pipeline é controlado pelo arquivo **`config.json`**, que permite configurar:

* Nome da aluna exibido na execução;
* Ativação da limpeza de dados nulos;
* Porcentagem dos dados utilizada no treinamento;
* Fator de qualidade do modelo.

---

## Objetivo Educacional

Este projeto foi desenvolvido para auxiliar estudantes a compreender conceitos fundamentais de MLOps, como:

* ingestão de dados;
* engenharia de dados (ETL);
* preparação de dados para Machine Learning;
* treinamento de modelos;
* monitoramento de métricas;
* validação antes da implantação em produção.

## Conceito Principal

Este projeto reforça um dos princípios mais importantes da Ciência de Dados:

> **Garbage In, Garbage Out (GIGO)**

Quando dados de baixa qualidade são utilizados no treinamento, o desempenho do modelo tende a ser inferior. Em contrapartida, uma etapa adequada de limpeza e validação contribui para resultados mais confiáveis e para decisões mais seguras antes da implantação em produção.
