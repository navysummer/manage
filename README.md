# 安装依赖
在当前路径下执行一下命令：
```cmd
pip install -r requirements.txt
```

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
sk = 'xxxxxxxxxxxxxxxxxxx'
'''
ip可以填不带http://前缀的ip或者域名
'''
ip = 'xxxxxxxxxxxxxxxxxxx'
phone = '184xxxx0317'
password = 'xxxxxxxxxxxxxxxxxxx'
'''
System类的所有参数为System(ip,phone,password,sk,port=80)
port参数默认80,如果是80可以不太填
'''
sy = System(ip,phone,password,sk)
'''
getAuthList(page,limit)函数包含两个参数：page和limit
默认page=1,limit=100
'''
data = sy.getAuthList()
print(data)
```
