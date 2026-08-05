import sqlite3

#criando banco de dados .db e atualizando ele com a criação das tabelas
#ja definidas no arquivo tabelas.sql
with open('sql/tabelas.sql','r',encoding='utf-8') as arquivo_sql:
    conteudo=arquivo_sql.read()


import tkinter as tk
from tkinter import *

from classes import *




class Controlador:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Biblioteca")
        self.janela.geometry("400x400")

        self.banco = Banco()

        # cria as telas passando "self" (o controlador) pra cada uma
        self.tela_login = Tela_login(self.banco, self.janela, self)
        self.menu = Menu(self.banco, self.janela, self)

        # tela inicial
        self.ir_para_login()

    def ir_para_login(self):
        self.esconder_todos(self.menu)
        self.menu.lateral.pack_forget()
        self.tela_login.mostrar("login")

    def ir_para_menu(self):
        self.esconder_todos(self.tela_login)
        self.menu.lateral.pack(side="left", fill="y")
        self.menu.mostrar("principal")

    def esconder_todos(self, tela):
        for frame in tela.frame.values():
            frame.pack_forget()

    def rodar(self):
        self.janela.mainloop()



app = Controlador()
app.rodar()



