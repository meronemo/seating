from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from seat import run_seat
import logging
import base64
from prev_seat import get_prev_edge_stu, update_prev_edge_stu

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

logging.basicConfig(level=logging.ERROR)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"Exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/seat', response_class=HTMLResponse)
async def seat(request: Request):
    res = run_seat()
    if res: # vercel 환경에서는 stu_img, tea_img binary data로 return됨
        return templates.TemplateResponse('seat.html', {
            'request': request,
            'vercel': 1,
            'stu_img': base64.b64encode(res[0]).decode('utf-8'),
            'tea_img': base64.b64encode(res[1]).decode('utf-8')
        })
    else: # local 환경에서는 image를 file로 보여줌
        return templates.TemplateResponse('seat.html', {
            'request': request,
            'vercel': 0
            })

@app.get('/backstage', response_class=HTMLResponse)
async def backstage(request: Request):
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'content': get_prev_edge_stu(raw=1) # list 형식으로 가공하지 않고 그대로 가져와서 보여줌
    })

@app.post('/backstage/update', response_class=HTMLResponse)
async def backstage_update(request: Request, new_content: str = Form(...)):
    update_prev_edge_stu(new_content)
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'content': get_prev_edge_stu(raw=1)
    })
