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

### 6º Autenticação e autorização

Autenticação é se provar que é você é você mesmo. Realizar o login, por exemplo. A autorização é o que você pode fazer depois de se autenticar, as ações que tem permissão para realizar no sistema.

1 - Armazenamento senha de forma segura

Nosso armazenamento deveria ser diferente, pois hoje está sendo armazenado em texto puro. Precisamos prevenir até mesmo erros eventuais, como alterar um schema de formar a revelar a senha.

Um grande problema é que as pessoas usam a mesma senha para diversos lugares, deixando o cliente exposto.

O armazenamento de senhas vamos usar um hash com uma biblioteca de senhas. o ```pwdlib ``` é uma lib de encriptação de mão única (por conta do uso do hash), ou seja, significa que não dá para descriptar. E o argon2 é o padrão de hash mais atual.

```
poetry add "pwdlib[argon2]"
```

Com contexto da classe PassWordHash no arquivo ```security.py```, é possível encripta e verificar a senha.

2 - OAuth2 

Para desenvolver um login com um form do FastAPI com OAuth2, devemos usar um token de 30 minutos validado por um timedelta.

```
OAuth2PasswordRequestForm
```

O endpoint de tem algumas especificidades. Por exemplo, existe uma injeção de dependência como um placebo com a notação ``` = Dependes()```. Essa notação diz ao sistema que o tipo deve ser respeitado.
Esse endpoint não tem como padrão o json(), mas sim um x-www-form-urlencoded, por isso, o request.form(). O que já força a inserção de um username e password por default.

Para usar o request.form acima vai ser preciso o python-multipart.

```
poetry add python-multipart
```

3 - JWT

O JWT é um padrão (RFC 7519) para transmitir informações de maneira segura. É um JSON transmitido via Web em formato de Token. O JWT assina (com o algoritmo HMAC) a comunicação para que o servidor saiba que a mensagem não foi alterada e a pessoa se encontra autenticada. 

o JWT consiste em 3 partes, o headers, contendo informações sobre o tipo de assinatura e token utilizados. Temos o payload, que contém as claims.

O payload e as claims. Os playload tem as restrições e informações sobre o token. Por exemplo, o sub é quem tem o token e o exp é o tempo. 

https://www.iana.org/assignments/jwt/jwt.xhtml

```
sub (subject) = Entidade à quem o token pertence, normalmente o ID do usuário;
iss (issuer) = Emissor do token;
exp (expiration) = Timestamp de quando o token irá expirar;
iat (issued at) = Timestamp de quando o token foi criado;
aud (audience) = Destinatário do token, representa a aplicação que irá usá-lo.
```

E por fim, a signature. A assinatura utilizada que confirma que a mensagem não foi alterada. O exemplo de um JWT é esse formato separado por ponto.

```
HMACSHA256(
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
 nosso-segredo
)

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.Nx0P_ornVwJBH_LLLVrlJoh6RmJeXR-Nr7YJ_mlGY04
```

Vamos gerar o token em python com ```pyjwt```. Em outros projetos existe, por exemplo, python-jose.

```
poetry add pyjwt
```

Ao gerar tokens, você pode ver as informações por meio da função encode(). Também podemos verificar o decoded de um jwt com no site https://jwt.io/ Ou seja, isso quer dizer que é possível ler as informações transmitidas no JWT, não é possível alterar a informação ou forjar um novo token, mas ler sim! ENtão não inclua informações sensíveis

A resposta vai ser formatado por um BaseModel onde especifica o token de acesso e o tipo de token, para que o usuário saiba lidar. 

Para o JWT, o usuário vai enviar as credenciais para o endpoint de geração de token (função geradora nossa está em security em create_access_token), e esse vai devolver o token de acesso com base nesse Model. Ai todas as solicitações subsequentes vão ser feitas com o token de acesso.


```
class Token(BaseModel):
    access_token: str
    token_type: str
```

Agora nos testes do token, para enviar formulário não é JSON, é sim data.

** Bug ** 🐛
```
E       pwdlib.exceptions.UnknownHashError: This hash can't be identified. Make sure it's valid and that its corresponding hasher is enabled.
```

Quando inserimos a senha por fixture, o password estava limpo, e não foi passado pelo hash. Por isso, o erro. FOi preciso adapatar no conftest.py para passar a senha pelo hash para User.

Quando sujamos a senha, então temos um bad_request.

```
==================================================== short test summary info ====================================================
FAILED tests/test_app.py::test_login_for_access_token - assert 400 == <HTTPStatus.OK: 200>
 +  where 400 = <Response [400 Bad Request]>.status_code
 +  and   <HTTPStatus.OK: 200> = HTTPStatus.OK

``` 

Isso ocorre, pois agora ele só conhece a senha suja. Portanto,vamos usar **Monkey Patch**, que é alterar o objeto em tempo de execução. Adicionando então o clean_password nesse user. 

4 - Autorização.

Garantir que o cliente possa alterar ou deletar somente sua conta.

Após a descrição da função get_current_user, que é a função que vai pegar o token e verificar se ele é válido, agora no openapi.json da aplicação é possível logar E os eventos de put e delete são restritos. 

![alt text](/static/imgs/autorização.png)

Preciso ajustar os testes com fixture de token!


### 7º Routers

1 - O routers ajuda a reorganizar o código em subaplicativo. O routers permite aplicar o design soc.

Soc - Separation of Concerns. É um princípio de design de software para separar um programa em seções distintas, de tal forma que cada seção aborde uma preocupação separada.


Onde prefixo serão adicionados automaticamente, e tags servirão para separar as seções no /docs.

```
router = APIRouter(
    prefix='/users',
    tags=['users']
)
```

Caso não se atente na inclusão das rotas, pode acabar esquecendo de incluir o ```.router``` de seus arquivos. E isso pode gerar o erro estranho.

*bug* 🐛
![alt text](/static/imgs/bugsrouter.png)

Então, ao invés de users, deve usar users.router


```
app.include_router(users)
app.include_router(users.router)
```

2 - O tipo Annotated

O FastApi vai executar a função, anotar o tipo e retornar para variável. Então isso:

```
session: Session = Depends(get_session)
current_user: User = Depends(get_current_user)
```
Podemos abreviar tudo para que vire isso aqui: 

```
from typing import Annotated

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

```

3- Env

Agora retiramos todas as variáveis de ambiente que estavam chumbadas no código e passamos para o .env. A gente substituir pelo retorno do Settings(). 

O importante é usar o extra='ignore' para que possamos ter mais variáveis a mais no .env que pode não ter haver com settings. Como por exemplo o endereço do banco de dados. Ou configs da AWS.


### 8º Tornando o sistema de autenticação mais robusto

Para representar algo mais próximo de um ambiente de produção nos testes, decidi criar objetos usando o `factory-boy`. A ideia é ter uma fábrica de modelos que cria instâncias de uma `modelClass`.

```bash
poetry add --group dev factory-boy
```
Criei uma classe `UserFactory` no `conftest.py`, que herda do `factory-boy`. Dentro dela, defini uma classe `Meta` que indica qual modelo será construído (`model = User`). Com a criação de atributos padrão, não é necessário definir os campos manualmente toda vez.

```python

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}') # Sequence Adicionará +1 em cada objeto criado
    # esse é um objeto ansioso
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    # esse dado não é pré-pronto, mas sim quando ele é carregado, em tempo de execução.
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')
    # objeto lazy usando ansioso

```

Isso permite criar objetocs do tipo usuário em testes facilmente:

```python
user = UserFactory(username='bla', password='bla', email='bla') 
user2 = UserFactory(username='bla', password='bla', email='bla')  # elas retornarão um novo User, pois estamos fixando apenas a senha
user == user2  # False
```

Com os atributos padrão definidos, não preciso definir os campos manualmente. Isso é útil para criar `other_user` em casos onde um usuário deve interagir com outros usuários.
Assim, podemos avaliar como nosso sistema reage quando um usuário tenta realizar uma ação não autorizada.

Testando a expiração do token.

Para realizar esse teste, usaremos uma biblioteca chamada freezegun. freezeguné uma biblioteca Python que nos permite "congelar" o tempo em um ponto específico ou avançá-lo conforme necessário durante os testes. Isso é útil para testar a expiração de tokens de acesso.

```bash
poetry add --group dev freezegun
pip list | grep freezegun
```
---

Além disso, criei um endpoint POST na rota `/refresh_token` para atualizar o token de acesso de um usuário autenticado. Utilizo a função `get_current_user` para obter o usuário atual e, em seguida, gero um novo token de acesso com o email do usuário. 
Caso esteja expirado o tempo especificado no exp na claim, então temos um ExpiredSignatureError. 
O endpoint retorna um dicionário contendo o novo token de acesso e o tipo de token (`bearer`).
Assim, posso usar um token existente para gerar um novo token. A renovação só é válida enquanto o token de acesso estiver ativo, caso esteja inválido, isso não vai funcionar. 

Foi adotado a estratégia do refresh para renovar o token. O login é feito uma vez e, a partir daí, o token é atualizado. Isso é útil para evitar que o usuário tenha que fazer login toda vez que o token expirar e evitar enviar novamente os dados.

### 9º Criando Rotas CRUD para Gerenciamento de Tarefas

Serão CRUDs bem feitos associados aos Users!

Na criação do schema de resposta do ToDo, foi importado um Enum `TodoState` descrito como classe nos models para servir ao `response_class` do endpoint `create_todo`. 
Isso garante que todo ToDo é criado com um estado padrão, um conjunto fixo de constantes, neste caso o 'draft', e só poderá ter os estados possíveis listados no Enum, que também está documentado.

O `back_populates` permite uma associação bilateral das tabelas. Tanto User acessar ToDo, quanto ToDo acessar User. 
 
**Bugs** 🐛
Com a implementação da classe `TodoState` e o uso do Enum, surgiu um erro estranho de `PydanticSchemaGenerationError`, indicando que o Pydantic não conseguiu gerar o schema para `TodoState`.
O problema era que a importação do Enum estava errada; estava sendo importado do SQLAlchemy, mas deveria ser `from enum import Enum`.

![alt text](static/imgs/enums.png)

Uma dica valiosa é gerar um `task test -x --pdb` para depurar o erro. Isso permite que você veja o erro e o código que o causou.

Agora um endpoint de get com filtros. Nesse endpoint, se os parametros forem passados, ele deve ser acrescido na query. Esse endpoint possue 'offset' que serve para pular um número específico de resultados sequenciamente, e o 'limit' para quantos objetos devem retornar a consulta. Esse recurso é uma forma de paginação simples

```
todos = session.scalars(query.offset(offset).limit(limit)).all()
```

O método scalars é um método do SQLAlchemy que retorna um objeto escalar, ou seja, um objeto que não é uma lista, mas um objeto único. O método all() é um método do SQLAlchemy que retorna todos os objetos de uma consulta. Diferente do execute, que retorna um objeto de resultado.

* Estudo o padrão do tipo Query passando pelo validador. 

Como necessitamos de vários ToDos, então avaçamos no uso do FactoryBoy. A partir de um método do tipo ToDo. Usamos um user_id = 1, pois não temos um sistema de autenticação, então todos os ToDos são do mesmo usuário.

```python
class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text') #Com faker, ele cria algo qualquer do mesmo tipo para o lugar : gerador de LeroLero
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState) # FuzzyChoice é um valor randômico a partir do TodoState
    user_id = 1
```

O factoryBoy tem base na lib do faker, protanto, você solicita um novo objeto por meio do `TodoFactory.create_batch(XQUEVCQUER)`. Além de você mencionar algum campo específico. 

```python   
TodoFactory.create_batch(5, user_id=user.id)
```

Para lidar com adição de mais de um objeto no banco de dados, usamos no SQLAlchemy o bulk_save_objects. Isso é útil para inserir muitos objetos de uma vez. 


```python
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
```

Com os testes voltados para o Patch, algo muito interessante ocorre em termos de atualização do objeto. 

```
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

```

Para podermos alterar **somente** os valores que recebemos no modelo, temos que fazer um dump somente dos valores que recebemos e os atualizar no objeto que pegamos da base de dados. 
A linha for key, value in todo.model_dump(exclude_unset=True).items(): está iterando através de todos os campos definidos na instância todo do modelo de atualização. 
A função model_dump é um método que vem do modelo BaseModel do Pydantic e permite exportar o modelo para um dicionário.
O parâmetro exclude_unset=True é importante aqui, pois significa que apenas os campos que foram explicitamente definidos (ou seja, aqueles que foram incluídos na solicitação PATCH) serão incluídos no dicionário resultante. Isso permite que você atualize apenas os campos que foram fornecidos na solicitação, deixando os outros inalterados.

Qual a diferença entre session.update com com `for key, value in todo.model_dump(exclude_unset=True).items()`? E se eu mandar vazio, ele vai atualizar com vazio?


Se você usar session.query(Model).filter(...).update(data), ele gera um UPDATE direto no banco de dados e pode sobrescrever campos inteiros, inclusive tornando valores NULL caso não estejam no data.
Ele não lida automaticamente com apenas os campos modificados, a menos que você controle isso explicitamente.
Isso pode ser perigoso se você passar um dicionário incompleto porque ele pode definir campos não mencionados como NULL, dependendo da configuração do banco e da modelagem do ORM.

✅ Evita sobrescrever valores inexistentes na requisição (pois só atualiza os recebidos).
✅ Mantém a integridade do objeto (dado que só altera campos específicos).
✅ Permite manipulação antes do commit (caso queira validar algo antes de persistir).


**Bugs** 🐛
Para adicionar created_at e updated_at ToDo , foi realizado uma migração. Porém, nos testes relativos a create_todo, não foi possível usar o freeze_time, pois o created_at e updated_at são gerados no banco de dados. E o freeze_time não alcança essa operação. Portanto, usei do artifício (feio) do mock.any para verificar o retorno. Ou teria que trocar para

```
created_at: Mapped[datetime] = mapped_column(
    init=False, default=datetime.utcnow
)

```