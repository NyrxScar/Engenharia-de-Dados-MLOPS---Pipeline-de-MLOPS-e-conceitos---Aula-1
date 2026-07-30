# 🚀 Simulação de Pipeline MLOps

Este projeto é uma simulação didática de uma **pipeline de MLOps (Machine Learning Operations)** desenvolvida em Python. O objetivo é demonstrar, de forma simples e prática, como funciona o ciclo de vida de um projeto de Machine Learning, destacando a importância da qualidade dos dados e do monitoramento antes da implantação de um modelo.

A pipeline utiliza um arquivo **`config.json`** para definir seu comportamento, permitindo configurar a limpeza de dados, parâmetros do treinamento e outras informações da simulação.

---

# Etapas da Pipeline

## 1. Ingestão de Dados

A primeira etapa simula a coleta de dados de clientes.

Cada registro contém:

* ID
* Idade
* Renda

Para representar problemas comuns encontrados em bases reais, alguns registros possuem valores `None`, simulando dados incompletos ou corrompidos.

---

## 2. Engenharia de Dados (ETL)

Nesta etapa, o sistema verifica o arquivo **`config.json`** para decidir se a limpeza de dados será realizada.

### Quando `limpar_dados_nulos` é `true`

* Registros com idade ou renda ausentes são removidos.
* Apenas dados válidos seguem para o treinamento.

### Quando `limpar_dados_nulos` é `false`

* Nenhum registro é removido.
* Dados incompletos seguem para a próxima etapa.
* O sistema exibe um alerta informando que registros corrompidos estão sendo utilizados.

Essa etapa demonstra como decisões de engenharia de dados podem influenciar a qualidade do modelo.

---

## 3. Treinamento do Modelo

O treinamento é simulado utilizando as configurações presentes no **`config.json`**.

Durante essa etapa, o sistema:

* informa a porcentagem de dados utilizada no treinamento;
* calcula uma acurácia simulada para o modelo.

O resultado depende da qualidade dos dados:

### Dados sem limpeza

A acurácia é gerada aleatoriamente entre **40% e 55%**, simulando um modelo prejudicado por dados inconsistentes.

### Dados limpos

A acurácia é calculada utilizando:

* `tamanho_treino_porcentagens`
* `fator_qualidade_modelo`

Na configuração padrão deste projeto (`70%` de treino e fator `1.2`), a acurácia obtida é **74%**.

---

## 4. MLOps e Monitoramento

Após o treinamento, a aplicação simula uma etapa de monitoramento registrando informações do experimento no terminal.

São exibidos:

* status dos dados (Limpos ou Sujos);
* acurácia final do modelo.

Em seguida, o sistema compara a acurácia obtida com um critério mínimo para aprovação:

* ✅ **Acurácia maior ou igual a 75%:** modelo aprovado para produção.
* ❌ **Acurácia menor que 75%:** modelo reprovado e necessita de ajustes.

**Na configuração padrão do projeto, a acurácia é de 74%, resultando na reprovação do modelo.** Esse comportamento foi mantido para ilustrar que, mesmo após a limpeza dos dados, o modelo ainda pode não atingir o desempenho mínimo esperado.

---

# Arquivo de Configuração

O arquivo **`config.json`** controla o comportamento da simulação.

Parâmetros disponíveis:

* `nome_aluna` → nome exibido no início da execução;
* `limpar_dados_nulos` → ativa ou desativa a limpeza dos dados;
* `tamanho_treino_porcentagens` → percentual utilizado no treinamento;
* `fator_qualidade_modelo` → influencia o cálculo da acurácia simulada.

---

# Objetivo Educacional

Este projeto foi desenvolvido para auxiliar estudantes na compreensão dos principais conceitos de MLOps, incluindo:

* ingestão de dados;
* engenharia de dados (ETL);
* preparação de dados para Machine Learning;
* treinamento de modelos;
* monitoramento de métricas;
* validação antes da implantação em produção.

---

# Conceito Principal

Este projeto reforça um princípio fundamental da Ciência de Dados:

> **Garbage In, Garbage Out (GIGO)**

A qualidade dos dados influencia diretamente o desempenho de um modelo de Machine Learning. Além disso, o projeto demonstra que a limpeza dos dados, por si só, não garante um modelo aprovado: é necessário que ele também atinja critérios mínimos de desempenho antes de ser considerado apto para produção.
