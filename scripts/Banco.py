import mysql.connector
import json
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

class Banco():

    def __init__(self):
        dbconfig = {
            "host":     config.get("MYSQL", "host"),
            "user":     config.get("MYSQL", "user"),
            "passwd":   config.get("MYSQL", "passwd"),
            "db":       config.get("MYSQL", "db"),
        }

        self.conn = mysql.connector.connect(pool_name = "mypool", pool_size = 10,**dbconfig)
        self.cursor = self.conn.cursor();

    def verificarExistenciaDeTokensNaBase(self, tokens):
        for token in tokens:
            self.cursor.execute("""SELECT 1 from startstop where token like %s""", (token,))
            if(not self.cursor.fetchone()):
                self.cursor.execute("""INSERT INTO startstop(token, continuar) VALUES (%s,0)""", (token,) )
                self.conn.commit()


    def getListaReposParaVerificarTestes(self):
        linhas = self.cursor.execute("""
                SELECT nameWithOwner from repositorios
                    where temTeste is null
                    and prs_recuperados is null
            """)
        return self.cursor.fetchall();



    def getRepoParaRecuperarPRs(self):
        retorno = False;
        linhas = self.cursor.execute("""
                SELECT * from repositorios
                    where temTeste = 1
                    and prs_recuperados is null
                    -- and temTeste = 0
                    limit 1
            """)
        for linha in self.cursor.fetchall():
            retorno = linha

        return retorno;
    

    def getPullRequestsToAnalizer(self):

        retorno = False;
        linhas = self.cursor.execute("""
                SELECT b.* from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    limit 1
            """)
        for linha in self.cursor.fetchall():
            retorno = linha

        return retorno;

    def getPullRequestsToAnalizerOrder(self):

        retorno = False;
        linhas = self.cursor.execute("""
                SELECT b.* from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    order by id desc
                    limit 1
            """)
        for linha in self.cursor.fetchall():
            retorno = linha

        return retorno;

    def getPullRequestsToAnalizerRange(self, inicio, fim):

        retorno = False;
        linhas = self.cursor.execute("""
                SELECT b.* from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    and b.id >= """+str(inicio)+""" 
                    and b.id <= """+str(fim)+"""
                    order by id desc
                    limit 1
            """)
        for linha in self.cursor.fetchall():
            retorno = linha

        return retorno;


    def getPullRequestsToAnalizerPull(self):
        linhas = self.cursor.execute("""
                SELECT b.* from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    order by b.id
                    limit 20
            """)

        return self.cursor.fetchall();



    def novoRepositorio(self, id, node_id, name, full_name,html_url,  jsonData):
        self.cursor.execute(
            """INSERT INTO repositorios(id, node_id, name, full_name, html_url, data) 
                    VALUES (%s,%s,%s,%s,%s,%s)""", (id, node_id, name, full_name, html_url, jsonData) )
        self.conn.commit()


    def salvarPR(self, repo_id, github_id, number, state, locked, user, user_id, url, created_at, updated_at):
        self.cursor.execute(
            """
                INSERT INTO 
                    pull_requests 
                        (
                            repo_id, 
                            github_id, 
                            number, 
                            state, 
                            locked, 
                            user, 
                            user_id, 
                            url, 
                            created_at, 
                            updated_at)
                    VALUES 
                        ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);


            """, (repo_id, github_id, number, state, locked, user, user_id, url, created_at, updated_at) )
        self.conn.commit()


    def salvarFilesPR(self, pr_id, filename, additions, deletions, sha):
        self.cursor.execute(
            """
                INSERT INTO pull_request_files
                    (pr_id,
                    filename,
                    additions,
                    deletions,
                    sha)
                    VALUES
                    (%s,%s, %s, %s, %s);


            """, (pr_id, filename, additions, deletions, sha) )
        self.conn.commit()

    def registrarPRsEncontrados(self, repo_id):
        self.cursor.execute("""UPDATE repositorios set prs_recuperados = 1 where id = %s""", (repo_id,) )
        self.conn.commit()

    def registraArquivosEncontrados(self, pullRequest):
        self.cursor.execute("""UPDATE pull_requests set pr_analisado = 1 where id = %s""", (pullRequest[0] ,) )
        self.conn.commit()


    def getUltimoId(self):
        retorno = 0;
        linhas = self.cursor.execute("""SELECT id FROM repositorios order by id desc limit 1;""")
        for linha in self.cursor.fetchall():
            retorno = linha[0]
        return retorno;
    

    def setStatusRequest(self, status):
        self.cursor.execute("""UPDATE startstop set continuar = %s where 1=1""", (status,) )
        self.conn.commit()



    def setStatusRequestV2(self, status, token):
        self.cursor.execute("""UPDATE startstop set continuar = %s where token like %s""", (status, token,) )
        self.conn.commit()



    def getStatusRequestV2(self, token):
        retorno = 0;
        linhas = self.cursor.execute("""select * from startstop where token = %s limit 1;""", (token, ) )
        for linha in self.cursor.fetchall():
            retorno = linha[1]
        return retorno;



