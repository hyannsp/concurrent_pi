<!--
OBS: PARA ABRIR A VISUALIZAÇÃO DO DOCUMENTO FORMATADO TECLAR CTRL + SHIFT + V

Turma CC7N

Alunos:
    Ingridy Rodrigues Fagundes - 202201383
    Hyann Silva Piffer - 202201110
-->

<div style="text-align: center;">
    <img src="images\logo_uvv.png" alt="Logo UVV" width="20%"/>
</div>

<div style="text-align: center;">

# UNIVERSIDADE VILA VELHA

### CIÊNCIA DA COMPUTAÇÃO

---

## **PROGRAMAÇÃO DISTRIBUÍDA E CONCORRENTE**

**Trabalho Bimestral**

---

**Autor(es)**: [Hyann Silva Piffer](https://github.com/hyannsp) e [Ingridy Rodrigues Fagundes](https://github.com/ingridyr)

**Professor(a)**: Wanderson Muniz de Santana

**Disciplina**: Programação Distribuída e Concorrente

**Disponível em [Github](https://github.com/hyannsp/concurrent_pi)**

---

**Vila Velha - ES**  
**2025**

</div>

## Índice

- [1. Objetivo do Trabalho](#1-objetivo-do-trabalho)
- [2. Metodologia](#2-metodologia)
- [3. Implementação e análise](#3-implementação-e-análise)
  - [3.1 Implementação Sequencial](#31-implementação-sequencial)
  - [3.2 Implementação Concorrente](#32-implementação-concorrente)
- [4. Resultados e Conclusão](#4-resultados-e-conclusão)
- [5. Referências](#5-referências)

## 1. Objetivo do Trabalho

Este trabalho tem como objetivo realizar o **cálculo do valor de $\pi$ (pi)** utilizando a linguagem de programação Python. Para tal, o código será dividido em duas abordagens: a primeira consiste na implementação sequencial do cálculo, acompanhada da medição do tempo de execução. A segunda abordagem consiste na implementação concorrente do mesmo cálculo, empregando a biblioteca `concurrent.futures`, seguida de uma análise comparativa dos tempos de execução.

## 2. Metodologia

A técnica empregada para a obtenção do valor de $\pi$ baseia-se no **Método de Monte Carlo**, fundamentado em princípios probabilísticos. Considera-se um círculo de raio 1 inscrito em um quadrado de lado 2. A área do quadrado é 4, enquanto a área do círculo é $\pi$. Ao gerar pontos aleatórios dentro do quadrado, a proporção de pontos que caem dentro do círculo tende a se aproximar da razão entre as áreas dessas figuras, ou seja:
$\frac{Pontos no Circulo}{Total de Pontos} \cong \frac{\Pi}{4}$

A partir dessa relação, multiplica-se o resultado por 4 para estimar o valor de $\pi$. Quanto maior a quantidade de pontos gerados, mais próxima será a aproximação do valor real de $\pi$. As imagens a seguir ilustram os resultados obtidos com 1.000, 10.000 e 100.000 pontos, respectivamente, utilizando a biblioteca `matplotlib`.

<div style="display: flex; justify-content: center;">
    <img src="images/output_1k.png" width="20%" alt="Monte Carlo Output 1k">
    <img src="images/output_10k.png" width="20%" alt="Monte Carlo Output 10k">
    <img src="images/output_100k.png" width="20%" alt="Monte Carlo Output 100k">
</div>

## 3. Implementação e análise

A implementação do método de Monte Carlo foi realizada de duas maneiras: sequencial e concorrente.

### 3.1 Implementação Sequencial

A abordagem sequencial é composta pelos seguintes passos:

1. Implementa-se a função `monte_carlo_seq`, que recebe como entrada a quantidade de pontos a serem gerados. Os pontos são distribuídos aleatoriamente dentro de um quadrado de coordenadas x e y variando entre -1 e 1, formando uma área total igual a 4.

2. Para cada ponto gerado, verifica-se se ele está dentro do círculo ao calcular sua distância até a origem (0,0). Se a distância for menor ou igual ao raio, ou seja,
   $x² + y² \leq r²$, considera-se que o ponto pertence ao círculo. Neste caso, o raio adotado é igual a 1.

3. A quantidade de pontos dentro do círculo é armazenada e, ao final, o valor de $\pi$ é calculado como:
   $\frac{Pontos No Circulo}{Total De Pontos} \times 4$. O tempo de execução é registrado para análise comparativa.

```python
import random
from timeit import default_timer as timer

def monte_carlo_seq(n_points: int) -> tuple[float, float]:
    inside_circle = 0
    start = timer()
    for _ in range(n_points):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1

    return (inside_circle / n_points) * 4, timer() - start
```

### 3.2 Implementação Concorrente

Para a abordagem concorrente, foram criadas duas funções: uma auxiliar, chamada `monte_carlo_worker`, responsável pela execução individual de cada tarefa, e uma função principal, `monte_carlo_concurrent`, que divide o trabalho entre os executores.

- A função `monte_carlo_concurrent`, funciona da mesma forma que a função da [implementação sequencial](#31-implementação-sequencial), onde é inserido vários pontos no quadrado de área 4, x = (-1, 1) e y = (-1, 1). A principal diferença é que essa retornará apenas a **quantidade de pontos dentro do círculo** e não o valor de $\pi$.

    ```python
    def monte_carlo_concurrent(n_points: int, n_workers: int = 4) -> tuple[float, float]:
        points_per_worker = n_points // n_workers
        start = timer()

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
            results = executor.map(monte_carlo_worker, [points_per_worker] * n_workers)

        inside_circle = sum(results)
        return (inside_circle / n_points) * 4, timer() - start
    ```

- A outra função recebe o número de pontos e o número de trabalhadores (com padrão de 4) e faz o seguinte:

1. Ela distribui a quantidade de pontos entre os trabalhadores, ou seja, se tivermos 1000 pontos e 5 trabalhadores, cada um ficará responsável por 200 pontos.
2. Em seguida, chama os trabalhadores e faz com que cada um execute a função `monte_carlo_worker`. Isso é feito utilizando o `ThreadPoolExecutor` junto com o `map`, que retorna uma lista com os resultados.
   
    >O map funciona com 2 parâmetros: `(func, iteravel)`, onde a função será o que cada operador executará e uma lista com os parâmetros de cada função,  
    >por exemplo: se forem 1000 pontos e 5 operadores, os parâmetros do map seriam `(monte_carlo_worker, [200, 200, 200, 200, 200])`;  
    >O resultado gera uma lista com os pontos achados por cada operador, exemplo: `[140, 137, 144, 130, 142]`.
    
3. Depois, somamos os valores de cada lista e calculamos o valor de $\pi$ com o total. Por fim, a função retorna o valor de $\pi$ e o tempo gasto para executar todo o processo.

    ```python
    def monte_carlo_worker(n_points: int) -> int:
        # Função auxiliar para calcular parte do Monte Carlo.
        inside_circle = 0
        for _ in range(n_points):
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            if x**2 + y**2 <= 1:
                inside_circle += 1
        return inside_circle
    ```

### 4. Resultados e Conclusão

Neste trabalho, foram analisadas as abordagens sequencial e concorrente para o cálculo de $\pi$ usando o Método de Monte Carlo. Apesar de o objetivo ser explorar o uso de threads, os resultados mostraram que a implementação concorrente não trouxe grandes melhorias de desempenho em comparação com a versão sequencial como nos exemplos a seguir:

- Para **1.000.000 de pontos**, a versão sequencial levou cerca de 0.32 segundos para calcular o valor de $\pi$, resultando em 3.142772. Em comparação, a versão concorrente encontrou um valor de $\pi$ igual a 3.139436 e teve um tempo de execução de 0.33 segundos.
- Para **10.000.000 de pontos**, o tempo de execução da versão sequencial foi de 3.09 segundos, com o valor calculado para $\pi$ sendo 3.1423172. A versão concorrente teve um tempo muito próximo, de 3.08 segundos, com o valor de 3.1410876.
- Para **100.000.000 de pontos**, a versão sequencial levou 31.93 segundos com valor de 3.14174644, enquanto a concorrente executou em 31.36 segundos com $\pi$ igual a 3.14162984.
    
>É importante notar que, a cada execução do código, os resultados podem variar devido à natureza aleatória do Método de Monte Carlo, e por mais que em algumas execuções a versão concorrente pareça ser mais rápida, essa diferença não é consistente.

Isso aconteceu porque o cálculo de $\pi$ é uma tarefa que exige bastante poder de processamento (CPU-bound) e a Trava Global do Interpretador (GIL) do Python impede que o código seja executado em múltiplos núcleos ao mesmo tempo.

A sobrecarga de gerenciar as threads e a limitação de não conseguir aproveitar múltiplos núcleos resultaram em um tempo de execução da versão concorrente similar, ou até um pouco maior, que o da versão sequencial. Se tivéssemos utilizado a biblioteca multiprocessing, que permite rodar processos em núcleos diferentes e contorna a GIL, provavelmente teríamos visto uma melhora no desempenho, mas como o objetivo era explorar a concorrência com threads, ficou claro que essa abordagem não é ideal para esse tipo de problema.

Em resumo, o trabalho mostrou como é **importante** <u>entender a natureza da tarefa</u> e as <u>limitações do ambiente</u> ao escolher a melhor forma de implementar a concorrência. Para problemas de processamento pesado como o cálculo de $\pi$, a solução mais adequada seria usar múltiplos processos ou programação distribuída, em vez de depender das threads no Python, que não trazem os benefícios esperados nesse caso.

### 5. Referências

**SHARMA, Vishal .** Estimating Pi Using Monte Carlo Methods. *Medium*, 2018. Disponível em: [https://medium.com/the-modern-scientist/estimating-pi-using-monte-carlo-methods-dbdf26c888d6](https://medium.com/the-modern-scientist/estimating-pi-using-monte-carlo-methods-dbdf26c888d6). Acesso em: 19 mar. 2025.

**GUSTAFSENN, Andrea .** Estimating Pi Using Monte Carlo Simulation in R. *Towards Data Science*, 2021. Disponível em: [https://towardsdatascience.com/estimating-pi-using-monte-carlo-simulation-in-r-91d1f32406af](https://towardsdatascience.com/estimating-pi-using-monte-carlo-simulation-in-r-91d1f32406af/). Acesso em: 19 mar. 2025.

**RAMALHO, Luciano.** _Python fluente: segunda edição_. 2. ed. Rio de Janeiro: Novatec, 2023. Cap. 19, seção 19.3.1, p. 421-423. Disponível em: [https://pythonfluente.com/#concurrency_models_ch](https://pythonfluente.com/#concurrency_models_ch). Acesso em: 21 mar. 2025.
