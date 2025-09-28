from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
import vercel_blob
import os
import io
import base64

def generate_image(seat, type): # type == student | teacher
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

    # 이미지 binary data와 date return
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    binary_data = buf.read()
    binary_data = base64.b64encode(binary_data).decode('utf-8')
    date = now.strftime('%y%m%d%H%M')
    return binary_data, date

def get_blob():
    blobs = vercel_blob.list()['blobs']
    image_items = []
    for item in blobs:
        if item.get('pathname') != 'robots.txt':
            image_items.append(item)
    return image_items

def upload_blob(date, type, binary_data):
    # production에서만 blob에 upload(dev때는 올라가지 않게)
    if os.getenv('VERCEL_ENV') == 'production':
        binary_data = base64.b64decode(binary_data)
        vercel_blob.put(f'{date}_{type}.jpg', binary_data, verbose=True)
        return True
    return False
    