import feedparser
import subprocess
import os

# ssh-agent 실행
ssh_agent = subprocess.Popen(['ssh-agent', '-s'], stdout=subprocess.PIPE)
# ssh-add 실행
subprocess.call('ssh-add ~/.ssh/id_rsa', shell=True)

# 언론사 및 분야별 RSS 피드 URL 설정

rss_urls = {
    '조선일보': {
        '전체기사': 'https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml',
        '정치': 'https://www.chosun.com/arc/outboundfeeds/rss/category/politics/?outputType=xml',
        '경제': 'https://www.chosun.com/arc/outboundfeeds/rss/category/economy/?outputType=xml',
        '사회': 'https://www.chosun.com/arc/outboundfeeds/rss/category/national/?outputType=xml',
        '국제': 'https://www.chosun.com/arc/outboundfeeds/rss/category/international/?outputType=xml',
        '문화라이프': 'https://www.chosun.com/arc/outboundfeeds/rss/category/culture-life/?outputType=xml',
        '오피니언': 'https://www.chosun.com/arc/outboundfeeds/rss/category/opinion/?outputType=xml',
        '스포츠': 'https://www.chosun.com/arc/outboundfeeds/rss/category/sports/?outputType=xml',
        '연예': 'https://www.chosun.com/arc/outboundfeeds/rss/category/entertainments/?outputType=xml'
    },
    '동아일보': {
        '전체기사': 'https://rss.donga.com/total.xml',
        '정치': 'https://rss.donga.com/politics.xml',
        '사회': 'https://rss.donga.com/national.xml',
        '경제': 'https://rss.donga.com/economy.xml',
        '국제': 'https://rss.donga.com/international.xml',
        '사설칼럼': 'https://rss.donga.com/editorials.xml',
        '의학과학': 'https://rss.donga.com/science.xml',
        '문화연예': 'https://rss.donga.com/culture.xml',
        '스포츠': 'https://rss.donga.com/sports.xml',
        '사람속으로': 'https://rss.donga.com/inmul.xml',
        '건강': 'https://rss.donga.com/health.xml',
        '레져': 'https://rss.donga.com/leisure.xml',
        '도서': 'https://rss.donga.com/book.xml',
        '공연': 'https://rss.donga.com/show.xml',
        '여성': 'https://rss.donga.com/woman.xml',
        '여행': 'https://rss.donga.com/travel.xml',
        '생활정보': 'https://rss.donga.com/lifeinfo.xml',
        '스포츠': 'https://rss.donga.com/sportsdonga/sports.xml',
        '야구MLB': 'https://rss.donga.com/sportsdonga/baseball.xml',
        '축구': 'https://rss.donga.com/sportsdonga/soccer.xml',
        '골프': 'https://rss.donga.com/sportsdonga/golf.xml',
        '일반': 'https://rss.donga.com/sportsdonga/sports_general.xml',
        'e스포츠': 'https://rss.donga.com/sportsdonga/sports_game.xml',
        '엔터테인먼트': 'https://rss.donga.com/sportsdonga/entertainment.xml',
    },
    '매일경제': {
        '헤드라인': 'https://www.mk.co.kr/rss/30000001/',
        '전체뉴스': 'https://www.mk.co.kr/rss/40300001/',
        '경제': 'https://www.mk.co.kr/rss/30100041/',
        '정치': 'https://www.mk.co.kr/rss/30200030/',
        '사회': 'https://www.mk.co.kr/rss/50400012/',
        '국제': 'https://www.mk.co.kr/rss/30300018/',
        '기업경영': 'https://www.mk.co.kr/rss/50100032/',
        '증권': 'https://www.mk.co.kr/rss/50200011/',
        '부동산': 'https://www.mk.co.kr/rss/50300009/',
        '문화연예': 'https://www.mk.co.kr/rss/30000023/',
        '스포츠': 'https://www.mk.co.kr/rss/71000001/',
        '게임': 'https://www.mk.co.kr/rss/50700001/',
        'MBA': 'https://www.mk.co.kr/rss/40200124/',
        '머니앤리치스': 'https://www.mk.co.kr/rss/40200003/',
        'English': 'https://www.mk.co.kr/rss/30800011/',
        '이코노미': 'https://www.mk.co.kr/rss/50000001/',
        '시티라이프': 'https://www.mk.co.kr/rss/60000007/'
    },
        'NHK': {
        '主要ニュース': 'https://www3.nhk.or.jp/rss/news/cat0.xml',
        '社会': 'https://www3.nhk.or.jp/rss/news/cat1.xml',
        '科学・医療': 'https://www3.nhk.or.jp/rss/news/cat2.xml',
        '政治': 'https://www3.nhk.or.jp/rss/news/cat3.xml',
        '経済': 'https://www3.nhk.or.jp/rss/news/cat4.xml',
        '国際': 'https://www3.nhk.or.jp/rss/news/cat5.xml',
        'スポーツ': 'https://www3.nhk.or.jp/rss/news/cat6.xml',
        '文化・エンタメ': 'https://www3.nhk.or.jp/rss/news/cat7.xml',
    },
    'ニッカンスポーツ':{
        'スポーツ':'https://www.nikkansports.com/sports/atom.xml',
        '野球': 'https://www.nikkansports.com/baseball/atom.xml',
        'サッカー':'https://www.nikkansports.com/soccer/atom.xml',
        'ゴルフ': 'https://www.nikkansports.com/sports/golf/atom.xml',
        '格闘技':'https://www.nikkansports.com/battle/atom.xml',
        '競馬':'http://p.nikkansports.com/goku-uma/rss/atom.xml',
        '芸能':'https://www.nikkansports.com/entertainment/atom.xml',
        'AKB48':'https://www.nikkansports.com/entertainment/akb48/atom.xml',
        '社会':'https://www.nikkansports.com/general/atom.xml'
    },
    'Google':{
        '天気':'https://news.google.com/rss/search?q=天気&hl=ja&gl=JP&ceid=JP:ja',
        'WORLD':'https://news.google.com/news/rss/headlines/section/topic/WORLD?hl=ja&gl=JP&ceid=JP:ja',
        'NATION':'https://news.google.com/news/rss/headlines/section/topic/NATION?hl=ja&gl=JP&ceid=JP:ja',
        'BUSINESS' : 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=ja&gl=JP&ceid=JP:ja',
        'TECHNOLOGY' : 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja',
        'ENTERTAINMENT' : 'https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT?hl=ja&gl=JP&ceid=JP:ja',
        'SPORTS' : 'https://news.google.com/news/rss/headlines/section/topic/SPORTS?hl=ja&gl=JP&ceid=JP:ja',
        'SCIENCE' : 'https://news.google.com/news/rss/headlines/section/topic/SCIENCE?hl=ja&gl=JP&ceid=JP:ja',
    },

}

# 저장할 파일 경로 설정
file_path = "/home/dls32208/Documents/VRChatKoreaNews/"

# html 파일 생성 및 깃허브에 업로드
for press in rss_urls:
    for category in rss_urls[press]:
        rss_url = rss_urls[press][category]
        if not os.path.exists(file_path+"/"+press):
            os.mkdir(file_path+"/"+press)
        file_name = f"{press}/{category}.html"

        # feedparser로 RSS 뉴스 기사 파싱
        feed = feedparser.parse(rss_url)

        # html 파일 생성
        with open(os.path.join(file_path, file_name), "w") as f:
            f.write("<html>\n<head>\n<title>News</title>\n</head>\n<body>\n")
            # 뉴스 기사 쓰기
            for entry in feed.entries:
                f.write(f"<h2><a href='{entry.link}'>{entry.title}</a></h2>\n")
                f.write(f"<p>{entry.summary}</p>\n\n")
            f.write("</body>\n</html>")

        # 깃허브에 업로드
        subprocess.call(f"cd {file_path} && git add {file_name} && git commit -m 'Update news' && git push", shell=True)

# ssh-agent 종료
ssh_agent.kill()
