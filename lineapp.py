from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

# ローカルで動かす際にはdotenvをインポート
#from dotenv import load_dotenv
#load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_USER_ID = os.environ['LINE_USER_ID']

# エラーの送信
def sendError(sentText):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text="【Fatal Error】" + "\n" + "app: createEvernoteAutomatically" + "\n" + "server: GAE" + "\n" + "repository: EvernoteApi" + "\n" + sentText)
    line_bot_api.push_message(LINE_USER_ID, messages=messages)

# メッセージの送信
def sendMes(sentText):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    messages = TextSendMessage(text=sentText)
    line_bot_api.push_message(LINE_USER_ID, messages=messages)