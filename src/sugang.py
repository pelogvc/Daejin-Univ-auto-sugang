# -*- coding: utf-8 -*-
#
# auto sugang for Daejin Univ.
#
import requests
import string
import datetime
from datetime import datetime, timedelta
import time

class sugang(object):
    id = None
    pw = None
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    cookie = None

    def __init__(self, id, pw, date, code):
        self.id = id
        self.pw = pw
        self.date = date
        self.codes = list(code)

    #login
    def login(self):

        url = "http://dreams2.daejin.ac.kr/sugang/LoginB"
        header = {
            "User-Agent" : self.agent ,
            "referer"    : "http://dreams2.daejin.ac.kr"
        }
        data = {
            "user_flag"  : 1 ,
            "stdNo"      : self.id ,
            "passwd"     : self.pw
        }
        res = requests.post(url, data = data, headers = header, cookies = self.cookie)

        if res.status_code != 200:
            return False

        if res.cookies:
            self.cookie = res.cookies

        if res.content.find("window.history.go(-1);"):
            return False
        return True

    # 수강신청
    def sugang(self, code):
        # type: (object) -> object

        url = "http://dreams2.daejin.ac.kr/sugang/SugangWlsn0410"
        header = {
            "User-Agent" : self.agent ,
            "referer"    : "http://dreams2.daejin.ac.kr"
        }
        data = {
            "dir"       : "1" ,
            "cmd"       : "aply" ,
            "ic_sbjcd"  : code.replace("-", "") ,
            "urltype"   : "direct" ,
            "getsbjt_no": code.split("-")[0] ,
            "getclss_no": code.split("-")[1]
        }

        res = requests.post(url, data = data, headers = header, cookies = self.cookie)

        if res.status_code == 200 and res.content.find("과목이 수강 신청되었습니다") :
            return True
        else:
            return False

    #main
    def run(self):

        if self.id == None or self.pw == None or self.codes == None or self.date == None :
            print("아이디, 비밀번호, 수강목록을 확인하세요.")
            return False

        self.date = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')

        while True:

            now = datetime.now()
            starttime = datetime.now() + timedelta(minutes=1)


            #시간확인
            if self.date < starttime:
                print( "[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] 1초 쉼"  )
                time.sleep(1)
                continue

            #로그인
            if self.login() == False:
                print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] 로그인 실패, 1초 쉼")
                time.sleep(1)
                continue
            else:
                print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] 로그인 성공")

            #수강신청
            for i in self.codes:
                if self.sugang(self.codes[i]) == True:
                    print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] " + self.codes[i] + "신청 완료")
                    del(self.codes[i])

            #아직 남아있는가
            if len(self.codes) > 0:
                time.sleep(1)
                continue

            print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] 모든 과목 신청 완료")
            break





date = "2017-08-07 09:20:00"
id = "test"
pw = "test"
code = {
    "2014-22",
    "4213-11"
}

auto = sugang(id, pw, date, code)
auto.run()
