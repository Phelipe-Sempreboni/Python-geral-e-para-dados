#Exemplo de conexão do Python com o SQL Server com autenticação do SQL Server, com necessidade de senha.
#Notar que o comando abaixo faz a conexão e consulta por input e nome do cliente, conforme abaixo com execução do comando for com loop.
#Notar que, neste caso, faremos a procura por nome do cliente. Isso não pede dos campos serem alterados para outro tipo de pesquisa de acordo com sua necessidade.
#Neste caso, pode ser utilizado quando a autentição for pelo SQL Server, pois, nota-se que possui o campo ("pwd=SENHA").

#Nota: Caso não queira autenticação por SQL Server e sim autenticação por Windows, altere o comando da função (conectar()) chamado (Trusted_Connection) de 'no' para 'yes', e, retire o campo (pwd), pois, conexões com autenticação não necessitam de senhas, logo, o campo pode ser apagado.

#Nota2: Para verificar o (DRIVER) do SQL Server, conforme temos em todos comandos, você pode seguir o caminho: Tecla do Windows ou no pesquisa, digitar (ODBC), irá abrir uma janela com algumas abas, procure por (DRIVERS) e procure os referente a (SQL Server). Lá estarão as informações de (DRIVERS).

#Nota3: Caso queira testar este comando Python com o a consulta (UPDATE) que foi deixada como exemplo, irei deixar abaixo do comando Python, um script para ser executado no SQL Server que irá gerar essa infos.
#Nota4: Copie e cole a parte do SQL Server Management Studio no SQL ou no Visual Studio Code e execute. Leia os passos antes para entender como e o quê executar.

def conectar():

    import pyodbc

    try:
        conexao = pyodbc.connect(
            Driver='{SQL Server Native Client 11.0}', #Altere de acordo com seu driver. A (#Nota4) fala desse assunto.
            Server='SERVIDOR', #Insira seu servidor.
            Database='DATABASENAME',#Insira o nome do banco de dados (database) que você quer conectar.
            uid='USUARIO', #Insira seu usuário.
            pwd='SENHA', #Insira sua senha.
            Trusted_Connection='no' #Este campo em (no) refere-se ao tipo de autentição, neste caso, autenticação SQL Server.
        )
        return conexao.cursor()
    except:
        print('Não foi possível conectar ao banco de dados.')


# Nota: Neste caso, você pode trocar o comando de (SELECT) e os parametros para o que preferir. Irei deixar o exemplo abaixo onde:
# [LPUS_ENERGIA]          = database
# [clientes]              = schema (agrupaemento) da tabela
# [tbl_cadastro_clientes] = tabela criada para cadastro de clientes.

def query():

    import os #Bibliote padrão do Python para o sistema.

    os.system("cls") #Limpa a tela (termina e/ou Output) de execução.

    consultar_registros_cliente = input("Digite o nome: ") #Input para pesquisa na tela de execução.
    #Notar que, neste caso, faremos a procura por nome do cliente. Isso não pede dos campos serem alterados para outro tipo de pesquisa de acordo com sua necessidade.

    try:  
        cursor = conectar()
        cursor.execute("SELECT * FROM [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] WHERE T_NOMECLIENTE LIKE '%"+consultar_registros_cliente+"%'") #Insira sua consulta e neste caso faremos a busca por input, pela variavel (consultar_registros_cliente).
        resultado = cursor.fetchall()
        limite = 25 #Limite de linhas que irão aparecer na tela de execução.
        contador = 0 #Contador para utilização do comando for.
        for r in resultado: #Comando for (laço de repetição). Neste caso, tudo será executado de uma só vez.
            print("ID: {0: <3} Nome: {1: <30} Telefone: {2: <15} E-mail {3: <30}".format(r[0], r[1], r[2], r[3])) #Este é o resultado da query, porém, formatada para aparecer em um formato amigável.
            #"ID: {0: <3} -> Número da coluna, o espaço para diferenciar os caracteres e o <3 indicando a quantidade de caracteres que o ID pode chegar.
            #Válido para todos os outros campos formatados.
            contador+=1; #Contador para utilização do comando for sempre somando de 1 a 1.
            if(contador>=limite): #Contador para utilização do comando for sempre somando de 1 a 1 até chegar no limite, caso 25.
                contador = 0 #Chegando no limite, o contador zera e caso tenha mais registros, ele continuará até o final.
                os.system("pause") #Pausa o comando até que seja apertada alguma tecla. Aqui servirá caso o usuário queira verificar os dados com calma.
                os.system("cls")
    except:
        print('Não foi possível retornar os dados da consulta')
    finally:
        print('Consulta executada com sucesso.')
        os.system("pause")

query()

#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------#------------


#Comandos SQL. Execute no SQL Server Management Studio.
#Notar que, os comandos SQL estão comentados no padrão Python, então copie e cole no SQL e retira essas três aspas simples do inicio e final para não ocorrer erros no SQL Server.

'''
-- 1º Passo: Criar um database para alocar as informações. Criarei um chamado (LPUS_Energia) com nome ficticio.

-- Criação com comando (CREATE TABLE) mais simples, sem parametros.
USE master;
CREATE DATABASE LPUS_ENERGIA;
GO

-- Comando (DROP DATABASE) caso queira execluir 0 banco de dados.
USE master;
DROP DATABASE LPUS_ENERGIA;
GO

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- 2º Passo: Criar um schema (agrupamento) para tabela que iremos criar para cadastros de clientes.

-- Criação com comando (CREATE SCHEMA) mais simples, sem parametros.
USE LPUS_ENERGIA;
GO

CREATE SCHEMA clientes;
GO

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- 3º Passo: Criar a tabela que receberá os dados dos cadastros dos clientes.
-- Essa tabela terá uma chave primária, que será a coluna N_IDCONTATO com autoincremento do número de ID.

-- Criação com comando (CREATE TABLE).
CREATE TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
(
    N_IDCLIENTE INT IDENTITY (1,1) NOT NULL,
    T_NOMECLIENTE VARCHAR (80),
    T_TELEFONECLIENTE VARCHAR (30),
    T_EMAILCLIENTE VARCHAR (50)
    CONSTRAINT PK_N_IDCLIENTE PRIMARY KEY CLUSTERED (N_IDCLIENTE)
);
GO

-- Teste com comando (SELECT) para verificar estrutura da tabela.
SELECT * FROM [LPUS_Energia].[clientes].[tbl_cadastro_clientes]

-- Comando auxiliar de (STORED PROCEDURE) do sistema para verificar estrutura/informações da tabela.
USE LPUS_ENERGIA;
GO

sp_help 'clientes.tbl_cadastro_clientes'

-- Comando de (DROP TABELA) caso seja necessário execluir a tabela criada.
DROP TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]

-- Comando de (TRUNCATE TABLE) caso seja necessário excluir dados da tabela. Essa opção também zera os ids de autoincremento e não é possível recuperar esses dados, pois, não temos arquivos de logs de transações no comando (TRUNCATE TABLE).
-- Você se quiser também pode utilizar o (DELETE), que continua com os ids de autoincremento e tem arquivos de logs de transações para possíveis recuperações.
TRUNCATE TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
DELETE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- Comando abaixo de (INSERT INTO) para fazer testes de inserção, tanto no SQL quanto em Python.

INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Ronaldo Henrique', '1194458264', 'ronaldoe@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Adriano Barbosa', '1194454785', 'adriano@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Eduardo Leão', '1188596347', 'eduardo@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Silvio de Lima', '11974126895', 'silvio@outlook.com')

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x
'''