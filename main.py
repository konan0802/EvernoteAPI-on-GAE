from flask import Flask, request
import everapp

app = Flask(__name__)

# 新規ノートの作成
@app.route('/create')
def createEvernote():
    text = everapp.copyDailyReview()
    return text

# 朝のリマインドの送信
@app.route('/remind-morning')
def remindMorning():
    text = everapp.remindDailyReview("morning")
    return text

# 夜のリマインドの送信
@app.route('/remind-night')
def remindNight():
    text = everapp.remindDailyReview("night")
    return text

# 対象ノートに記載されたメッセージを送信
@app.route('/message')
def messageFromNote():
    # ノートブック名を取得
    notebook = "Storage"
    if request.args.get('notebook') is not None:
        notebook = request.args.get('notebook')
    
    # ノート名を取得
    note = "DailyWinnerMind"
    if request.args.get('note') is not None:
        note = request.args.get('note')
    
    everapp.messageFromNote(notebook, note)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
