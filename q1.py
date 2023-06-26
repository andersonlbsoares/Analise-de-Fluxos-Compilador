
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

def imprimirMatriz(matriz):
    janela = tk.Tk()
    
    frame1 = tk.Frame(janela)
    frame1.pack(side=tk.LEFT, padx=10, pady=10)

    tabela1 = ttk.Treeview(frame1)
    tabela1["columns"] = ("Bloco", "inb","defb","useb", "outb")

    tabela1.column("#0", width=0, stretch=tk.NO)
    tabela1.column("Bloco", anchor=tk.CENTER)
    tabela1.column("inb", anchor=tk.CENTER)
    tabela1.column("defb", anchor=tk.CENTER)
    tabela1.column("useb", anchor=tk.CENTER)
    tabela1.column("outb", anchor=tk.CENTER)
    
    # Definir os cabeçalhos das colunas
    tabela1.heading("#0", text="", anchor=tk.CENTER)
    tabela1.heading("Bloco", text="Bloco", anchor=tk.CENTER)
    tabela1.heading("inb", text="inb", anchor=tk.CENTER)
    tabela1.heading("defb", text="defb", anchor=tk.CENTER)
    tabela1.heading("useb", text="useb", anchor=tk.CENTER)
    tabela1.heading("outb", text="outb", anchor=tk.CENTER)

    # Adicionar os dados à tabela1
    for linha in reversed(matriz):
        bloco = linha[0]
        inb = ""
        defb = ""
        useb = ""
        outb = ""

        for caracter in linha[1]:
            inb += caracter + " "
        for caracter in linha[2]:
            defb += caracter + " "
        for caracter in linha[3]:
            useb += caracter + " "
        for caracter in linha[4]:
            outb += caracter + " "

        tabela1.insert("", tk.END, text=bloco, values=(bloco, inb, defb, useb, outb))
        
    tabela1.pack()
    janela.mainloop()



def __main__():
    user_input = ""
    blocoAtual = None
    blocos = []
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
                numeroDefinicao += 1
            user_input = input()
            blocoAtual.addSaida(user_input.split())

            
    matriz = []
    for bloco in reversed(blocos):
        entra = [] 
        define = [] 
        usa = []
        sai = [] 
        blocosAlcancaveis = []

        for saida in bloco.saida:
            blocosAlcancaveis.append(saida)

        for definicao in bloco.conteudo:
            #não está em define e nem repete na mesma linha
            if definicao.conteudo[0] not in define and definicao.conteudo[0] not in usa and definicao.conteudo.count(definicao.conteudo[0]) == 1: 
                define.append(definicao.conteudo[0])
            
            for caracter in definicao.conteudo[2:]:
                if caracter != "+" and caracter != "-" and caracter != "*" and caracter != "/" and not caracter.isdigit():
                    if caracter not in define and caracter not in usa:
                        usa.append(caracter)
            

        linha = [bloco.nome, entra, define, usa, sai, blocosAlcancaveis]
        matriz.append(linha)

    for i in range(30):
        for linha in matriz:

            for blocoAlcancavel in linha[5]:
                for linha2 in matriz:
                    if linha2[0] == blocoAlcancavel:
                        linha[4] = list(set(linha[4] + linha2[1]))
            
            linha[1] = list(set(linha[3] + linha[4]) - set(linha[2]))


    imprimirMatriz(matriz)

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
