from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
import vercel_blob
import os
import io
import threading

def upload_blob(date, type, binary_data):
    vercel_blob.put(f'{date}_{type}.jpg', binary_data, verbose=True)

def generate_image(seat, type): # type == student | teacher
    print(os.getenv("VERCEL_ENV"))
    # 이미지 그리기
    font = ImageFont.truetype('static/NanumGothic.ttf', 70)
    font_date = ImageFont.truetype('static/NanumGothic.ttf', 55)
    now = datetime.now(tz=ZoneInfo('Asia/Seoul'))
    display_date = now.strftime('%Y-%m-%d')
    x_coords = [150, 540, 980, 1370, 1810, 2200, 2640, 3030]
    y_coords = [810, 1130, 1450, 1770]
    date_coord = (1600, 2380)
    img = Image.open(f'static/base_{type}.jpg')
    draw = ImageDraw.Draw(img)
    idx = 0
    for row in y_coords:
        for col in x_coords:
            draw.text((col, row), seat[idx], font=font, fill='black')
            idx += 1
    draw.text(date_coord, display_date, font=font_date, fill='black')

    # 이미지 저장
    if os.getenv('VERCEL') == '1': # vercel 환경
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        buf.seek(0)
        binary_data = buf.read()
        date = now.strftime('%y%m%d%H%M')
        if os.getenv('VERCEL_ENV') == 'production': # production에서만 blob에 upload(dev때는 올라가지 않게)
            threading.Thread(target=upload_blob, args=(date, type, binary_data)).start()
        return binary_data
    else: # local 환경
        img.save(f'static/output_{type}.jpg')
        return