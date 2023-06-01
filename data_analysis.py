from konlpy.tag import Okt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime
import datetime as dt
import re
from konlpy.tag import Komoran
import os
#한글 폰트 설정
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.animation as animation
matplotlib.use('TkAgg')  # 사용할 백엔드 지정 (TkAgg, Qt5Agg 등)
import time
import matplotlib.cm as cm
import random
import networkx as nx
from wordcloud import WordCloud
import matplotlib.colors as mcolors

font_location = 'C:/Windows/Fonts/malgun.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
# 폰트 설정 적용
plt.rcParams['font.family'] = font_name
plt.rcParams['font.sans-serif'] = font_name

# 사용자 사전 추가
komoran = Komoran(userdic='C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_dict_ER.txt')

# 데이터 정리
patch_note = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/patchnote.csv')

user_comment = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_comment.csv')

user_demand = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_demand.csv')

patch_note = patch_note.drop(columns=['Unnamed: 0'])

user_comment = user_comment.drop(columns=['Unnamed: 0'])

user_demand = user_demand.drop(columns=['Unnamed: 0'])

def keep_numeric_special(text):
    pattern = r'[^0-9\s!@#$%^&*()-:]'  # 숫자와 특수문자를 제외한 패턴
    result = re.sub(pattern, '', text)
    return result

patch_note['date'] = patch_note['date'].apply(keep_numeric_special)

user_comment['date'] = user_comment['date'].apply(keep_numeric_special)

user_demand['date'] = user_demand['date'].apply(keep_numeric_special)

def find_different_length_rows(df):
    lengths = df.apply(len)  # 각 행의 문자열 길이 계산
    different_lengths = lengths[lengths != lengths.iloc[0]]  # 길이가 다른 행 선택
    different_indexes = different_lengths.index.tolist()  # 인덱스 번호 추출
    return different_indexes

result = find_different_length_rows(user_comment['date'])

def split_sth(x, ind, split_key, split_num):
    x.split(split_key, split_num)[ind]

    return x.split(split_key, split_num)[ind]

user_comment['date'].loc[result] = user_comment['date'].loc[result].apply(lambda x: split_sth(x, ind=1, split_key=' ', split_num=1))

result = find_different_length_rows(user_demand['date'])

user_demand['date'].loc[result] = user_demand['date'].loc[result].apply(lambda x: split_sth(x, ind=1, split_key=' ', split_num=1))

patch_note['patch'] = patch_note['patch'].apply(lambda x: split_sth(x, ind=1, split_key='         ', split_num=1))

user_comment['comment'] = user_comment['comment'].apply(lambda x: split_sth(x, ind=1, split_key='        ', split_num=1))

user_demand['comment'] = user_demand['comment'].apply(lambda x: split_sth(x, ind=1, split_key='        ', split_num=1))

daily_user = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/daily_user.csv')

daily_user['DateTime'] = pd.to_datetime(daily_user['DateTime'])

user_comment['date'] = pd.to_datetime(user_comment['date'])

# user_comment.to_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_commentV1.csv')

# patch_note.to_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/patch_noteV1.csv')

# 형태소 분석기 인스턴스 생성
from ckonlpy.tag import Twitter
twitter = Twitter()

stopwords_char = ['임', '면', '나', '게', '거', '데','요','!', '합니다', '-','...','.','..', '이', '있', '하', '것', '들', '그', '되', '수', '이', '보',' ', '에', '을', ',', '?', '은',
              '주', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', '일', '위하', '는', '도', '를', '로', '에서',
              '의', '으로', '다', '안', '만', '좀','하는', '하고', '(', ')', '고', '입니다', ':', '지만', '까지', '', 'ㄹ',
              '게임', '1', '못', '해', '할', '니', '3', '2', '인','분', '개','해서', '클랜', '면서', '서', '그냥', '너무',
              '/', '겜', '스킬', '+', '블서', '같이', '인데', '"', '아', '왜', '다가', '잘', '함', '>',
              '전', '랑', '뭐', '경우', '⭐️', 'ㅋㅋ', '4', '기', '하면', '저', '중', '디코', '점', '니까', '해주',
              '부터', '??', '라', '더','시', '던데', '내', '이나', '히', '과', '와', '원', '드', '한테', '제','네',
              '이다', '애', '하나','정도', '디스코', '하는데', '들이', '보다', '지는', '가능', '\'', '했는데', '같은', '함께', 
              '이상', '있는', '지금', '진짜', '다른', '아니', '근데', '없', '거나', '[', ']', '키', '하기','모', '⭐️⭐️',
              '~',' 처럼', 'ㄴ', '어', 'ㅁ', '었', '명', '좋', '는데', '었' , '', '5', '번', '야', '디', '이런', '라고', '두', '대',
              '\xa0', '가입', 'ㅠㅠ', '글', '뒤', '하실', 'e', '같은데', '판', '카톡', '결국', '현재', '까','방',
              '됨', '해도', '아무', '그리', '건가', '어떻게', '에게', '또', '하게', '후', 'ㅋㅋㅋ', '오픈', '밖에',
              '어가', '에는', '얘', '있습니다', '어요', '이랑', ';;', '아직', '언제', '아닌', '려고', '제발', '마다',
              '리', '#', '한번', '있는데', '걸', '오늘', '이제', '여','혹시', '서로','하니', '위해', '분들', '이렇게',
              '부탁', '<', '>', '-', '->', '<-', '리턴',  '이터널', '📣', '𐅀', '어어', '터널', '해줘', 
              '나딘','나타폰','니키','다니엘','띠아','라우라','레녹스','레온','로지','루크','리 다이린','리오',
              '마르티나','마이','마커스','매그너스','바냐','바바라','버니스','비앙카','셀린','쇼우','쇼이치','수아'
              ,'시셀라','실비아','아델라','아드리아나','아디나','아야','아이솔','아이작','알렉스','얀','에스텔','에이든',
              '에키온','엘레나','엠마','요한','윌리엄','유키','이렘','이바','이안','일레븐','자히르','재키','제니',
              '카밀로','칼라','캐시','클로에','키아라','타지아','테오도르','펠릭스','프리야','피오라',
              '피올로','하트','헤이즈','현우','혜진','리다', '리다이린','냐','들은','없이','보고','및', '이라',
              '많이','라는', '처럼', '계속','놈','끼리','이서', '건', '된', '이고']

stopwords= ['임', '면', '나', '게', '거', '데','요','!', '합니다', '-','...','.','..', '이', '있', '하', '것', '들', '그', '되', '수', '이', '보',' ', '에', '을', ',', '?', '은',
              '주', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', '일', '위하', '는', '도', '를', '로', '에서',
              '의', '으로', '다', '안', '만', '좀','하는', '하고', '(', ')', '고', '입니다', ':', '지만', '까지', '', 'ㄹ',
              '게임', '1', '못', '해', '할', '니', '3', '2', '인','분', '개','해서', '클랜', '면서', '서', '그냥', '너무',
              '/', '겜', '스킬', '+', '블서', '같이', '인데', '"', '아', '왜', '다가', '잘', '함', '>',
              '전', '랑', '뭐', '경우', '⭐️', 'ㅋㅋ', '4', '기', '하면', '저', '중', '디코', '점', '니까', '해주',
              '부터', '??', '라', '더','시', '던데', '내', '이나', '히', '과', '와', '원', '드', '한테', '제','네',
              '이다', '애', '하나','정도', '디스코', '하는데', '들이', '보다', '지는', '가능', '\'', '했는데', '같은', '함께', 
              '이상', '있는', '지금', '진짜', '다른', '아니', '근데', '없', '거나', '[', ']', '키', '하기','모', '⭐️⭐️',
              '~',' 처럼', 'ㄴ', '어', 'ㅁ', '었', '명', '좋', '는데', '었' , '', '5', '번', '야', '디', '이런', '라고', '두', '대',
              '\xa0', '가입', 'ㅠㅠ', '글', '뒤', '하실', 'e', '같은데', '판', '카톡', '결국', '현재', '까','방',
              '됨', '해도', '아무', '그리', '건가', '어떻게', '에게', '또', '하게', '후', 'ㅋㅋㅋ', '오픈', '밖에',
              '어가', '에는', '얘', '있습니다', '어요', '이랑', ';;', '아직', '언제', '아닌', '려고', '제발', '마다',
              '리', '#', '한번', '있는데', '걸', '오늘', '이제', '여','혹시', '서로','하니', '위해', '분들', '이렇게',
              '부탁', '<', '>', '-', '->', '<-', '리턴','이라', '들은', '이터널', '📣', '𐅀', '어어', '터널',
                '해줘','냐', '없이', '많이','라는', '처럼', '계속','놈','끼리','이서','건', '된', '이고']

char_list = ['나딘','나타폰','니키','다니엘','띠아','라우라','레녹스','레온','로지','루크','리 다이린','리오',
              '마르티나','마이','마커스','매그너스','바냐','바바라','버니스','비앙카','셀린','쇼우','쇼이치','수아'
              ,'시셀라','실비아','아델라','아드리아나','아디나','아야','아이솔','아이작','알렉스','얀','에스텔','에이든',
              '에키온','엘레나','엠마','요한','윌리엄','유키','이렘','이바','이안','일레븐','자히르','재키','제니',
              '카밀로','칼라','캐시','클로에','키아라','타지아','테오도르','펠릭스','프리야','피오라',
              '피올로','하트','헤이즈','현우','혜진','리다', '리다이린']


def preprocess_text(text):
    # 형태소 분석
    word_tokens = twitter.morphs(text)
    word_tokens_unique = list(set(word_tokens))
    # 불용어 제거
    filtered_text = [word for word in word_tokens_unique if word not in stopwords]
    return filtered_text

def preprocess_text_char_off(text):
    # 형태소 분석
    word_tokens = twitter.morphs(text)
    word_tokens_unique = list(set(word_tokens))
    # 불용어 제거
    filtered_text = [word for word in word_tokens_unique if word not in stopwords_char]
    return filtered_text

start_date = dt.date(2020, 11, 21)
end_date = dt.date(2023, 5, 1)

date_list = []

current_date = start_date
while current_date <= end_date:
    current_date += dt.timedelta(days=1)
    date_list.append(current_date)

import tkinter as tk
import threading
# Tkinter 애플리케이션의 메인 루프 실행을 위한 함수
def run_mainloop():
    root = tk.Tk()
    root.mainloop()

# Tkinter 애플리케이션의 메인 루프 실행
mainloop_thread = threading.Thread(target=run_mainloop)
mainloop_thread.start()

texts = user_comment['comment']

# 전처리 수행
preprocessed_texts = [preprocess_text(text) for text in texts]

# 단어 빈도수 계산
word_counter = Counter([word for sentence in preprocessed_texts for word in sentence])

# 가장 많이 등장하는 단어 Top 10
agg_most_common_words = word_counter.most_common(1000)

agg_word_list = []
agg_count_list = []

for word, freq in agg_most_common_words:
    agg_word_list.append(word)
    agg_count_list.append(freq)

# 색상 맵 선택
cmap = cm.get_cmap('rainbow')

random.seed(42)

# 고유한 이름에 대한 색상 할당
color_dict = {}
for i, word in enumerate(agg_word_list):
    color_dict[word] = cmap(random.uniform(len(agg_word_list)/20, len(agg_word_list) * 0.95,) / len(agg_word_list))

aaa = 0

def make_plot():
    for day in pd.to_datetime(date_list[780:]):
        global aaa
        global color_dict

        print(aaa)
        aaa += 1
        front_Day = datetime.strptime(day.strftime("%Y-%m-%d"),"%Y-%m-%d") + dt.timedelta(days = 14)
        back_Day = datetime.strptime(day.strftime("%Y-%m-%d"),"%Y-%m-%d") - dt.timedelta(days = 14)

        # 예시 문장 리스트
        texts = user_comment.loc[(user_comment['date'] > back_Day) & (user_comment['date'] <  front_Day)]['comment']

        # 전처리 수행
        preprocessed_texts = [preprocess_text(text) for text in texts]

        # 단어 빈도수 계산
        word_counter = Counter([word for sentence in preprocessed_texts for word in sentence])

        # 가장 많이 등장하는 단어 Top 10
        most_common_words = word_counter.most_common(20)

        word_list = []
        count_list = []

        for word, freq in most_common_words:
            word_list.append(word)
            count_list.append(freq)

        # Seaborn의 barplot 함수를 사용하여 시각화
        plt.figure(figsize=(19.2, 10.8), dpi=100)
        sns.barplot(x = count_list, y = word_list, palette=[color_dict.get(i, 'gray') for i in word_list])
        plt.title(f'{day.strftime("%Y-%m-%d")}', fontsize=30, pad=40)
        plt.xlabel('언급된 수', fontsize=25, labelpad=40)
        plt.ylabel('키워드', fontsize=25, labelpad=60, rotation=0)
        plt.xticks([])
        plt.yticks([])

        # 그래프 끝 부분에 컬럼 이름 표시
        for i, value in enumerate(count_list):
            plt.text(value , i + 0.07 , str(value), ha='left', va='center', fontsize=15)
            plt.text(value - 1, i + 0.07, word_list[i], ha='right', va='center', fontsize=18, fontweight='bold')

        plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/keyword_frequencies_{day.strftime("%Y-%m-%d")}.png')  # 그래프를 이미지 파일로 저장
        
        plt.close()  # 그래프 창을 닫음

# make_plot()

def section_ploting(start_date, end_date, section_name):
    date_dt = datetime.strptime(f'{start_date}', '%Y-%m-%d')
    date_dt1 = datetime.strptime(f'{end_date}', '%Y-%m-%d')

    # 예시 문장 리스트
    texts = user_comment.loc[(user_comment['date'] > date_dt) & (user_comment['date'] <  date_dt1)]['comment']

    # 전처리 수행
    preprocessed_texts = [preprocess_text_char_off(text) for text in texts]

    # 단어 빈도수 계산
    word_counter = Counter([word for sentence in preprocessed_texts for word in sentence])

    # 가장 많이 등장하는 단어 Top 30
    most_common_words = word_counter.most_common(30)

    word_list = []
    count_list = []

    for word, freq in most_common_words:
        word_list.append(word)
        count_list.append(freq)

    # Seaborn의 barplot 함수를 사용하여 시각화
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    sns.barplot(x = count_list, y = word_list, palette=[color_dict.get(i, 'gray') for i in word_list])
    plt.title(f'{section_name} \n {start_date + "~" + end_date}', fontsize=25, pad=20)
    plt.xlabel('언급된 수', fontsize=25, labelpad=40)
    plt.ylabel('키워드', fontsize=25, labelpad=60, rotation=0)
    plt.xticks([])
    plt.yticks([])

    # 그래프 끝 부분에 컬럼 이름 표시
    for i, value in enumerate(count_list):
        plt.text(value , i + 0.07 , str(value), ha='left', va='center', fontsize=15)
        plt.text(value - 1, i + 0.07, word_list[i], ha='right', va='center', fontsize=17, fontweight='bold')

    plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/keyword_frequencies_{section_name}.png')  # 그래프를 이미지 파일로 저장
    
    plt.close()  # 그래프 창을 닫음

def section_ploting_char(start_date, end_date, section_name):
    date_dt = datetime.strptime(f'{start_date}', '%Y-%m-%d')
    date_dt1 = datetime.strptime(f'{end_date}', '%Y-%m-%d')

    # 예시 문장 리스트
    texts = user_comment.loc[(user_comment['date'] > date_dt) & (user_comment['date'] <  date_dt1)]['comment']

    # 전처리 수행
    preprocessed_texts = [preprocess_text(text) for text in texts]

    # 단어 빈도수 계산
    word_counter = Counter([word for sentence in preprocessed_texts for word in sentence if word in char_list])

    # 가장 많이 등장하는 단어 Top 30
    most_common_words = word_counter.most_common(10)

    word_list = []
    count_list = []

    for word, freq in most_common_words:
        word_list.append(word)
        count_list.append(freq)

    # Seaborn의 barplot 함수를 사용하여 시각화
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    sns.barplot(x = count_list, y = word_list, palette=[color_dict.get(i, 'gray') for i in word_list])
    plt.title(f'{section_name} \n {start_date + "~" + end_date}', fontsize=25, pad=20)
    plt.xlabel('언급된 수', fontsize=25, labelpad=40)
    plt.ylabel('키워드', fontsize=25, labelpad=60, rotation=0)
    plt.xticks([])
    plt.yticks([])

    # 그래프 끝 부분에 컬럼 이름 표시
    for i, value in enumerate(count_list):
        plt.text(value , i  , str(value), ha='left', va='center', fontsize=15)
        plt.text(value - 1, i , word_list[i], ha='right', va='center', fontsize=17, fontweight='bold')

    plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/keyword_frequencies_{section_name}.png')  # 그래프를 이미지 파일로 저장
    
    plt.close()  # 그래프 창을 닫음


def section_ploting_char_target(start_date, end_date, section_name, char_name):
    date_dt = datetime.strptime(f'{start_date}', '%Y-%m-%d')
    date_dt1 = datetime.strptime(f'{end_date}', '%Y-%m-%d')

    # 예시 문장 리스트
    texts = user_comment.loc[(user_comment['date'] > date_dt) & (user_comment['date'] <  date_dt1)]['comment']

    # 전처리 수행
    preprocessed_texts = [preprocess_text(text) for text in texts]

    target_word = f'{char_name}'
    co_occurrence = Counter()

    for sentence in preprocessed_texts:
        if target_word in sentence:
            co_occurrence.update([word for word in sentence if word != target_word])

    word_list = []
    count_list = []

    for word, count in co_occurrence.most_common(10):
        word_list.append(word)
        count_list.append(count)

    # Seaborn의 barplot 함수를 사용하여 시각화
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    sns.barplot(x = count_list, y = word_list, palette=[color_dict.get(i, 'gray') for i in word_list])
    plt.title(f'{section_name} { char_name} \n {start_date + "~" + end_date}', fontsize=25, pad=20)
    plt.xlabel('언급된 수', fontsize=25, labelpad=40)
    plt.ylabel('키워드', fontsize=25, labelpad=60, rotation=0)
    plt.xticks([])
    plt.yticks([])

    # 그래프 끝 부분에 컬럼 이름 표시
    for i, value in enumerate(count_list):
        plt.text(value , i  , str(value), ha='left', va='center', fontsize=15)
        plt.text(value - 1, i , word_list[i], ha='right', va='center', fontsize=17, fontweight='bold')

    plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/keyword_frequencies_{section_name}{char_name}.png')  # 그래프를 이미지 파일로 저장
    
    plt.close()  # 그래프 창을 닫음



def section_ploting_node(start_date, end_date):
    date_dt = datetime.strptime(f'{start_date}', '%Y-%m-%d')
    date_dt1 = datetime.strptime(f'{end_date}', '%Y-%m-%d')

    # 예시 문장 리스트
    texts = user_comment.loc[(user_comment['date'] > date_dt) & (user_comment['date'] <  date_dt1)]['comment']

    # 전처리 수행
    preprocessed_texts = [preprocess_text(text) for text in texts]

    # 단어 빈도수 계산
    word_counter = Counter([word for sentence in preprocessed_texts for word in sentence])

    # 가장 많이 등장하는 단어 Top 10
    common_words = word_counter.most_common(30)

    common_dict = {}

    for word, freq in common_words:
        common_dict[word] = freq

    target_words = common_dict.keys()

    co_occurrence_dict = {}
    co_occurrence = Counter()

    for target_word in target_words:
        co_occurrence = Counter()
        for sentence in preprocessed_texts:
            if target_word in sentence:
                co_occurrence.update([word for word in sentence if word != target_word])

        co_occurrence_most = co_occurrence.most_common(5)

        co_occurrence_dict_temp = {}
        for word, freq in co_occurrence_most:
            co_occurrence_dict_temp[word] = freq
            co_occurrence_dict[target_word] = co_occurrence_dict_temp

    return co_occurrence_dict, common_dict

word_func = section_ploting_node('2020-09-06' ,'2020-12-06')

word_func[0]

# 그래프 생성
G = nx.Graph()

# 노드 추가 (노드 크기는 단어 등장 횟수에 비례)
for word1, count1 in word_func[1].items():
    G.add_node(word1, size=count1)

for node in G.nodes(data=True):
    print(node)

# 엣지 추가 (엣지 가중치는 단어들이 같이 나온 횟수에 비례)
for word, connections in word_func[0].items():
    for target_word, weight in connections.items():
        if weight >= 6:  # 가중치가 2 이상일 때만 엣지를 추가
            G.add_edge(word, target_word, weight=weight)

for node in G.edges(data=True):
    node[0]


# 노드와 엣지 그리기
pos = nx.spring_layout(G, k = 1.5, seed = 17, iterations = 55)

# 노드 그리기 (노드 크기는 단어 등장 횟수에 비례, 색상은 word_colors 딕셔너리에 따름)
nx.draw_networkx_nodes(G, pos, 
                       node_size=[G.nodes[u].get('size', 5)*100 for u in G.nodes()], 
                       node_color=[color_dict[u] for u in G.nodes()])

# 그 다음, 엣지를 그립니다. 이 때, 엣지의 두께는 가중치에 비례하도록 합니다.
edges = nx.draw_networkx_edges(G, pos, edge_color=[color_dict[u[0]] for u in G.edges()],
                               width=[G[u][v]['weight']/5 for u, v in G.edges()])

# 라벨 그리기
labels = nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')

plt.show()






# Seaborn의 barplot 함수를 사용하여 시각화
plt.figure(figsize=(19.2, 10.8), dpi=100)
sns.barplot(x = count_list, y = word_list, palette=[color_dict.get(i, 'gray') for i in word_list])
plt.title(f'{section_name} { char_name} \n {start_date + "~" + end_date}', fontsize=25, pad=20)
plt.xlabel('언급된 수', fontsize=25, labelpad=40)
plt.ylabel('키워드', fontsize=25, labelpad=60, rotation=0)
plt.xticks([])
plt.yticks([])

# 그래프 끝 부분에 컬럼 이름 표시
for i, value in enumerate(count_list):
    plt.text(value , i  , str(value), ha='left', va='center', fontsize=15)
    plt.text(value - 1, i , word_list[i], ha='right', va='center', fontsize=17, fontweight='bold')

plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/keyword_frequencies_{section_name}{char_name}.png')  # 그래프를 이미지 파일로 저장

plt.close()  # 그래프 창을 닫음

# abc = ['쇼이치는 좋다, 너프해라, 너프, 너프, 너프 고양이',
#        '쇼이치 인벤',
#        '쇼이치 인벤',
#        '쇼이치 인벤',
#        '인벤 너프',
#        '인벤 너프',
#        '인벤 너프',
#        '인벤 너프',
#        '인벤 너프',
#        '인벤 너프',]
       


# date_dt = datetime.strptime(f'2020-09-06', '%Y-%m-%d')
# date_dt1 = datetime.strptime(f'2020-12-06', '%Y-%m-%d')

# # 예시 문장 리스트
# texts = user_comment.loc[(user_comment['date'] > date_dt) & (user_comment['date'] <  date_dt1)]['comment']

# # 전처리 수행
# preprocessed_texts = [preprocess_text(text) for text in abc]
# preprocessed_texts
# target_word = '쇼이치'
# co_occurrence = Counter()

# for sentence in preprocessed_texts:
#     if target_word in sentence:
#         co_occurrence.update([word for word in sentence if word != target_word])



section_ploting('2020-09-06' ,'2020-12-06', '유저 유입')
section_ploting('2020-12-06' ,'2021-01-10', '유저 유지')
section_ploting('2021-01-10' ,'2021-04-20', '유저 이탈')
section_ploting('2021-02-10' ,'2021-04-20', '유저 이탈 (티밍)')
section_ploting('2021-01-10' ,'2021-03-01', '유저 이탈 (티밍)1')
section_ploting('2021-04-20', '2022-05-22' ,'충성 고객(loyal customers)')
section_ploting('2022-05-22', '2022-06-25' ,'일시적 증가')
section_ploting('2022-06-25', '2023-05-16' ,'다시 감소')

section_ploting_char('2020-09-06' ,'2020-12-06', '유저 유입 (캐릭터)')
section_ploting_char('2020-12-06' ,'2021-01-10', '유저 유지 (캐릭터)')
section_ploting_char('2021-01-10' ,'2021-04-20', '유저 이탈 (캐릭터)')
section_ploting_char('2021-04-20', '2022-05-22' ,'충성 고객(loyal customers) (캐릭터)')
section_ploting_char('2022-05-22', '2022-06-25' ,'일시적 증가 (캐릭터)')
section_ploting_char('2022-06-25', '2023-05-16' ,'다시 감소 (캐릭터)')

section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '쇼이치')
section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '실비아')
section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '아이솔')
section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '피오라')
section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '문제')
section_ploting_char_target('2020-09-06' ,'2020-12-06', '유저 유입', '생각')

section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '재키')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '현우')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '쇼이치')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '아이솔')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '아야')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '유키')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '리다')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '문제')
section_ploting_char_target('2020-12-06' ,'2021-01-10', '유저 유지', '생각')

section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '로지')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '아야')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '루크')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '재키')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '로지')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '쇼이치')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '피오라')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '유키')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '문제')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '생각')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '유저')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '사람')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '공지')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '제재')
section_ploting_char_target('2021-01-10' ,'2021-04-20', '유저 이탈', '패치')
section_ploting_char_target('2020-12-29' ,'2021-01-15', '유저 이탈', '티밍')
section_ploting_char_target('2020-12-29' ,'2021-01-15', '유저 이탈', '전략')

section_ploting_char_target('2021-04-20', '2022-05-22', '충성 고객(loyal customers)', '알렉스')
section_ploting_char_target('2021-04-20', '2022-05-22', '충성 고객(loyal customers)', '유키')
section_ploting_char_target('2021-04-20', '2022-05-22', '충성 고객(loyal customers)', '재키')
section_ploting_char_target('2021-04-20', '2022-05-22', '충성 고객(loyal customers)', '아야')
section_ploting_char_target('2021-04-20', '2022-05-22', '충성 고객(loyal customers)', '문제')


# target_word = '쇼이치'

# co_occurrence = Counter([word for sentence in preprocessed_texts for word in sentence])

# for sentence in texts:
#     words = [word for word in komoran.morphs(sentence) if word not in stopwords]
#     if target_word in words:
#         co_occurrence.update([word for word in words if word != target_word])

# word_list = []
# count_list = []

# for word, count in co_occurrence.most_common(70):
#     word_list.append(word)
#     count_list.append(count)


# for day, data in zip(pd.to_datetime(user_comment['date']), user_comment['comment']):
#     print(day, data)


plt.figure(figsize=(25.6, 14.4), dpi=100)
plt.plot(daily_user['DateTime'][:250], daily_user['Players'][:250])
plt.xlabel('date')
plt.ylabel('User')
plt.title('User Num')

# plt.axvline(x=pd.to_datetime('2020-12-06'), color='r', linestyle='--')
# plt.axvline(x=pd.to_datetime('2021-01-10'), color='r', linestyle='--')
# plt.axvline(x=pd.to_datetime('2021-02-10'), color='g', linestyle='--')
plt.axvline(x=pd.to_datetime('2021-03-31'), color='b', linestyle='--')
# plt.axvline(x=pd.to_datetime('2021-04-20'), color='r', linestyle='--')
# plt.axvline(x=pd.to_datetime('2022-05-22'), color='r', linestyle='--')
# plt.axvline(x=pd.to_datetime('2022-06-25'), color='r', linestyle='--')

# plt.text(pd.to_datetime('2020-09-29'), max(daily_user['Players']), '유저 유입', rotation=0, va='bottom')
# plt.text(pd.to_datetime('2020-12-08'), max(daily_user['Players']), '유저 유지', rotation=0, va='bottom')
# plt.text(pd.to_datetime('2021-02-10'), max(daily_user['Players']), '유저 이탈', rotation=0, va='bottom')
# plt.text(pd.to_datetime('2021-09-20'), max(daily_user['Players']), '충성 고객(loyal customers)', rotation=0, va='bottom')
# plt.text(pd.to_datetime('2022-05-28'), max(daily_user['Players']), '일시적\n 증가', rotation=0, va='bottom')
# plt.text(pd.to_datetime('2022-12-15'), max(daily_user['Players']), '다시 감소', rotation=0, va='bottom')
plt.text(pd.to_datetime('2021-03-31'), max(daily_user['Players']), '2021-03-31', rotation=0, va='bottom')

plt.show()

plt.savefig(f'C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/plot/agg_user_num.png')  # 그래프를 이미지 파일로 저장


plt.close()

