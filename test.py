from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from time import sleep

s = serializer('key', 100)
info = {'id': 1234}
token = s.dumps(info)
token = token.decode()
hypertext = '<a href="localhost:8000/user/verify/%s" >localhost:8000/user/verify/%s </a>' %(token, token)
print(hypertext)