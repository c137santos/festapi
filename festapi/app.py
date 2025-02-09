from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from festapi.routers import auth, todos, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='helloworld.html',
        context={'message': 'Hello World'},
    )
