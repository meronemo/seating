import numpy as np
import random
from dotenv import dotenv_values
import ast
import os
from prev_seat import get_prev_edge_stu, update_prev_edge_stu
from image import generate_image

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
    stu_img = generate_image(stu_seat, 'student')
    tea_seat = np.rot90(seat, 2).flatten() # 90도 회전 2번(180도)
    tea_img = generate_image(tea_seat, 'teacher')

    if os.getenv('VERCEL') == '1':
        return stu_img, tea_img
    else:
        return

if __name__ == '__main__':
    run_seat()