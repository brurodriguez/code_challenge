from datetime import datetime
import sqlite3
from datetime import date
con = None
dbname = './BANCO.db'

class BancoDados:

    def create():

        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE TBL_USUARIO (
                ID INTEGER PRIMARY KEY AUTOINCREMENT
                ,CPF TEXT
                ,NOME TEXT
                ,SENHA TEXT
                ,DATA_CADASTRO TEXT
                );
                """
            )
            con.commit()
        except:
            pass
        try:
            cursor.execute(
                """
                CREATE TABLE TBL_SALDO (
                ID_SALDO INTEGER PRIMARY KEY AUTOINCREMENT
                ,CPF TEXT
                ,SALDO TEXT DEFAULT "0" NOT NULL
                ,DATA_REGISTRO TEXT
                );
                """
            )
            con.commit()
        except:
            pass
        try:
            cursor.execute(
                """
                CREATE TABLE TBL_TRANSACOES (
                ID_TRANSACAO INTEGER PRIMARY KEY AUTOINCREMENT
                ,CPF TEXT
                ,SALDO_ANTIGO NUMERIC
                ,TRANSFERENCIA NUMERIC
                ,SALDO_ATUALIZADO NUMERIC
                ,CONTA_TRANSFERIDA NUMERIC
                ,DATA_REGISTRO TEXT
                );
                """
            )
            con.commit()
        except sqlite3.Error as e:
            print(e)

        cursor.close()
        con.close()
        return

    def insertCadastro(cpf,nome,senha):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()
        try:
            cursor.execute(
                f"""
                INSERT INTO TBL_USUARIO (
                CPF
                ,NOME
                ,SENHA
                ,DATA_CADASTRO
                ) VALUES ('{cpf}','{nome}','{senha}','{datetime.now()}');
                """
            )
            con.commit()
            cursor.close()
            con.close()
            return "1"
        except sqlite3.Error as e:
            print(e)
            cursor.close()
            con.close()
            return 'erro: ' + e

    def insertTransacoes(cpf,saldoAntigo,transferencia,contaficticia):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()

        saldoAtual = float(saldoAntigo) - float(transferencia)

        try:
            cursor.execute(
                f"""
                INSERT INTO TBL_TRANSACOES (
                 CPF   
                ,SALDO_ANTIGO
                ,TRANSFERENCIA
                ,SALDO_ATUALIZADO
                ,CONTA_TRANSFERIDA
                ,DATA_REGISTRO
                ) VALUES ('{cpf}','{saldoAntigo}','{transferencia}','{saldoAtual}','{contaficticia}','{datetime.now()}');
                """
            )
            con.commit()
            cursor.execute(
                f"""
                UPDATE TBL_SALDO 
                SET SALDO = '{str(saldoAtual)}'
                , DATA_REGISTRO = '{datetime.now()}'
                WHERE CPF = '{cpf}';
                """
            )
            con.commit()
            cursor.close()
            con.close()
            return "1"
        except sqlite3.Error as e:
            print(e)
            cursor.close()
            con.close()
            return 'erro: ' + e

    def insertDeposito(cpf,valorDeposito):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()
        cursor.execute(f"SELECT SALDO FROM TBL_SALDO WHERE CPF = '{cpf}' ORDER BY DATA_REGISTRO DESC")
        contadorCPF = cursor.fetchone()
        saldoantigo = 0

        if contadorCPF is None:
            saldoantigo = 0
            saldoatual = float(saldoantigo) + float(valorDeposito)
            print(saldoatual)
            try:
                cursor.execute(
                    f"""
                    INSERT INTO TBL_SALDO (CPF, SALDO, DATA_REGISTRO)
                    VALUES ('{cpf}', '{str(saldoatual)}','{datetime.now()}');                    
                    """
                )
                con.commit()
                cursor.close()
                con.close()
                return "1"
            except sqlite3.Error as e:
                print(e)
                cursor.close()
                con.close()
                return 'erro: ' + e          

        else:
            saldoantigo = contadorCPF[0]  
            saldoatual = float(saldoantigo) + float(valorDeposito)
            print(saldoatual)

            try:
                cursor.execute(
                    f"""
                    UPDATE TBL_SALDO 
                    SET SALDO = '{str(saldoatual)}'
                    , DATA_REGISTRO = '{datetime.now()}'
                    WHERE CPF = '{cpf}';
                    """
                )
                con.commit()
                cursor.close()
                con.close()
                return "1"
            except sqlite3.Error as e:
                print(e)
                cursor.close()
                con.close()
                return 'erro: ' + e            

    def insertSaque(cpf,valorSaque):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()
        cursor.execute(f"SELECT SALDO FROM TBL_SALDO WHERE CPF = '{cpf}' ORDER BY DATA_REGISTRO DESC")
        contadorCPF = cursor.fetchone()

        saldoantigo = 0
        if contadorCPF is None:
            saldoantigo = 0
        else:
            saldoantigo = contadorCPF[0]

        if float(valorSaque) > float(saldoantigo):
            return "0"
        else:
            saldoatual = float(saldoantigo) - float(valorSaque)

            try:
                cursor.execute(
                    f"""
                    UPDATE TBL_SALDO 
                    SET SALDO = '{str(saldoatual)}'
                    , DATA_REGISTRO = '{datetime.now()}'
                    WHERE CPF = '{cpf}';
                    """
                )
                con.commit()
                cursor.close()
                con.close()
                return "1"
            except sqlite3.Error as e:
                print(e)
                cursor.close()
                con.close()
                return 'erro: ' + e


    def consultaCPF(cpf):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')
        except sqlite3.Error as e:
            print(e)
            exit(1)

        cursor = con.cursor()
        try:
            cursor = con.cursor()
            consulta = cursor.execute(f"SELECT COUNT(CPF) FROM TBL_USUARIO WHERE CPF = '{cpf}'")
            print(consulta)
            contadorCPF = cursor.fetchone()

            return contadorCPF[0]
        except sqlite3.Error as e:
            print(e)
            return 'erro: ' + e

    def consultaLogin(cpf,senha):
        try:
            con = sqlite3.connect(dbname)
            print('The database is successfully open ')

            cursor = con.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM TBL_USUARIO WHERE CPF = '{cpf}'  AND SENHA = '{senha}'")
            contadorCPF = cursor.fetchone()

            return contadorCPF[0]
        except sqlite3.Error as e:
            print(e)
            return 'erro: ' + e

    def consultaContaUsuario(cpf):
        try:
            cursor = con.cursor()
            cursor.execute(f"SELECT COUNT(CPF) FROM TBL_USUARIO WHERE CPF = '{cpf}'")
            contadorCPF = cursor.fetchone()
            return contadorCPF
        except sqlite3.Error as e:
            print(e)
            return 'erro: ' + e
    
    def consultasaldo(cpf):
        try:
            con = sqlite3.connect(dbname)
            cursor = con.cursor()
            cursor.execute(f"SELECT SALDO FROM TBL_SALDO WHERE CPF = '{cpf}' ORDER BY DATA_REGISTRO DESC")
            contadorCPF = cursor.fetchone()
            if contadorCPF is None:
                return "0"
            else:    
                return contadorCPF

        except sqlite3.Error as e:
            print(e)
            return 'erro: ' + e