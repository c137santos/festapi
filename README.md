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

```
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