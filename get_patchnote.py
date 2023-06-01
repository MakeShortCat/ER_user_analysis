import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

agg_note = pd.DataFrame(columns=['date', 'patch'])

def get_patchnote(patch_num):

    global agg_note
    # 웹페이지의 URL
    url = f"https://www.inven.co.kr/board/er/5772/{patch_num}"

    # 웹페이지에 GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    # 응답의 내용을 파싱하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, "html.parser")

    # 웹페이지의 전체 내용을 출력
    paragraphs = soup.find_all(attrs={'id':'tbArticle'})

    patchnote = []

    for paragraph in paragraphs:
        patchnote.append(paragraph.get_text())

    patchnote_split = patchnote[0].replace('\n', ' ').replace('\t', ' ').split('목록\r')
    
    date = patchnote_split[0].split('조회')[0][9:-2]

    patch = patchnote_split[1]

    new_row = pd.DataFrame({'date': date, 'patch': patch}, index = [0])

    agg_note = pd.concat([agg_note, new_row], ignore_index=True)

for i in range(30, 93):
    get_patchnote(i)

agg_note

for i in range(94, 291):
    get_patchnote(i)

for i in range(270, 291):
    get_patchnote(i)

# agg_note.to_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/patchnote.csv')
