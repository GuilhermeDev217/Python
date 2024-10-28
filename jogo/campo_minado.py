import tkinter as tk
from tkinter import messagebox
import random
import pygame


class CampoMinado:
    def __init__(self, master, largura=10, altura=10, minas=10):
        self.master = master
        self.largura = largura
        self.altura = altura
        self.minas = minas
        self.matriz = [[0 for _ in range(largura)] for _ in range(altura)]
        self.botao_matriz = [[None for _ in range(largura)] for _ in range(altura)]
        self.jogo_ativo = True

        # Inicializar pygame para tocar sons
        pygame.mixer.init()
        self.som_explosao = pygame.mixer.Sound("explosao.wav")
        self.som_clique = pygame.mixer.Sound("click.wav")

        self.master.geometry("800x600")
        self.master.title("Campo Minado")
        self.master.config(bg="#cce5ff")

        self.inicializar_minas()
        self.criar_interface()

    def inicializar_minas(self):
        posicoes = random.sample(range(self.largura * self.altura), self.minas)
        for pos in posicoes:
            x, y = pos % self.largura, pos // self.largura
            self.matriz[y][x] = 'M'
            self.atualizar_contadores(x, y)

    def atualizar_contadores(self, x, y):
        for i in range(max(0, y - 1), min(self.altura, y + 2)):
            for j in range(max(0, x - 1), min(self.largura, x + 2)):
                if self.matriz[i][j] != 'M':
                    self.matriz[i][j] += 1

    def criar_interface(self):
        self.frame = tk.Frame(self.master, bg="#cce5ff")
        self.frame.pack(pady=10)

        # Título do jogo
        titulo = tk.Label(self.master, text="Campo Minado", font=('Arial', 24, 'bold'), bg="#cce5ff", fg="#ff5733")
        titulo.pack(pady=20)

        # Botão para reiniciar o jogo
        self.reiniciar_btn = tk.Button(self.master, text="Reiniciar", command=self.reiniciar,
                                       font=('Arial', 14), bg='lightgreen', activebackground='darkgreen', bd=0,
                                       padx=10, pady=5)
        self.reiniciar_btn.pack(pady=10)

        for y in range(self.altura):
            for x in range(self.largura):
                botao = tk.Button(self.frame, text='', width=6, height=3, font=('Arial', 14),
                                  bg='lightblue', activebackground='skyblue', bd=0,
                                  command=lambda x=x, y=y: self.revelar(x, y))
                botao.bind("<Button-3>", lambda event, x=x, y=y: self.marcar_bandeira(x, y))  # Clique direito
                botao.grid(row=y, column=x, padx=2, pady=2)
                self.botao_matriz[y][x] = botao

    def reiniciar(self):
        for y in range(self.altura):
            for x in range(self.largura):
                self.botao_matriz[y][x].config(text='', bg='lightblue', state='normal')
        self.jogo_ativo = True
        self.matriz = [[0 for _ in range(self.largura)] for _ in range(self.altura)]
        self.inicializar_minas()

    def revelar(self, x, y):
        if not self.jogo_ativo:
            return

        if self.matriz[y][x] == 'M':
            self.jogo_ativo = False
            self.som_explosao.play()
            self.animacao_bomba(x, y)
        else:
            self.som_clique.play()
            self.botao_matriz[y][x].config(text=str(self.matriz[y][x]), bg='lightgrey')
            if self.matriz[y][x] == 0:
                self.revelar_vizinhos(x, y)

    def animacao_bomba(self, x, y):
        for _ in range(6):  # Número de piscadas
            self.botao_matriz[y][x].config(bg='red')
            self.master.after(100, lambda: self.botao_matriz[y][x].config(bg='lightblue'))
            self.master.after(200, lambda: self.revelar_todas_as_minas())  # Revelar minas após animação
            return  # Terminar a função após iniciar a animação

    def marcar_bandeira(self, x, y):
        if not self.jogo_ativo:
            return

        cor_bandeira = 'orange'  # Cor da bandeira
        if self.botao_matriz[y][x]['bg'] == cor_bandeira:
            self.botao_matriz[y][x].config(bg='lightblue')
        else:
            self.botao_matriz[y][x].config(bg=cor_bandeira)  # Marcar bandeira

    def revelar_todas_as_minas(self):
        for y in range(self.altura):
            for x in range(self.largura):
                if self.matriz[y][x] == 'M':
                    self.botao_matriz[y][x].config(bg='red')  # Mudar fundo para vermelho

    def revelar_vizinhos(self, x, y):
        for i in range(max(0, y - 1), min(self.altura, y + 2)):
            for j in range(max(0, x - 1), min(self.largura, x + 2)):
                if self.botao_matriz[i][j]['text'] == '' and self.matriz[i][j] != 'M':
                    self.revelar(j, i)


def selecionar_dificuldade():
    def iniciar_jogo(dificuldade):
        if dificuldade == "Fácil":
            jogo = CampoMinado(root, largura=8, altura=8, minas=10)
        elif dificuldade == "Médio":
            jogo = CampoMinado(root, largura=16, altura=16, minas=40)
        elif dificuldade == "Difícil":
            jogo = CampoMinado(root, largura=24, altura=16, minas=99)
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Selecione a Dificuldade")
    janela.config(bg="#cce5ff")

    # Título da janela de dificuldade
    tk.Label(janela, text="Escolha a Dificuldade", font=('Arial', 20, 'bold'), bg="#cce5ff", fg="#ff5733").pack(pady=20)

    # Adicionar botões de dificuldade com mais estilo
    for nivel in ["Fácil", "Médio", "Difícil"]:
        botao = tk.Button(janela, text=nivel, command=lambda n=nivel: iniciar_jogo(n),
                          font=('Arial', 16), bg='lightgreen', activebackground='darkgreen', bd=0,
                          padx=10, pady=5)
        botao.pack(pady=10, padx=20)  # Adicionando espaçamento

    # Adicionar uma borda ao redor da janela
    janela_frame = tk.Frame(janela, bg="#cce5ff", bd=2, relief='groove')
    janela_frame.pack(padx=20, pady=20)

    # Instruções
    instrucoes = tk.Label(janela_frame, text="Clique em uma dificuldade abaixo para começar!",
                          font=('Arial', 12), bg="#cce5ff", fg="#555")
    instrucoes.pack(pady=10)

    # Nomes dos criadores
    criadores = tk.Label(janela_frame, text="Criadores do Jogo:\nGuilherme Figueiredo\nFernanda Carvalho\nDiogo Nogueira",
                         font=('Arial', 12), bg="#cce5ff", fg="#555")
    criadores.pack(pady=10)

    # Adicionar um botão de sair
    btn_sair = tk.Button(janela, text="Sair", command=janela.destroy,
                         font=('Arial', 14), bg='red', activebackground='darkred', bd=0,
                         padx=10, pady=5)
    btn_sair.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()

    # Selecionar dificuldade antes de iniciar o jogo
    selecionar_dificuldade()

    root.mainloop()
