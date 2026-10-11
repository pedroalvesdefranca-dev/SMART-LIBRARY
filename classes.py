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


class Tela_Inicial:
    def __init__(self,banco,janela,controlador):
        
        self.banco=banco
        self.controlador=controlador
        self.frame={"login":tk.Frame(janela)}
        self.control=False
        self.control1=False
        self.NUM_LINHAS=16
        self.NUM_COLUNAS=9
        self.criar_widgets()

    def mostrar(self,nome):
        self.frame[nome].pack(fill="both", expand=True)
        return self.frame[nome]

    def criar_widgets(self):
        
        login=self.mostrar("login")
        bloco_inferior=tk.Frame(login)
        

        for i in range(self.NUM_LINHAS):
            login.rowconfigure(i,weight=1)

        for j in range(self.NUM_COLUNAS):
            login.columnconfigure(j, weight=1)

        login.rowconfigure(8, weight=3) 
        self.error_label=tk.Label(login, text="", fg="red")
        self.error_label.grid(row=7, column=1, columnspan=7)

        tk.Label(login,text="Bem-Vindo(a)",font=("Arial", 16, "bold")).grid(row=0,column=1,columnspan=7,pady=20)

        id_main_text=tk.Label(login,text="ID")
        self.id_input=tk.Entry(login)


        cpf_main_text=tk.Label(login,text="CPF")
        self.cpf_input=tk.Entry(login)

        
        id_main_text.grid(row=2,column=1,columnspan=7,padx=10, pady=5)
        self.id_input.grid(row=3,column=1,columnspan=7,padx=10, pady=5)
        cpf_main_text.grid(row=4,column=1,columnspan=7,padx=10, pady=5)
        self.cpf_input.grid(row=5,column=1,columnspan=7,padx=10, pady=5)

        botao_main_acesso=tk.Button(login, text="acessar",width=10,height=2,command=lambda:self.acessar_login())
        botao_main_acesso.grid(row=6,column=1,columnspan=7)

        bloco_inferior.grid(row=15,column=0,columnspan=9,sticky="se",padx=15,pady=15)
        mensagem_cadastro1=tk.Label(bloco_inferior,text="Não possui login?")
        mensagem_cadastro2=tk.Label(bloco_inferior,text="Realize o cadastro da nossa biblioteca")
        botao_cadastro=tk.Button(bloco_inferior, text="Cadastrar-se",width=11,height=2,command=lambda:self.controlador.ir_para_cadastramento())
        
        mensagem_cadastro1.pack()
        mensagem_cadastro2.pack()
        botao_cadastro.pack(pady=5)
    

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

class Cadastramento:
    def __init__(self,banco,janela,controlador):
        self.banco=banco
        self.controlador=controlador
        self.frame={
                "1_cadastro": tk.Frame(janela),
                "2_cadastro": tk.Frame(janela),
                "3_cadastro": tk.Frame(janela),
                }
                
        self.control=False
        self.control1=False
        self.NUM_LINHAS=16
        self.NUM_COLUNAS=9
        self.primeira_etapa_cadastro()
    
    def mostrar(self,nome):
             for frame in self.frame.values():
                  frame.pack_forget()
             self.frame[nome].pack(fill="both", expand=True)
             return self.frame[nome]
        
    def primeira_etapa_cadastro(self):
            self.control=True
            primeira_etapa=self.mostrar("1_cadastro")
            bloco_inferior=tk.Frame(primeira_etapa)

            for i in range(self.NUM_LINHAS):
                primeira_etapa.rowconfigure(i, weight=1)
            
            for j in range(self.NUM_COLUNAS):
                primeira_etapa.columnconfigure(j, weight=1)

            titulo=tk.Label(primeira_etapa,text="Preencha Todos os campos a seguir")
    
            m_nome=tk.Label(primeira_etapa,text="Nome")
            self.nome=tk.Entry(primeira_etapa)
    
            m_sobrenome=tk.Label(primeira_etapa,text="Sobrenome")
            self.sobrenome=tk.Entry(primeira_etapa)
    
            m_cpf=tk.Label(primeira_etapa,text="CPF (somente números)")
            self.cpf=tk.Entry(primeira_etapa)
            
    
            m_celular=tk.Label(primeira_etapa,text="Celular (somente números deve conter o DDD)")
            self.celular=tk.Entry(primeira_etapa)
            
    
            m_email=tk.Label(primeira_etapa,text="email")
            self.email=tk.Entry(primeira_etapa)
            
    
            botao_de_finalizacao_cadastro=tk.Button(primeira_etapa,text="Finalizar",width=11,height=2,command=lambda:self.segunda_etapa_cadastro() )
            self.error_label_cadastro=tk.Label(primeira_etapa, text="", fg="red")

            titulo.grid(row=0,column=1,columnspan=7,pady=20)
            m_nome.grid(row=2,column=1,columnspan=7,padx=10,pady=10)
            self.nome.grid(row=3,column=1,columnspan=7,padx=5,pady=5)
            m_sobrenome.grid(row=4,column=1,columnspan=7,padx=10,pady=10)
            self.sobrenome.grid(row=5,column=1,columnspan=7,padx=5,pady=5)
            m_cpf.grid(row=6,column=1,columnspan=7,padx=10,pady=10)
            self.cpf.grid(row=7,column=1,columnspan=7,padx=5,pady=5)
            m_celular.grid(row=8,column=1,columnspan=7,padx=10,pady=10)
            self.celular.grid(row=9,column=1,columnspan=7,padx=5,pady=5)
            m_email.grid(row=10,column=1,columnspan=7,padx=10,pady=10)
            self.email.grid(row=11,column=1,columnspan=7,padx=5,pady=5)
            botao_de_finalizacao_cadastro.grid(row=12,column=1,columnspan=7,padx=10,pady=10)
            self.error_label_cadastro.grid(row=13,column=1,columnspan=7,padx=15,pady=15)

            primeira_etapa.rowconfigure(14, weight=3)


            bloco_inferior.grid(row=15,column=0,columnspan=9,sticky="se",padx=15,pady=15)
            tk.Button(bloco_inferior,text="Voltar",width=6,height=2,command=lambda:self.quarta_etapa_cadastro()).pack()

            

    def segunda_etapa_cadastro(self):
        primeira_etapa=self.mostrar("1_cadastro")
        if self.nome.get()=="" or self.sobrenome.get()=="":
            self.error_label_cadastro.config(text="NOME/SOBRENOME INVALIDO")
            primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
            return

        if not self.nome.get().isalpha():
             self.error_label_cadastro.config(text="NOME/SOBRENOME INVALIDO")
             primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
             return

        variavel=self.sobrenome.get().split()
        for caractere in variavel:
            if not caractere.isalpha():
                  self.error_label_cadastro.config(text="NOME/SOBRENOME INVALIDO")
                  primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
                  return

        try:
            int(self.cpf.get())
        except:
            self.error_label_cadastro.config(text="CPF INVALIDO")
            primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
            return
    
        contador_caracteres=len(self.cpf.get())
        if contador_caracteres!=11:
           self.error_label_cadastro.config(text="CPF INVALIDO")
           primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
           return
           
        
        try:
            int(self.celular.get())
        except:
              self.error_label_cadastro.config(text="CELULAR INVALIDO")
              primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
              return
               
        contador_caracteres=len(self.celular.get())
        if contador_caracteres!=11:
            self.error_label_cadastro.config(text="CELULAR INVALIDO")
            primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
            return
            
        validador_email="@"
        if validador_email not in self.email.get():
           self.error_label_cadastro.config(text="EMAIL INVALIDO")
           primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
           return
           
    
        try:
            resposta=self.banco.buscar_one("SELECT EXISTS(SELECT 1 FROM CUSTOMERS WHERE CPF=?);",(self.cpf.get(),))
        
            if resposta[0]:
             self.error_label_cadastro.config(text="CPF JÁ CADASTRADO")
             primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
             return
            
               
            else:
                try:
                    self.banco.executar('''INSERT INTO CUSTOMERS (First_name,Last_name,CPF,Cellphone,Email,Registration_Date) 
                    VALUES (?,?,?,?,?,DATE('now'));''',(self.nome.get().lower(),self.sobrenome.get().lower(),
                                                        self.cpf.get(),self.celular.get(),self.email.get()))
                    self.controlador_cadastro2()
    
                except Exception as erro:
                    self.error_label_cadastro.config(primeira_etapa,text=f"Erro ao realizar cadastro, tente novamente {erro}")
                    primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
                    return
        except Exception as e:
            self.error_label_cadastro.config(primeira_etapa,text=f"Erro ao Tentar Conectar ao Banco de Dados, tente novamente {erro}")
            primeira_etapa.after(8000,lambda:self.error_label_cadastro.config(text=""))
            return
           
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
        self.controlador.tela_login.id_input.delete(0,tk.END)
        self.controlador.tela_login.cpf_input.delete(0,tk.END)
        self.controlador.inicio_programa()
        self.controlador.inicio_programa()

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
        self.controlador.inicio_programa()
            