# Motivate App

## **概要**
毎朝の目標確認と寝る前の振り返りを習慣化、効果の最大化を目的とした、<br>
EvernoteとLINEのAPIを利用した **「Motivate App」** のプログラム

## **構成**
### **◇技術スタック**
* インフラ：GAE
* サーバーサイド：Python
* フレームワーク：Flask

### **◇API**
| エンドポイント | 概要 |
| ---- | ---- |
| /create | 新規ノートの作成 |
| /remind-morning  | 朝のリマインドの送信 |
| /remind-night  | 夜のリマインドの送信 |

### **◇動作**
* GAEの`Cloud Scheduler`により定刻にAPIを叩く
* EvernoteとLINEの接続情報は環境変数に持たせる
* 本番環境での環境変数は`app.yaml`に持たせる
* ローカル環境での環境変数は`.env`に持たせる
    * コメントアウトしている`dotenv`のインポートをアクティベートする必要がある

## **デプロイ方法**
```bash:bash
$ gcloud init
```
※ 私の場合 `target project` に `evernoteapi-py3` を選択
```bash:bash
$ gcloud app deploy
```

## **後書き**
* あまり拡張性や運用を意識していない作りだが、そこはご愛嬌
    * 全体的なクラス設計や文言の引数化など
* Pythonの例外処理を行えていない
    * Goライク?な例外処理で済ませている 