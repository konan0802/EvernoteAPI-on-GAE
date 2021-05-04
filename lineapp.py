from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = "ChZVXqJ0p77jaRvxCIMmunAKUNrPJuyTKf5P8ROL8PoQQ+SNrotL5ebjRqRkJ9WplS+xPFSJabUChA8bFs6aQJMU9paAY6/Qxw0Sln3aHYmhbCV5hBVe+EMCRFH9cYGG2FK97Ks+PsKMjvhdFYt32AdB04t89/1O/w1cDnyilFU="
USER_ID = "Uf6dc052d62c879a4e6befd2fa43dd742"

#エラーの送信
def sendError(sentText):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text="【Fatal Error】" + "\n" + "app: createEvernoteAutomatically" + "\n" + "server: GAE" + "\n" + "repository: EvernoteApi" + "\n" + sentText)
    line_bot_api.push_message(USER_ID, messages=messages)

#リマインドの送信
def sendMes(sentText):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text=sentText)
    line_bot_api.push_message(USER_ID, messages=messages)