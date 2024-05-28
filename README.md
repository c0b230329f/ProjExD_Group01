# 倒せこうかとん

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
・おおまかな流れ
オープニング(タイトル)→あらすじ→工科大マップのシーン(かたけん)→単位を落とした。単位を拾いながら学部長賞をとる(こうかとんをたおすと学部長賞がもらえる)。(ぷしみ先生がさらわれたからとらわれている場所をさがす。)→エンディング

・オープニング
タイトル:たおせこうかとん。背景:明るい感じの学校。スタートボタン。(キャラクターを貼る)

・工科大マップのシーン
あらすじ表示して、クリックで移動できるようにする。プレイヤーが動けるようになって、単位を拾う(マップのある所に行ったら戦いが起こる)。こうかとんを倒す(学部長賞をもらう)。(詳細の機能に関しては担当者に任せる)

・戦うシーン
キャラクターを表示させる。
敵という概念を用意する。あとで決める。
技を選択して、攻撃。
プレイヤーの体力、攻撃力、防御力。技。を定義して、戦いの時に表示する。

・エンディング(ゲームオーバー)
結果表示させる。あとで決める。
ゲームオーバーの時はタイトルに戻る。

・BGMなど
文字では表現できないが、BGMなどの音付ける

## ゲームの実装
### 共通基本機能
* こんにちは世界のプログラム

### 担当追加機能
* マップのシーン(担当:北林):右上に獲得した単位数、左上に今いる場所、各マップに敵を配置、下部にプレイヤーの語りを表示
* 戦うシーン(担当:稲川):
* オープニング(担当:間野):オープニングの実装,キャラクタープロフィール実装
* あらすじ・BGMと効果音(担当:小川):あらすじ：このゲームのあらすじを表示させる　　音：それぞれのシーンでBGMを流す、戦うシーンでの攻撃音
* エンディング(担当:大谷):

### ToDo
- [ ] シーンを切り替えるときにBGMをフェードアウトさせたかったができなかった
- [ ] 音源を読み込むのが遅い(重い)

### メモ
* modeが切り替わったらBGMが流れるようにしてある
* 攻撃音は攻撃シーンで呼び出す
