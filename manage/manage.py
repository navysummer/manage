# -*- coding: UTF-8 -*-
import requests
from .auth import GoogleAuthenticator
try:
    from urllib.parse import urlparse,parse_qs
except ImportError:
    from urlparse import urlparse,parse_qs

class System(object):
    """docstring for System"""
    def __init__(self,url,phone,password,sk):
        super(System, self).__init__()
        self.urlinfo = urlparse(url)
        Host = self.urlinfo.netloc
        scheme = self.urlinfo.scheme
        path = self.urlinfo.path
        params = self.urlinfo.params
        querys = self.urlinfo.query
        queryDict = parse_qs(querys)
        self.__url = scheme + "://" + Host
        self.phone = phone
        self.password = password
        self.__sk = sk
        self.session = None
        self.cookies = None
        self.__login()

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
        response = requests.post(__login_url,data=__login_data,headers=__login_headers,allow_redirects=False)
        if response.status_code == 302:
            cookies = response.cookies.get_dict()
            if not cookies:
                raise Exception('login fail')
            if 'session' in cookies:
                self.session = cookies['session']
                self.cookies = cookies
            else:
                raise Exception('login fail')
        else:
            self.__login()
        

    def getAuthList(self,page=1,limit=100):
        __authList_url = self.__url + '/system/auth/getSystemsByPage'
        if self.cookies is None:
            raise Exception('login fail')
        __form_data = {
            'page':page,
            'limit':limit
        }
        response = requests.post(__authList_url,data=__form_data,cookies=self.cookies)
        data = response.json()
        self.__logout()
        return data

    def __logout(self):
        __logout_url = self.__url + '/logout'
        if self.cookies is None:
            raise Exception('login fail')
        response = requests.get(__logout_url,cookies=self.cookies)
        if response.status_code == 200:
            return True
        else:
            return False

        