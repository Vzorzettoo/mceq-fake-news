"""Reanálise de contagens publicadas na Tabela 3 de Almeida et al. (2021)."""

import csv
import json
from pathlib import Path

from scipy.optimize import brentq
from scipy.stats import beta

from figura import gerar_figura

ROOT = Path(__file__).resolve().parent
ALPHA = 0.05
MODELOS = ("SVM linear", "Naive Bayes multinomial")


def ler_contagens():
    origem = ROOT / "dados/brutos/almeida2021_tabela3.csv"
    with origem.open(newline="", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    if tuple(linha["modelo"] for linha in linhas) != MODELOS:
        raise ValueError("O arquivo deve conter os dois modelos na ordem prevista.")

    matrizes = []
    totais = set()
    for linha in linhas:
        positivas = int(linha["n_falsas"])
        negativas = int(linha["n_nao_falsas"])
        fn = int(linha["falsos_negativos"])
        fp = int(linha["falsos_positivos"])
        if min(positivas, negativas) <= 0 or not (0 <= fn <= positivas and 0 <= fp <= negativas):
            raise ValueError(f"Contagens incompatíveis com os totais: {linha}")
        totais.add((negativas, positivas))
        matrizes.append((negativas - fp, fp, fn, positivas - fn))
    if len(totais) != 1:
        raise ValueError("As contagens devem ter os mesmos totais de classe.")
    return matrizes


def f1_macro(tn, fp, fn, tp):
    """Calcula a média do F1 para os dois rótulos."""
    return (2 * tn / (2 * tn + fp + fn) + 2 * tp / (2 * tp + fp + fn)) / 2


def intervalo_binomial(acertos, total, cauda):
    inferior = beta.ppf(cauda, acertos, total - acertos + 1) if acertos else 0.0
    superior = beta.isf(cauda, acertos + 1, total - acertos) if acertos < total else 1.0
    return inferior, superior


def limites_f1(matriz, cauda):
    tn, fp, fn, tp = matriz
    negativas, positivas = tn + fp, tp + fn
    lo0, hi0 = intervalo_binomial(tn, negativas, cauda)
    lo1, hi1 = intervalo_binomial(tp, positivas, cauda)

    def f1_taxas(taxa0, taxa1):
        return f1_macro(negativas * taxa0, negativas * (1 - taxa0),
                        positivas * (1 - taxa1), positivas * taxa1)

    return f1_taxas(lo0, lo1), f1_taxas(hi0, hi1)


def descrever(modelo, matriz):
    tn, fp, fn, tp = matriz
    return {
        "modelo": modelo, "VN": tn, "FP": fp, "FN": fn, "VP": tp,
        "acuracia": (tn + tp) / sum(matriz),
        "revocacao_falsas": tp / (tp + fn),
        "f1_macro": f1_macro(*matriz),
    }


def analisar():
    svm, nb = ler_contagens()
    svm_lo, svm_hi = limites_f1(svm, ALPHA / 8)
    nb_lo, nb_hi = limites_f1(nb, ALPHA / 8)

    def limite_unilateral(alpha):
        return limites_f1(svm, alpha / 4)[0] - limites_f1(nb, alpha / 4)[1]

    def limite_log(log_alpha):
        return limite_unilateral(10 ** log_alpha)

    if limite_log(0) <= 0:
        p = 1.0
    elif limite_log(-250) > 0:
        p = 1e-250  # Limite superior reportável para raízes menores.
    else:
        p = 10 ** brentq(limite_log, -250, 0)

    return {
        "n": sum(svm), "nao_falsas": sum(svm[:2]), "falsas": sum(svm[2:]),
        "modelos": [descrever(nome, m) for nome, m in zip(MODELOS, (svm, nb))],
        "diferenca_f1_macro": f1_macro(*svm) - f1_macro(*nb),
        "ic95_diferenca": [svm_lo - nb_hi, svm_hi - nb_lo],
        "limite_inferior_unilateral_95": limite_unilateral(ALPHA),
        "p_conservador": p, "alpha": ALPHA, "rejeita_h0": p <= ALPHA,
    }


def main():
    resultado = analisar()
    saida = ROOT / "resultados"
    saida.mkdir(exist_ok=True)
    texto = json.dumps(resultado, indent=2, ensure_ascii=False)
    (saida / "analise.json").write_text(texto + "\n", encoding="utf-8")
    with (saida / "descritiva.csv").open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(resultado["modelos"][0]))
        writer.writeheader()
        writer.writerows(resultado["modelos"])
    gerar_figura(resultado, saida / "figura.pdf")
    print(texto)


if __name__ == "__main__":
    main()
