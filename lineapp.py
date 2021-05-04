from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

#エラーの送信
def sendError(sentText):
    line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
    messages = TextSendMessage(text="【Fatal Error】" + "\n" + "app: createEvernoteAutomatically" + "\n" + "server: GAE" + "\n" + "repository: EvernoteApi" + "\n" + sentText)
    line_bot_api.push_message(os.environ['LINE_USER_ID'], messages=messages)

#メッセージの送信
def sendMes(sentText):
    line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
    messages = TextSendMessage(text=sentText)
    line_bot_api.push_message(os.environ['LINE_USER_ID'], messages=messages)