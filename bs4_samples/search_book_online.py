"""
# 교보문고 검색결과를 크롤링으로 보여 줌 -- by Ask Company
# 써치 키워드의 인코딩을 다소 어렵게 함 ... keyword_encode()
#
# https://gist.github.com/allieus/2a083babf5a24bc10e7f5c9877473af5?fbclid=IwAR19rnMgVLeMi1-wp28hSMye685vRoSzcQMhp_qjX3WregAzQDmzZsqrj_U
#
#
#\n\n\n"""
print(__doc__)

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin


def keyword_encode(s):
    """ 인코드를 이상하게 함: '파이썬' --> &#54028;&#51060;&#50028;
    # keyword_encode 로직은 교보문고 페이지의 javascript
    # 로직을 그대로 흉내내어 만들었음.
    """
    encoded = ''
    for ch in s:
        code = ord(ch)
        if code > 127:
            encoded += '&#' + str(code) + ';'
        else:
            encoded += str(code)
    return encoded

def search(keyword):
    data = {
        'vPstrKeyWord': keyword_encode(keyword),
        'vPstrCategory': 'TOT',
        'vPplace': 'top',
        'searchKeyword': quote(keyword.encode('euckr')),
    }

    search_url = "http://www.kyobobook.co.kr/search/SearchCommonMain.jsp"

    res = requests.post(search_url, data=data)
    soup = BeautifulSoup(res.text, 'html.parser')

    for tag in soup.select('.title a'):
        detail_url = tag['href']
        if 'detailViewKor' in detail_url:

            detail_url = urljoin(search_url, detail_url)
            title = tag.select_one('strong').text.strip()

            print(title)
            print(detail_url)


if __name__ == '__main__':
    _encoded = keyword_encode('파이썬')
    print(_encoded)                     # &#54028;&#51060;&#50028;

    # search('파이썬')

    # TODO: 써치결과를 MD화일로 작성해서 WRITE 화일을 만듬
    # TODO: 상위 3페이지의 결과를 마크다운으로 만들어 WRITE 해줌


""" Keyword = '파이썬'

Do it! 점프 투 파이썬
http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9788997390915&orderClick=LAG&Kc=

케라스 창시자에게 배우는 딥러닝(Deep Learning with Python)
http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9791160505979&orderClick=LAG&Kc=
... continue ...
"""
