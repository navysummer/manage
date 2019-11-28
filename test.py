from manage import GoogleAuthenticator
sk = 'xxxxxxxxxxxxxxxxxxx'
ga = GoogleAuthenticator(sk)
code = ga.getTotp()
print(code)

from manage import GoogleAuthenticator
ga = GoogleAuthenticator()
QR_path = 'chart.png'
code = ga.QR2code(QR_path)
print(code)

from manage import System
ip = 'xxx.xxx.xxx.xxx'
phone = '184xxxx0317'
password = 'xxxxxxxxx'
sy = System(ip,phone,password,sk)
data = sy.getAuthList()
print(data)

