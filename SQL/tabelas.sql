CREATE TABLE IF NOT EXISTS CUSTOMERS (
    ID INTEGER  PRIMARY KEY AUTOINCREMENT,
    First_Name Varchar(255) NOT NULL,
    Last_Name Varchar(255) NOT NULL,
    CPF Varchar(255) NOT NULL UNIQUE,
    Cellphone Varchar(255) NOT NULL,
    Email Varchar(255) NOT NULL,
    Registration_Date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS BOOKS (
   Codigo INTEGER PRIMARY KEY AUTOINCREMENT,
   Name Varchar(255) NOT NULL,
   volume Varchar(255) not NULL,
   genero Varchar(255) not NULL,
   autor Varchar(255) not NULL,
   editora Varchar(255) not NULL
);

CREATE TABLE IF NOT EXISTS EMPRESTIMOS(
    EMPRESTIMO_ID INTEGER PRIMARY KEY,
    ID not NULL,
    Codigo not NULL,
    Data_emprestimo datetime not NULL, 
    Data_devolução datetime Check (Data_devolução>Data_emprestimo OR Data_devolução IS NULL),
    Status Varchar(255) not NULL,
    CONSTRAINT fk_id FOREIGN KEY (ID) REFERENCES CUSTOMERS(ID),
    CONSTRAINT fk_codigo FOREIGN KEY (Codigo) REFERENCES BOOKS(Codigo) 
);