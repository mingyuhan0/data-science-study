import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# ctrl+페이지 클릭 -> 다른 url로 열림

def step1_GetData():
    #영화코드
    code_list=[184318, 191597]
    #현재 크롤링 중인 영화가 첫번째 영화인지 여부
    chk = False
    #영화의 갯수만큼 반복
    for code in code_list:
        #1단계 : 해당 영화의 평점 페이지 수 계산
        site1 = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=%d&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false' % code #str처리
        res1 = requests.get(site1)
        if res1.status_code == requests.codes.ok:
            # html 코드 분석
            bs1 = BeautifulSoup(res1.text, 'html.parser')

            # class = 중복가능
            # id = 중복불가능(중복되는 경우도 꽤 있음 -> html5를 지키지 않는 곳)
            score_total = bs1.find(class_="score_total")
            ems = score_total.find_all('em') #find_all : list로 리턴
            #print(ems[0]) #ems확인
            score_total = int(ems[0].text.replace(',',''))

            #페이지수 계산
            pageCnt = score_total // 10
            if score_total % 10 > 0:
                pageCnt += 1
            print(pageCnt)

            #현재 페이지 번호
            now_page = 1
            pageCnt = 1 #나중에 지우기

            #2단계 : 평점, 글, 평점 ...필요한 정보 가져오기
            while now_page <= pageCnt:
                sleep(0.5) #잠시 대기
                #요청 페이지 주소
                site2 = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=%d&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=%d' % (code, now_page)
                now_page += 1
                #print(site2)
                res2 = requests.get(site2)
                if res2.status_code ==requests.codes.ok:
                    bs2 = BeautifulSoup(res2.text, 'html.parser')
                    score_result = bs2.find(class_='score_result')
                    lis = score_result.find_all('li')
                    #print(lis)
                    df = pd.DataFrame()
                    for obj in lis:
                        #평점
                        star_score = obj.find(class_='star_score')
                        star_em = star_score.find('em')
                        star_score = int(star_em.text)
                        #평가글
                        score_reple = obj.find(class_='score_reple')
                        reple_p = score_reple.find('p')
                        reple_p_span = reple_p.find_all('span')
                        #print(len(reple_p_span[1].text))
                        if len(reple_p_span) >= 1:
                            score_reple = reple_p_span[1].text
                        #id
                        reple_id = obj.find(class_='score_reple')
                        id_a = reple_id.find('a')
                        id_span = reple_id.find_all('span')
                        #print(id_span[2].text)
                        id = id_span[2].text

                        # 데이터 누적(저장 위치에 대한 고민 필요 -> 지금은 2단계 안에 있으니 여기다 표시)
                        df = df.append([[id, score_reple, star_score]], ignore_index=True)
                    #저장 : 처음 저장(파일이 없을 때), 두번째 이후 저장(파일이 있을 때)
                    if chk == False:
                        df.columns = ['id', 'text','star']
                        df.to_csv('naver_star_data.csv', index=False, encoding='utf-8')
                    else:
                        df.to_csv('naver_star_data.csv', index=False, encoding='uth-8', mode='a', header=False)
                # %d/%d형식 지정
                print('%d / %d' % (now_page, pageCnt))
                now_page += 1

