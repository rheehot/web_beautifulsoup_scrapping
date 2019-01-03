"""
# 인천 청라, 송도지역 미세먼지 측정값 스크래핑
# > 1. 송도 = https://bit.ly/2EWi9vM
# > 1. 청라 = https://bit.ly/2Al7h6y
#
# * TODO: 계측 센서 갯수가 다르므로 필터링 방식이 달라져야 한다
# * 송도 = 6개 / 청라 = 4개
"""
# * 청라, 송도지역 미세먼지 측정값 스크래핑
print(__doc__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests

from pprint import pprint
from bs4 import BeautifulSoup


URLS = [
    'http://air.incheon.go.kr/airinch/real3.html?area_other_index=999991',
    'http://air.incheon.go.kr/airinch/real3.html?area_other_index=999992',
]

""" 주의!: 송도와 청라는 데이터 갯수가 틀려서 필터링 방법을 달리해야 함. """
URL = URLS[0]  # 0=청라 - 측정치 1+3 = 4개
URL = URLS[1]  # 1=송도 - 측정치 1+6 = 7개


RESPONSE = requests.get(URL)
SOUP = BeautifulSoup(RESPONSE.content, 'html.parser')
TABLE = SOUP.find_all('table', {'class': 'view'})

TDS = TABLE[0].find_all('td')
FONTS = TABLE[0].find_all('font')
SPANS = TABLE[0].find_all('span')


def pause_process():
    input('GO?:')


# 데이터의 길이를 기준으로 구분한다 (EDA)
# > 12자 길이를 넘어가는 데이터는 한글 테이터이다.
# In[3]:

DATA = []
DATE = []

for n, span in enumerate(SPANS, 0):
    neat_span = str(span.text).strip()

    if len(neat_span) > 12:
        """ 날짜와 시간을 분리해서 각각 넣는다 """
        DATE.append(neat_span[:-3])     # 날짜
        DATA.append(neat_span[-3:])     # 시간
    else:
        DATA.append(neat_span)


""" 리스트에 담긴 해당 날짜를 보여준다, 그래봤자 2개 지만.. """
print(DATE[0])      # 2018년12월 29일 -- 오늘
print(DATE[1])      # 2018년12월 28일 -- 하루 전
pause_process()

START = 8           # 8,
REPEAT = 100
NUM = 0             # 넘버링(갯수 카운트)

for n in range(START, (6 * (REPEAT + 2)), 7):
    datum = DATA[n:n + 7]

    if len(datum) is not 0:
        NUM += 1
        print("%2s .. %s" % (NUM, datum))
    else:
        break


pause_process()

# 센서값 컬럼 7개 저장. ... 센서컬럼(단위)
# ['Time(24Hr)', 'SO2(ppm)', 'NO2(ppm)',
#   'O3(ppm)', 'CO(ppm)', 'PM10(㎍/㎥)', 'PM2.5(㎍/㎥)']

COLUMNS = ['Time(24Hr)',]

for n in range(2,8):
    COLUMNS.append(DATA[n])

print(COLUMNS)
pause_process()



START = 8
REPEAT = 100

AIR_DATA = []

for n in range(START, (6 * (REPEAT + 2)), 7):
    datum = DATA[n:n + 7]             # 시간 + 센서값6개

    if len(datum) is not 0:
        datum[0] = datum[0][:2]            # (시간) 숫자 만 잘라냄
        AIR_DATA.append(datum)
    else:
        break

pprint(AIR_DATA)        # 48시간 데이터
len(AIR_DATA)
pause_process()



# Numpy Array 로 변경 한다.
AIR_DATA_NP = np.array(AIR_DATA)
print(AIR_DATA_NP)
pause_process()


# Pandas DataFrame 오브젝트로 변경한다.
df = pd.DataFrame(AIR_DATA_NP, columns=COLUMNS)
df.head(n=10)



""" 1. 그래프를 그리는 옵션 """
# x축의 해상도를 설정한다 (시작, 끝, div_number)

x_args = [0, 50, 50]
# x = np.linspace(*x_args)

plt.hist(df.head(5))
""" 그래프에 텍스트를 입히는 옵션 """
plt.title("DATA-PLOT")        # 타이틀
plt.xlabel('x label')           # x 라벨
plt.ylabel('y label')           # y 라벨
plt.show()

plt.hist(DATA)
""" 그래프에 텍스트를 입히는 옵션 """
plt.title("HISTOGRAM - DISTRIBUTION")        # 타이틀
plt.xlabel('x label')           # x 라벨
plt.ylabel('y label')           # y 라벨
plt.show()

plt.plot(DATA)
""" 그래프에 텍스트를 입히는 옵션 """
plt.title("DATA-PLOT")        # 타이틀
plt.xlabel('x label')           # x 라벨
plt.ylabel('y label')           # y 라벨
plt.show()


# Data Frame 을 엑셀로 저장한다. (CSV화일)
df.to_csv('air_incheon.csv', sep=',', encoding='utf-8')