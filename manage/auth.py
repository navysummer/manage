# -*- coding: UTF-8 -*-

import time
import datetime
import math
import hmac
import base64
import qrcode
from PIL import Image
from pyzbar import pyzbar
from hashlib import sha1

'''
depend: qrcode,pillow,PIL,pyzbar

'''

class GoogleAuthenticator(object):

    def __init__(self,secretKey=None,digits=6,interval=30):
        self.secretKey = secretKey
        self.digits = digits
        self.interval = interval

    def __str_extend(self,old_str,length,extend_str):
        new_strs = None
        if len(old_str) < length:
            clen = length - len(old_str)
            s0 = ''.join([extend_str for i in range(clen)])
            new_strs = s0 + old_str
        elif len(old_str) == length:
            new_strs =  old_str
        return new_strs

    def __str_split(self,old_str,split_len,prefix='',suffix=''):
        array = []
        str_len = len(old_str)
        for i in range(0,str_len,4):
            if i + 4 < str_len:
                array.append(prefix+old_str[i:i+4]+suffix)
            else:
                array.append(prefix+old_str[i:str_len]+suffix)
        return array

    def __base32tohex(self,base32str):
        base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        bits = ""
        for i in range(len(base32str)):
            char = str(base32str[i]).upper()
            idx = int(base32chars.index(char))
            bit = self.__str_extend(format(idx,'b'),5,'0')
            if bit is None:
                raise Exception('bit={},len={}'.format(bit,len(bit)))
            bits += bit
        bitArray = self.__str_split(bits,4,'0b')
        hexstr = ''.join([format(int(i,2),'x') for i in bitArray])
        return hexstr

    def __get_HexSecret(self):
        hexstr = self.__base32tohex(self.secretKey)
        return hexstr

    def __byte_secret(self):
        missing_padding = len(self.secretKey) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode(self.secretKey, casefold=True)

    def __int_to_bytestring(self,i, padding=8):
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

    def __timecode(self, for_time):
        i = time.mktime(for_time.timetuple())
        return int(i / self.interval)

    def get_QR_url(self):
        base_url = "https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=200x200&chld=M|0&cht=qr&chl="
        QR_url = base_url + "otpauth://totp/user@host.com\%3Fsecret%3D" + self.secretKey
        return QR_url

    def get_QR_code(self):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
        data = self.get_QR_url()
        qr.add_data(data=data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="green", back_color="white")
        img.show()

    def QR2url(self,QR_path):
        base_url = 'https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=200x200&chld=M|0&cht=qr&chl='
        ourl = pyzbar.decode(Image.open(QR_path), symbols=[pyzbar.ZBarSymbol.QRCODE])[0].data.decode("utf-8")
        QR_url = base_url + ourl
        return QR_url

    def QR2code(self,QR_path):
        QR_url = pyzbar.decode(Image.open(QR_path), symbols=[pyzbar.ZBarSymbol.QRCODE])[0].data.decode("utf-8")
        i = QR_url.find('\%3Fsecret%3D')
        l = len('\%3Fsecret%3D')
        if i == -1:
            i = QR_url.find('?secret=')
            l = len('?secret=')
        if i == -1:
        	raise Exception('QR is error')
        j = QR_url.find('?',i+1)
        if j == -1:
            j = QR_url.find('\%3F',i+1)
        if j == -1:
            sk = QR_url[i+l:]
        else:
            sk = QR_url[i+l:j]
        self.secretKey = sk
        timestamp = self.__timecode(datetime.datetime.now())
        str_code = self.generate_otp(timestamp)
        return str_code 


    def generate_otp(self,timestamp):
        key = self.secretKey
        hasher = hmac.new(self.__byte_secret(), self.__int_to_bytestring(timestamp), sha1)
        # print(hasher.hexdigest())
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code
        return str_code

    def getTotp(self):
        timestamp = self.__timecode(datetime.datetime.now())
        str_code = self.generate_otp(timestamp)
        return str_code

    def at(self, for_time, counter_offset=0):
        if not isinstance(for_time, datetime.datetime):
            for_time = datetime.datetime.fromtimestamp(int(for_time))
        return self.generate_otp(self.timecode(for_time) + counter_offset)

    def verifyTotp(self,str_code):
        gTotp = self.getTotp()
        if gTotp == str_code:
            return True
        else:
            return False

