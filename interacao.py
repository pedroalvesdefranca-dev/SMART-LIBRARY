import sqlite3

#criando banco de dados .db e atualizando ele com a criação das tabelas
#ja definidas no arquivo tabelas.sql
with open('sql/tabelas.sql','r',encoding='utf-8') as arquivo_sql:
    conteudo=arquivo_sql.read()

conexao=sqlite3.connect("biblioteca.db")
cursor=conexao.cursor()
conexao.executescript(conteudo)
conexao.commit()
conexao.close()

#RODANDO O PROGRAMA
#interface grafica usada tkinter
import tkinter as tk
from tkinter import *
from funcoes import *

#criação da janela onde ocorrerá toda a interação do programa
janela=tk.Tk()
janela.title("BIBLIOTECA INTELIGENTE v0.1")
janela.geometry("700x400")

pagina_login=tk.Frame(janela)
pagina_cadastro=tk.Frame(janela)
pagina_finalizacao_cadastro=tk.Frame(janela)
pagina_login.pack()


tk.Label(pagina_login,text="Bem-Vindo(a)").pack()

#linhas de texto (ID) seguido de caixa de digitação de input
id_main_text=tk.Label(pagina_login,text="ID")
id_input=tk.Entry(pagina_login)

#linhas de texto (CPF) seguido de caixa de digitacao de input
cpf_main_text=tk.Label(pagina_login,text="CPF")
cpf_input=tk.Entry(pagina_login)

#Linhas de ativação
id_main_text.pack()
id_input.pack()
cpf_main_text.pack()
cpf_input.pack()

#BOTÃO DE ACESSO RESPONSAVEL POR ATIVAR A FUNÇÃO QUE VALIDA OU NÃO O ACESSO
botao_main_acesso=tk.Button(pagina_login, text="acessar",width=10,height=2,command=lambda: acessar_login(id_input.get(),cpf_input.get(),pagina_login))
botao_main_acesso.pack()

#botão de cadastro de novos usuarios;
mensagem_cadastro=tk.Label(pagina_login,text="Não possui login? Realize o cadastro da nossa biblioteca")
botao_cadastro=tk.Button(pagina_login, text="Cadastrar",width=11,height=2,command=lambda: primeira_etapa_cadastro(pagina_cadastro,pagina_login,pagina_finalizacao_cadastro))
mensagem_cadastro.pack()
botao_cadastro.pack() 

janela.mainloop()

