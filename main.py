import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import *
from classes import *


class Controlador:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Biblioteca")
        self.janela.geometry("800x600")

        self.banco = Banco()

        # cria as telas passando "self" (o controlador) pra cada uma
        self.tela_login = Tela_Inicial(self.banco, self.janela, self)
        self.menu = Menu(self.banco, self.janela, self)
        self.cadastramento=Cadastramento(self.banco, self.janela, self)

        # tela inicial
        self.inicio_programa()

    def inicio_programa(self):
        self.esconder_todos(self.menu)
        self.esconder_todos(self.cadastramento)
        self.menu.lateral.pack_forget()
        self.tela_login.mostrar("login")

    def ir_para_menu(self):
        self.esconder_todos(self.tela_login)
        self.esconder_todos(self.cadastramento)
        self.menu.lateral.pack(side="left", fill="y")
        self.menu.mostrar("principal")
        self.menu.mostrar_name()

    def ir_para_cadastramento(self):
         self.esconder_todos(self.menu)
         self.esconder_todos(self.tela_login)
         self.menu.lateral.pack_forget()
         self.cadastramento.controlador_cadastro1()

    def esconder_todos(self, tela):
        for frame in tela.frame.values():
            frame.pack_forget()

    def rodar(self):
        self.janela.mainloop()



app = Controlador()
app.rodar()



