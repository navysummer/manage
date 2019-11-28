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
ga = GoogleAuthenticator()
QR_path = 'chart.png'
code = ga.QR2code(QR_path)
print(code)
```
# 获取授权列表
```python
from manage import System
ip = 'xxx.xxx.xxx.xxx'
phone = '184xxxx0317'
password = 'xxxxxxxxx'
sy = System(ip,phone,password,sk)
data = sy.getAuthList()
print(data)
```
