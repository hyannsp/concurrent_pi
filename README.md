# Programação Concorrente
Trabalho feito por [Hyann Piffer](https://github.com/hyannsp) e [Ingridy Rodrigues](https://github.com/ingridyr) para a disciplina de **Programação Distribuída e Concorrente**.

## 1. Objetivo do Trabalho
Como objetivo do trabalho visamos realizar o **calculo do valor de pi (𝜋)** utilizando python.  
Dividiremos o código em duas partes: A primeira é calculando com programação sequencial e marcando seu tempo, a segunda será calculado o valor utilizando programação concorrente com a biblioteca `concurrent.futures` seguida de uma breve análise com a diferença de tempo.

## 2. Como Calcular o Valor de 𝜋?
Para encontra-lo utilizaremos do **Método do Monte Carlo**, baseado em conceitos probabilísticos.  
Em um contexto hipotético existe um círculo de raio 1 inscrito dentro de um quadrado de lado 2. A área do quadrado é 4 e a do círculo é 𝜋, se gerarmos pontos aleatórios dentro do quadrado, a fração de pontos que caem dentro do círculo deve ser aproximadamente igual à razão das áreas, ou seja: $\frac{Pontos no Circulo}{Total de Pontos} \cong \frac{\Pi}{4}$ e assim multiplicamos o resultado por 4, retornando o valor de pi. Quanto maior a entrada, mais próximo ficamos do valor de PI, por exemplo, nas imagens abaixo criadas por código com a biblioteca `matplotlib` temos a visualização de 1.000 pontos, 10.000 pontos e 100.000 pontos respectivamente.


![Monte Carlo Output 1k](images/output_1k.png)
![Monte Carlo Output 10k](images/output_10k.png)
![Monte Carlo Output 100k](images/output_100k.png)

## 3. Praticando com os Códigos
Entendendo o método, tanto a função sequêncial quanto a concorrente se tornam simples:
### 3.1 Aplicação Sequêncial
 1. criamos uma função `monte_carlo_seq` que receberá a quantidade de pontos que serão usados. Esses pontos são gerados aleatóriamente em um range de coordenadas de -1 a 1 na horizontal (eixo X) e -1 a 1 na vertical (eixo Y) , formando um quadrado 2x2 de **área igual à 4**;
 2. Em seguida verificamos se o ponto gerado pertence à área do circulo, vai pertencer se a distância da origem (0,0) for menor ou igual ao raio: $x² + y² \leq r²$ e **levando em consideração que nosso raio é 1**. Para cada ponto dentro do circulo, acrescenta-se 1 à variavel `inside_circle`;
 3. Ao final, retornamos o valor de PI com o cálculo $\frac{Pontos no Circulo}{Total de Pontos} \times 4$ e a diferença do tempo no final do código com o seu começo, ou seja, o tempo gasto para o código inteiro.

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

### 3.2 Aplicação Concorrente
Para a concorrente foram criadas 2 funções, uma auxiliar que será qual cada executor irá realizar `monte_carlo_worker`, e a principal, que divide o processo entre os executores `monte_carlo_concurrent`.

- A primeira função, funciona da mesma forma que a função da [aplicação sequêncial]('3.1 Aplicação Sequêncial'), onde é inserido vários pontos no quadrado de área 4, x = (-1, 1) e y = (-1, 1). A principal diferença é que essa retornará apenas a **quantidade de pontos dentro do circulo** e não o valor de $\pi$. 
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
- Já a outra função, vai receber o numero de pontos e número de trabalhadores (com padrão = 4) e fará o seguinte:
    1. Dividr a quantidade de pontos para cada operados, ou seja, caso tenhamos 1000 pontos e 5 operadores, cada operador ficará com 200 pontos.
    2. Chamar os operadores e colocar cada um deles para resolver a função `monte_carlo_worker`, isso é feito utilizando ProcessPoolExecutor e um map, retornando a lista de resultados.
        - O map funciona com 2 parâmetros: `(func, iteravel)`, onde a função será o que cada operador executará e uma lista com os parametros de cada funcao, por exemplo se for 1000 pontos e 5 operadores, os parametros do map seriam `(monte_carlo_worker, [200, 200, 200, 200, 200])` e o resultado uma lista com os pontos achados por cada operador, exemplo: `[140, 137, 144, 130, 142]`.
    3. Somamos os valores encontrados por cada uma das listas e fazemos o calculo de $\pi$ com esse valor total, retornando $\pi$ e o tempo de duração
```python
def monte_carlo_concurrent(n_points: int, n_workers: int = 4) -> tuple[float, float]:
    points_per_worker = n_points // n_workers
    start = timer()

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = executor.map(monte_carlo_worker, [points_per_worker] * n_workers)

    inside_circle = sum(results)
    return (inside_circle / n_points) * 4, timer() - start
```

## Resultados e Conclusão