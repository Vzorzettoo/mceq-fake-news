# Comparação de classificadores no Fake.Br

O notebook compara SVM linear, Naive Bayes multinomial e regressão logística nas mesmas notícias de teste, usando o mesmo TF-IDF.

## Reproduzir

1. Abra [analise.ipynb](https://colab.research.google.com/github/Vzorzettoo/mceq-fake-news/blob/main/fakebr/analise.ipynb) no Google Colab.
2. Selecione **Ambiente de execução → Executar tudo**. O notebook baixa a revisão indicada do corpus automaticamente.
3. Na aba **Arquivos**, baixe **MCEQ_Resultados_FakeBr.zip**, com tabelas, figuras, partições e previsões do teste.

A execução de referência usou Python 3.12.14, scikit-learn 1.9.1, pandas 3.1.1, NumPy 2.5.5 e Matplotlib 3.11.2. O arquivo `reprodutibilidade.json` registra as versões de cada execução.

## Dados

Usamos os textos completos da [revisão 780f551 do Fake.Br Corpus](https://github.com/roneysco/Fake.br-Corpus/tree/780f5516c4ae070761632d98ac3368f3ded09d35), consultada em 25 de novembro de 2026. A fonte científica é [Monteiro et al. (2018)](https://doi.org/10.1007/978-3-319-99722-3_33). A revisão usada não traz licença explícita e o repositório da equipe não redistribui os textos.

A análise em `fakebr/` é a comparação de três modelos. A análise na raiz corresponde ao estudo anterior com as contagens de Almeida et al.
