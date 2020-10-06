# Projeto 1: Ricochet Robots

## Índice
- [Introdução](#introdução)
- [Objetivo](#objetivo)
- [Formato de input e output](#formato-de-input-e-output)
    -[Input](#input)
    -[Output](#output)
- [Avaliação](#avaliação)
    -[Entrega](#instruções-para-a-entrega)
    -[Relatório](#relatório)

## Introdução

**Ambiente:**
- grelha quadrada
- cada célula pode ter barreiras nas bordas e o tabuleiro é limitado por barreiras em toda a sua volta
- 4 robôs de cores diferentes e 1 alvo com a cor de um dos robôs

**Objetivo:** identificar uma sequência de jogadas, em que cada jogada corresponde a um movimento de um robô, tal que após a execução dessa sequência o robô da cor do alvo se encontre na mesma célula que o alvo

- um robô pode movimentar-se para cima, baixo, esquerda e direita, mas não na diagonal
- quando um robô se movimenta, só para quando embate numa barreira ou noutro robô

## Objetivo

Desenvolver um programa em Python 3.8 que dado um tabuleiro do jogo retorne uma solução (sequência de movimentos dos robôs que permitem ganhar o jogo).

Nome do ficheiro: `ricochet_robots.py`

Argumentos: path para um ficheiro que contém uma instância do jogo

Utilização:

    python3 ricochet_robots.py <instance_file>


## Formato de Input e Output
- robos identificados pela cor R (red), Y (yellow), B (blue) e G (green)
- movimentos e barreiras identificados por u (up), d (down), l (left) e r (right)

### Input
- primeira linha: dimensão do tabuleiro *N* x *N*
- quatro linhas seguintes: posição dos robôs - cor linha coluna
        
        Y 4 2

- sexta linha: cor e posição do alvo - cor linha coluna
- sétima linha: um número *K* que define o número de barreiras internas
- *K* linhas seguintes: indica onde estão as barreiras interas: linha coluna posição

        4 2 r

### Output
Descreve uma solução para o problema: uma sequeência de movimentos dos robôs tais que, após aplicados ao estado inicial do tabuleiro, o alvo e o robô ocupem a mesma célula no tabuleiro

- primeira linha: um número *M* que define o número total de movimentos
- *M* linhas seguintes: movimentos efectuados por ordem - cor direção

        B 1

## Avaliação
- 12 valores Mooshak
- 4 valores testes adicionais
- 4 valores relatório

**Entrega:** 30 de outubro através do Mooshak

### Instruções para a entrega
- primeiras linhas: comentário com o nosso número e nome
- só podemos submeter o projeto de 15 em 15 minutos
- não há limite de submissões

### Relatório
- 2 páginas de texto, no máximo, com fonte 12pt
- para além das duas páginas podem ser acrescentadas imagens, figuras e tabelas
- incluir os resultados obtidos executando uma procura em **largura**,**profundidade**, **gananciosa** e **A\***. Estes devem conter o tempo de execução, número de nós expandidos e número de nós gerados
- usar a classe `InstrumentedProblem` e o exemplo que se encontra no fim do ficheiro `search.py`
- fazer uma análise crítica dos resultados obtidos, comparando em termos de **completude**, **eficiência** e **otimalidade**
- fazer uma análise da **heurística** implementada e compará-la a outras heurísticas avaliadas


