from manage import GoogleAuthenticator
sk = 'cie5rsgznzqaxtkclxjrra4cxhkajuam'
ga = GoogleAuthenticator(sk)
code = ga.getTotp()
print(code)

from manage import System
ip = '10.129.133.205'
phone = '18401170317'
password = 'ctsso'
sy = System(ip,phone,password,sk)
data = sy.getAuthList()
print(data)