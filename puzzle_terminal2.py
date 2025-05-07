import tkinter as tk
from tkinter import messagebox
import random
import heapq
from collections import deque

class Puzzle8:
    def __init__(self):
        self.estado_objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.tabuleiro = self.gerar_puzzle_solucionavel()
        self.tile_vazio = self.encontrar_tile_vazio()
        self.lista_movimentos = []
        self.tentativas = 0

    def gerar_puzzle_solucionavel(self):
        while True:
            tiles = list(range(9))
            random.shuffle(tiles)
            if self.eh_solucionavel(tiles):
                return [tiles[i:i+3] for i in range(0, 9, 3)]

    def eh_solucionavel(self, tiles):
        inversoes = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] != 0 and tiles[j] != 0 and tiles[i] > tiles[j]:
                    inversoes += 1
        return inversoes % 2 == 0

    def encontrar_tile_vazio(self):
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == 0:
                    return (i, j)

    def mover(self, direcao):
        i, j = self.tile_vazio
        if direcao == 'up' and i > 0:
            self.trocar(i, j, i - 1, j)
            self.tile_vazio = (i - 1, j)
        elif direcao == 'down' and i < 2:
            self.trocar(i, j, i + 1, j)
            self.tile_vazio = (i + 1, j)
        elif direcao == 'left' and j > 0:
            self.trocar(i, j, i, j - 1)
            self.tile_vazio = (i, j - 1)
        elif direcao == 'right' and j < 2:
            self.trocar(i, j, i, j + 1)
            self.tile_vazio = (i, j + 1)

        self.lista_movimentos.append(direcao)
        self.tentativas += 1

    def trocar(self, i1, j1, i2, j2):
        self.tabuleiro[i1][j1], self.tabuleiro[i2][j2] = self.tabuleiro[i2][j2], self.tabuleiro[i1][j1]

    def esta_resolvido(self):
        return self.tabuleiro == self.estado_objetivo

    def copiar_tabuleiro(self):
        return [linha[:] for linha in self.tabuleiro]

    def distancia_manhattan(self, tabuleiro):
        distancia = 0
        for i in range(3):
            for j in range(3):
                valor = tabuleiro[i][j]
                if valor != 0:
                    objetivo_x, objetivo_y = (valor - 1) // 3, (valor - 1) % 3
                    distancia += abs(i - objetivo_x) + abs(j - objetivo_y)
        return distancia

    def busca_generica(self, estrutura, adicionar_na_estrutura, remover_da_estrutura, heuristica=None):
        visitados = set()
        estados_visitados = 0

        estado_inicial = (self.tabuleiro, self.tile_vazio, [])
        adicionar_na_estrutura(estrutura, (0, 0, estado_inicial)) if heuristica else adicionar_na_estrutura(estrutura, estado_inicial)
        visitados.add(tuple(tuple(linha) for linha in self.tabuleiro))

        while estrutura:
            if heuristica:
                _, custo, (tabuleiro_atual, posicao_vazia, caminho) = remover_da_estrutura(estrutura)
            else:
                tabuleiro_atual, posicao_vazia, caminho = remover_da_estrutura(estrutura)

            estados_visitados += 1

            if tabuleiro_atual == self.estado_objetivo:
                return caminho, estados_visitados

            if len(caminho) > 50:
                continue

            i, j = posicao_vazia
            direcoes = [('up', i-1, j), ('down', i+1, j), ('left', i, j-1), ('right', i, j+1)]

            for direcao, novo_i, novo_j in direcoes:
                if 0 <= novo_i < 3 and 0 <= novo_j < 3:
                    novo_tabuleiro = [linha[:] for linha in tabuleiro_atual]
                    novo_tabuleiro[i][j], novo_tabuleiro[novo_i][novo_j] = novo_tabuleiro[novo_i][novo_j], novo_tabuleiro[i][j]
                    novo_estado = tuple(tuple(linha) for linha in novo_tabuleiro)

                    if novo_estado not in visitados:
                        visitados.add(novo_estado)
                        novo_caminho = caminho + [direcao]
                        if heuristica:
                            nova_heuristica = heuristica(novo_tabuleiro) + custo + 1
                            adicionar_na_estrutura(estrutura, (nova_heuristica, custo + 1, (novo_tabuleiro, (novo_i, novo_j), novo_caminho)))
                        else:
                            adicionar_na_estrutura(estrutura, (novo_tabuleiro, (novo_i, novo_j), novo_caminho))

        return None, estados_visitados




    def resolver_busca_largura(self):
        estrutura = deque()  
        return self.busca_generica(estrutura, deque.append, deque.popleft)

    def resolver_busca_profundidade(self):
        estrutura = []
        return self.busca_generica(estrutura, list.append, list.pop)

    def resolver_com_a_estrela(self):
        estrutura = []
        return self.busca_generica(estrutura, heapq.heappush, heapq.heappop, heuristica=self.distancia_manhattan)

class PuzzleGUI:
    def __init__(self, root, puzzle):
        self.root = root
        self.puzzle = puzzle
        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        self.menu_frame = None
        self.estado_anterior = None  
        self.criar_interface()
        self.atualizar_botoes()
        self.adicionar_controles_teclado()

    def criar_interface(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.grid(row=0, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', width=10, height=5, font=('Helvetica', 20), bg="lightblue")
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                self.botoes[i][j] = btn

        resolver_botao = tk.Button(self.menu_frame, text="Resolver", command=self.escolher_algoritmo)
        resolver_botao.pack(side=tk.LEFT)

        embaralhar_botao = tk.Button(self.menu_frame, text="Embaralhar", command=self.embaralhar)
        embaralhar_botao.pack(side=tk.LEFT)
        
        restaurar_botao = tk.Button(self.menu_frame, text="Restaurar Puzzle Anterior", command=self.restaurar_estado_anterior)
        restaurar_botao.pack(side=tk.LEFT)

    def restaurar_estado_anterior(self):
        if self.estado_anterior:
            self.puzzle.tabuleiro = [linha[:] for linha in self.estado_anterior]
            self.puzzle.tile_vazio = self.puzzle.encontrar_tile_vazio()
            self.atualizar_botoes()
        else:
            messagebox.showinfo("Aviso", "Não há nenhum estado salvo para restaurar.")

    def escolher_algoritmo(self):
        algoritmo = tk.StringVar()
        opcoes = [("Busca em Largura", "largura"), ("Busca em Profundidade", "profundidade"), ("A*", "a_estrela")]

        def confirmar_escolha():
            if algoritmo.get() == "largura":
                self.resolver_automaticamente(self.puzzle.resolver_busca_largura, "Busca em Largura")
            elif algoritmo.get() == "profundidade":
                self.resolver_automaticamente(self.puzzle.resolver_busca_profundidade, "Busca em Profundidade")
            elif algoritmo.get() == "a_estrela":
                self.resolver_automaticamente(self.puzzle.resolver_com_a_estrela, "A*")
            janela_algoritmo.destroy()

        janela_algoritmo = tk.Toplevel(self.root)
        janela_algoritmo.title("Escolha do Algoritmo")
        
        for texto, valor in opcoes:
            tk.Radiobutton(janela_algoritmo, text=texto, variable=algoritmo, value=valor).pack(anchor=tk.W)

        botao_confirmar = tk.Button(janela_algoritmo, text="Confirmar", command=confirmar_escolha)
        botao_confirmar.pack()

    def atualizar_botoes(self):
        for i in range(3):
            for j in range(3):
                valor = self.puzzle.tabuleiro[i][j]
                self.botoes[i][j].config(text=str(valor) if valor != 0 else '')

    def adicionar_controles_teclado(self):
        self.root.bind('<Up>', lambda e: self.mover('up'))
        self.root.bind('<Down>', lambda e: self.mover('down'))
        self.root.bind('<Left>', lambda e: self.mover('left'))
        self.root.bind('<Right>', lambda e: self.mover('right'))

    def mover(self, direcao):
        self.puzzle.mover(direcao)
        self.atualizar_botoes()

        if self.puzzle.esta_resolvido():
            messagebox.showinfo("Parabéns!", f"Você resolveu o quebra-cabeça!\nTentativas: {self.puzzle.tentativas}")
        else:
            pass  

    def resolver_automaticamente(self, algoritmo_resolucao, nome_algoritmo):
        self.estado_anterior = self.puzzle.copiar_tabuleiro()
        caminho, estados_visitados = algoritmo_resolucao()
        if caminho:
            messagebox.showinfo("Solução encontrada!",
                                f"O puzzle foi resolvido com {len(caminho)} movimentos.\n"
                                f"Estados visitados: {estados_visitados}\n"
                                f"Algoritmo usado: {nome_algoritmo}")
            self.mostrar_resultado(caminho, estados_visitados, nome_algoritmo)
        else:
            messagebox.showerror("Erro", "Não foi possível resolver o quebra-cabeça.")

    def mostrar_resultado(self, caminho, estados_visitados, nome_algoritmo):
        
        if(nome_algoritmo=="Busca em Profundidade"):
                
                resposta = messagebox.askquestion("Escolha de Velocidade", 
                                      "Deseja resolver o puzzle muito rápido?", 
                                      icon='question', 
                                      type='yesno')
                if resposta == 'yes': 
                    velocidade = 10  
                else:
                    velocidade = 500  
        else:
            velocidade = 500
                    
        for movimento in caminho:
            self.puzzle.mover(movimento)
            self.atualizar_botoes()
            self.root.update()
            self.root.after(velocidade)
                
        messagebox.showinfo("Solução encontrada!",
                            f"O puzzle foi resolvido com {len(caminho)} movimentos.\n")

    def embaralhar(self):
        self.puzzle.tabuleiro = self.puzzle.gerar_puzzle_solucionavel()
        self.puzzle.tile_vazio = self.puzzle.encontrar_tile_vazio()
        self.puzzle.lista_movimentos = []
        self.puzzle.tentativas = 0
        self.atualizar_botoes()
        self.estado_anterior = None 


root = tk.Tk()
root.title("8-Puzzle")
puzzle = Puzzle8()
gui = PuzzleGUI(root, puzzle)
root.mainloop()
