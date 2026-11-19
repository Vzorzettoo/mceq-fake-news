# SVM linear e Naive Bayes na detecção de notícias políticas falsas

Projeto final de Métodos de Computação Experimental e Quantitativa,
Engenharia de Software, PUC-Campinas.

## Pergunta de pesquisa

Em um teste publicado de notícias políticas brasileiras, o SVM linear com
TF-IDF tem F1 macro maior que o Naive Bayes multinomial com TF-IDF?

## Reproduzir a análise

Use Python 3.12. Na pasta deste repositório, execute:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analise.py
```

No Windows PowerShell, use `.\.venv\Scripts\Activate.ps1` no lugar da segunda
linha. O script executa localmente, sem precisar baixar os textos das notícias
ou treinar classificadores. Ele gera `resultados/analise.json`,
`resultados/descritiva.csv` e `resultados/figura.pdf`.

## Dados

As contagens em `dados/brutos/almeida2021_tabela3.csv` foram transcritas das
tabelas 2 e 3 de [Almeida et al. (2021)](https://sol.sbc.org.br/index.php/wics/article/download/15966/15807).
O artigo informa 761 notícias no teste, 471 falsas e 290 não falsas, e as
contagens de falsos positivos e negativos por modelo. O projeto reutiliza os
resultados dos autores. Veja [a proveniência](dados/PROVENIENCIA.md) para
identificação da fonte, versão, data de acesso e escopo da reutilização.

## Método e resultado esperado

O F1 macro é a média do F1 de cada classe. A estatística é a diferença
SVM menos Naive Bayes. Para o teste unilateral de superioridade com α = 0,05,
o programa inverte um limite de confiança simultâneo construído com quatro
caudas de Clopper–Pearson e ajuste de Bonferroni. O IC bilateral usa oito
caudas. O ajuste acomoda dependência entre os modelos, à condição de que
as taxas de acerto dentro das classes possam ser tratadas como binomiais.

Com as contagens publicadas, o resultado esperado é F1 macro de 0,688 para
SVM linear e 0,306 para Naive Bayes, diferença de 38,2 pontos percentuais,
IC de 95% de 29,6 a 45,5 pontos percentuais e p ≈ 1,33 × 10⁻²².
O contraste se refere ao teste político de quatro portais e aos pipelines avaliados.
