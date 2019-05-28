from process.dealfile import readelejson,readmeituanjson,readxingxuanjson

htmlpath='/Users/netboss/program/Ncode/text/023json/eleme1.json'
response=readelejson.delay(htmlpath)
responsetext=response.get()
print (responsetext)


