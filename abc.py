from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models import FlexSendMessage
from urllib.parse import quote
app = Flask(__name__)
#Line-bot
line_bot_api = LineBotApi('gBbTtdzjIqATV1CqqqEBUoR3PBD7T6aa0PCyw0ePimZ6GDsbDOCft8jIZGFaLkhNnEZsrg0gV34ScgiAWEhs7W55Plh5Ksk/x52ylRBCrSA2YbtlBR2sytPPKZZLVN1RzPM7PlOnQsrI5q/H94DrBwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f218a1113705cacc8f5868035c84c9a3')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#爬蟲
def eat(x,y):
    import requests
    from bs4 import BeautifulSoup
    store_list =[]
    star_list = [] 
    address_list = []
    img_url_list = []
    time_list = []
    url_list = []
    map_list = []
    keys1 = x
    keys2 = y
    
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    r = requests.get("https://ifoodie.tw/explore/"+keys1+"/list/"+keys2,headers = my_headers)
    if r.status_code == 200:
        # print(r.text)
        soup = BeautifulSoup(r.text,'html.parser')
        title = soup.find_all('a', class_="jsx-558691085 title-text")
        star = soup.find_all('div', class_="jsx-1207467136 text")
        address = soup.find_all('div',class_="jsx-558691085 address-row")
        img = soup.select("div.jsx-3081451459.item-list img")
        time = soup.select("div.jsx-558691085.info")
        url = soup.find_all('a',class_='jsx-558691085 click-tracker')
#抓出來存取到list
        for t,l,a,h,u in zip(title,star,address,time,url):
            store_list.append(t.text)
            star_list.append(l.text + "☆")
            address_list.append(a.text)
            time_list.append(h.text)
            url_list.append("https://ifoodie.tw"+u.get('href'))
            map_list.append("https://www.google.com.tw/maps/dir//"+quote(a.text))
            
#圖檔判別
            for i in img:
                if 'src' in i.attrs:  
                    if i['src'].startswith('data'):
                            i_url=i.get('data-src')
                            if i_url.endswith('360'):
                                img_url_list.append(i_url)
                    else:
                        i_url=i.get('src')
                        if i_url.endswith('360'):
                            img_url_list.append(i_url)
   
    message = image_carousel(store_list,star_list,address_list,img_url_list,time_list,url_list,map_list,"收尋美食結果")
    return message

#網路爬蟲組合成FlexSendMessage物件
def image_carousel(store_list,star_list,address_list,img_url_list,time_list,url_list,map_list,alt_text):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for store, star, address, img, time ,url1,mapurl in zip(store_list, star_list, address_list, img_url_list, time_list, url_list, map_list):
        
        if i<10:
            bubble =    {     
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": img,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": store[:30]if len(store)<30 else store[:30] + '...',
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "icon",
            "size": "sm",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": star,
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1,
                "text": "地點"
              },
              {
                "type": "text",
                "text": address,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "營業時間",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": str(time),
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "地圖",
          "uri": mapurl
        }
      },
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "網站",
          "uri": url1
        }
      }
    ],
    "flex": 0
  }
}
            contents['contents'].append(bubble)
            i+=1 
    #print(contents)
    message = FlexSendMessage(alt_text=alt_text,contents=contents)
    return message

#客戶端訊息處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    city = event.message.text.split(' ')[0]
    food = event.message.text.split(' ')[1]
    message = eat(city,food)
    # print(type(message))
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ.get('PORT', 5000))
