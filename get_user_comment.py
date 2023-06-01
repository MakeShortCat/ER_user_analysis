import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import time
from scipy.stats import poisson
import asyncio
import dc_api

user_comment = pd.DataFrame(columns=['date','comment','ind_id'])

async def run():
  i = 0
  async with dc_api.API() as api:
    global user_comment
    async for index in api.board(board_id="bser", start_page=101145):
        time.sleep(0.15)

        doc = await index.document()
        if doc == None:
            print('NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
            time.sleep(1)
            continue
        date = doc.time
        comment_dc_temp = ''
        async for comm in index.comments():
            comment_dc_temp += comm.contents

        comment_dc = index.title + doc.contents + comment_dc_temp

        new_row = pd.DataFrame({'date': date, 'comment': comment_dc, 'ind_id' : doc.id}, index = [0])

        user_comment = pd.concat([user_comment, new_row], ignore_index=True)

        i += 1
        
        if i % 1000 == 0:
            ind = user_comment.iloc[-1]['ind_id']
            user_comment.to_csv(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_comment_dc_api{ind}.csv')
            
        print(user_comment.tail(1))

asyncio.run(run())

812753 - 775208

17202/500


812753 - 801446
37545 / 32.2

new_row = pd.DataFrame({'date': date, 'comment': comment}, index = [0])

user_comment = pd.concat([user_comment, new_row], ignore_index=True)


# 정규분포 생성
mean = 0.4  # 정규분포의 평균
stddev = 0.2  # 정규분포의 표준편차

# 포아송 분포 생성
lambda_param = 0.8  # 포아송 분포의 평균과 분산 파라미터
poisson_dist = poisson(mu=lambda_param)

user_comment = pd.DataFrame(columns=['date', 'comment'])

error_List = []

headers = [
{'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'},
]

for i, num in enumerate(range(1264,3000)):

    random_number_n = np.random.normal(mean, stddev, size=1)
    random_number_p = poisson_dist.rvs(size=1)

    if num%1000 == 0:
        user_comment.to_csv(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_comment_dc{num/1000}.csv')
        time.sleep(60 + random_number_n[0]*20)

    time.sleep(abs(random_number_n[0] + random_number_p[0]/10))

    url = f'https://gall.dcinside.com/mgallery/board/view/?id=bser&no={num}'

    response = requests.get(url, headers=headers[0])

    # 응답의 내용을 파싱하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.content, "html")

    # 웹페이지의 전체 내용을 출력
    paragraphs_title = soup.find(attrs={'class' : 'title_subject'})

    paragraphs_content = soup.find(attrs={'class' : 'write_div'})

    paragraphs_date = soup.find(attrs={'class' : 'gall_date'})

    if response.status_code == 200:
        
        # 응답의 내용을 파싱하여 BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, "html.parser")

        # 웹페이지의 전체 내용을 출력
        paragraphs_title = soup.find(attrs={'class' : 'title_subject'})

        paragraphs_content = soup.find(attrs={'class' : 'write_div'})

        if paragraphs_title == None or paragraphs_date == None:
            print('None')
            continue

        comment = paragraphs_title.get_text() + paragraphs_content.get_text()

        date = paragraphs_date.get_text()

        new_row = pd.DataFrame({'date': date, 'comment': comment}, index = [0])

        user_comment = pd.concat([user_comment, new_row], ignore_index=True)

    else: error_List.append([response.status_code, num])

    print(num)












def get_user_comment(num, base_url):

    base_url = 'https://gall.dcinside.com/mgallery/board/view/?id=bser&no='
    # 웹페이지의 URL
    url = base_url + f"{num}"

    # 웹페이지에 GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    if response.status_code == 200:
            
        # 응답의 내용을 파싱하여 BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, "html.parser")

        # 웹페이지의 전체 내용을 출력
        paragraphs = soup.find_all(attrs={'id':'tbArticle'})

        comment_list = []

        for paragraph in paragraphs:
            comment_list.append(paragraph.get_text())

        comment_split = comment_list[0].replace('\n', ' ').replace('\t', ' ').split('목록\r')

        date = comment_split[0].split('조회')[0][6:-2]

        comment = comment_split[1]

        new_row = pd.DataFrame({'date': date, 'comment': comment}, index = [0])

        user_comment = pd.concat([user_comment, new_row], ignore_index=True)
    
    else: error_List.append([response.status_code, num])

    return num

for i in range(5788, 5900):
    time.sleep(0.3)
    get_user_comment(i)

# user_comment.to_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_comment.csv')


user_demand = pd.DataFrame(columns=['date', 'comment'])

def get_user_demand(num):

    global user_demand
    # 웹페이지의 URL
    url = f"https://www.inven.co.kr/board/er/5786/{num}"

    # 웹페이지에 GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    if response.status_code == 200:
            
        # 응답의 내용을 파싱하여 BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, "html.parser")

        # 웹페이지의 전체 내용을 출력
        paragraphs = soup.find_all(attrs={'id':'tbArticle'})

        comment_list = []

        for paragraph in paragraphs:
            comment_list.append(paragraph.get_text())

        comment_split = comment_list[0].replace('\n', ' ').replace('\t', ' ').split('목록\r')

        date = comment_split[0].split('조회')[0][6:-2]

        comment = comment_split[1]

        new_row = pd.DataFrame({'date': date, 'comment': comment}, index = [0])

        user_demand = pd.concat([user_demand, new_row], ignore_index=True)

    return num


for i in range(1, 702):
    time.sleep(0.4)
    get_user_demand(i)

# user_demand.to_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_demand.csv')