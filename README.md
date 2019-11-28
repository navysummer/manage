# 获取验证码
1.通过secretKey获取
```python
from manage import GoogleAuthenticator
sk = 'xxxxxxxxxxx'
ga = GoogleAuthenticator(sk)
code = ga.getTotp()
print(code)
```
2.通过二维码获取
```python
from manage import GoogleAuthenticator
sk = 'xxxxxxxxxxx'
ga = GoogleAuthenticator(sk)
QR_path = ''
code = ga.QR2code(QR_path)
print(code)
```
# 获取授权列表
```python
from manage import System
ip = '127.0.0.1'
phone = '137****3738'
password = 'xxxxxx'
sy = System(ip,phone,password,sk)
data = sy.getAuthList()
print(data)
```
