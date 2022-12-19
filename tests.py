import requests
import base64

daata = {"userId":"xkykm9p6","game":"67","channelNo":"410001","token":"d09c3e08c6908dcf947d72a42e3c1ffb","username":""}
a = requests.post("https://lvdgjosgame.ltgamesglobal.net/SDKLogin",data=daata)
ac = a.content.decode("utf-8")

f = open("testsfile.txt","wb")
f.write(base64.b64decode(ac))
print(base64.b64decode(ac).decode("ASCII"))