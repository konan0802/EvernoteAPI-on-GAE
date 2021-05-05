from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import datetime
import lineapp
import json
import pytz
import os

#ローカルで動かす際にはdotenvをインポート
#from dotenv import load_dotenv
#load_dotenv()

EVERNOTE_DEV_TOKEN = os.environ['EVERNOTE_DEV_TOKEN']

#新規ノート, コピー元のノートブック、ノートのタイトルの作成
def makeTitle():

    #新規ノートのタイトルの作成
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    weekday = dt_now.weekday()
    jp_weekday = dt_now.weekday()
    if weekday == 0:
        jp_weekday = "月"
    elif weekday == 1:
        jp_weekday = "火"
    elif weekday == 2:
        jp_weekday = "水"
    elif weekday == 3:
        jp_weekday = "木"
    elif weekday == 4:
        jp_weekday = "金"
    elif weekday == 5:
        jp_weekday = "土"
    elif weekday == 6:
        jp_weekday = "日"
    else:
        return "", "", ""
    
    new_note_name = str(dt_now.year) + "年" + str(dt_now.month) + "月" + str(dt_now.day) + "日(" + jp_weekday + ")_Daily Review"

    #コピー元のノートブック、ノートのタイトルの作成
    notebook_name = 'Daily Review ' + str(dt_now.year)
    copied_note_name = str(dt_now.year) + '年月日()_Daily Review'

    return new_note_name, notebook_name, copied_note_name

#Evernoteインスタンスの生成
def initializeEvernote(evernote_dev_tolen):
    
    #clientの生成
    client = EvernoteClient(token=evernote_dev_tolen, sandbox=False)

    #ノートブックの取得
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    return client, note_store, notebooks

#ノートの取得
def searchNote(client, note_store, notebooks, notebookname, notename):

    #対象のノートブックを検索
    copied_notebook_guid = None
    for notebook in notebooks:
        if notebook.name == notebookname:
            copied_notebook_guid = notebook.guid
            break
    #該当するノートブックが存在しない場合にはエラー
    if copied_notebook_guid == None:
        return "", ""
    
    #対象のノートを検索
    offset = 0
    max_notes = 400
    filter = NoteFilter(notebookGuid=copied_notebook_guid)
    result_spec = NotesMetadataResultSpec(includeTitle=True)
    result_list = note_store.findNotesMetadata(EVERNOTE_DEV_TOKEN, filter, offset, max_notes, result_spec)
    copied_note_guid = None
    for note in result_list.notes:
        if note.title == notename:
            copied_note_guid = note.guid
            break
    #該当するノートが存在しない場合にはエラー
    if copied_note_guid == None:
        return "", ""

    return copied_notebook_guid, copied_note_guid








#新規ノートの作成
def copyDailyReview():

    #Evernoteインスタンスの生成
    client, note_store, notebooks = initializeEvernote(EVERNOTE_DEV_TOKEN)

    #新規ノート, コピー元のノートブック、ノートのタイトルの作成
    new_note_name, notebook_name, copied_note_name = makeTitle()
    if new_note_name == "" and notebook_name == "" and copied_note_name == "":
        lineapp.sendError("Failed to makeTitle()")
        return "Failed to makeTitle()"

    #ノートブックとノートのIDを取得
    copied_notebook_guid, copied_note_guid = searchNote(client, note_store, notebooks, notebook_name, copied_note_name)
    if copied_notebook_guid == "" and copied_note_guid == "":
        lineapp.sendError("Couldn't find the Notebook.")
        return "Couldn't find the Notebook."
    elif copied_notebook_guid == "" and copied_note_guid == "":
        lineapp.sendError("Couldn't find the Note.")
        return "Couldn't find the Note."
    
    #作成予定のノートがすでに存在しないか確認
    cofirm_new_notebook_guid, cofirm_new_note_guid = searchNote(client, note_store, notebooks, notebook_name, new_note_name)
    if cofirm_new_notebook_guid != "" and cofirm_new_note_guid != "":
        lineapp.sendError("That note already exists.")
        return "That note already exists."

    #ノートをコピー
    new_note = note_store.copyNote(EVERNOTE_DEV_TOKEN, copied_note_guid, copied_notebook_guid)
    #コピーしたノート名を編集
    new_note.title = new_note_name
    #コピー先のノートを編集
    note_store.updateNote(EVERNOTE_DEV_TOKEN, new_note)

    return "Evernote succeeded in creating a note."

#リマインドメッセージの送信
def remindDailyReview(time):

    #Evernoteインスタンスの生成
    client, note_store, notebooks = initializeEvernote(EVERNOTE_DEV_TOKEN)

    #新規ノート, コピー元のノートブック、ノートのタイトルの作成
    new_note_name, notebook_name, copied_note_name = makeTitle()
    if new_note_name == "" and notebook_name == "" and copied_note_name == "":
        lineapp.sendError("Failed to makeTitle()")
        return "Failed to makeTitle()"

    #ノートブックとノートのIDを取得
    copied_notebook_guid, copied_note_guid = searchNote(client, note_store, notebooks, notebook_name, new_note_name)
    if copied_notebook_guid == "" and copied_note_guid == "":
        lineapp.sendError("Couldn't find the Notebook.")
        return "Couldn't find the Notebook."
    elif copied_notebook_guid == "" and copied_note_guid == "":
        lineapp.sendError("Couldn't find the Note.")
        return "Couldn't find the Note."

    #メッセージの送信
    if time == "morning":
        sentText = "おはよう！！" + "\n" + "今日の頑張りも記録していこう👍" + "\n" + "https://www.evernote.com/shard/s440/nl/181315865/" + copied_note_guid
    else:
        sentText = "今日はどうだった？？" + "\n" + "今日も忘れずに振り返りを行っていきましょう👍" + "\n" + "https://www.evernote.com/shard/s440/nl/181315865/" + copied_note_guid

    lineapp.sendMes(sentText)

    return time

#copyDailyReview()