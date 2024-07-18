# Aulas do curso de FastAPI Dunossauro

### Aula 01 - Configuração do ambiente e hello world com testes

1º Foi criado o ambiente inicial com comando do poetry
``
poetry new fastapi
``

Mudamos a versão do poetry para "3.12.*" no arquivo pyproject.toml

No terminal, eu devo mudar a versão do python. Isso vai criar o .python-version

```
pyenv local 3.12.4
```

Na pasta fastapi é o pacote que terá com todos os arquivos do projeto. 

2º Ambiente virtual com o comando poetry install

```
poetry install 
```

Ativando ambiente virtual

```
$ poetry shell
Spawning shell within .../virtualenvs/festapi--uhppGGl-py3.12
. .../virtualenvs/festapi--uhppGGl-py3.12/bin/activate
$ . .../virtualenvs/festapi--uhppGGl-py3.12/bin/activate
```

3º Adicionando o FastAPI.

Isso vai gerar as dependências abstratas do FastApi. E dentro do poetry.lock ficam as dependências concretas, com as versões exatas instaladas da lib e de suas dependências. 
Devo subir o poetry.lock? Sim

```
poetry add fastapi
```

4º Escreva a 1ª função no festapi/app.py. Vamos então testar tudo pelo shell.

```
$ python -i festapi/app.py 
>>> read_root()
{'message': 'Hello World'}
```

A função do framework Web é entregar essa resposta de código à internet! E é por meio do instanciamento do FastApi que conseguimos obter a estrutura de uma aplicação web.

5º Subindo servidor de desenvolvimento

```
fastapi dev festapi/app.py
```

![alt text](./static/imgs/image.png)

Agora temos enpoint /docs e /redoc. O primeiro é mais bonito e o segundo é mais funcional.

6º Ferramentas de desenvolvimentos

ruff: é um linter e um formatador!
pytest: e taskipy!

Instalação apenas para desenvolvimento deve ser identificada com --group!

```
$ poetry add --group dev pytest pytest-cov taskipy ruff httpx
```

Para o tasks, as abreaviaturas são definidas no arquivo pyproject.toml. E existe um macete. Se você escreve pre e pos em um comando, ao rodar o central, ele vai 1ª rodar os pré comandos, depois o comando central e por fim os pós comandos.

```
[tool.taskipy.tasks]
pre_test = 'task lint'
test = 'pytest -s -x --cov=fast_zero -vv'
post_test = 'coverage html'
```

Para configurações de pytest, foi definido que o pytest rodará na RAIZ do projeto. Portanto, as importações devem considerar esse nível de diretório. 
```
[tool.pytest.ini_options]
pythonpath = "."
addopts = "-p no:warnings"
```


### Aula 02 - Fundamentos do desenvolvimento web

Local (*LAN*): rede local (por isso lanhouse)
Longa distância (*WAN*): Roteadores interconectados

![alt text](./static/imgs/internet.png)

Quando falamos em comunicação, existem diversos formatos. O mais comum é o HTTP.
Quando rodamos fastapi run, significa que subimos um servidor que vái servir páginas para web.

```
Cliente <-> servidor <-> aplicação python
```

O servidor é que se encarrega de rodar aplicação python. Embora o FastAPI seja um ótimo framework web, ele não é um "servidor de aplicação". Por baixo dos panos, ele chama Uvicorn para rodar a aplicação.

o Uvicorn serve a aplicação por meio do padrao ASGI, é o mais moderno do que o WSGI. Ele que sabe sobre as regras do HTTP, e não o fastapi. 

Servidor web x servidor de aplicação. O servidor web é responsável por servir páginas web. O servidor de aplicação é responsável por rodar a aplicação.

*HTTP* é um protocolo fundamental na web baseado em requisições e respostas. Isso significa que estamos emitindo e recebendo mensagens!
Existem uma série de informações advindas de uma resposta HTTP, como por exemplo, seu Content-Type: Especifica o tipo de mídia no corpo da mensagem. Por exemplo, Content-Type: application/json indica que o corpo da mensagem está em formato JSON. Ou Content-Type: text/html, para mensagens que contém HTML.

*API* é uma interface de programação de aplicações. É um conjunto de regras e padrões que permite a comunicação entre aplicações. O que vamos retornar aqui é JSON. API Rest retornam HTML, o que faremos é uma API não REST, pois vai retornar um JSON. 

*Pydantic* para fazer esses contratos, o pydantic já vem embutido no FastAPI e é escrito em Rust (muito rápido). Vamos documentar com o pydantic e vai ficar disponível no /docs. 

```
from pydantic import Base Model 

class Message(BaseModel):
    message: str
```

De tal forma que, o que estiver fora do definido pelo schema, vai ser ignorado. E se o valor estiver no tipo errado, vai ser convertido, se possível (se não é erro de validação).

### Aula 03 - Criando Rotas CRUD 

O pydantic serve para estabelecer contratos de API e para validação de dados. Pydantic valida contrato de entrada e contrato de saída. Uma curiosidade é que para validar e-mail pode ser com EmailString, classe do BaseModel. 
Pydantic serve muito para documentar no docs!

Response model x response class. Response classe troca a classe da resposta, por exemplo, trocar json pelo html. Já o response model define e valida a estrutura dos responses e request.

Por padrão, o FastApi response 200 ok! Mas a resposta do POST é 201 created. Por isso é bom alterar para status_code=HTTPStatus.CREATED .

Uma coisa linda é: criar o banco de dados FAKE apenas como uma lista! Então o ID será por meio do índice da lista.

```
database = []
user_with_id = userDB(
    id = len(database) + 1
    **user.model_dump()
)
database.append(user_with_id)
```

O interessante dessa estratégia é o **user.model_dump(), o ** desempacota o objeto user (que está em formato pydantic) em chave e valor e adiciona o id, tudo para a função dump, que transforma em dict para ser inserido a lista, retornando apenas um formato específico determinado pelo pydantic, mesmo que você retorne o User inteiro!. 

**DRY - Dont Repeat Yourself**. 
O que é bom, é bom para ser reutilizado. Por isso, é bom criar uma função para criar um usuário. E devem ficar no arquivo confTest

```
@pytest.fixture()
def client():
    return TestClient(app)
```

No caso que não temos banco de dados ainda, o teste de read_users depende da execução do teste anterior que insere dados! Isso é péssimo, mas será resolvido na próxima aula, PORÉM, olha que legal que já funciona nem banco e com testes!

### Aula 04 - Banco de Dados com SQLAlchemy e Gerenciando Migrações com Alembic

#### SQLAlchemy
Uma biblioteca para trabalhar com SQL. SQLAlchemy realiza automações com a iteração com o db, e também contém um ORM (Object Relational Mapping) que mapeia objetos python para tabelas em um banco de dados relacional.

```@table_registry.mapped_as_dataclass```  registra uma tabela mapeando a classe de DADOS! Pode ser também o declarative_base, imperative_base!

Esse mapeamento é necessário, porque existem diversos tipos no DB para de algum tipo do Python, ex, int para python é um, para o DB pode ser diversos tipos de int diferente! O que se deseja é mapear o tipo Python para SQL e vice-versa, ou seja, trazer o dado do banco de modo a ser possível sua conversão para o tipo determinado em Python, qual nossa exemplo é int. Por isso Mapped[]!

o SQLAlchemy escolhe que ID pode ser um smallInt, pois é mais adequado para armazenamento de dados de int Python, e quando for chamado para o código, é possível converter o smallInt em um Int python sem problemas.

```
id: Mapped[int] <-> smallInt
```

Para formalização, o nome da classe do Model é User (singular), pois cria um User, onde os atributos são colunas da tabela. Mas o nome da tabela, ou seja, __tablename__ é users, pois manipula users!

mapped_column é quem dá restrições as colunas. Por exemplo, nullable=False.
User é um objeto scalar$ 

Como testar?

```
$ python -i festapi/models.py 
>>> User(username='Santos', password='senha', email='mail@gmail.com')
User(id=None, username='Santos', password='senha', email='mail@gmail.com', created_at=None)
```

Os none foram porque decidimos com mapped_column que isso ia ser responsabilidade do DB. Essa questão vai ocorrer quando o banco de dados for criado.

func.now() é data e hora do servidor, e não UTC. (?)

**Engine** é o ponto de conexão do DB. Podemos criar um db provisório com sqlite (esse vem junto com a instalação do Python), em memória para os testes, e um permanente para aplicação. 
Falando de testes! Imporanto o register com create_all dá a vantagem de conseguir criar todos os metadados de uma vez.

```
engine = create_engine('sqlite:///:memory:')
table_registry.metadata.create_all(engine)
```

Importante que seja :memory:, pois caso crie um arquivo, ele não vai ser jogado fora, e então os objetos vão persistir no banco de teste e causar interferências ruins. 
Para aplicação, vamos criar como arquivo, pois queremos persistir os dados.

```
engine = create_engine('sqlite:///database.db')
```

**Session**  Para não ter uma chamada direta do DB, usamos a session, pois ela é a camada intermediaria entre nosso código e o DB. ELe é um espaço temporário, ela é um stage, por isso ele consegue dar commit de diversos add!

Isso é um padrão de projeto chamado Unit of Work (UoW) que garante a ACID (Atomicidade, Consistência, Isolamento e Durabilidade) das transações, proporcionando uma maneira robusta de manter a integridade dos dados.

scalar = comando que realiza o mapeamento do query sql como objeto python.

A session deve ser transformado em um fixture no conftest.py usando recursos de yield, para que a session seja fechada após o teste.

**pydantic-settings** ajudará a separar as configurações do projeto do código. O arquivo vai buscar as infos no .env.

#### Alembic
É uma ferramenta de migração de banco de dados para SQLAlchemy que ajuda na evolução do banco.

```
alembic init migrations
```

Lá dentro do env.py do migrations que criou, conseguimos indicar onde está o banco de dados com metadata do registry!

O target_metadata ajuda no comando --autogenerate, pois o alembic sabe onde inspencionar os metadados do banco e gerar uma nova versão a partir de como o modelo se encontra.

```
config.set_main_option('sqlachemy.url', Settings().DATABASE_URL)
target_metadata = table_registry.metadata
```

**bugs**  🐛
Eu tive alguns bugs nessa aula, simplesmente meu comando ```alembic revision --autogenerate -m 'criar user' ``` criava upgrade e donwgrades vazios. E por mais que tivesse importado o metadados para o env.py do migrations de alembic, mesmo com alembic.ini, ele continuava gerando vazio. O que ocorreu é que, ao tentar rodar um teste com o endereço database.db onde há o comando de criar tabelas, em um momento que eu havia apenas escrito o criar tabelas e não deletar tabelas após o teste! Então ele criou tabelas nesse database.db! 

Ai eu estava pedindo para o alembic evoluir meu banco, e nada de detectar mudanças. Afinal, o alembic via  o database.db com a tabela criada no teste e concluia que a class User já existia. Descobri isso quando eu adicionei um campo na Class User e ele mapeou apenas a mudança daquele campo. Diante disso, deletei database.db e rodei o comando novamente, e ele gerou o upgrade e o downgrade corretamente.


### Aula 05 -  Integrando Banco de Dados (SQLAlchemy) ao FastAPI

1 - Vamos deixar o db fake de listinha para trás. Isso significa abri uma engine a partir da função create_engine, onde o endereço do banco está dentro da função Settings().DATABASE_URL. Após isso, abre uma session, onde se utilizar o scalar do SQLAlchemy para fazer as queries, seja com select, insert, update, delete. 

uma sessão é aquilo que fica em stage, e que só vai gravar no banco após o commit!

```
-- criando a sessão --
session = Session()
-- Stage --
session.add(user)
-- Commit--
session.commit()
```

Para retornar um erro no endpoint, o padrão, essencial, é que seja por meio do raise HTTPException. 

**bugs**  🐛
Eu não havia aplicado o ```alembic upgrade head``` para atualizar o banco de dados, e ai ficava rolando um erro 500 em relação tabela user



2- Desacoplando a chamada do DB com injeção de dependência. 

O fastApi tem o Depends() para realizar a injeção de dependência. Usar isso ajuda a trocar o cliente de prod para o cliente de teste com a função dependency_overrides no confest.py.
Sem a injeção com possibilidade de reescrita com dependency_overrides, seria necessário mockar o get_session em todos os testes que acessam o db. Ele é um fixture que recebe outra fixute.

 Depends ajuda a declarar e gerenciar essas dependências: "Antes de executar esta função, execute primeiro essa outra função e passe-me o resultado"

```
@pytest.fixture()
def client(session):

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

        app.dependency_overrides.clear()
```

Com isso, tudo que depende do banco de dados, em produção, será sobrescrito para usar o banco de teste.

**bugs**  🐛

Com o ``` python -x ``` a gente consegue perceber esse erro

```
sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 127811301049920 and this is thread id 127811391511424.
```

Como todo mundo depende do mesmo esquema do db. Um objeto do SQLAlchemy não pode ser compartilhado entre threads. Por isso, é necessário criar um novo objeto de sessão para cada thread. Tanto teste quanto a produção estão rodando em threads diferentes. E ele não consegue compartilhar a sessão do db. Então vamos dizer a ele para não checar na mesma thread, ou seja, se os objetos forem criados em threads diferentes, ele não vai reclamar. 

Tudo isso a parti do   connect_args={'check_same_thread': False}, pool=StaticPool

3 - Boas práticas de paginação

O fastapi pode contar com ```limit``` para resultados, e o ```offset``` com a variável skip para pular resultados de x em x. Isso traz os resultados paginados.

4 - Comparando modelos do pydantic na saída de teste de endpoint

Não é possível usar o user fixture direto na comparação de json() do assert do teste, o ideial é usar o model_validate com model_dump.

```
user_schema = UserPublic.model_validate(user).model_dump()
```

Isso deve ser combinado com essa linha lá no schema. POis o model_config um schema do pydantic altera o comportamento do 'model_validate'

```
model_config = ConfigDict(from_attributes=True)
```

5 - Ajustando o coverage

Devido ao fato que mudamos a sessão por uma injeção de dependência de banco de teste, então a session nunca é testado, por isso, pode rolar inserir o pragma: no cover para não ser testado.

```
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
```