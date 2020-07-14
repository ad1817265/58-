from lxml import etree
import re
import requests
import re
import base64
from fontTools.ttLib import TTFont
header={
 
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    
}

r=requests.get('https://gl.58.com/chuzu/',headers=header)
seletor=etree.HTML(r.text)
# for item in seletor.cssselect('div.money'):
#     print(item.xpath("string(.)"))
font1= re.findall("charset=utf-8;base64,(.*?)'\)",r.text)[0]
# print(font1)
byte=base64.b64decode(font1)
with open('d:/58fangchan.ttf','wb') as f:
    f.write(byte)
font1=TTFont('d:/58fangchan.ttf')
font1.saveXML('d:/58fangchan.ttf')  



def transCharByfont(font1:TTFont,string:str):

    unicode_to_glyph=font1.getBestCmap()
    true_string=''
    for char in string:
        unicode=ord(char)
        if unicode in unicode_to_glyph:
            # 判断是否经过字体反扒处理
            glyph=unicode_to_glyph[unicode]
            char=str(font1.getReverseGlyphMap()[glyph]-1)
        true_string+=char
    return true_string

def get_true():
    # 获取真实的房产信息
    seletor1=etree.HTML(r.text)
    for item in seletor.cssselect('.house-list li')[:-1]:
        # print(item)
        title=item.xpath("./div[@class='des']/h2/a/text()")[0].strip()
        true_title=transCharByfont(font1,title)
        room=item.xpath("normalize-space(./div[@class='des']/p[@class='room']/text())")
        true_room=transCharByfont(font1,room)
        price=item.xpath("./div[@class='list-li-right']/div[@class='money']/b/text()")[0].strip()
        true_price=transCharByfont(font1,price)
        
        print(true_title,true_room,true_price+'元/月')
        
        
get_true()
