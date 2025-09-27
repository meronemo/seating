from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from seat import run_seat
import uvicorn
import os

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/seat', response_class=HTMLResponse)
async def seat(request: Request):
    res = run_seat()
    if res:
        return templates.TemplateResponse('seat.html', {'request': request, 'error': res})
    return templates.TemplateResponse('seat.html', {'request': request})

@app.get('/backstage', response_class=HTMLResponse)
async def backstage(request: Request):
    file_exists = os.path.exists('previous_seat.txt')
    file_content = ''
    if file_exists:
        with open('previous_seat.txt', 'r') as f:
            file_content = f.read()
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'file_exists': file_exists,
        'file_content': file_content
    })

@app.post('/backstage/update', response_class=HTMLResponse)
async def backstage_update(request: Request, new_content: str = Form(...)):
    with open('previous_seat.txt', 'w') as f:
        f.write(new_content)
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'file_exists': True,
        'file_content': new_content
    })

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)