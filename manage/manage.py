# -*- coding: UTF-8 -*-
import requests
from .auth import GoogleAuthenticator

class System(object):
    """docstring for System"""
    def __init__(self,ip,phone,password,sk,port=80):
        super(System, self).__init__()
        self.ip = ip
        if port == 80:
            self.__url = 'http://' + ip
        else:
            self.__url = 'http://'+ ip + ':' + port
        self.phone = phone
        self.password = password
        self.__sk = sk
        self.session = None

    def __login(self):
        __login_url = self.__url + '/login'
        __login_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'44',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':self.ip,
            'Origin':self.__url,
            'Referer':__login_url,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        ga = GoogleAuthenticator(self.__sk)
        code = ga.getTotp()
        __login_data = {
            'phone':self.phone,
            'password':self.password,
            'code':code
        }
        # s = requests.Session()
        response = requests.post(__login_url,data=__login_data,headers=__login_headers,allow_redirects=False)
        if response.status_code == 302:
            cookies = response.cookies.get_dict()
            if not cookies:
                raise Exception('get cookies fail')
            if 'session' in cookies:
                session = cookies['session']
                # print(session)
                return session
            else:
                raise Exception('get session fail')
        else:
            self.__login()
        

    def getAuthList(self,page=1,limit=100):
        __authList_url = self.__url + '/system/auth/getSystemsByPage'
        if self.session is None:
            self.session = self.__login()
        __headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'16',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':'session=' + self.session,
            'Host':self.ip,
            'Origin':self.__url,
            'Referer':self.__url + '/system/authList',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        __form_data = {
            'page':page,
            'limit':limit
        }
        response = requests.post(__authList_url,data=__form_data,headers=__headers)
        data = response.json()
        self.__logout()
        return data

    def __logout(self):
        __logout_url = self.__url + '/logout'
        if self.session is None:
            raise Exception('session not exist,logout fail')
        __logout_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Cookie':'session=' + self.session,
            'Host':self.ip,
            'Referer':self.__url,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = requests.get(__logout_url,headers=__logout_headers)
        if response.status_code == 200:
            return True
        else:
            return False

        