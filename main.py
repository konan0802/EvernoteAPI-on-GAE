from flask import Flask
import everapp

app = Flask(__name__)

#新規ノートの作成
@app.route('/create')
def createEvernote():
    text = everapp.copyDailyReview()
    return text

#朝のリマインドの送信
@app.route('/remind-morning')
def remindMorning():
    text = everapp.remindDailyReview("morning")
    return text

#夜のリマインドの送信
@app.route('/remind-night')
def remindNight():
    text = everapp.remindDailyReview("night")
    return text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
