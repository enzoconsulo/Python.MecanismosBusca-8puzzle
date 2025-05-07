# 8-Puzzle com Interface Gráfica e Resolução Por Mecanismos de Busca

Este projeto implementa o clássico quebra-cabeça 8-Puzzle (jogo dos 8) em Python, utilizando mecanismos de busca clássicos para encontrar a solução de forma **automática**. A interface gráfica é feita com `tkinter`, permitindo interagir manualmente ou observar a resolução passo a passo pelos algoritmos.

## Funcionalidades

- **Geração aleatória** de estados sempre solucionáveis.
- **Movimentação manual** das peças via clique ou setas do teclado ( Neste caso os movimentos serão salvos em caminhos.txt, para ser feita uma analise).
   - **Busca em Largura (BFS)**: explora o nível completo de cada profundidade antes de avançar.
- **Embaralhar** para reiniciar o puzzle com nova configuração.
- **Resolver automaticamente** utilizando três **mecanismos de busca**:
  - **Busca em Largura (BFS)**: explora o nível completo de cada profundidade antes de avançar.
  - **Busca em Profundidade (DFS)**: explora um ramo até o fim antes de retroceder.
  - **A\*** (A-Star): usa a heurística de Distância de Manhattan para priorizar estados mais promissores.
- Exibição de **quantidade de movimentos** e **estados visitados** por cada algoritmo.
- **Animação** da sequência de movimentos após encontrar a solução.
- **Restaurar** o estado anterior ao início da resolução automática (undo).

## Destaque: Mecanismos de Busca

O coração do solver está na implementação genérica de busca (`busca_generica`), que adapta a estrutura de dados e as operações de inserção/remoção para cada algoritmo:

- **BFS** usa uma fila (`deque`) para garantir exploração em largura.
- **DFS** usa uma pilha (lista) para exploração em profundidade.
- **A\*** usa uma fila de prioridade (`heapq`), combinando custo e heurística (Distância de Manhattan).

Essa arquitetura modular permite comparar desempenho, profundidade de busca e eficiência de cada método.

## Pré-requisitos

- Python 3.7 ou superior
- Biblioteca `tkinter` (instalada por padrão na maioria das distribuições)

## Instalação e Execução

1. Clone ou baixe este repositório e abra o terminal na pasta do projeto:
   ```bash
   git clone https://github.com/enzoconsulo/Python.MecanismosBusca-8puzzle.git
   cd Python.MecanismosBusca-8puzzle

## Como Usar
Mover manualmente: clique na peça adjacente ao espaço vazio ou use as setas do teclado.

Embaralhar: clique em “Embaralhar” para uma nova configuração.

Resolver: clique em “Resolver”, escolha o algoritmo de busca e veja:

- Janela com número de movimentos e estados visitados.

- Puzzle sendo resolvido automaticamente em animação.

Restaurar: botão “Restaurar Puzzle Anterior” retorna ao estado pré-solução.

## Estrutura de Arquivos

Python.MecanismosBusca-8puzzle/

─ puzzle8.py       # Código-fonte principal com implementação de mecanismos de busca

─ README.md        # Documentação do projeto
