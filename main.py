from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from seat import run_seat
import logging
import os
from prev_seat import get_prev_edge_stu, update_prev_edge_stu
from image import upload_blob, get_blob

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
    return templates.TemplateResponse('index.html', {
        'request': request,
        'content': get_prev_edge_stu(raw=1)
    })

@app.get('/seat', response_class=HTMLResponse)
async def seat(request: Request):
    res = run_seat()
    return templates.TemplateResponse('seat.html', {
        'request': request,
        'stu_img': res[0],
        'tea_img': res[1],
        'date': res[2]
    })

@app.get('/backstage', response_class=HTMLResponse)
async def backstage(request: Request):
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'content': get_prev_edge_stu(raw=1), # list 형식으로 가공하지 않고 그대로 가져와서 보여줌
        'kakao_api_key': os.getenv('KAKAO_API_KEY')
    })

@app.post('/backstage/update', response_class=HTMLResponse)
async def backstage_update(request: Request, new_content: str = Form(...)):
    update_prev_edge_stu(new_content)
    return templates.TemplateResponse('backstage.html', {
        'request': request,
        'content': get_prev_edge_stu(raw=1),
        'kakao_api_key': os.getenv('KAKAO_API_KEY')
    })

@app.post('/api/upload_image', response_class=JSONResponse)
async def upload_image(request: Request):
    try:
        data = await request.json()
        res = upload_blob(data['date'], data['type'], data['image_data'])
        if res: # production 환경에서 업로드가 성공적으로 된 경우
            return {"status": "success"} 
        else: # production 환경이 아니라서 업로드를 진행하지 않은 경우
            return {"status": "skipped"} 
    except Exception as e: # 업로드 중 실패한 경우
        logging.error(f"Upload failed: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get('/api/get_images', response_class=JSONResponse)
async def get_images(request: Request):
    return get_blob()
