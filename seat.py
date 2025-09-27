from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import random
from dotenv import dotenv_values
import ast
import os
from prev_seat import get_prev_edge_stu, update_prev_edge_stu

# 이미지 생성
def generate_image(seat, type):
    font = ImageFont.truetype('static/NanumGothic.ttf', 70)
    font_date = ImageFont.truetype('static/NanumGothic.ttf', 55)
    base_img_path = f'static/base_{type}.jpg'
    output_img_path = f'static/output_{type}.jpg'
    date = datetime.now(tz=ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d')
    x_coords = [150, 540, 980, 1370, 1810, 2200, 2640, 3030]
    y_coords = [810, 1130, 1450, 1770]
    date_coord = (1600, 2380)

    img = Image.open(base_img_path)
    draw = ImageDraw.Draw(img)
    idx = 0
    for row in y_coords:
        for col in x_coords:
            draw.text((col, row), seat[idx], font=font, fill='black')
            idx += 1
    draw.text(date_coord, date, font=font_date, fill='black')
    img.save(output_img_path)

# 자리 배치
def run_seat():
    # 학생 이름 리스트 불러오기 (local에서는 .env에서, Vercel에서는 env variables 읽어옴)
    name_list = ast.literal_eval(os.getenv('NAME_LIST') or dotenv_values('.env').get('NAME_LIST'))

    row, col = 4, 8
    seat = np.empty((4, 8), dtype=object) # 자리 배치 들어갈 2차원 배열

    # edge 자리 구분
    edge_seat = []
    nonedge_seat = []
    for i in range(row):
        for j in range(col):
            if i == row-1 or j in [0, col-1]: # 마지막 행, 첫번째 열, 마지막 열
                edge_seat.append((i, j))
            else:
                nonedge_seat.append((i, j))

    # 저번 edge 학생 번호 가져오기
    prev_edge_stu = get_prev_edge_stu()

    # 이번 edge, nonedge 학생 번호 shuffle
    prev_nonedge_stu = list(set(range(1, 32+1)) - set(prev_edge_stu))
    nonedge_stu = prev_edge_stu + random.sample(prev_nonedge_stu, 4) # 이번 nonedge에 앉을 학생 번호 (저번 edge + 저번 non_edge 4명 = 18명)
    edge_stu = list(set(range(1, 32+1)) - set(nonedge_stu)) # 이번 edge에 앉을 학생 번호
    random.shuffle(nonedge_stu)
    random.shuffle(edge_stu)

    # previous_seat 업데이트
    update_prev_edge_stu(' '.join(str(i) for i in edge_stu))

    # 학생 번호 + 이름을 자리 배열에 배치
    for students, seats in [(nonedge_stu, nonedge_seat), (edge_stu, edge_seat)]:
        for i, j in zip(students, seats):
            seat[j[0]][j[1]] = f'{i:02}. {name_list[i-1]}'

    # 배치 결과 이미지 생성
    stu_seat = seat.flatten()
    generate_image(stu_seat, 'student')
    tea_seat = np.rot90(seat, 2).flatten() # 90도 회전 2번(180도)
    generate_image(tea_seat, 'teacher')
    return

if __name__ == '__main__':
    run_seat()