import sqlite3
import tkinter as tk

def conectar():
    conexao=sqlite3.connect("biblioteca.db")
    return conexao

def cadastrar_usuarios(first_name,last_name,cpf,email,telefone):
    cursor=conectar().cursor()
    cursor.execute('''
        INSERT INTO CUSTOMERS
        VALUES (?,?,?,?,?,DATE('NOW'));''',(first_name,last_name,cpf,telefone,email)
    )

def cadastrar_livro(nome,volume,genero,autor,editora):
    cursor=conectar().cursor()
    cursor.execute("INSERT INTO BOOKS VALUES (?,?,?,?,?);",(nome,volume,genero,autor,editora))

def acessar_login(id,cpf,pagina_login):
    try:
        verificador1=int(id)
        verificador2=int(cpf)
    except:
        tk.Label(pagina_login,text="ID/CPF INVALIDOS").pack()
        return    

    try:
        conn=conectar()
        cursor=conn.cursor()
        cursor.execute("SELECT EXISTS( SELECT 1 FROM CUSTOMERS WHERE (id=? AND cpf=?));",(verificador1,verificador2))
        resultado=cursor.fetchone()
        if resultado[0]:
            print("login_encontrado")
        else:
            tk.Label(pagina_login,text="ID/CPF INVALIDOS").pack() 
        cursor.close()
        conn.close()          
    except Exception as erro:
        tk.Label(pagina_login,text=f"ERRO AO TENTAR CONECTAR AO BANCO DE DADOS {erro}").pack() 
        return    

def primeira_etapa_cadastro(pagina_cadastro,pagina_login,pagina_finalizacao_cadastro):
        tk.Label(pagina_cadastro,text="Preencha Todos os campos a seguir").pack()

        tk.Label(pagina_cadastro,text="Nome").pack()
        nome=tk.Entry(pagina_cadastro)
        nome.pack()

        tk.Label(pagina_cadastro,text="Sobrenome").pack()
        sobrenome=tk.Entry(pagina_cadastro)
        sobrenome.pack()

        tk.Label(pagina_cadastro,text="CPF (somente números)").pack()
        cpf=tk.Entry(pagina_cadastro)
        cpf.pack()

        tk.Label(pagina_cadastro,text="Celular (somente números deve conter o DDD)").pack()
        celular=tk.Entry(pagina_cadastro)
        celular.pack()

        tk.Label(pagina_cadastro,text="email").pack()
        email=tk.Entry(pagina_cadastro)
        email.pack()

        botao_de_finalizacao_cadastro=tk.Button(pagina_cadastro,text="Finalizar",width=11,height=2,command=lambda: segunda_etapa_cadastro(pagina_cadastro,nome.get(),sobrenome.get(),cpf.get(),celular.get(),email.get(),pagina_finalizacao_cadastro))
        botao_de_finalizacao_cadastro.pack()

        pagina_login.pack_forget()
        pagina_cadastro.pack()

def segunda_etapa_cadastro(pagina_cadastro,nome,sobrenome,cpf,celular,email,pagina_finalizacao_cadastro):

    if nome=="" or sobrenome=="":
        erro_mensager_0=tk.Label(pagina_cadastro,text="NOME/SOBRENOME INVALIDO",fg='red')
        erro_mensager_0.pack()
        pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
        return
    try:
        int(cpf)
    except:
        erro_mensager_0=tk.Label(pagina_cadastro,text="cpf invalido",fg='red')
        erro_mensager_0.pack()
        pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
        return

    contador_caracteres=len(cpf)
    if contador_caracteres!=11:
       erro_mensager_0=tk.Label(pagina_cadastro,text="cpf invalido",fg='red')
       erro_mensager_0.pack()
       pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
       return
       
    
    try:
        int(celular)
    except:
          erro_mensager_0=tk.Label(pagina_cadastro,text="celular invalido",fg='red')
          erro_mensager_0.pack()
          pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
          return
           
    contador_caracteres=len(celular)
    if contador_caracteres!=11:
        erro_mensager_0=tk.Label(pagina_cadastro,text="celular invalido",fg='red')
        erro_mensager_0.pack()
        pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
        return
        
    validador_email1=".com"
    validador_email2="@"
    if validador_email1 not in email or validador_email2 not in email:
       erro_mensager_0=tk.Label(pagina_cadastro,text="email invalido",fg='red')
       erro_mensager_0.pack()
       pagina_cadastro.after(8000,erro_mensager_0.pack_forget)
       return
       

    try:
        conn=conectar()
        cursor=conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM CUSTOMERS WHERE CPF=?);",(cpf,))
        resposta=cursor.fetchone()
        if resposta[0]:
            erro_mensager_=tk.Label(pagina_cadastro,text="CPF já possui cadastro",fg='red')
            erro_mensager_.pack()
            pagina_cadastro.after(8000,erro_mensager_.pack_forget)
            cursor.close()
            conn.close()
            return
        else:
            try:
                cursor.execute('''INSERT INTO CUSTOMERS (First_name,Last_name,CPF,Cellphone,Email,Registration_Date) 
                VALUES (?,?,?,?,?,DATE('now'));''',(nome,sobrenome,cpf,celular,email))
                conn.commit()
                cursor.close()
                conn.close()
                terceira_etapa_cadastro(pagina_cadastro,pagina_finalizacao_cadastro)

            except Exception as erro:
                erro_mensager_2=tk.Label(pagina_cadastro,text=f"Erro ao realizar cadastro, tente novamente {erro}",fg='red')
                erro_mensager_2.pack()
                pagina_cadastro.after(8000,erro_mensager_2.pack_forget)
                cursor.close()
                conn.close()
                return
    except Exception as e:
        tk.Label(pagina_cadastro,text=f"Erro ao tentar conectar ao servidor {e}",fg='red')
        cursor.close()
        conn.close()
                        
          
def terceira_etapa_cadastro(pagina_cadastro,pagina_finalizacao_cadastro):
    pagina_cadastro.pack_forget()
    pagina_finalizacao_cadastro.pack()
    tk.Label(pagina_finalizacao_cadastro,text="funcionou").pack()        