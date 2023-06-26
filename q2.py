
import tkinter as tk
from tkinter import ttk


class Definicao:
    def __init__(self, numero, conteudo):
        self.numero = numero
        self.conteudo = conteudo

class BlocoBasico:
    def __init__(self, nome):
        self.nome = nome
        self.conteudo = []
        self.saida = []

    def add(self, linha):
        self.conteudo.append(linha)
    
    def addSaida(self, vetor):
        for i in range(len(vetor)):
            self.saida.append(vetor[i])

def definicao_carater(caracter, definicoes):
    definicoesEnviar = []
    for definicao in definicoes:
        if definicao.conteudo[0] == caracter:
            definicoesEnviar.append(definicao)
    return definicoesEnviar

def imprimirBlocos(blocos): #Função para imprimir os blocos (para testes)
    for bloco in blocos:
        print(bloco.nome)
        for definicao in bloco.conteudo:
            print(definicao.conteudo)
        print("")

def imprimirMatriz(matriz, definicoes):
    janela = tk.Tk()
    
    frame1 = tk.Frame(janela)
    frame1.pack(side=tk.LEFT, padx=10, pady=10)

    tabela1 = ttk.Treeview(frame1)
    tabela1["columns"] = ("Bloco", "genb","killb", "inb", "outb")

    tabela1.column("#0", width=0, stretch=tk.NO)
    tabela1.column("Bloco", anchor=tk.CENTER)
    tabela1.column("genb", anchor=tk.CENTER)
    tabela1.column("killb", anchor=tk.CENTER)
    tabela1.column("inb", anchor=tk.CENTER)
    tabela1.column("outb", anchor=tk.CENTER)
    
    # Definir os cabeçalhos das colunas
    tabela1.heading("#0", text="", anchor=tk.CENTER)
    tabela1.heading("Bloco", text="Bloco", anchor=tk.CENTER)
    tabela1.heading("genb", text="genb", anchor=tk.CENTER)
    tabela1.heading("killb", text="killb", anchor=tk.CENTER)
    tabela1.heading("inb", text="inb", anchor=tk.CENTER)
    tabela1.heading("outb", text="outb", anchor=tk.CENTER)

    # Adicionar os dados à tabela1
    for linha in matriz:
        bloco = linha[0]
        genb = ""
        killb = ""
        inb = ""
        outb = ""
        
        for definicao in linha[1]:
            genb += "d"+str(definicao.numero) + " "
        for definicao in linha[2]:
            killb += "d"+str(definicao.numero) + " "
        for definicao in linha[3]:
            inb += "d"+str(definicao.numero) + " "
        for definicao in linha[4]:
            outb += "d"+str(definicao.numero) + " "
        tabela1.insert("", tk.END, text=bloco, values=(bloco, genb, killb, inb, outb))
        
    tabela1.pack()

    frame2 = tk.Frame(janela)
    frame2.pack(side=tk.RIGHT, padx=10, pady=10)

    tabela2 = ttk.Treeview(frame2)
    tabela2["columns"] = ("Numero", "Definição")

    tabela2.column("#0", width=0, stretch=tk.NO)
    tabela2.column("Numero", anchor=tk.CENTER)
    tabela2.column("Definição", anchor=tk.CENTER)

    # Definir os cabeçalhos das colunas
    tabela2.heading("#0", text="", anchor=tk.CENTER)
    tabela2.heading("Numero", text="Numero", anchor=tk.CENTER)
    tabela2.heading("Definição", text="Definição", anchor=tk.CENTER)

    # Adicionar os dados à tabela2
    for definicao in definicoes:
        tabela2.insert("", tk.END, text=definicao.numero, values=("d"+str(definicao.numero), definicao.conteudo))

    tabela2.pack()



    # Iniciar o loop principal da aplicação
    janela.mainloop()



def __main__():
    user_input = ""
    blocoAtual = None
    blocos = []
    definicoes = []
    numeroDefinicao = 1
    while user_input != "quit":
        user_input = input()
        if len(user_input.split()) == 2:
            blocos.append(BlocoBasico(user_input.split()[0]))
            blocoAtual = blocos[-1]
            vezes = int(user_input.split()[1])
            for i in range(vezes):
                user_input = input()
                definicaoAtual = Definicao(numeroDefinicao, user_input)
                blocoAtual.add(definicaoAtual)
                definicoes.append(definicaoAtual)
                numeroDefinicao += 1
            user_input = input()
            blocoAtual.addSaida(user_input.split())

            
    matriz = []
    for bloco in blocos:
        # 1° posição: número do bloco
        # 2° posição: todas as definições que o bloco gera
        # 3° posição: todas as definições que o bloco mata
        # 4° posição: todas as definições que entra no bloco
        # 5° posição: todas as definições que sai do bloco (o que ele gera + o que chega nele - o que ele mata)
        
        gera = [] 
        mata = [] 
        entra = []
        sai = [] 
        blocosAlcancaveis = []

        for definicao in bloco.conteudo:
            gera.append(definicao)
        
        for gerada in gera:
            for definicao in definicoes:
                if gerada.conteudo[0] == definicao.conteudo[0] and gerada.numero != definicao.numero:
                    mata.append(definicao)
        
        for saida in bloco.saida:
            blocosAlcancaveis.append(saida)

        linha = [bloco.nome, gera, mata, entra, sai, blocosAlcancaveis]
        matriz.append(linha)

    # Gera a saida e entrada de cada bloco
    for i in range(30):
        for linha in matriz:
            linha[4] = list(set(linha[3] + linha[1]) - set(linha[2]))
            for bloco in linha[5]:
                for linha2 in matriz:
                    if linha2[0] == bloco[0]:
                        linha2[3] = list(set(linha2[3]+linha[4]))


    imprimirMatriz(matriz, definicoes)

__main__()

# 1 2
# a=a+c
# b=4-a
# 2
# 2 1
# b=20*c
# 3
# 3 2
# d=a+b
# b=0
# 0
# quit
