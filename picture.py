import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd


user_comment = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/user_commentV1.csv')

user_comment = user_comment.drop(columns=['Unnamed: 0'])

daily_user = pd.read_csv('C:/Users/pgs66/Desktop/GoogleDrive/python/ER_user_analysis/data/daily_user.csv')

daily_user['DateTime'] = pd.to_datetime(daily_user['DateTime'])

user_comment['date'] = pd.to_datetime(user_comment['date'])





# 단어 등장 횟수를 나타내는 dictionary 예시
word_counts = {'apple': 10, 'banana': 10, 'cherry': 7, 'date': 2, 'elderberry': 4}

# 단어들이 같이 나온 횟수를 나타내는 nested dictionary 예시
# 'apple'과 'banana'가 2번 같이 나왔다면, cooccurrence['apple']['banana'] = 2
cooccurrence = {
    'apple': {'banana': 10, 'cherry': 1},
    'banana': {'apple': 10, 'cherry': 1, 'date': 1},
    'cherry': {'apple': 1, 'banana': 1, 'date': 2, 'elderberry': 1},
    'date': {'banana': 1, 'cherry': 2, 'elderberry': 2},
    'elderberry': {'cherry': 1, 'date': 2},
}

# 가능한 색상 목록 가져오기
colors = list(mcolors.CSS4_COLORS.keys())

# 각 단어에 대해 임의의 색상 선택
word_colors = {word: colors[i % len(colors)] for i, word in enumerate(word_counts.keys())}

# 그래프 생성
G = nx.Graph()

# 노드 추가 (노드 크기는 단어 등장 횟수에 비례)
for word, count in word_counts.items():
    G.add_node(word, size=count)

# 엣지 추가 (엣지 가중치는 단어들이 같이 나온 횟수에 비례)
for word, connections in cooccurrence.items():
    for target_word, weight in connections.items():
        if weight >= 2:  # 가중치가 2 이상일 때만 엣지를 추가
            G.add_edge(word, target_word, weight=weight)

# 노드와 엣지 그리기
pos = nx.fruchterman_reingold_layout(G)

# 노드 그리기 (노드 크기는 단어 등장 횟수에 비례, 색상은 word_colors 딕셔너리에 따름)
nx.draw_networkx_nodes(G, pos, node_size=[G.nodes[u]['size']*200 for u in G.nodes()],
                       node_color=[word_colors[u] for u in G.nodes()])

# 그 다음, 엣지를 그립니다. 이 때, 엣지의 두께는 가중치에 비례하도록 합니다.
edges = nx.draw_networkx_edges(G, pos, edge_color=[G[u][v]['weight'] for u, v in G.edges()],
                               width=[G[u][v]['weight'] for u, v in G.edges()])

# 노드 라벨을 그립니다.
nx.draw_networkx_labels(G, pos)

plt.show()

