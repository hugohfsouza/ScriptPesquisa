# Scripts para Análise de PRs e Arquivos

A pasta Dataset contem um dump da base no final da análise dos repositórios
A pasta scripts contém todos os scripts usados

## Requisitos mínimos:
- Mysql
- Python3

módulos do python:
- mysql.connector
- requests
- configparser
- BeautifulSoup
- PrettyTable


## Instalação
Após ter feito o git clone, execute:
`$ cd scripts`
`$ cp .\example.config.ini config.ini`

Insira seu(s) tokens no arquivo `config.ini` na seção **TOKENS **

Após ter feito isso: 

`$ pip install -r requirements.txt` 

## Módulo
Esta seção irá apresentar uma explicação rápida dos módulos exitentes e a sugestão de ordem de execução

### Módulo 0-BuscaRepos.py:
Este módulo é responsável por aplicar uma query em formato *graphql* na api do Github. 
- Ela vai utilizar o token1 configurado no arquivo `config.ini` .
- Não possui formato de paralelismo na requisição. Ou seja, é possível executar este script 1 por vez. 

Forma de execução (simples):

`python .\0-BuscaRepos.py` 


### Módulo: 1-verificarExistenciaTeste.py
Este módulo irá fazer um scrap na página dos projetos recuperados pelo script 0-BuscaRepos.py e irá verificar se há menções da palavra TEST em seus arquivos. 

Após sua execução, este script irá gerar um arquivo csv com o resultado. Necessário fazer os scripts de update no banco com base no resultado do csv. 

Forma de execução (simples):

`python .\1-verificarExistenciaTeste.py` 


### Módulo 2-buscaListaPrs.py
Este script erá recuperar os PRs abertos e fechados dos repositórios que possuem testes. 
- Ela vai utilizar o token1 configurado no arquivo `config.ini` .
- Não possui formato de paralelismo na requisição. Ou seja, é possível executar este script 1 por vez. 

Forma de execução (simples):

`python .\2-buscaListaPrs.py` 

### Módulo 3-VerLimiteApi.py
Eu julgo que é o principal módulo. É ele que faz o controle de quais tokens podem ou não ser utilizado no módulo 3 (teoricamente o mais pesado e demorado). 

**Este módulo deverá ficar em execução a todo momento. **

Ele irá mostrar o token, qual o limite atual de requisições e em que horário haverá uma próxima janela para o token específico. 

Forma de execução (simples):

`python .\3-VerLimiteApi.py` 


### Módulo 4-recuperaArquivosPR.py
**necessário que o módulo 3 esteja em execução**
Neste módulo é possível executar paralelismo. Você pode executar quantas instancias achar melhor. 
Para que fosse simples, rapido e que nao fosse necessário algum sistema de mensageria, você terá que passar os ranges dos ids dos PRs recuperados na etapa anterior.  Você deverá utilizar o script da seguinte forma (utilizar parâmetros:

`python .\3-recuperaArquivosPR.py token2 496105 496106`

onde:
- token2 é o token configurado no `config.ini` 
- 496105 é o id do PR inicial
- 496106 é o id do PR final

Desta forma você pode distruir quais tokens você deseja usar mais (ou menos) e para quais ranges da tabela de PRs.

### Módulo 5-ConsolidarDados.py
Módulo não obrigatório. Criei ele para que os selects fossem mais rápidos.  Ele também fica executando a todo momento. 


### Módulo 6-GerarDados.py
Módulo não obrigatório. Criei para facilitar as consultas e extração dos dados finais. 


### Extras
- Banco.py: a maioria das consutlas se concentra nele. 
- SQLApoio.sql: são querys que acabei utilizando ao longo do trabalho. 
