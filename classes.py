import tkinter as tk
import sqlite3
from datetime import datetime

class Banco():
    def __init__(self):
        self.conn = sqlite3.connect("biblioteca.db")
        self.cursor = self.conn.cursor()
        with open('sql/tabelas.sql','r',encoding='utf-8') as arquivo_sql:
            comandos_sql=arquivo_sql.read()
        self.cursor.executescript(comandos_sql)    

    def executar(self,comando,parametro=()):
        self.cursor.execute(comando,parametro)
        self.conn.commit()

    def buscar_all(self,comando,parametro=()):
        self.cursor.execute(comando,parametro)
        return self.cursor.fetchall()

    def buscar_one(self,comando,parametro=()):
        self.cursor.execute(comando,parametro)
        return self.cursor.fetchone()      


class Tela_login:
    def __init__(self,banco,janela,controlador):
        
        self.banco=banco
        self.controlador=controlador
        self.frame={
                     "login": tk.Frame(janela),
                     "1_cadastro": tk.Frame(janela),
                     "2_cadastro": tk.Frame(janela),
                     "3_cadastro": tk.Frame(janela),
        }
        
        self.control=False
        self.control1=False
        self.criar_widgets()

    def mostrar(self,nome):
         for frame in self.frame.values():
              frame.pack_forget()
         self.frame[nome].pack(fill="both", expand=True)
         return self.frame[nome]

    def criar_widgets(self):

        login=self.mostrar("login")
        bloco_inferior=tk.Frame(login)
        NUM_LINHAS=16
        NUM_COLUNAS=9

        for i in range(NUM_LINHAS):
            login.rowconfigure(i, weight=1, minsize=50)

        for j in range(NUM_COLUNAS):
            login.columnconfigure(j, weight=1, minsize=50)

        self.error_label=tk.Label(login, text="", fg="red")
        self.error_label.grid(row=7, column=1, columnspan=7)

        tk.Label(login,text="Bem-Vindo(a)",font=("Arial", 16, "bold")).grid(row=0,column=1,columnspan=7)

        id_main_text=tk.Label(login,text="ID")
        self.id_input=tk.Entry(login)


        cpf_main_text=tk.Label(login,text="CPF")
        self.cpf_input=tk.Entry(login)

        
        id_main_text.grid(row=2,column=1,columnspan=7,padx=10, pady=10)
        self.id_input.grid(row=3,column=1,columnspan=7,padx=10, pady=10)
        cpf_main_text.grid(row=4,column=1,columnspan=7,padx=10, pady=10)
        self.cpf_input.grid(row=5,column=1,columnspan=7,padx=10, pady=10)

        botao_main_acesso=tk.Button(login, text="acessar",width=10,height=2,command=lambda:self.acessar_login())
        botao_main_acesso.grid(row=6,column=1,columnspan=7)

        bloco_inferior.grid(row=13,column=7,rowspan=2)
        mensagem_cadastro1=tk.Label(bloco_inferior,text="Não possui login?")
        mensagem_cadastro2=tk.Label(bloco_inferior,text="Realize o cadastro da nossa biblioteca")
        botao_cadastro=tk.Button(bloco_inferior, text="Cadastrar-se",width=11,height=2,command=lambda:self.primeira_etapa_cadastro())
        
        mensagem_cadastro1.pack()
        mensagem_cadastro2.pack()
        botao_cadastro.pack()
    

    def acessar_login(self):

         login=self.mostrar("login")
         try:
                verificador1=int(self.id_input.get())
                verificador2=int(self.cpf_input.get())
         except:
                self.error_label.config(text="ID/CPF INVALIDOS")  
                login.after(3000,lambda:self.error_label.config(text=""))     
                return    
        
         try:
                
                resultado=self.banco.buscar_one("SELECT EXISTS( SELECT 1 FROM CUSTOMERS WHERE (id=? AND cpf=?));",(verificador1,verificador2))
                
                if resultado[0]:
                    self.controlador.ir_para_menu()
                else:
                    self.error_label.config(text=f"ERRO AO TENTAR CONECTAR AO BANCO DE DADOS {erro}")
                    login.after(3000,lambda:self.error_label.config(text=""))   
         except Exception as erro:
                self.error_label.config(text=f"ERRO AO TENTAR CONECTAR AO BANCO DE DADOS {erro}")  
                login.after(3000,lambda:self.error_label.config(text=""))   
                return    
   
    def primeira_etapa_cadastro(self):

            self.control=True
            primeira_etapa=self.mostrar("1_cadastro")
            tk.Label(primeira_etapa,text="Preencha Todos os campos a seguir").pack(pady=10)
    
            tk.Label(primeira_etapa,text="Nome").pack(pady=10)
            self.nome=tk.Entry(primeira_etapa)
            self.nome.pack()
    
            tk.Label(primeira_etapa,text="Sobrenome").pack(pady=10)
            self.sobrenome=tk.Entry(primeira_etapa)
            self.sobrenome.pack()
    
            tk.Label(primeira_etapa,text="CPF (somente números)").pack(pady=10)
            self.cpf=tk.Entry(primeira_etapa)
            self.cpf.pack()
    
            tk.Label(primeira_etapa,text="Celular (somente números deve conter o DDD)").pack(pady=10)
            self.celular=tk.Entry(primeira_etapa)
            self.celular.pack(pady=10)
    
            tk.Label(primeira_etapa,text="email").pack(pady=10)
            self.email=tk.Entry(primeira_etapa)
            self.email.pack(pady=10)
    
            botao_de_finalizacao_cadastro=tk.Button(primeira_etapa,text="Finalizar",width=11,height=2,command=lambda:self.segunda_etapa_cadastro() )
            botao_de_finalizacao_cadastro.pack(pady=10)

    def segunda_etapa_cadastro(self):
        primeira_etapa=self.mostrar("1_cadastro")
        if self.nome.get()=="" or self.sobrenome.get()=="":
            erro_mensager_0=tk.Label(primeira_etapa,text="NOME/SOBRENOME INVALIDO",fg='red')
            erro_mensager_0.pack()
            primeira_etapa.after(8000,erro_mensager_0.pack_forget)
            return

        if not self.nome.get().isalpha():
            erro_mensager_0=tk.Label(primeira_etapa,text="NOME/SOBRENOME INVALIDO",fg='red')
            erro_mensager_0.pack()
            primeira_etapa.after(8000,erro_mensager_0.pack_forget)
            return

        variavel=self.sobrenome.get().split()
        for caractere in variavel:
            if not caractere.isalpha():
                 erro_mensager_0=tk.Label(primeira_etapa,text="NOME/SOBRENOME INVALIDO",fg='red')
                 erro_mensager_0.pack()
                 primeira_etapa.after(8000,erro_mensager_0.pack_forget)
                 return

        try:
            int(self.cpf.get())
        except:
            erro_mensager_0=tk.Label(primeira_etapa,text="cpf invalido",fg='red')
            erro_mensager_0.pack()
            primeira_etapa.after(8000,erro_mensager_0.pack_forget)
            return
    
        contador_caracteres=len(self.cpf.get())
        if contador_caracteres!=11:
           erro_mensager_0=tk.Label(primeira_etapa,text="cpf invalido",fg='red')
           erro_mensager_0.pack()
           primeira_etapa.after(8000,erro_mensager_0.pack_forget)
           return
           
        
        try:
            int(self.celular.get())
        except:
              erro_mensager_0=tk.Label(primeira_etapa,text="celular invalido",fg='red')
              erro_mensager_0.pack()
              primeira_etapa.after(8000,erro_mensager_0.pack_forget)
              return
               
        contador_caracteres=len(self.celular.get())
        if contador_caracteres!=11:
            erro_mensager_0=tk.Label(primeira_etapa,text="celular invalido",fg='red')
            erro_mensager_0.pack()
            primeira_etapa.after(8000,erro_mensager_0.pack_forget)
            return
            
        validador_email1=".com"
        validador_email2="@"
        if validador_email1 not in self.email.get() or validador_email2 not in self.email.get():
           erro_mensager_0=tk.Label(primeira_etapa,text="email invalido",fg='red')
           erro_mensager_0.pack()
           primeira_etapa.after(8000,erro_mensager_0.pack_forget)
           return
           
    
        try:
            resposta=self.banco.buscar_one("SELECT EXISTS(SELECT 1 FROM CUSTOMERS WHERE CPF=?);",(self.cpf.get(),))
        
            if resposta[0]:
                erro_mensager_=tk.Label(primeira_etapa,text="CPF já possui cadastro",fg='red')
                erro_mensager_.pack()
                primeira_etapa.after(8000,erro_mensager_.pack_forget)
            
                return
            else:
                try:
                    self.banco.executar('''INSERT INTO CUSTOMERS (First_name,Last_name,CPF,Cellphone,Email,Registration_Date) 
                    VALUES (?,?,?,?,?,DATE('now'));''',(self.nome.get().lower(),self.sobrenome.get().lower(),
                                                        self.cpf.get(),self.celular.get(),self.email.get()))
                    self.controlador_cadastro2()
    
                except Exception as erro:
                    erro_mensager_2=tk.Label(primeira_etapa,text=f"Erro ao realizar cadastro, tente novamente {erro}",fg='red')
                    erro_mensager_2.pack()
                    primeira_etapa.after(8000,erro_mensager_2.pack_forget)
                    return
        except Exception as e:
            tk.Label(primeira_etapa,text=f"Erro ao tentar conectar ao servidor {e}",fg='red')
           
    def terceira_etapa_cadastro(self):

        self.control1=True

        pagina_finalizacao_cadastro=self.mostrar("2_cadastro")

        tk.Label(pagina_finalizacao_cadastro,text="CADASTRO REALIZADO COM SUCESSO").pack()
        tk.Label(pagina_finalizacao_cadastro,text="SEU ID DE LOGIN É:").pack()
        
        id_do_usuario=self.banco.buscar_one("SELECT ID FROM CUSTOMERS WHERE CPF=?;",(self.cpf.get(),))
        self.mensagem_2=tk.Label(pagina_finalizacao_cadastro,text=f"({id_do_usuario[0]})",fg="blue")
        self.mensagem_2.pack()
        
        tk.Button(pagina_finalizacao_cadastro,text="retornar ao login",command=lambda: self.quarta_etapa_cadastro()).pack()

    def quarta_etapa_cadastro(self):
        self.mostrar("login")

    def controlador_cadastro1(self):
        
        if self.control==False:
            self.primeira_etapa_cadastro()
            return
        else:
            self.mostrar("1_cadastro")
            self.nome.delete(0,tk.END)
            self.sobrenome.delete(0,tk.END)
            self.cpf.delete(0,tk.END)
            self.celular.delete(0,tk.END)
            self.email.delete(0,tk.END)

    def controlador_cadastro2(self):
        if self.control1==False:
            self.terceira_etapa_cadastro()   
        else:
            
            id_do_usuario=self.banco.buscar_one("SELECT ID FROM CUSTOMERS WHERE CPF=?;",(self.cpf.get(),))
            self.mensagem_2.config(text=f"({id_do_usuario[0]})",fg="blue")
            self.mostrar("2_cadastro")



class Menu:
    def __init__(self, banco, janela, controlador):
        self.banco = banco
        self.controlador = controlador

        # lateral é FIXA, fora do dicionário de troca
        self.lateral = tk.Frame(janela, width=180, bg="#2c3e50")
        self.lateral.pack(side="left", fill="y")
        self.lateral.pack_propagate(False)
        

        # só as telas que alternam ficam no dicionário
        self.frame = {
            "principal": tk.Frame(janela),
            "2_cadastro": tk.Frame(janela),
        }

        self.criar_widgets()

    def mostrar(self, nome):
        for frame in self.frame.values():
            frame.pack_forget()
        self.frame[nome].pack(side="right", fill="both", expand=True)
        return self.frame[nome]

    def criar_widgets(self):
        principal = self.mostrar("principal")
        tk.Label(principal, text="Bem-vindo ao Menu").pack()

        botao_sair = tk.Button(self.lateral, text="Sair", command=lambda: self.retornar_ao_login())
        botao_sair.pack(side="bottom", pady=10)
        self.label_saudacao = tk.Label(principal, text="")
        self.label_saudacao.pack()
        

    def mostrar_name(self):

        try:
            agora=datetime.now()
            horas=agora.hour
            if 5<=horas<12:
                saudacao="Bom Dia"
            elif 12<=horas<18:
                saudacao="Boa Tarde"
            else:
                saudacao="Boa Noite"        

            id_acessado=self.controlador.tela_login.id_input.get()
            resultado=self.banco.buscar_one("SELECT First_Name,Last_Name FROM CUSTOMERS WHERE ID=?;",(id_acessado,))
            nome,sobrenome=resultado
            self.label_saudacao.config(text=f"{saudacao}! {nome.title()}, {sobrenome.title()}")
            
        except:
            return      

    def retornar_ao_login(self):
        self.controlador.tela_login.id_input.delete(0,tk.END)
        self.controlador.tela_login.cpf_input.delete(0,tk.END)
        self.controlador.ir_para_login()
            