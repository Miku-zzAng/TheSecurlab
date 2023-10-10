from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)

def makeUrl(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page)
        print("생성url: ", url)
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
        print("생성url: ", urls)
        return urls    

# html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

#html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
def articles_crawler(url):
    #html 불러오기
    original_html = requests.get(i,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver,'href')
    return url


#####크롤링 시작#####

#검색어 입력
search = ["접근권한취약점", "암호화실패", "암호화오류", "SSRF", "CSRF", "취약한컴포넌트", "오래된컴포넌트", "OWASP"]
#검색 시작할 페이지 입력
page = 1 
#검색 종료할 페이지 입력
page2 = 10

#뉴스 크롤러 실행
news_titles = []
finding_url = []
news_contents =[]
news_dates = []
news_image = []
news_writer = []


# naver url 생성
for search_num in range(len(search)) :
    url = makeUrl(search[search_num],page,page2)

    news_url =[]
    
    for i in url:
        url = articles_crawler(url)
        news_url.append(url)


    #제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
    def makeList(newlist, content):
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist

    
    #제목, 링크, 내용 담을 리스트 생성
    news_url_1 = []

    #1차원 리스트로 만들기(내용 제외)
    makeList(news_url_1,news_url)

    #NAVER 뉴스만 남기기
    final_urls = []
    for i in tqdm(range(len(news_url_1))):
        if "news.naver.com" in news_url_1[i]:
            final_urls.append(news_url_1[i])
        else:
            pass

    # 내용 크롤링
    for i in tqdm(final_urls):
        #각 기사 html get하기
        news = requests.get(i,headers=headers)
        news_html = BeautifulSoup(news.text,"html.parser")

        # 제목 가져오기
        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")
    
        # 본문 가져오기
        content = news_html.select("article#dic_area")
        if content == []:
            content = news_html.select("#articeBody")
        content = ''.join(str(content))

        # 사진 url 가져오기
        image = news_html.find("img", id="imga1")
        if image:
            link = image.get('src')
        else:
            image_url = news_html.find("meta", property="og:image")
            if image_url:
                link = image_url['content']
            else:
                link = None

        # 작성자 가져오기
        writer = news_html.select_one("span.byline_s")
        if title == None:
            title = news_html.select_one("p.byline_p > span")

        # html태그제거 및 텍스트 다듬기
        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        writer = re.sub(pattern=pattern1, repl='', string=str(writer))
        pattern2 = """[\n\// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')
        content = content.replace("[", "").replace("]", "")
        
        search_info = ["피해사례", "피해액", "피해 사례", "피해자", "피해그룹", "피해 그룹", "피해 규모", "피해규모", "실제 피해"] 
        for info in search_info:
            if info in content:
                news_titles.append(title)
                news_contents.append(content)
                news_writer.append(writer)
                news_image.append(link)
                finding_url.append(i)

                try:
                    html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
                    news_date = html_date.attrs['data-date-time']
                except AttributeError:
                    news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
                    news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
                # 날짜 가져오기
                news_dates.append(news_date)
    

    #크롤링 데이터 각 길이 확인
    print('news_title: ',len(news_titles))
    print('news_url: ',len(finding_url))
    print('news_contents: ',len(news_contents))
    print('news_dates: ',len(news_dates))
    print('news_image: ',len(news_image))
    print('news_writer: ', len(news_writer))

###데이터 프레임으로 만들기###
import pandas as pd

#데이터 프레임 만들기
news_df = pd.DataFrame({'date':news_dates,'title':news_titles,'writer':news_writer,'link':finding_url,'content':news_contents,'image':news_image})

#중복 행 지우기
news_df = news_df.drop_duplicates(keep='first',ignore_index=True)
print("\n")
print(news_df)

#데이터 프레임 저장
now = datetime.datetime.now() 
news_df.to_csv('{}_{}.csv'.format(search,now.strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)