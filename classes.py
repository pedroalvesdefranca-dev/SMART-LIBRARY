import tkinter as tk
import sqlite3

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
        
        self.criar_widgets()

    def mostrar(self,nome):
         for frame in self.frame.values():
              frame.pack_forget()
         self.frame[nome].pack()
         return self.frame[nome]

    def criar_widgets(self):

        login=self.mostrar("login")

        tk.Label(login,text="Bem-Vindo(a)").pack()

        id_main_text=tk.Label(login,text="ID")
        self.id_input=tk.Entry(login)


        cpf_main_text=tk.Label(login,text="CPF")
        self.cpf_input=tk.Entry(login)


        id_main_text.pack()
        self.id_input.pack()
        cpf_main_text.pack()
        self.cpf_input.pack()

        botao_main_acesso=tk.Button(login, text="acessar",width=10,height=2,command=lambda:self.acessar_login())
        botao_main_acesso.pack()

        mensagem_cadastro=tk.Label(login,text="Não possui login? Realize o cadastro da nossa biblioteca")
        botao_cadastro=tk.Button(login, text="Cadastrar",width=11,height=2,command=lambda: self.primeira_etapa_cadastro())
        mensagem_cadastro.pack(side="bottom")
        botao_cadastro.pack(side="bottom") 

    def acessar_login(self):

         login=self.mostrar("login")

         try:
                verificador1=int(self.id_input.get())
                verificador2=int(self.cpf_input.get())
         except:
                mensagem=tk.Label(login,text="ID/CPF INVALIDOS",fg='red')
                mensagem.pack()
                login.after(3000,mensagem.pack_forget)
                return    
        
         try:
                
                resultado=self.banco.buscar_one("SELECT EXISTS( SELECT 1 FROM CUSTOMERS WHERE (id=? AND cpf=?));",(verificador1,verificador2))
                
                if resultado[0]:
                    self.controlador.ir_para_menu()
                else:
                    mensagem=tk.Label(login,text="ID/CPF INVALIDOS",fg='red')
                    mensagem.pack()
                    login.after(3000,mensagem.pack_forget) 
                          
         except Exception as erro:
                tk.Label(login,text=f"ERRO AO TENTAR CONECTAR AO BANCO DE DADOS {erro}").pack() 
                return    

    def primeira_etapa_cadastro(self):

            primeira_etapa=self.mostrar("1_cadastro")
            tk.Label(primeira_etapa,text="Preencha Todos os campos a seguir").pack()
    
            tk.Label(primeira_etapa,text="Nome").pack()
            self.nome=tk.Entry(primeira_etapa)
            self.nome.pack()
    
            tk.Label(primeira_etapa,text="Sobrenome").pack()
            self.sobrenome=tk.Entry(primeira_etapa)
            self.sobrenome.pack()
    
            tk.Label(primeira_etapa,text="CPF (somente números)").pack()
            self.cpf=tk.Entry(primeira_etapa)
            self.cpf.pack()
    
            tk.Label(primeira_etapa,text="Celular (somente números deve conter o DDD)").pack()
            self.celular=tk.Entry(primeira_etapa)
            self.celular.pack()
    
            tk.Label(primeira_etapa,text="email").pack()
            self.email=tk.Entry(primeira_etapa)
            self.email.pack()
    
            botao_de_finalizacao_cadastro=tk.Button(primeira_etapa,text="Finalizar",width=11,height=2,command=lambda:self.segunda_etapa_cadastro() )
            botao_de_finalizacao_cadastro.pack()

    def segunda_etapa_cadastro(self):
        primeira_etapa=self.mostrar("1_cadastro")
        if self.nome.get()=="" or self.sobrenome.get()=="":
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
                    self.terceira_etapa_cadastro()
    
                except Exception as erro:
                    erro_mensager_2=tk.Label(primeira_etapa,text=f"Erro ao realizar cadastro, tente novamente {erro}",fg='red')
                    erro_mensager_2.pack()
                    primeira_etapa.after(8000,erro_mensager_2.pack_forget)
                    return
        except Exception as e:
            tk.Label(primeira_etapa,text=f"Erro ao tentar conectar ao servidor {e}",fg='red')
           
    def terceira_etapa_cadastro(self):

        pagina_finalizacao_cadastro=self.mostrar("2_cadastro")

        tk.Label(pagina_finalizacao_cadastro,text="CADASTRO REALIZADO COM SUCESSO").pack()
        tk.Label(pagina_finalizacao_cadastro,text="SEU ID DE LOGIN É:").pack()
        
        id_do_usuario=self.banco.buscar_one("SELECT ID FROM CUSTOMERS WHERE CPF=?;",(self.cpf.get(),))
        tk.Label(pagina_finalizacao_cadastro,text=f"({id_do_usuario[0]})",fg="blue").pack()
        
        tk.Button(pagina_finalizacao_cadastro,text="retornar ao login",command=lambda: self.quarta_etapa_cadastro()).pack()

    def quarta_etapa_cadastro(self):
        self.mostrar("login")                                              

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

        botao_sair = tk.Button(self.lateral, text="Sair", command=self.controlador.ir_para_login)
        botao_sair.pack(side="bottom", pady=10)