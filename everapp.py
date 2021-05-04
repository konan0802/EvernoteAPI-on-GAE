from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import datetime
import lineapp
import json
import os

#新規ノート, コピー元のノートブック、ノートのタイトルの作成
def makeTitle():

    #新規ノートのタイトルの作成
    dtNow = datetime.datetime.now()
    weekday = dtNow.weekday()
    jpWeekday = dtNow.weekday()
    if weekday == 0:
        jpWeekday = "月"
    elif weekday == 1:
        jpWeekday = "火"
    elif weekday == 2:
        jpWeekday = "水"
    elif weekday == 3:
        jpWeekday = "木"
    elif weekday == 4:
        jpWeekday = "金"
    elif weekday == 5:
        jpWeekday = "土"
    elif weekday == 6:
        jpWeekday = "日"
    else:
        return "", "", ""
    
    new_note_name = str(dtNow.year) + "年" + str(dtNow.month) + "月" + str(dtNow.day) + "日(" + jpWeekday + ")_Daily Review"

    #コピー元のノートブック、ノートのタイトルの作成
    copied_notebook_name = 'Daily Review ' + str(dtNow.year)
    copied_note_name = str(dtNow.year) + '年月日()_Daily Review'

    return new_note_name, copied_notebook_name, copied_note_name

#Evernoteインスタンスの生成
def initializeEvernote(EVERNOTE_DEV_TOKEN):
    
    #clientの生成
    client = EvernoteClient(token=EVERNOTE_DEV_TOKEN, sandbox=False)

    #ノートブックの取得
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()

    return client, noteStore, notebooks

#ノートの取得
def searchNote(client, noteStore, notebooks, notebookname, notename):

    #対象のノートブックを検索
    copiedNotebookGuid = None
    for notebook in notebooks:
        if notebook.name == notebookname:
            copiedNotebookGuid = notebook.guid
            break
    #該当するノートブックが存在しない場合にはエラー
    if copiedNotebookGuid == None:
        return -1, -1
    
    #対象のノートを検索
    offset = 0
    max_notes = 400
    filter = NoteFilter(notebookGuid=copiedNotebookGuid)
    result_spec = NotesMetadataResultSpec(includeTitle=True)
    result_list = noteStore.findNotesMetadata(os.environ['EVERNOTE_DEV_TOKEN'], filter, offset, max_notes, result_spec)
    copiedNoteGuid = None
    for note in result_list.notes:
        if note.title == notename:
            copiedNoteGuid = note.guid
            break
    #該当するノートが存在しない場合にはエラー
    if copiedNoteGuid == None:
        return -2, -2

    return copiedNotebookGuid, copiedNoteGuid








#新規ノートの作成
def copyDailyReview():

    #Evernoteインスタンスの生成
    client, noteStore, notebooks = initializeEvernote(os.environ['EVERNOTE_DEV_TOKEN'])

    #新規ノート, コピー元のノートブック、ノートのタイトルの作成
    new_note_name, copied_notebook_name, copied_note_name = makeTitle()
    if new_note_name == "" and copied_notebook_name == "" and copied_note_name == "":
        lineapp.sendError("Failed to makeTitle()")
        return "Failed to makeTitle()"

    #ノートブックとノートのIDを取得
    copiedNotebookGuid, copiedNoteGuid = searchNote(client, noteStore, notebooks, copied_notebook_name, copied_note_name)
    if copiedNotebookGuid == -1 and copiedNoteGuid == -1:
        lineapp.sendError("Couldn't find the Notebook.")
        return "Couldn't find the Notebook."
    elif copiedNotebookGuid == -2 and copiedNoteGuid == -2:
        lineapp.sendError("Couldn't find the Note.")
        return "Couldn't find the Note."

    #ノートをコピー
    newNote = noteStore.copyNote(os.environ['EVERNOTE_DEV_TOKEN'], copiedNoteGuid, copiedNotebookGuid)
    #コピーしたノート名を編集
    newNote.title = new_note_name
    #コピー先のノートを編集
    noteStore.updateNote(os.environ['EVERNOTE_DEV_TOKEN'], newNote)

    return "Evernote succeeded in creating a note."

#リマインドメッセージの送信
def remindDailyReview(time):

    #Evernoteインスタンスの生成
    client, noteStore, notebooks = initializeEvernote(os.environ['EVERNOTE_DEV_TOKEN'])

    #新規ノート, コピー元のノートブック、ノートのタイトルの作成
    new_note_name, copied_notebook_name, copied_note_name = makeTitle()
    if new_note_name == "" and copied_notebook_name == "" and copied_note_name == "":
        lineapp.sendError("Failed to makeTitle()")
        return "Failed to makeTitle()"

    #ノートブックとノートのIDを取得
    copiedNotebookGuid, copiedNoteGuid = searchNote(client, noteStore, notebooks, copied_notebook_name, new_note_name)
    if copiedNotebookGuid == -1 and copiedNoteGuid == -1:
        lineapp.sendError("Couldn't find the Notebook.")
        return "Couldn't find the Notebook."
    elif copiedNotebookGuid == -2 and copiedNoteGuid == -2:
        lineapp.sendError("Couldn't find the Note.")
        return "Couldn't find the Note."

    #メッセージの送信
    if time == "morning":
        sentText = "おはよう！！" + "\n" + "今日の頑張りも記録していこう👍" + "\n" + "https://www.evernote.com/shard/s440/nl/181315865/" + copiedNoteGuid
    else:
        sentText = "今日はどうだった？？" + "\n" + "今日も忘れずに振り返りを行っていきましょう👍" + "\n" + "https://www.evernote.com/shard/s440/nl/181315865/" + copiedNoteGuid

    lineapp.sendMes(sentText)

    return time

#copyDailyReview()