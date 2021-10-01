import urllib 
import requests 
 
def mapppost_content(useraccount,apikey,chatsn,content):
    content_utf8 = content.encode("UTF-8")#轉UTF8
    content_utf8_url = urllib.parse.quote_plus(content_utf8)#轉URL
    url = "http://mapp.local/teamplus_innolux/API/IMService.ashx" 
    payload = "ask=sendChatMessage&account={}&api_Key={}&chat_sn={}&content_type=1&msg_content={}&file_show_name=&undefined=".format(useraccount,apikey,chatsn,content_utf8_url)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return(response.text)

