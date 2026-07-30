import json
import os

NOTEBOOK_PATH = r"Atividade Prática\atividade.ipynb"

resposta_1_md = """### ✅ Resposta — Questão 1: Diagnóstico

**Por que o filtro `is not None` falhou?**

O operador `is not None` verifica **apenas** se o valor é literalmente `None`. Ele **não** valida o tipo nem o conteúdo do dado.

No registro `id: 102`, o campo `"idade"` contém a string `"desconhecido"`. Como `"desconhecido" is not None` é **`True`**, o registro **passa** pelo filtro — mesmo sendo completamente inválido.

| id  | idade          | renda  | Passa no filtro atual? | Deveria passar? |
|-----|----------------|--------|------------------------|-----------------|
| 101 | 30             | 4500   | ✅ Sim                  | ✅ Sim           |
| 102 | "desconhecido" | 3200   | ✅ Sim (BUG!)           | ❌ Não           |
| 103 | 0              | -1000  | ✅ Sim (BUG!)           | ❌ Não           |
| 104 | 42             | None   | ❌ Não                  | ❌ Não           |

**Erro específico na fase de treinamento:**

Quando a biblioteca de ML (ex.: `scikit-learn`) tentar converter as features para array numérico, o campo `idade = "desconhecido"` causará:

```
ValueError: could not convert string to float: 'desconhecido'
```

Isso porque operações como `np.array(...)` com `dtype=float` ou métodos internos do estimador (ex.: `fit()`) exigem valores numéricos. Uma string não pode ser convertida, quebrando a pipeline inteiramente em produção."""

resposta_2_code = """\
dados_brutos = [
    {"id": 101, "idade": 30,            "renda": 4500},
    {"id": 102, "idade": "desconhecido","renda": 3200},
    {"id": 103, "idade": 0,             "renda": -1000},
    {"id": 104, "idade": 42,            "renda": None},
]

def is_valido(valor):
    \"\"\"
    Retorna True se:
    - o valor for numérico (int ou float), OU convertível para float
    - E for estritamente maior que zero
    Retorna False para None, strings não numéricas, zero ou negativos.
    \"\"\"
    try:
        num = float(valor)
        return num > 0
    except (TypeError, ValueError):
        return False

# ETL / Sanitização corrigida
dados_limpos = [
    d for d in dados_brutos
    if is_valido(d["idade"]) and is_valido(d["renda"])
]

# ── Relatório ──────────────────────────────────────────────
print("=" * 45)
print(f"  Registros originais  : {len(dados_brutos)}")
print(f"  Registros válidos    : {len(dados_limpos)}")
print(f"  Registros descartados: {len(dados_brutos) - len(dados_limpos)}")
print("=" * 45)
print("\\nDados aprovados no ETL:")
for d in dados_limpos:
    print(f"  {d}")

print("\\nDados rejeitados:")
rejeitados = [d for d in dados_brutos if d not in dados_limpos]
for d in rejeitados:
    motivo = []
    if not is_valido(d["idade"]):
        motivo.append(f"idade inválida ({d['idade']!r})")
    if not is_valido(d["renda"]):
        motivo.append(f"renda inválida ({d['renda']!r})")
    print(f"  id={d['id']} → {', '.join(motivo)}")
"""

resposta_3_md = """### ✅ Resposta — Questão 3: Governança e Qualidade MLOps

**Não. O modelo NÃO deve ser aprovado automaticamente para produção.**

Abaixo a justificativa detalhada segundo boas práticas de MLOps:

---

#### 1. 🔢 Amostra Estatisticamente Insuficiente

50 registros representam apenas **5%** do lote original. Esse volume é insuficiente para garantir qualquer representatividade estatística. Em análise de crédito, padrões de inadimplência, perfis de renda e comportamento de consumo são altamente heterogêneos — 50 amostras não capturam essa diversidade.

- **Risco:** Overfitting severo. Um modelo com 50 amostras de treino pode "memorizar" os dados em vez de aprender padrões generalizáveis.
- **Consequência:** Acurácia de 98% num conjunto tão pequeno é **estatisticamente suspeita**, não confiável.

---

#### 2. 📉 Data Drift — Alarme Crítico

O descarte de **95% dos registros** é um sinal gravíssimo de **Data Drift** (deriva de dados): a distribuição dos dados de entrada mudou drasticamente em relação ao que o modelo originalmente aprendeu.

- **O que causou:** A atualização não homologada da API gerou dados corrompidos em escala.
- **Por que importa:** O modelo em produção receberá dados com a distribuição *corrompida*, enquanto foi treinado com dados *limpos* (ou vice-versa). Isso cria uma **discrepância train-serve** que invalida as métricas de acurácia.
- **Ação necessária:** Investigar a raiz do drift antes de qualquer novo treinamento.

---

#### 3. ⚖️ Viés de Sobrevivência (*Survivorship Bias*)

Os 50 registros "válidos" podem não ser representativos da população real de clientes. Se apenas perfis de uma faixa etária ou faixa de renda específica sobreviveram à corrupção, o modelo aprenderá um **subgrupo enviesado** — e tomará decisões discriminatórias ou economicamente inviáveis em produção.

---

#### 4. 🏛️ Boas Práticas de Governança MLOps que foram violadas

| Critério                          | Situação atual        | Adequado?  |
|-----------------------------------|-----------------------|------------|
| Volume mínimo de treino           | 50 registros          | ❌ Não      |
| Representatividade da amostra     | 5% do lote original   | ❌ Não      |
| Análise de Data Drift             | Não realizada         | ❌ Não      |
| Testes em conjunto de validação   | Não mencionado        | ❌ Não      |
| Aprovação humana (*human-in-loop*)| Ignorada (automática) | ❌ Não      |
| Rollback plan definido            | Não mencionado        | ❌ Não      |

---

#### 5. ✅ O que deveria ser feito

1. **Bloquear o pipeline** e acionar alerta de qualidade de dados.
2. **Investigar e corrigir** a API responsável pela corrupção dos dados.
3. **Reprocessar o lote** completo após a correção.
4. **Retreinar o modelo** com volume adequado (mínimo recomendado: centenas a milhares de amostras por classe).
5. **Validar métricas** em conjunto de teste independente e comparar com o modelo em produção via **A/B testing** ou **Shadow mode**.
6. **Monitorar continuamente** indicadores de drift (ex.: PSI — Population Stability Index) antes de qualquer promoção para produção.

> **Conclusão:** A acurácia de 98% em 50 registros é uma **métrica enganosa e perigosa**. A aprovação automática nesse cenário violaria os princípios fundamentais de confiabilidade, rastreabilidade e governança de um sistema MLOps responsável."""

# ── Construir as células ──────────────────────────────────────────
def make_md_cell(source: str, cell_id: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [source]
    }

def make_code_cell(source: str, cell_id: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": [source]
    }

# ── Carregar notebook existente ───────────────────────────────────
with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

q1_cell = nb["cells"][0]  # questão 1
q2_cell = nb["cells"][1]  # questão 2
q3_cell = nb["cells"][2]  # questão 3

novas_cells = [
    q1_cell,
    make_md_cell(resposta_1_md,  "a1_q1_resp"),
    q2_cell,
    make_code_cell(resposta_2_code, "a1_q2_code"),
    q3_cell,
    make_md_cell(resposta_3_md,  "a1_q3_resp"),
]

nb["cells"] = novas_cells

# ── Salvar ────────────────────────────────────────────────────────
with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("[OK] atividade.ipynb atualizado com sucesso!")
print(f"   Total de celulas: {len(novas_cells)}")
